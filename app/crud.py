from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Expense
from app.schemas import ExpenseCreate


def create_expense(
    db: Session,
    expense_data: ExpenseCreate,
) -> Expense:
    expense = Expense(
        amount=expense_data.amount,
        category=expense_data.category,
        note=expense_data.note,
        date=expense_data.date,
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


def get_expenses(
    db: Session,
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[Expense]:
    query = select(Expense)

    if category:
        query = query.where(
            Expense.category == category.strip()
        )

    if start_date:
        query = query.where(
            Expense.date >= start_date
        )

    if end_date:
        query = query.where(
            Expense.date <= end_date
        )

    query = query.order_by(
        Expense.date.desc(),
        Expense.id.desc(),
    )

    return list(db.scalars(query).all())