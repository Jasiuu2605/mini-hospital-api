from sqlmodel import Field, SQLModel


class HospitalRequest(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    department: str
    item: str
    quantity: int
    status: str = "pending"
