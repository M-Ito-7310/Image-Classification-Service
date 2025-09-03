"""
Real-time video stream processing API endpoints.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status, Form, Query
from fastapi.responses import JSONResponse
import json

from app.services.realtime_stream import realtime_processor

router = APIRouter()

@router.post("/stream/create")
async def create_stream_session(
    user_id: str = Form(...),
    stream_type: str = Form("webcam", pattern="^(webcam|rtmp|upload)$"),
    classification_interval: float = Form(1.0, ge=0.1, le=10.0),
    model_name: str = Form("imagenet_mobilenet_v2"),
    camera_index: Optional[int] = Form(None),
    rtmp_url: Optional[str] = Form(None)
) -> Dict[str, Any]:
    """
    Create a new real-time stream processing session.
    
    Args:
        user_id: User creating the stream
        stream_type: Type of stream (webcam, rtmp, upload)
        classification_interval: Seconds between classifications
        model_name: AI model to use for classification
        camera_index: Camera device index (for webcam streams)
        rtmp_url: RTMP stream URL (for RTMP streams)
    
    Returns:
        Stream session information
    """
    
    # Generate unique stream ID
    import uuid
    stream_id = f"{user_id}_{uuid.uuid4().hex[:8]}"
    
    # Prepare stream configuration
    stream_config = {
        "stream_type": stream_type,
        "classification_interval": classification_interval,
        "model_name": model_name
    }
    
    if stream_type == "webcam":
        if camera_index is None:
            camera_index = 0
        stream_config["camera_index"] = camera_index
    elif stream_type == "rtmp":
        if not rtmp_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="rtmp_url is required for RTMP streams"
            )
        stream_config["rtmp_url"] = rtmp_url
    
    try:
        # Create stream session
        result = await realtime_processor.create_stream_session(
            stream_id=stream_id,
            user_id=user_id,
            stream_config=stream_config
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to create stream session")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create stream session: {str(e)}"
        )

@router.post("/stream/{stream_id}/start/webcam")
async def start_webcam_stream(
    stream_id: str,
    camera_index: int = Form(0),
    classification_interval: float = Form(1.0, ge=0.1, le=10.0),
    model_name: str = Form("imagenet_mobilenet_v2")
) -> Dict[str, Any]:
    """
    Start webcam stream with real-time classification.
    
    Args:
        stream_id: Stream identifier
        camera_index: Camera device index
        classification_interval: Seconds between classifications
        model_name: AI model to use
    
    Returns:
        Stream start result
    """
    
    try:
        result = await realtime_processor.start_webcam_stream(
            stream_id=stream_id,
            camera_index=camera_index,
            classification_interval=classification_interval,
            model_name=model_name
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to start webcam stream")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start webcam stream: {str(e)}"
        )

@router.post("/stream/{stream_id}/start/rtmp")
async def start_rtmp_stream(
    stream_id: str,
    rtmp_url: str = Form(...),
    classification_interval: float = Form(2.0, ge=0.5, le=10.0),
    model_name: str = Form("imagenet_mobilenet_v2")
) -> Dict[str, Any]:
    """
    Start RTMP stream processing with real-time classification.
    
    Args:
        stream_id: Stream identifier
        rtmp_url: RTMP stream URL
        classification_interval: Seconds between classifications
        model_name: AI model to use
    
    Returns:
        Stream start result
    """
    
    try:
        result = await realtime_processor.process_rtmp_stream(
            stream_id=stream_id,
            rtmp_url=rtmp_url,
            classification_interval=classification_interval,
            model_name=model_name
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to start RTMP stream")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start RTMP stream: {str(e)}"
        )

@router.post("/stream/{stream_id}/stop")
async def stop_stream(stream_id: str) -> Dict[str, Any]:
    """
    Stop a real-time stream.
    
    Args:
        stream_id: Stream identifier
    
    Returns:
        Stop operation result
    """
    
    try:
        result = await realtime_processor.stop_stream(stream_id)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result.get("error", "Stream not found")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to stop stream: {str(e)}"
        )

@router.get("/stream/{stream_id}/status")
async def get_stream_status(stream_id: str) -> Dict[str, Any]:
    """
    Get current status of a stream.
    
    Args:
        stream_id: Stream identifier
    
    Returns:
        Stream status information
    """
    
    try:
        result = await realtime_processor.get_stream_status(stream_id)
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["error"]
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stream status: {str(e)}"
        )

@router.get("/streams")
async def get_active_streams() -> Dict[str, Any]:
    """
    Get information about all active streams.
    
    Returns:
        Active streams information
    """
    
    try:
        result = await realtime_processor.get_active_streams()
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get active streams: {str(e)}"
        )

@router.websocket("/stream/{stream_id}/ws")
async def websocket_stream_endpoint(websocket: WebSocket, stream_id: str):
    """
    WebSocket endpoint for real-time stream data.
    
    Args:
        websocket: WebSocket connection
        stream_id: Stream identifier
    """
    
    await websocket.accept()
    
    # Add client to stream
    client_added = await realtime_processor.add_websocket_client(stream_id, websocket)
    
    if not client_added:
        await websocket.close(code=4004, reason="Stream not found")
        return
    
    try:
        # Send welcome message
        welcome_message = {
            "type": "connected",
            "stream_id": stream_id,
            "message": "Connected to real-time stream",
            "timestamp": "2025-09-03T12:00:00Z"
        }
        await websocket.send_text(json.dumps(welcome_message))
        
        # Keep connection alive and handle client messages
        while True:
            try:
                # Wait for client messages (e.g., configuration changes)
                message = await websocket.receive_text()
                client_message = json.loads(message)
                
                # Handle different message types
                if client_message.get("type") == "ping":
                    pong_message = {
                        "type": "pong",
                        "timestamp": "2025-09-03T12:00:00Z"
                    }
                    await websocket.send_text(json.dumps(pong_message))
                
                elif client_message.get("type") == "get_status":
                    status = await realtime_processor.get_stream_status(stream_id)
                    status_message = {
                        "type": "status_response",
                        "data": status
                    }
                    await websocket.send_text(json.dumps(status_message))
                
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                # Invalid JSON from client, ignore
                continue
            except Exception:
                # Other errors, continue listening
                continue
                
    except WebSocketDisconnect:
        pass
    finally:
        # Remove client from stream
        await realtime_processor.remove_websocket_client(stream_id, websocket)

@router.get("/capabilities")
async def get_realtime_capabilities() -> Dict[str, Any]:
    """
    Get real-time processing capabilities and limitations.
    
    Returns:
        Capabilities information
    """
    
    return {
        "supported_stream_types": [
            {
                "type": "webcam",
                "description": "Local camera/webcam streams",
                "supported_devices": "USB cameras, built-in cameras",
                "max_resolution": "1920x1080",
                "typical_fps": 30
            },
            {
                "type": "rtmp",
                "description": "RTMP stream processing",
                "supported_protocols": ["RTMP", "RTMPS"],
                "max_bitrate": "5 Mbps",
                "typical_latency": "2-5 seconds"
            }
        ],
        "classification_models": [
            "imagenet_mobilenet_v2",
            "imagenet_resnet50",
            "pytorch_resnet18"
        ],
        "performance_limits": {
            "max_concurrent_streams": 5,
            "min_classification_interval": 0.1,
            "max_classification_interval": 10.0,
            "recommended_resolution": "640x480",
            "max_websocket_clients_per_stream": 10
        },
        "features": [
            "Real-time frame classification",
            "WebSocket live updates",
            "Multi-client support",
            "Stream statistics",
            "Error handling and recovery",
            "Configurable classification intervals"
        ],
        "message_types": [
            {
                "type": "frame",
                "description": "Video frame data (base64 encoded)",
                "frequency": "~30 FPS"
            },
            {
                "type": "classification",
                "description": "AI classification results",
                "frequency": "Based on classification_interval"
            },
            {
                "type": "stream_status",
                "description": "Stream status updates",
                "frequency": "On status changes"
            },
            {
                "type": "error",
                "description": "Error notifications",
                "frequency": "When errors occur"
            }
        ]
    }

@router.get("/stream/{stream_id}/export")
async def export_stream_data(
    stream_id: str,
    format: str = Query("json", pattern="^(json|csv)$"),
    include_frames: bool = Query(False),
    max_records: int = Query(100, ge=1, le=1000)
) -> Dict[str, Any]:
    """
    Export stream classification data.
    
    Args:
        stream_id: Stream identifier
        format: Export format (json, csv)
        include_frames: Whether to include frame data
        max_records: Maximum number of records to export
    
    Returns:
        Exported stream data
    """
    
    try:
        # Get stream status to access classification data
        stream_status = await realtime_processor.get_stream_status(stream_id)
        
        if "error" in stream_status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Stream not found"
            )
        
        # Get recent classifications (limited by max_records)
        classifications = stream_status.get("recent_classifications", [])
        if len(classifications) > max_records:
            classifications = classifications[-max_records:]
        
        # Prepare export data
        export_data = {
            "stream_id": stream_id,
            "export_timestamp": "2025-09-03T12:00:00Z",
            "total_records": len(classifications),
            "format": format,
            "classifications": []
        }
        
        # Process classifications for export
        for classification in classifications:
            record = {
                "frame_count": classification["frame_count"],
                "timestamp": classification["timestamp"],
                "model_used": classification["model_used"],
                "predictions": classification["classification"].get("predictions", [])
            }
            
            if not include_frames:
                # Remove frame data to reduce size
                record["classification"] = {
                    "predictions": classification["classification"].get("predictions", []),
                    "processing_time": classification["classification"].get("processing_time", 0)
                }
            else:
                record["classification"] = classification["classification"]
            
            export_data["classifications"].append(record)
        
        return export_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export stream data: {str(e)}"
        )