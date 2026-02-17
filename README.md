# SmokeWatch AI Backend (Railway)

This repository contains a minimal FastAPI backend designed to be
deployed on platforms like [Railway](https://railway.app/) for the
SmokeWatch AI project. It provides two endpoints: a root health
check and a video upload endpoint that streams incoming files to
disk. This skeleton is a starting point for integrating more
sophisticated machine‑learning models (e.g. YOLO for smoke
detection) and additional API functionality.

## Endpoints

| Method | Path      | Description                              |
|-------:|-----------|------------------------------------------|
| `GET`  | `/`       | Returns a JSON object indicating the service is up |
| `POST` | `/upload` | Accepts a video file via multipart/form‑data and saves it to `uploads/` |

## Running locally

To run the server locally, first install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. You can test
file uploads using `curl` or any HTTP client:

```bash
curl -F "video=@path/to/your/video.mp4" http://localhost:8000/upload
```

## Deploying on Railway

1. Create a new project on Railway and choose “Deploy from GitHub”.
2. Select this repository. Railway will detect the `Procfile` and
   automatically install dependencies and run the app.
3. Once deployed, Railway will provide a public URL. Use that URL as
   the backend base URL in your Lovable frontend.

## Notes

* The `upload` endpoint currently only saves the incoming file and
  does not process it. Integrate your smoke detection logic here
  after saving the file.
* The repository includes a `.gitignore` to exclude uploaded files
  from version control.