import urllib.request
import os

from fastapi import FastAPI, UploadFile, File, Request
from pipeline import NovaNotes

app      = FastAPI()
pipeline = NovaNotes()

@app.post("/question")
async def give_question(file: UploadFile = File(...)):
    # Make sure the uploads folder exists
    os.makedirs("uploads", exist_ok=True)

    # Save the uploaded file
    file_path = f"uploads/temp.pdf"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    response = pipeline.get_questions_with_file(file_path=file_path)
    return {"status": "ok", "message": response}

@app.post("/answer")
async def give_response(request: Request):
    data    = await request.json()
    url     = data.get("message", "")

    urllib.request.urlretrieve(url, 'temp.png')
    
    response = pipeline.run_inference('temp.png')
    return {"status": "ok", "message": response}