import urllib.request

from fastapi import FastAPI, Request
from NovaNotes import NovaNotes

app      = FastAPI()
pipeline = NovaNotes()

@app.post("/question")
async def give_question(request: Request):
    data    = await request.json()
    message = data.get("message", "")
    
    response = pipeline.__ask_gpt(str(message), answer_mode = False)
    return {"status": "ok", "message": response}

@app.post("/answer")
async def give_response(request: Request):
    data    = await request.json()
    url     = data.get("message", "")

    urllib.request.urlretrieve(url, 'temp.png')
    
    response = pipeline.run_inference('temp.png')
    return {"status": "ok", "message": response}