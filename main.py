from contextlib import asynccontextmanager

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import create_db_and_tables
from services.request_service import create_request as create_request_service
from services.request_service import get_all_requests, get_request_by_id


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return {"message": "Mini Hospital API is running"}


@app.get("/requests")
def get_requests():
    return get_all_requests()


@app.get("/requests/view", response_class=HTMLResponse)
def requests_view(request: Request):
    requests = get_all_requests()

    return templates.TemplateResponse(
        request=request, name="requests.html", context={"requests": requests}
    )


@app.get("/requests/create", response_class=HTMLResponse)
def create_request_view(request: Request):
    return templates.TemplateResponse(request=request, name="requests/create.html")


@app.post("/requests/create")
def create_request(
    department: str = Form(...),
    item: str = Form(...),
    quantity: int = Form(..., gt=0),
):
    create_request_service(department, item, quantity)

    return RedirectResponse(
        url="/requests/view",
        status_code=303,
    )


@app.get("/requests/{request_id}")
def get_request(request_id: int):
    request = get_request_by_id(request_id)

    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    return request
