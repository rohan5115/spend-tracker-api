# Spend Tracker

A lightweight expense tracking application built with Python and FastAPI.

The application allows users to:

- Create expenses
- List expenses
- Filter expenses by category
- Filter expenses by date range
- View total monthly spending
- View spending by category
- Compare spending month-over-month
- Receive an insight when category spending increases by more than 20%


## Live Demo

- Frontend: https://spend-tracker-api-3zx2.onrender.com/ui
- API Docs: https://spend-tracker-api-3zx2.onrender.com/docs

> Note: The application is deployed on Render's free tier. The service may take some time to respond after a period of inactivity.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- HTML
- JavaScript
- CSS

## Running Locally

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Then open:

- UI: http://127.0.0.1:8000/ui
- API Docs: http://127.0.0.1:8000/docs

## Running Tests

```bash
python -m pytest -v
```

All automated tests pass locally.


## Project Structure

```text
spend-tracker/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── services/
│       └── summary.py
│
├── tests/
│   ├── conftest.py
│   ├── test_expenses.py
│   └── test_summary.py
│
├── static/
│   ├── index.html
│   ├── app.js
│   └── style.css
│
├── requirements.txt
├── README.md
└── .gitignore