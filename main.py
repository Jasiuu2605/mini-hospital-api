from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

requests = [
    {
        "id": 1,
        "department": "Kardiologia",
        "item": "Monitor pacjenta",
        "quantity": 2,
        "status": "pending",
    },
    {
        "id": 2,
        "department": "Chirurgia",
        "item": "Rękawiczki jednorazowe",
        "quantity": 100,
        "status": "approved",
    },
]


@app.get("/")
def root():
    return {"message": "Mini Hospital API is running"}


@app.get("/requests")
def get_requests():
    return requests


@app.get("/requests/view", response_class=HTMLResponse)
def requests_view(request: Request):
    return templates.TemplateResponse(
        request=request, name="requests.html", context={"requests": requests}
    )


@app.get("/requests/{request_id}")
def get_request(request_id: int):
    request = next((item for item in requests if item["id"] == request_id), None)

    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    return request
