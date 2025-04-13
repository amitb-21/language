from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.segment_request import SegmentRequest
from app.utils.pdf_extractor import extract_text_from_pdf
from app.models.segment_model import segment_text

app = FastAPI()

# Enable CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/segment-text")
def segment_text_api(payload: SegmentRequest):
    try:
        segments = segment_text(payload.text, payload.language)
        return {"segments": segments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/segment-pdf")
async def segment_pdf_api(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        # Pass the file directly to the extractor
        content = extract_text_from_pdf(file.file)

        if not content.strip():
            raise HTTPException(status_code=400, detail="No extractable text found in the PDF.")

        segments = segment_text(content, language="hindi")  # or detect language dynamically
        return {"segments": segments}

    except HTTPException as e:
        # Re-raise HTTP exceptions from the extractor
        raise e
    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
