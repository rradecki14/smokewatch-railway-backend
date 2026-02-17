"""SmokeWatch AI Backend for Railway deployment.

This FastAPI application provides a simple API for checking the
health of the backend and uploading video files. It is intended to be
deployed to services like Railway, which can run ASGI applications
via Uvicorn.

Endpoints:

* GET `/` – Returns a JSON status message confirming the API is running.
* POST `/upload` – Accepts a video file upload via multipart form
  data, saves it to an `uploads/` directory, and returns a JSON
  response with the uploaded filename. This endpoint is structured
  for streaming writes so that large files do not exhaust memory.

The code is kept intentionally minimal for demonstration. In a
production system you would likely add authentication, proper
validation, error handling, and integrate a machine‑learning model
such as YOLO for smoke detection.
"""

import os
import shutil
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SmokeWatch AI Backend")

# Allow cross‑origin requests so that a frontend can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory where uploaded videos are stored
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
async def root() -> dict[str, str]:
    """Health check endpoint.

    Returns a simple status message. Railway will use this to ensure
    the service is running and responsive.
    """
    return {"status": "SmokeWatch AI Backend Running"}


@app.post("/upload")
async def upload(video: UploadFile = File(...)) -> dict[str, str]:
    """Upload a video file.

    The uploaded video is streamed to disk to avoid memory bloat. The
    file is saved under the `uploads/` directory using the original
    filename. In a full application you might process the file with a
    machine‑learning model after saving.

    Args:
        video: The uploaded video file provided via multipart/form data.

    Returns:
        A JSON object containing the saved filename.
    """
    if not video.filename:
        raise HTTPException(status_code=400, detail="No video file provided")

    destination = UPLOAD_DIR / video.filename

    # Stream the file to disk in chunks
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
    finally:
        await video.close()

    return {"filename": video.filename, "detail": "Upload successful"}