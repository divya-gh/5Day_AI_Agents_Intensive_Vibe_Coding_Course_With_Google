"""
ocr_simulator.py
----------------
Pure-Python simulated OCR module.

All outputs are deterministic per (filename, file_size_bytes, content_type) so
repeated uploads of the same file produce consistent metadata rows, making it
easy to spot duplicates or test idempotency.
"""

import hashlib
import random
from typing import List

# ---------------------------------------------------------------------------
# Tag mappings
# ---------------------------------------------------------------------------

# Extension → semantic tags
_EXTENSION_TAGS: dict[str, List[str]] = {
    ".pdf":  ["pdf", "document", "printable"],
    ".docx": ["docx", "document", "word"],
    ".doc":  ["doc", "document", "word", "legacy"],
    ".txt":  ["txt", "plaintext", "document"],
    ".png":  ["png", "image", "raster"],
    ".jpg":  ["jpg", "image", "raster", "photo"],
    ".jpeg": ["jpeg", "image", "raster", "photo"],
    ".gif":  ["gif", "image", "animated"],
    ".tiff": ["tiff", "image", "raster", "high-res"],
    ".bmp":  ["bmp", "image", "raster"],
    ".xlsx": ["xlsx", "spreadsheet", "excel"],
    ".xls":  ["xls", "spreadsheet", "excel", "legacy"],
    ".pptx": ["pptx", "presentation", "slides"],
    ".ppt":  ["ppt", "presentation", "slides", "legacy"],
    ".csv":  ["csv", "tabular", "data"],
    ".json": ["json", "data", "structured"],
    ".xml":  ["xml", "data", "structured", "markup"],
    ".html": ["html", "web", "markup"],
    ".md":   ["markdown", "document", "plaintext"],
    ".mp4":  ["mp4", "video", "media"],
    ".mp3":  ["mp3", "audio", "media"],
    ".zip":  ["zip", "archive", "compressed"],
}

# MIME category → extra tag
_MIME_CATEGORY_TAGS: dict[str, str] = {
    "image":       "visual-content",
    "video":       "media-rich",
    "audio":       "audio-content",
    "application": "binary",
    "text":        "text-based",
}

# ---------------------------------------------------------------------------
# Word-count model
# ---------------------------------------------------------------------------
# Approximate bytes-per-word ratios per broad file category.
# PDFs and office docs are denser (lots of binary overhead).
_BYTES_PER_WORD: dict[str, float] = {
    "text":        5.5,   # plain text is compact
    "image":       200.0,  # images have very few "words" (alt-text equivalent)
    "video":       500.0,
    "audio":       1000.0,
    "application": 80.0,   # generic binary: PDF, DOCX, etc.
}
_MIN_WORD_COUNT = 10
_MAX_WORD_COUNT = 50_000


def _mime_category(content_type: str) -> str:
    """Return the top-level MIME category (e.g. 'image' from 'image/png')."""
    if not content_type:
        return "application"
    return content_type.split("/")[0].lower()


def _seed_from_file(filename: str, file_size_bytes: int) -> int:
    """Produce a stable integer seed from filename + size."""
    key = f"{filename}:{file_size_bytes}"
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % (2**32)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def simulate_ocr(
    filename: str,
    file_size_bytes: int,
    content_type: str,
) -> dict:
    """
    Simulate OCR processing and return extracted metadata.

    Parameters
    ----------
    filename : str
        The original uploaded file name (e.g. "invoice_2024.pdf").
    file_size_bytes : int
        Size of the file in bytes as reported by GCS.
    content_type : str
        MIME type of the file (e.g. "application/pdf").

    Returns
    -------
    dict with keys:
        word_count          int
        confidence_score    float  (0.70 – 0.99)
        tags                list[str]
    """
    rng = random.Random(_seed_from_file(filename, file_size_bytes))

    category = _mime_category(content_type)

    # --- word_count ---
    bpw = _BYTES_PER_WORD.get(category, 80.0)
    raw_count = int(file_size_bytes / bpw)
    word_count = max(_MIN_WORD_COUNT, min(_MAX_WORD_COUNT, raw_count))

    # --- confidence_score ---
    # Images and binary files get a slightly lower simulated confidence
    base_low  = 0.70 if category in ("image", "video", "audio") else 0.82
    base_high = 0.95 if category in ("image", "video", "audio") else 0.99
    confidence_score = round(rng.uniform(base_low, base_high), 4)

    # --- tags ---
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    tags: List[str] = list(_EXTENSION_TAGS.get(ext, ["unknown"]))

    mime_extra = _MIME_CATEGORY_TAGS.get(category)
    if mime_extra and mime_extra not in tags:
        tags.append(mime_extra)

    return {
        "word_count":       word_count,
        "confidence_score": confidence_score,
        "tags":             tags,
    }
