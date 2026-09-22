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