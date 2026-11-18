from sqlmodel import Session, select

from database import engine
from models import HospitalRequest


def get_all_requests():
    with Session(engine) as session:
        statement = select(HospitalRequest)
        result = session.exec(statement)
        return result.all()


def get_request_by_id(request_id: int):
    with Session(engine) as session:
        request = session.get(HospitalRequest, request_id)
        return request


def create_request(department: str, item: str, quantity: int):
    new_request = HospitalRequest(
        department=department,
        item=item,
        quantity=quantity,
        status="pending",
    )

    with Session(engine) as session:
        session.add(new_request)
        session.commit()
        session.refresh(new_request)
    return new_request


def update_request_status(request_id: int, new_status: str):
    with Session(engine) as session:
        request = session.get(HospitalRequest, request_id)

        if request is None:
            return None

        request.status = new_status

        session.add(request)
        session.commit()
        session.refresh(request)

        return request
