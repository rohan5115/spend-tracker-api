const expenseForm = document.getElementById("expense-form");

const amountInput = document.getElementById("amount");
const categoryInput = document.getElementById("category");
const noteInput = document.getElementById("note");
const dateInput = document.getElementById("date");

const message = document.getElementById("message");

const totalSpend = document.getElementById("total-spend");
const momChange = document.getElementById("mom-change");

const categoryList = document.getElementById("category-list");
const insightList = document.getElementById("insight-list");


function setDefaultDate() {
    const today = new Date();

    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");

    dateInput.value = `${year}-${month}-${day}`;
}


async function loadSummary() {
    try {
        const response = await fetch("/summary");

        if (!response.ok) {
            throw new Error("Failed to load summary");
        }

        const data = await response.json();

        totalSpend.textContent =
            `₹${data.total_spend.toFixed(2)}`;

        if (data.month_over_month_change === null) {
            momChange.textContent = "N/A";
        } else {
            const change = data.month_over_month_change;
            const sign = change > 0 ? "+" : "";

            momChange.textContent =
                `${sign}${change.toFixed(2)}%`;
        }

        categoryList.innerHTML = "";

        const categories =
            Object.entries(data.spend_by_category);

        if (categories.length === 0) {
            categoryList.innerHTML =
                "<li>No expenses yet.</li>";
        } else {
            categories.forEach(([category, amount]) => {
                const li = document.createElement("li");

                li.textContent =
                    `${category}: ₹${amount.toFixed(2)}`;

                categoryList.appendChild(li);
            });
        }

        insightList.innerHTML = "";

        if (data.category_insights.length === 0) {
            insightList.innerHTML =
                "<li>No insights.</li>";
        } else {
            data.category_insights.forEach((insight) => {
                const li = document.createElement("li");

                li.textContent = insight.message;

                insightList.appendChild(li);
            });
        }

    } catch (error) {
        console.error(error);

        message.textContent =
            "Unable to load summary.";
    }
}


expenseForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();

        message.textContent = "";

        const expense = {
            amount: Number(amountInput.value),
            category: categoryInput.value.trim(),
            note: noteInput.value.trim() || null,
            date: dateInput.value
        };

        try {
            const response = await fetch(
                "/expenses",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(expense)
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail || "Failed to add expense."
                );
            }

            message.textContent =
                "Expense added successfully.";

            expenseForm.reset();

            setDefaultDate();

            await loadSummary();

        } catch (error) {
            console.error(error);

            message.textContent =
                error.message;
        }
    }
);


setDefaultDate();

loadSummary();