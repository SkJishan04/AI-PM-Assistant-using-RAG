"""OCR fallback for scanned/image-based PDFs.

Used when pypdf's text extraction returns empty content, which typically
means the PDF has no embedded text layer (i.e., it's a scanned image).
"""

from pdf2image import convert_from_path
import pytesseract


def ocr_pdf(file_path: str) -> str:
    """Rasterizes each PDF page to an image and runs OCR to extract text."""
    pages = convert_from_path(file_path, dpi=300)
    text_parts = []

    for page_image in pages:
        page_text = pytesseract.image_to_string(page_image)
        if page_text.strip():
            text_parts.append(page_text)

    return "\n".join(text_parts)