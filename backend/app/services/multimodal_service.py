"""
Multi-modal classification service for video and audio files.
Extends the existing image classification to support multiple media types.
"""

import asyncio
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import cv2
import numpy as np
from PIL import Image
import librosa
import torch
import torchvision.transforms as transforms
from transformers import pipeline
import moviepy as mp

from app.services.classification_service import ClassificationService
from app.core.config import settings


class MultiModalService:
    """Service for handling multi-modal classification (image, video, audio)."""
    
    def __init__(self):
        self.image_classifier = ClassificationService()
        self.audio_classifier = None
        self.video_processor = None
        self.initialized = False
    
    async def initialize(self):
        """Initialize multi-modal classification models."""
        if self.initialized:
            return
        
        try:
            # Initialize audio classification pipeline
            self.audio_classifier = pipeline(
                "audio-classification",
                model="facebook/wav2vec2-base-960h",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Initialize video processing
            self.video_processor = VideoProcessor()
            
            self.initialized = True
            print("Multi-modal service initialized successfully")
            
        except Exception as e:
            print(f"Multi-modal service initialization warning: {e}")
            self.initialized = False
    
    async def classify_video(
        self,
        video_file_path: str,
        extract_frames: int = 5,
        extract_audio: bool = True
    ) -> Dict[str, Any]:
        """
        Classify video by extracting frames and optionally audio.
        
        Args:
            video_file_path: Path to video file
            extract_frames: Number of frames to extract for classification
            extract_audio: Whether to extract and classify audio
        
        Returns:
            Classification results for video frames and audio
        """
        if not self.initialized:
            await self.initialize()
        
        results = {
            "video_path": video_file_path,
            "frame_classifications": [],
            "audio_classification": None,
            "summary": {},
            "metadata": {}
        }
        
        try:
            # Extract video metadata
            cap = cv2.VideoCapture(video_file_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            
            results["metadata"] = {
                "duration_seconds": duration,
                "fps": fps,
                "total_frames": frame_count,
                "extracted_frames": extract_frames
            }
            
            # Extract and classify frames
            frame_results = await self._extract_and_classify_frames(
                video_file_path, extract_frames
            )
            results["frame_classifications"] = frame_results
            
            # Extract and classify audio if requested
            if extract_audio:
                audio_result = await self._extract_and_classify_audio(video_file_path)
                results["audio_classification"] = audio_result
            
            # Generate summary
            results["summary"] = self._generate_video_summary(results)
            
            cap.release()
            return results
            
        except Exception as e:
            return {
                "error": f"Video classification failed: {str(e)}",
                "video_path": video_file_path
            }
    
    async def classify_audio(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Classify audio file content.
        
        Args:
            audio_file_path: Path to audio file
        
        Returns:
            Audio classification results
        """
        if not self.initialized:
            await self.initialize()
        
        try:
            # Load audio file
            audio_data, sample_rate = librosa.load(audio_file_path, sr=16000)
            
            # Get audio features
            features = self._extract_audio_features(audio_data, sample_rate)
            
            # Classify using Hugging Face pipeline
            if self.audio_classifier:
                classification_results = self.audio_classifier(audio_file_path)
            else:
                classification_results = await self._fallback_audio_classification(
                    audio_data, sample_rate
                )
            
            return {
                "audio_path": audio_file_path,
                "classification": classification_results,
                "features": features,
                "metadata": {
                    "duration": len(audio_data) / sample_rate,
                    "sample_rate": sample_rate,
                    "channels": 1 if len(audio_data.shape) == 1 else audio_data.shape[1]
                }
            }
            
        except Exception as e:
            return {
                "error": f"Audio classification failed: {str(e)}",
                "audio_path": audio_file_path
            }
    
    async def _extract_and_classify_frames(
        self, 
        video_path: str, 
        num_frames: int
    ) -> List[Dict[str, Any]]:
        """Extract frames from video and classify each frame."""
        
        frame_results = []
        cap = cv2.VideoCapture(video_path)
        
        try:
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
            
            for i, frame_idx in enumerate(frame_indices):
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                
                if not ret:
                    continue
                
                # Convert frame to PIL Image
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(frame_rgb)
                
                # Save frame temporarily for classification
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                    pil_image.save(temp_file.name, 'JPEG')
                    temp_path = temp_file.name
                
                try:
                    # Classify frame using existing image classification service
                    classification_result = await self.image_classifier.classify_image(
                        temp_path, model_name="imagenet_mobilenet_v2"
                    )
                    
                    frame_results.append({
                        "frame_index": frame_idx,
                        "timestamp": frame_idx / cap.get(cv2.CAP_PROP_FPS),
                        "classification": classification_result
                    })
                    
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
            
        finally:
            cap.release()
        
        return frame_results
    
    async def _extract_and_classify_audio(self, video_path: str) -> Optional[Dict[str, Any]]:
        """Extract audio from video and classify it."""
        
        try:
            # Extract audio using moviepy
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                audio_path = temp_audio.name
            
            # Extract audio from video
            video_clip = mp.VideoFileClip(video_path)
            if video_clip.audio is None:
                return {"message": "No audio track found in video"}
            
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(audio_path, verbose=False, logger=None)
            
            try:
                # Classify extracted audio
                audio_result = await self.classify_audio(audio_path)
                return audio_result
                
            finally:
                # Clean up temporary files
                if os.path.exists(audio_path):
                    os.unlink(audio_path)
                video_clip.close()
                if audio_clip:
                    audio_clip.close()
        
        except Exception as e:
            return {"error": f"Audio extraction failed: {str(e)}"}
    
    def _extract_audio_features(self, audio_data: np.ndarray, sample_rate: int) -> Dict[str, Any]:
        """Extract audio features for analysis."""
        
        features = {}
        
        try:
            # Spectral features
            features["mfcc"] = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13).mean(axis=1).tolist()
            features["spectral_centroid"] = librosa.feature.spectral_centroid(y=audio_data, sr=sample_rate).mean()
            features["spectral_bandwidth"] = librosa.feature.spectral_bandwidth(y=audio_data, sr=sample_rate).mean()
            features["spectral_rolloff"] = librosa.feature.spectral_rolloff(y=audio_data, sr=sample_rate).mean()
            
            # Rhythm features
            features["tempo"] = librosa.beat.tempo(y=audio_data, sr=sample_rate)[0]
            features["zero_crossing_rate"] = librosa.feature.zero_crossing_rate(audio_data).mean()
            
            # Energy features
            features["rms_energy"] = librosa.feature.rms(y=audio_data).mean()
            
        except Exception as e:
            features["error"] = f"Feature extraction failed: {str(e)}"
        
        return features
    
    async def _fallback_audio_classification(
        self, 
        audio_data: np.ndarray, 
        sample_rate: int
    ) -> List[Dict[str, Any]]:
        """Fallback audio classification using basic features."""
        
        features = self._extract_audio_features(audio_data, sample_rate)
        
        # Basic classification based on audio features
        classifications = []
        
        # Tempo-based classification
        tempo = features.get("tempo", 0)
        if tempo > 140:
            classifications.append({"label": "High Tempo Music", "score": 0.8})
        elif tempo > 80:
            classifications.append({"label": "Medium Tempo Music", "score": 0.7})
        elif tempo > 0:
            classifications.append({"label": "Low Tempo Music", "score": 0.6})
        
        # Energy-based classification
        energy = features.get("rms_energy", 0)
        if energy > 0.1:
            classifications.append({"label": "High Energy Audio", "score": 0.75})
        elif energy > 0.05:
            classifications.append({"label": "Medium Energy Audio", "score": 0.65})
        else:
            classifications.append({"label": "Low Energy Audio", "score": 0.55})
        
        return classifications if classifications else [{"label": "Unknown Audio", "score": 0.5}]
    
    def _generate_video_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary from video classification results."""
        
        summary = {
            "dominant_objects": {},
            "scene_changes": 0,
            "confidence_stats": {},
            "temporal_analysis": {}
        }
        
        frame_classifications = results.get("frame_classifications", [])
        
        if not frame_classifications:
            return summary
        
        # Analyze dominant objects across frames
        object_counts = {}
        confidences = []
        
        for frame in frame_classifications:
            classification = frame.get("classification", {})
            predictions = classification.get("predictions", [])
            
            for pred in predictions[:3]:  # Top 3 predictions per frame
                class_name = pred.get("class_name", "unknown")
                confidence = pred.get("confidence", 0)
                
                if class_name in object_counts:
                    object_counts[class_name] += 1
                else:
                    object_counts[class_name] = 1
                
                confidences.append(confidence)
        
        # Sort objects by frequency
        summary["dominant_objects"] = dict(
            sorted(object_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        )
        
        # Confidence statistics
        if confidences:
            summary["confidence_stats"] = {
                "average": np.mean(confidences),
                "min": np.min(confidences),
                "max": np.max(confidences),
                "std": np.std(confidences)
            }
        
        # Temporal analysis (scene change detection)
        prev_top_class = None
        scene_changes = 0
        
        for frame in frame_classifications:
            classification = frame.get("classification", {})
            predictions = classification.get("predictions", [])
            
            if predictions:
                current_top_class = predictions[0].get("class_name")
                if prev_top_class and current_top_class != prev_top_class:
                    scene_changes += 1
                prev_top_class = current_top_class
        
        summary["scene_changes"] = scene_changes
        summary["temporal_analysis"] = {
            "total_frames_analyzed": len(frame_classifications),
            "scene_stability": 1 - (scene_changes / max(len(frame_classifications) - 1, 1))
        }
        
        return summary


class VideoProcessor:
    """Specialized video processing utilities."""
    
    @staticmethod
    def extract_frames(video_path: str, num_frames: int = 5) -> List[np.ndarray]:
        """Extract evenly spaced frames from video."""
        
        cap = cv2.VideoCapture(video_path)
        frames = []
        
        try:
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
            
            for frame_idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                
                if ret:
                    frames.append(frame)
            
        finally:
            cap.release()
        
        return frames
    
    @staticmethod
    def get_video_info(video_path: str) -> Dict[str, Any]:
        """Get video metadata and properties."""
        
        cap = cv2.VideoCapture(video_path)
        
        try:
            info = {
                "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "fps": cap.get(cv2.CAP_PROP_FPS),
                "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                "duration": 0,
                "codec": int(cap.get(cv2.CAP_PROP_FOURCC))
            }
            
            if info["fps"] > 0:
                info["duration"] = info["frame_count"] / info["fps"]
            
            return info
            
        finally:
            cap.release()
    
    @staticmethod
    def validate_video_file(file_path: str) -> Dict[str, Any]:
        """Validate video file format and properties."""
        
        validation = {
            "is_valid": False,
            "format": None,
            "error": None,
            "properties": {}
        }
        
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                validation["error"] = "File does not exist"
                return validation
            
            # Try to open with OpenCV
            cap = cv2.VideoCapture(file_path)
            
            if not cap.isOpened():
                validation["error"] = "Cannot open video file"
                return validation
            
            # Get basic properties
            validation["properties"] = VideoProcessor.get_video_info(file_path)
            
            # Validate properties
            if validation["properties"]["frame_count"] > 0:
                validation["is_valid"] = True
                validation["format"] = "video"
            else:
                validation["error"] = "Video contains no frames"
            
            cap.release()
            
        except Exception as e:
            validation["error"] = f"Video validation failed: {str(e)}"
        
        return validation


class AudioProcessor:
    """Specialized audio processing utilities."""
    
    @staticmethod
    def extract_audio_features(audio_path: str) -> Dict[str, Any]:
        """Extract comprehensive audio features."""
        
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=22050)
            
            features = {
                "duration": len(y) / sr,
                "sample_rate": sr,
                "num_samples": len(y)
            }
            
            # Spectral features
            features["mfcc"] = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).mean(axis=1).tolist()
            features["spectral_centroid"] = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
            features["spectral_bandwidth"] = librosa.feature.spectral_bandwidth(y=y, sr=sr).mean()
            features["spectral_rolloff"] = librosa.feature.spectral_rolloff(y=y, sr=sr).mean()
            
            # Rhythm features
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            features["tempo"] = tempo
            features["beat_count"] = len(beats)
            
            # Harmonic features
            harmony = librosa.effects.harmonic(y)
            percussive = librosa.effects.percussive(y)
            features["harmonic_ratio"] = np.sum(harmony) / (np.sum(harmony) + np.sum(percussive))
            
            # Energy features
            features["rms_energy"] = librosa.feature.rms(y=y).mean()
            features["zero_crossing_rate"] = librosa.feature.zero_crossing_rate(y).mean()
            
            return features
            
        except Exception as e:
            return {"error": f"Feature extraction failed: {str(e)}"}
    
    @staticmethod
    def validate_audio_file(file_path: str) -> Dict[str, Any]:
        """Validate audio file format and properties."""
        
        validation = {
            "is_valid": False,
            "format": None,
            "error": None,
            "properties": {}
        }
        
        try:
            # Try to load with librosa
            y, sr = librosa.load(file_path, sr=None, duration=0.1)  # Load just 0.1 seconds for validation
            
            validation["properties"] = {
                "sample_rate": sr,
                "channels": 1 if len(y.shape) == 1 else y.shape[1],
                "format": "audio"
            }
            
            validation["is_valid"] = True
            validation["format"] = "audio"
            
        except Exception as e:
            validation["error"] = f"Audio validation failed: {str(e)}"
        
        return validation


# Global instance
multimodal_service = MultiModalService()