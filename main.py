# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.controller import Controller
import json

app = FastAPI()
c = Controller()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Page(BaseModel):
    activities: list[str]
    breakTime: int
    from_: int
    to: int
    weekDays: list[int]

import uuid

@app.get("/")
def create_and_redirect():
    page_id = str(uuid.uuid4())
    default_page = {
        "activities": ["meditate", "stretch", "go for a walk"],
        "breakTime": 10,
        "from": 9,
        "to": 17,
        "weekDays": [0, 1, 2, 3, 4, 5]
    }
    c.db.create_or_update_page(page_id, json.dumps(default_page))
    return RedirectResponse(url=f"/{page_id}", status_code=302)

@app.get("/api/{page_id}")
def api_get_page(page_id: str):
    page = c.db.get_page(page_id)
    if not page:
        return JSONResponse(status_code=404, content={"message": "Page not found"})
    return json.loads(page)

@app.get("/{page_id}")
def serve_page(page_id: str):
    if not c.db.get_page(page_id):
        return JSONResponse(status_code=404, content={"message": "Page not found"})
    return FileResponse("templates/index.html", media_type="text/html")

@app.post("/api/{page_id}")
async def save_page(page_id: str, request: Request):
    data = await request.json()
    json_data = json.dumps(data)
    c.db.create_or_update_page(page_id, json_data)
    return {"message": "Page saved"}

