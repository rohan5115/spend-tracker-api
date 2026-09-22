from datetime import date

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app import models
from app.crud import create_expense, get_expenses
from app.database import Base, engine, get_db
from app.schemas import (
    ExpenseCreate,
    ExpenseResponse,
    SummaryResponse,
)
from app.services.summary import get_summary
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Spend Tracker API",
    description="A simple expense tracking API",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

@app.get("/ui")
def serve_ui():
    return FileResponse("static/index.html")

@app.get("/")
def root():
    return {"message": "Spend Tracker API is running"}


@app.post(
    "/expenses",
    response_model=ExpenseResponse,
    status_code=201,
)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
):
    return create_expense(db, expense)


@app.get(
    "/expenses",
    response_model=list[ExpenseResponse],
)
def list_expenses(
    category: str | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be later than end_date",
        )

    return get_expenses(
        db=db,
        category=category,
        start_date=start_date,
        end_date=end_date,
    )

@app.get(
    "/summary",
    response_model=SummaryResponse,
)
def summary(
    month: date | None = Query(
        default=None,
        description="Any date within the month to summarize",
    ),
    db: Session = Depends(get_db),
):
    target_date = month or date.today()

    return get_summary(
        db=db,
        target_date=target_date,
    )