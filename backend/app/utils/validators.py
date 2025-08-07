import os
import mimetypes
import re

MAX_FILE_SIZE_MB = 200

def is_allowed_pdf(filename: str, content_type: str, size_bytes: int) -> bool:
    if not filename.lower().endswith(".pdf"):
        return False
    if content_type not in ("application/pdf", "application/octet-stream"):
        # Some browsers send octet-stream; accept
        pass
    if size_bytes > MAX_FILE_SIZE_MB * 1024 * 1024:
        return False
    return True

SAFE_FILENAME_REGEX = re.compile(r"[^A-Za-z0-9_\-\.]")

def safe_filename(name: str) -> str:
    return SAFE_FILENAME_REGEX.sub("_", name)