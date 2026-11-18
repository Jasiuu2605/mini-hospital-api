from typing import Literal

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from services.request_service import create_request as create_request_service
from services.request_service import (
    get_all_requests,
    get_request_by_id,
    update_request_status,
)

router = APIRouter(prefix="/requests", tags=["Requests"])
templates = Jinja2Templates(directory="templates")


@router.get("")
def get_requests():
    return get_all_requests()


@router.get("/view", response_class=HTMLResponse)
def requests_view(request: Request):
    requests = get_all_requests()

    return templates.TemplateResponse(
        request=request, name="requests.html", context={"requests": requests}
    )


@router.get("/create", response_class=HTMLResponse)
def create_request_view(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="requests/create.html",
    )


@router.post("/create")
def create_request(
    department: str = Form(...), item: str = Form(...), quantity: int = Form(..., gt=0)
):
    create_request_service(department, item, quantity)

    return RedirectResponse(url="/requests/view", status_code=303)


@router.get("/{request_id}")
def get_request(request_id: int):
    request = get_request_by_id(request_id)

    if request is None:
        return HTTPException(status_code=404, detail="Request not found")

    return request


@router.patch("/{request_id}/status")
def change_request_status(request_id: int, status: Literal["pending", "approved"]):
    request = update_request_status(request_id, status)

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Request not found",
        )

    return request
