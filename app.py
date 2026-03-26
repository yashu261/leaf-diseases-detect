from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from utils import convert_image_to_base64_and_test

# ✅ Create app ONLY ONCE
app = FastAPI(title="Leaf Disease Detection API", version="1.0.0")

# ✅ Add CORS AFTER app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ API endpoint
@app.post('/disease-detection-file')
async def disease_detection_file(file: UploadFile = File(...)):
    try:
        logger.info("Received image file")

        contents = await file.read()
        result = convert_image_to_base64_and_test(contents)

        if result is None:
            raise HTTPException(status_code=500, detail="Failed to process image")

        return JSONResponse(content=result)

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Frontend (MAIN PAGE)
@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html") as f:
        return f.read()