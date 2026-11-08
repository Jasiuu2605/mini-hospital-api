from fastapi import FastAPI, HTTPException

app = FastAPI()

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


@app.get("/requests/{request_id}")
def get_request(request_id: int):
    request = next((item for item in requests if item["id"] == request_id), None)

    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    return request
