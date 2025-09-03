"""
Real-time video stream processing service for live classification.
Supports webcam feeds, RTMP streams, and WebSocket connections.
"""

import asyncio
import json
import cv2
import numpy as np
from typing import Dict, List, Any, Optional, AsyncGenerator, Callable
from datetime import datetime
import websockets
from websockets.exceptions import ConnectionClosed
import base64
from pathlib import Path
import tempfile
import threading

from app.services.classification_service import ClassificationService
from app.services.multimodal_service import multimodal_service
from app.core.config import settings


class RealTimeStreamProcessor:
    """Real-time video stream processing with live classification."""
    
    def __init__(self):
        self.classification_service = ClassificationService()
        self.active_streams: Dict[str, Dict[str, Any]] = {}
        self.stream_lock = asyncio.Lock()
        self.max_concurrent_streams = 5
        
    async def create_stream_session(
        self,
        stream_id: str,
        user_id: str,
        stream_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new real-time stream processing session.
        
        Args:
            stream_id: Unique stream identifier
            user_id: User creating the stream
            stream_config: Stream configuration parameters
        
        Returns:
            Stream session information
        """
        
        async with self.stream_lock:
            if len(self.active_streams) >= self.max_concurrent_streams:
                return {
                    "success": False,
                    "error": f"Maximum concurrent streams ({self.max_concurrent_streams}) reached"
                }
            
            if stream_id in self.active_streams:
                return {
                    "success": False,
                    "error": f"Stream {stream_id} already exists"
                }
            
            # Create stream session
            stream_session = {
                "stream_id": stream_id,
                "user_id": user_id,
                "config": stream_config,
                "status": "created",
                "created_at": datetime.utcnow().isoformat(),
                "frame_count": 0,
                "classifications": [],
                "websocket_clients": set(),
                "processing_task": None
            }
            
            self.active_streams[stream_id] = stream_session
            
            return {
                "success": True,
                "stream_id": stream_id,
                "session": {
                    "stream_id": stream_id,
                    "status": "created",
                    "websocket_url": f"ws://localhost:8000/api/v1/stream/{stream_id}/ws",
                    "config": stream_config
                }
            }
    
    async def start_webcam_stream(
        self,
        stream_id: str,
        camera_index: int = 0,
        classification_interval: float = 1.0,
        model_name: str = "imagenet_mobilenet_v2"
    ) -> Dict[str, Any]:
        """
        Start webcam stream with real-time classification.
        
        Args:
            stream_id: Stream identifier
            camera_index: Camera device index
            classification_interval: Seconds between classifications
            model_name: AI model to use for classification
        
        Returns:
            Stream start result
        """
        
        if stream_id not in self.active_streams:
            return {"success": False, "error": "Stream session not found"}
        
        stream_session = self.active_streams[stream_id]
        
        try:
            # Start webcam processing task
            stream_session["processing_task"] = asyncio.create_task(
                self._process_webcam_stream(
                    stream_id, camera_index, classification_interval, model_name
                )
            )
            
            stream_session["status"] = "active"
            
            return {
                "success": True,
                "message": f"Webcam stream {stream_id} started",
                "stream_info": {
                    "stream_id": stream_id,
                    "type": "webcam",
                    "camera_index": camera_index,
                    "classification_interval": classification_interval,
                    "model_name": model_name
                }
            }
            
        except Exception as e:
            stream_session["status"] = "error"
            return {
                "success": False,
                "error": f"Failed to start webcam stream: {str(e)}"
            }
    
    async def _process_webcam_stream(
        self,
        stream_id: str,
        camera_index: int,
        classification_interval: float,
        model_name: str
    ):
        """Process webcam stream with periodic classification."""
        
        stream_session = self.active_streams[stream_id]
        cap = None
        
        try:
            # Open camera
            cap = cv2.VideoCapture(camera_index)
            if not cap.isOpened():
                raise Exception(f"Cannot open camera {camera_index}")
            
            # Set camera properties
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 30)
            
            last_classification_time = 0
            
            while stream_session["status"] == "active":
                ret, frame = cap.read()
                if not ret:
                    break
                
                current_time = asyncio.get_event_loop().time()
                stream_session["frame_count"] += 1
                
                # Convert frame to base64 for WebSocket transmission
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                
                # Send frame to WebSocket clients
                frame_message = {
                    "type": "frame",
                    "stream_id": stream_id,
                    "frame_count": stream_session["frame_count"],
                    "timestamp": datetime.utcnow().isoformat(),
                    "frame_data": frame_base64
                }
                
                await self._broadcast_to_websocket_clients(stream_id, frame_message)
                
                # Perform classification at specified intervals
                if current_time - last_classification_time >= classification_interval:
                    last_classification_time = current_time
                    
                    # Save frame temporarily for classification
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                        cv2.imwrite(temp_file.name, frame)
                        temp_path = temp_file.name
                    
                    try:
                        # Classify frame
                        classification_result = await self.classification_service.classify_image(
                            temp_path, model_name
                        )
                        
                        # Store classification result
                        classification_data = {
                            "frame_count": stream_session["frame_count"],
                            "timestamp": datetime.utcnow().isoformat(),
                            "classification": classification_result,
                            "model_used": model_name
                        }
                        
                        stream_session["classifications"].append(classification_data)
                        
                        # Keep only last 50 classifications to prevent memory issues
                        if len(stream_session["classifications"]) > 50:
                            stream_session["classifications"] = stream_session["classifications"][-50:]
                        
                        # Send classification to WebSocket clients
                        classification_message = {
                            "type": "classification",
                            "stream_id": stream_id,
                            "frame_count": stream_session["frame_count"],
                            "timestamp": classification_data["timestamp"],
                            "result": classification_result
                        }
                        
                        await self._broadcast_to_websocket_clients(stream_id, classification_message)
                        
                    finally:
                        # Clean up temporary file
                        import os
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)
                
                # Small delay to prevent overwhelming the system
                await asyncio.sleep(0.03)  # ~30 FPS
                
        except Exception as e:
            stream_session["status"] = "error"
            error_message = {
                "type": "error",
                "stream_id": stream_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            await self._broadcast_to_websocket_clients(stream_id, error_message)
            
        finally:
            if cap:
                cap.release()
            stream_session["status"] = "stopped"
    
    async def process_rtmp_stream(
        self,
        stream_id: str,
        rtmp_url: str,
        classification_interval: float = 2.0,
        model_name: str = "imagenet_mobilenet_v2"
    ) -> Dict[str, Any]:
        """
        Process RTMP stream with real-time classification.
        
        Args:
            stream_id: Stream identifier
            rtmp_url: RTMP stream URL
            classification_interval: Seconds between classifications
            model_name: AI model to use
        
        Returns:
            Processing result
        """
        
        if stream_id not in self.active_streams:
            return {"success": False, "error": "Stream session not found"}
        
        stream_session = self.active_streams[stream_id]
        
        try:
            # Start RTMP processing task
            stream_session["processing_task"] = asyncio.create_task(
                self._process_rtmp_stream(
                    stream_id, rtmp_url, classification_interval, model_name
                )
            )
            
            stream_session["status"] = "active"
            
            return {
                "success": True,
                "message": f"RTMP stream {stream_id} processing started",
                "stream_info": {
                    "stream_id": stream_id,
                    "type": "rtmp",
                    "rtmp_url": rtmp_url,
                    "classification_interval": classification_interval,
                    "model_name": model_name
                }
            }
            
        except Exception as e:
            stream_session["status"] = "error"
            return {
                "success": False,
                "error": f"Failed to start RTMP stream processing: {str(e)}"
            }
    
    async def _process_rtmp_stream(
        self,
        stream_id: str,
        rtmp_url: str,
        classification_interval: float,
        model_name: str
    ):
        """Process RTMP stream with periodic classification."""
        
        stream_session = self.active_streams[stream_id]
        cap = None
        
        try:
            # Open RTMP stream
            cap = cv2.VideoCapture(rtmp_url)
            if not cap.isOpened():
                raise Exception(f"Cannot open RTMP stream: {rtmp_url}")
            
            last_classification_time = 0
            
            while stream_session["status"] == "active":
                ret, frame = cap.read()
                if not ret:
                    await asyncio.sleep(0.1)
                    continue
                
                current_time = asyncio.get_event_loop().time()
                stream_session["frame_count"] += 1
                
                # Resize frame for efficiency
                frame = cv2.resize(frame, (640, 480))
                
                # Convert frame to base64
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                
                # Send frame to WebSocket clients
                frame_message = {
                    "type": "frame",
                    "stream_id": stream_id,
                    "frame_count": stream_session["frame_count"],
                    "timestamp": datetime.utcnow().isoformat(),
                    "frame_data": frame_base64
                }
                
                await self._broadcast_to_websocket_clients(stream_id, frame_message)
                
                # Perform classification
                if current_time - last_classification_time >= classification_interval:
                    last_classification_time = current_time
                    
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                        cv2.imwrite(temp_file.name, frame)
                        temp_path = temp_file.name
                    
                    try:
                        classification_result = await self.classification_service.classify_image(
                            temp_path, model_name
                        )
                        
                        classification_data = {
                            "frame_count": stream_session["frame_count"],
                            "timestamp": datetime.utcnow().isoformat(),
                            "classification": classification_result,
                            "model_used": model_name
                        }
                        
                        stream_session["classifications"].append(classification_data)
                        
                        if len(stream_session["classifications"]) > 50:
                            stream_session["classifications"] = stream_session["classifications"][-50:]
                        
                        classification_message = {
                            "type": "classification",
                            "stream_id": stream_id,
                            "frame_count": stream_session["frame_count"],
                            "timestamp": classification_data["timestamp"],
                            "result": classification_result
                        }
                        
                        await self._broadcast_to_websocket_clients(stream_id, classification_message)
                        
                    finally:
                        import os
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)
                
                await asyncio.sleep(0.05)  # Control frame rate
                
        except Exception as e:
            stream_session["status"] = "error"
            error_message = {
                "type": "error",
                "stream_id": stream_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            await self._broadcast_to_websocket_clients(stream_id, error_message)
            
        finally:
            if cap:
                cap.release()
            stream_session["status"] = "stopped"
    
    async def stop_stream(self, stream_id: str) -> Dict[str, Any]:
        """
        Stop a real-time stream.
        
        Args:
            stream_id: Stream identifier
        
        Returns:
            Stop operation result
        """
        
        if stream_id not in self.active_streams:
            return {"success": False, "error": "Stream not found"}
        
        stream_session = self.active_streams[stream_id]
        
        try:
            # Update status to stop processing
            stream_session["status"] = "stopping"
            
            # Cancel processing task if it exists
            if stream_session.get("processing_task"):
                stream_session["processing_task"].cancel()
                try:
                    await stream_session["processing_task"]
                except asyncio.CancelledError:
                    pass
            
            # Notify WebSocket clients
            stop_message = {
                "type": "stream_stopped",
                "stream_id": stream_id,
                "timestamp": datetime.utcnow().isoformat(),
                "final_stats": {
                    "total_frames": stream_session["frame_count"],
                    "total_classifications": len(stream_session["classifications"]),
                    "duration": (
                        datetime.utcnow() - 
                        datetime.fromisoformat(stream_session["created_at"])
                    ).total_seconds()
                }
            }
            
            await self._broadcast_to_websocket_clients(stream_id, stop_message)
            
            # Remove from active streams
            async with self.stream_lock:
                del self.active_streams[stream_id]
            
            return {
                "success": True,
                "message": f"Stream {stream_id} stopped successfully",
                "final_stats": stop_message["final_stats"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to stop stream: {str(e)}"
            }
    
    async def get_stream_status(self, stream_id: str) -> Dict[str, Any]:
        """
        Get current status of a stream.
        
        Args:
            stream_id: Stream identifier
        
        Returns:
            Stream status information
        """
        
        if stream_id not in self.active_streams:
            return {"error": "Stream not found"}
        
        stream_session = self.active_streams[stream_id]
        
        # Calculate statistics
        recent_classifications = stream_session["classifications"][-10:] if stream_session["classifications"] else []
        
        return {
            "stream_id": stream_id,
            "status": stream_session["status"],
            "created_at": stream_session["created_at"],
            "frame_count": stream_session["frame_count"],
            "total_classifications": len(stream_session["classifications"]),
            "connected_clients": len(stream_session["websocket_clients"]),
            "recent_classifications": recent_classifications,
            "config": stream_session["config"]
        }
    
    async def add_websocket_client(self, stream_id: str, websocket) -> bool:
        """
        Add WebSocket client to stream.
        
        Args:
            stream_id: Stream identifier
            websocket: WebSocket connection
        
        Returns:
            Success status
        """
        
        if stream_id not in self.active_streams:
            return False
        
        stream_session = self.active_streams[stream_id]
        stream_session["websocket_clients"].add(websocket)
        
        # Send current stream status to new client
        status_message = {
            "type": "stream_status",
            "stream_id": stream_id,
            "status": stream_session["status"],
            "frame_count": stream_session["frame_count"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            await websocket.send(json.dumps(status_message))
        except:
            pass  # Client may have disconnected immediately
        
        return True
    
    async def remove_websocket_client(self, stream_id: str, websocket):
        """
        Remove WebSocket client from stream.
        
        Args:
            stream_id: Stream identifier
            websocket: WebSocket connection
        """
        
        if stream_id in self.active_streams:
            stream_session = self.active_streams[stream_id]
            stream_session["websocket_clients"].discard(websocket)
    
    async def _broadcast_to_websocket_clients(self, stream_id: str, message: Dict[str, Any]):
        """
        Broadcast message to all WebSocket clients of a stream.
        
        Args:
            stream_id: Stream identifier
            message: Message to broadcast
        """
        
        if stream_id not in self.active_streams:
            return
        
        stream_session = self.active_streams[stream_id]
        clients_to_remove = set()
        
        message_json = json.dumps(message)
        
        for client in stream_session["websocket_clients"]:
            try:
                await client.send(message_json)
            except:
                clients_to_remove.add(client)
        
        # Remove disconnected clients
        for client in clients_to_remove:
            stream_session["websocket_clients"].discard(client)
    
    async def get_active_streams(self) -> Dict[str, Any]:
        """
        Get information about all active streams.
        
        Returns:
            Active streams information
        """
        
        streams_info = []
        
        for stream_id, session in self.active_streams.items():
            stream_info = {
                "stream_id": stream_id,
                "user_id": session["user_id"],
                "status": session["status"],
                "created_at": session["created_at"],
                "frame_count": session["frame_count"],
                "classification_count": len(session["classifications"]),
                "connected_clients": len(session["websocket_clients"])
            }
            streams_info.append(stream_info)
        
        return {
            "active_streams": streams_info,
            "total_streams": len(self.active_streams),
            "max_concurrent_streams": self.max_concurrent_streams
        }


# Global instance
realtime_processor = RealTimeStreamProcessor()