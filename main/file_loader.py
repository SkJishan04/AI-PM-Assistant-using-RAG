from pathlib import Path


def read_file(file_path: str) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix in {".txt", ".md", ".csv"}:
        return path.read_text(encoding="utf-8", errors="ignore")

    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("Install pypdf to upload PDF files.") from exc

        reader = PdfReader(str(path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)

        if not text.strip():
            try:
                from ocr_loader import ocr_pdf
            except ImportError as exc:
                raise RuntimeError(
                    "This PDF appears to be scanned (no embedded text). "
                    "Install pytesseract and pdf2image to enable OCR fallback."
                ) from exc

            text = ocr_pdf(str(path))

            if not text.strip():
                raise RuntimeError(
                    "No text could be extracted from this PDF, even with OCR. "
                    "The scan quality may be too low."
                )

        return text

    if suffix == ".docx":
        try:
            from docx import Document
        except ImportError as exc:
            raise RuntimeError("Install python-docx to upload DOCX files.") from exc

        document = Document(str(path))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)

    raise RuntimeError(f"Unsupported file type: {suffix}")