from datetime import date

from pydantic import BaseModel, Field, field_validator


class ExpenseCreate(BaseModel):
    amount: float = Field(
        ...,
        gt=0,
        description="Expense amount must be greater than 0",
    )

    category: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    note: str | None = Field(
        default=None,
        max_length=500,
    )

    date: date

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Category cannot be empty")

        return value


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    note: str | None
    date: date

    model_config = {
        "from_attributes": True
    }

class CategoryInsight(BaseModel):
    category: str
    current_month_spend: float
    previous_month_spend: float
    increase_percentage: float
    message: str


class SummaryResponse(BaseModel):
    total_spend: float
    spend_by_category: dict[str, float]
    month_over_month_change: float | None
    category_insights: list[CategoryInsight]