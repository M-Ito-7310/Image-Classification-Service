"""Security service for file upload validation and protection."""

import os
import hashlib
import tempfile

# Try to import magic, but handle Windows compatibility issues
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False
    import mimetypes  # Fallback for Windows
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from PIL import Image, ImageFile
import logging

logger = logging.getLogger(__name__)

# Enable loading of truncated images (security consideration)
ImageFile.LOAD_TRUNCATED_IMAGES = False

class FileSecurityService:
    """Security service for validating uploaded files."""
    
    # Allowed MIME types for images
    ALLOWED_MIME_TYPES = {
        'image/jpeg',
        'image/png', 
        'image/webp',
        'image/bmp',
        'image/gif'
    }
    
    # Maximum file sizes by type
    MAX_FILE_SIZES = {
        'image/jpeg': 10 * 1024 * 1024,  # 10MB
        'image/png': 15 * 1024 * 1024,   # 15MB
        'image/webp': 10 * 1024 * 1024,  # 10MB
        'image/bmp': 20 * 1024 * 1024,   # 20MB
        'image/gif': 5 * 1024 * 1024,    # 5MB
    }
    
    # Dangerous file signatures to block
    DANGEROUS_SIGNATURES = [
        b'\x4D\x5A',  # PE executable
        b'\x7F\x45\x4C\x46',  # ELF executable
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A',  # PNG (but check later)
        b'\x25\x50\x44\x46',  # PDF
        b'\x50\x4B\x03\x04',  # ZIP/JAR
    ]
    
    def __init__(self):
        self.quarantine_dir = Path("quarantine")
        self.quarantine_dir.mkdir(exist_ok=True)
    
    async def validate_file_upload(
        self, 
        file_content: bytes, 
        filename: str,
        max_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive file validation for uploads.
        
        Args:
            file_content: Raw file bytes
            filename: Original filename
            max_size: Override maximum file size
            
        Returns:
            Validation result with security assessment
        """
        validation_result = {
            "valid": False,
            "mime_type": None,
            "file_size": len(file_content),
            "filename": filename,
            "security_score": 0,  # 0-100
            "warnings": [],
            "errors": []
        }
        
        try:
            # 1. Basic file size validation
            if len(file_content) == 0:
                validation_result["errors"].append("Empty file")
                return validation_result
            
            # 2. Detect actual MIME type
            try:
                if MAGIC_AVAILABLE:
                    detected_mime = magic.from_buffer(file_content, mime=True)
                else:
                    # Fallback for Windows - use file extension and header inspection
                    detected_mime = self._detect_mime_fallback(filename, file_content)
                validation_result["mime_type"] = detected_mime
            except Exception as e:
                validation_result["errors"].append(f"MIME type detection failed: {e}")
                return validation_result
            
            # 3. Validate MIME type is allowed
            if detected_mime not in self.ALLOWED_MIME_TYPES:
                validation_result["errors"].append(f"File type not allowed: {detected_mime}")
                return validation_result
            
            # 4. Check file size limits
            max_allowed_size = max_size or self.MAX_FILE_SIZES.get(detected_mime, 10 * 1024 * 1024)
            if len(file_content) > max_allowed_size:
                validation_result["errors"].append(
                    f"File too large: {len(file_content)} bytes (max: {max_allowed_size})"
                )
                return validation_result
            
            # 5. Check for dangerous file signatures
            file_header = file_content[:20]
            for dangerous_sig in self.DANGEROUS_SIGNATURES:
                if file_header.startswith(dangerous_sig) and detected_mime != 'image/png':
                    validation_result["errors"].append("Dangerous file signature detected")
                    return validation_result
            
            # 6. Validate image structure
            image_validation = await self._validate_image_structure(file_content, detected_mime)
            validation_result["warnings"].extend(image_validation["warnings"])
            if image_validation["errors"]:
                validation_result["errors"].extend(image_validation["errors"])
                return validation_result
            
            # 7. Filename security check
            filename_check = self._validate_filename(filename)
            validation_result["warnings"].extend(filename_check["warnings"])
            if filename_check["errors"]:
                validation_result["errors"].extend(filename_check["errors"])
                return validation_result
            
            # 8. Calculate security score
            validation_result["security_score"] = self._calculate_security_score(
                detected_mime, 
                len(file_content), 
                filename,
                image_validation,
                filename_check
            )
            
            # File is valid if no errors
            validation_result["valid"] = len(validation_result["errors"]) == 0
            
            logger.info(f"File validation completed: {filename} - Valid: {validation_result['valid']}")
            
        except Exception as e:
            validation_result["errors"].append(f"Validation failed: {str(e)}")
            logger.error(f"File validation error: {e}")
        
        return validation_result
    
    async def _validate_image_structure(self, file_content: bytes, mime_type: str) -> Dict[str, List[str]]:
        """Validate image file structure and metadata."""
        result = {"warnings": [], "errors": []}
        
        try:
            # Create temporary file for PIL validation
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(file_content)
                tmp_file.flush()
                
                try:
                    # Open and validate with PIL
                    with Image.open(tmp_file.name) as img:
                        # Basic validation
                        if img.size[0] < 1 or img.size[1] < 1:
                            result["errors"].append("Invalid image dimensions")
                        
                        if img.size[0] > 10000 or img.size[1] > 10000:
                            result["warnings"].append("Very large image dimensions")
                        
                        # Check for suspicious metadata
                        if hasattr(img, '_getexif') and img._getexif():
                            exif_data = img._getexif()
                            if exif_data and len(str(exif_data)) > 10000:
                                result["warnings"].append("Large EXIF metadata detected")
                        
                        # Verify image can be processed
                        try:
                            img.verify()
                        except Exception as e:
                            result["errors"].append(f"Image verification failed: {e}")
                            
                except Exception as e:
                    result["errors"].append(f"Image processing failed: {str(e)}")
                
                finally:
                    # Clean up temporary file
                    try:
                        os.unlink(tmp_file.name)
                    except:
                        pass
                        
        except Exception as e:
            result["errors"].append(f"Image structure validation failed: {str(e)}")
        
        return result
    
    def _validate_filename(self, filename: str) -> Dict[str, List[str]]:
        """Validate filename for security issues."""
        result = {"warnings": [], "errors": []}
        
        # Check for path traversal
        if ".." in filename or "/" in filename or "\\" in filename:
            result["errors"].append("Invalid filename: path traversal detected")
        
        # Check for dangerous characters
        dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\x00']
        if any(char in filename for char in dangerous_chars):
            result["warnings"].append("Filename contains potentially dangerous characters")
        
        # Check filename length
        if len(filename) > 255:
            result["errors"].append("Filename too long")
        
        if len(filename) < 1:
            result["errors"].append("Empty filename")
        
        # Check for executable extensions (double extension attack)
        filename_lower = filename.lower()
        executable_extensions = ['.exe', '.bat', '.cmd', '.scr', '.pif', '.com']
        if any(ext in filename_lower for ext in executable_extensions):
            result["errors"].append("Executable file extension detected")
        
        return result
    
    def _calculate_security_score(
        self, 
        mime_type: str, 
        file_size: int, 
        filename: str,
        image_validation: Dict[str, List[str]],
        filename_validation: Dict[str, List[str]]
    ) -> int:
        """Calculate security score (0-100) for the file."""
        score = 100
        
        # Deduct points for warnings and errors
        score -= len(image_validation["warnings"]) * 5
        score -= len(image_validation["errors"]) * 20
        score -= len(filename_validation["warnings"]) * 3
        score -= len(filename_validation["errors"]) * 25
        
        # Deduct points for large files
        if file_size > 5 * 1024 * 1024:  # > 5MB
            score -= 10
        
        # Bonus points for common safe formats
        if mime_type in ['image/jpeg', 'image/png']:
            score += 5
        
        return max(0, min(100, score))
    
    def _detect_mime_fallback(self, filename: str, file_content: bytes) -> str:
        """
        Fallback MIME type detection for Windows.
        Uses file extension and magic bytes inspection.
        """
        # Check file header magic bytes
        if len(file_content) >= 8:
            header = file_content[:8]
            
            # Check common image formats
            if header.startswith(b'\xff\xd8\xff'):
                return 'image/jpeg'
            elif header.startswith(b'\x89PNG\r\n\x1a\n'):
                return 'image/png'
            elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
                return 'image/gif'
            elif header.startswith(b'BM'):
                return 'image/bmp'
            elif header.startswith(b'\x00\x00\x01\x00') or header.startswith(b'\x00\x00\x02\x00'):
                return 'image/x-icon'
            elif header.startswith(b'RIFF') and file_content[8:12] == b'WEBP':
                return 'image/webp'
        
        # Fallback to extension-based detection
        ext = os.path.splitext(filename)[1].lower()
        mime_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.webp': 'image/webp',
            '.ico': 'image/x-icon',
            '.svg': 'image/svg+xml',
        }
        
        return mime_map.get(ext, 'application/octet-stream')
    
    def generate_safe_filename(self, original_filename: str, user_id: Optional[int] = None) -> str:
        """Generate a safe filename for storage."""
        # Extract extension
        path = Path(original_filename)
        extension = path.suffix.lower()
        
        # Generate safe name using hash
        timestamp = str(int(time.time()))
        user_prefix = f"u{user_id}_" if user_id else "anon_"
        content_hash = hashlib.md5(original_filename.encode()).hexdigest()[:8]
        
        safe_filename = f"{user_prefix}{timestamp}_{content_hash}{extension}"
        
        return safe_filename
    
    async def quarantine_suspicious_file(
        self, 
        file_content: bytes, 
        filename: str,
        validation_result: Dict[str, Any]
    ) -> str:
        """Move suspicious file to quarantine for manual review."""
        try:
            # Generate quarantine filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = self.generate_safe_filename(filename)
            quarantine_filename = f"quarantine_{timestamp}_{safe_name}"
            quarantine_path = self.quarantine_dir / quarantine_filename
            
            # Save file to quarantine
            with open(quarantine_path, 'wb') as f:
                f.write(file_content)
            
            # Save validation report
            report_path = quarantine_path.with_suffix('.json')
            import json
            with open(report_path, 'w') as f:
                json.dump(validation_result, f, indent=2)
            
            logger.warning(f"File quarantined: {filename} -> {quarantine_filename}")
            return str(quarantine_path)
            
        except Exception as e:
            logger.error(f"Quarantine failed for {filename}: {e}")
            return ""

# Global security service instance
security_service = FileSecurityService()

def get_security_service() -> FileSecurityService:
    """Dependency to get security service instance."""
    return security_service