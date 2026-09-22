from collections import defaultdict
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Expense
from app.schemas import CategoryInsight, SummaryResponse


def get_month_boundaries(target_date: date) -> tuple[date, date, date, date]:
    current_start = target_date.replace(day=1)

    if current_start.month == 1:
        previous_start = current_start.replace(
            year=current_start.year - 1,
            month=12,
        )
    else:
        previous_start = current_start.replace(
            month=current_start.month - 1,
        )

    next_month = (
        current_start.replace(year=current_start.year + 1, month=1)
        if current_start.month == 12
        else current_start.replace(month=current_start.month + 1)
    )

    current_end = next_month.fromordinal(next_month.toordinal() - 1)

    previous_end = current_start.fromordinal(
        current_start.toordinal() - 1
    )

    return (
        current_start,
        current_end,
        previous_start,
        previous_end,
    )


def get_summary(
    db: Session,
    target_date: date,
) -> SummaryResponse:

    (
        current_start,
        current_end,
        previous_start,
        previous_end,
    ) = get_month_boundaries(target_date)

    expenses = db.scalars(
        select(Expense).where(
            Expense.date >= previous_start,
            Expense.date <= current_end,
        )
    ).all()

    current_expenses = [
        expense
        for expense in expenses
        if current_start <= expense.date <= current_end
    ]

    previous_expenses = [
        expense
        for expense in expenses
        if previous_start <= expense.date <= previous_end
    ]

    total_spend = sum(
        expense.amount
        for expense in current_expenses
    )

    spend_by_category: dict[str, float] = defaultdict(float)

    for expense in current_expenses:
        spend_by_category[expense.category] += expense.amount

    current_total = sum(
        expense.amount
        for expense in current_expenses
    )

    previous_total = sum(
        expense.amount
        for expense in previous_expenses
    )

    if previous_total == 0:
        month_over_month_change = None
    else:
        month_over_month_change = (
            (current_total - previous_total)
            / previous_total
        ) * 100

    previous_category_spend: dict[str, float] = defaultdict(float)

    for expense in previous_expenses:
        previous_category_spend[expense.category] += expense.amount

    category_insights = []

    for category, current_amount in spend_by_category.items():
        previous_amount = previous_category_spend.get(
            category,
            0,
        )

        if previous_amount > 0:
            increase_percentage = (
                (current_amount - previous_amount)
                / previous_amount
            ) * 100

            if increase_percentage > 20:
                category_insights.append(
                    CategoryInsight(
                        category=category,
                        current_month_spend=current_amount,
                        previous_month_spend=previous_amount,
                        increase_percentage=round(
                            increase_percentage,
                            2,
                        ),
                        message=(
                            f"{category} spending increased "
                            f"by more than 20% compared "
                            f"with the previous month."
                        ),
                    )
                )

    return SummaryResponse(
        total_spend=round(total_spend, 2),
        spend_by_category={
            category: round(amount, 2)
            for category, amount in spend_by_category.items()
        },
        month_over_month_change=(
            round(month_over_month_change, 2)
            if month_over_month_change is not None
            else None
        ),
        category_insights=category_insights,
    )