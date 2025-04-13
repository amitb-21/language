import fitz  # PyMuPDF
import io
from fastapi import HTTPException, UploadFile

def extract_text_from_pdf(file_stream: UploadFile, max_size_mb: int = 10) -> str:
    try:
        # Read and check file size
        file_content = file_stream.file.read()
        file_size_mb = len(file_content) / (1024 * 1024)

        if file_size_mb > max_size_mb:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum allowed size is {max_size_mb}MB."
            )

        # Reset the stream position just in case
        file_stream.file.seek(0)

        # Read PDF from memory
        text = ""
        try:
            with io.BytesIO(file_content) as pdf_stream:
                doc = fitz.open(stream=pdf_stream.read(), filetype="pdf")

                # Check for password protection
                if doc.is_encrypted:
                    raise HTTPException(
                        status_code=400,
                        detail="Cannot process password-protected PDF files."
                    )

                # Extract text from each page
                for page in doc:
                    page_text = page.get_text().strip()
                    if page_text:
                        text += page_text + "\n"

            return text.strip()

        except fitz.FileDataError:
            raise HTTPException(
                status_code=400,
                detail="Invalid or corrupted PDF file."
            )

    except HTTPException:
        # Reraise expected HTTP errors
        raise
    except Exception as e:
        # Catch-all for any unexpected error
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while processing PDF: {str(e)}"
        )
