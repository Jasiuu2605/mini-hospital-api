from sqlmodel import SQLModel, create_engine

from models import HospitalRequest  # noqa: F401

# Adres lokalnej bazy PostgreSQL
DATABASE_URL = "postgresql+psycopg:///mini_hospital"

# Silnik połączenia z bazą
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
