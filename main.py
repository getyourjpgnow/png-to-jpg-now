# Project: PNG to JPG Now - File Conversion Tool
# Tech Stack: Python (FastAPI), HTML/CSS/JS (Vanilla), Hosting Ready

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import shutil, os, uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def homepage():
    return HTMLResponse("""
    <html>
    <head>
        <title>PNG to JPG Now</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: sans-serif;
                background: #f9f9f9;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            h1 {
                color: #333;
            }
            form {
                background: white;
                padding: 2rem;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            input[type=file] {
                padding: 0.5rem;
                margin-bottom: 1rem;
            }
            button {
                padding: 0.5rem 1rem;
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background: #45a049;
            }
        </style>
    </head>
    <body>
        <h1>PNG to JPG Now</h1>
        <form action="/convert" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/png" required><br>
            <button type="submit">Convert to JPG</button>
        </form>
    </body>
    </html>
    """)

@app.post("/convert")
async def convert_png_to_jpg(file: UploadFile = File(...)):
    temp_input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.png")
    temp_output_path = temp_input_path.replace(".png", ".jpg")

    with open(temp_input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    with Image.open(temp_input_path) as img:
        rgb = img.convert('RGB')
        rgb.save(temp_output_path, "JPEG")

    return FileResponse(temp_output_path, filename="converted.jpg")
