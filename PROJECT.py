import json
from datetime import datetime


class Expense:
    def __init__(self, category, amount, date=None):
        self.category = category
        self.amount = amount
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"Expense(category='{self.category}', amount={self.amount}, date='{self.date}')"


class Category:
    def __init__(self, name):
        self.name = name
        self.expenses = []

    def add_expense(self, amount):
        expense = Expense(self.name, amount)
        self.expenses.append(expense)
        print(f"Expense of ${amount} added to {self.name} category on {expense.date}.")

    def total_expenses(self):
        return sum(expense.amount for expense in self.expenses)

    def __repr__(self):
        return f"Category(name='{self.name}', total_expenses={self.total_expenses()})"


class ExpenseTracker:
    def __init__(self):
        self.categories = []

    def add_category(self, name):
        category = Category(name)
        self.categories.append(category)
        print(f"Category '{name}' added to the expense tracker.")

    def get_category(self, name):
        for category in self.categories:
            if category.name == name:
                return category
        return None

    def add_expense(self, category_name, amount):
        category = self.get_category(category_name)
        if category:
            category.add_expense(amount)
        else:
            print(
                f"Category '{category_name}' does not exist. Please add the category first."
            )

    def view_category_expenses(self, category_name):
        category = self.get_category(category_name)
        if category:
            print(f"Expenses in {category.name} category:")
            for expense in category.expenses:
                print(f"  {expense}")
            print(f"Total expenses: ${category.total_expenses()}")
        else:
            print(f"Category '{category_name}' does not exist.")

    def save_expenses(self, filename="expenses.json"):
        data = {"categories": []}
        for category in self.categories:
            category_data = {
                "name": category.name,
                "expenses": [
                    {"amount": expense.amount, "date": expense.date}
                    for expense in category.expenses
                ],
            }
            data["categories"].append(category_data)

        with open(filename, "w") as file:
            json.dump(data, file)
        print(f"Expenses saved to {filename}.")

    def load_expenses(self, filename="expenses.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)

            self.categories = []
            for category_data in data["categories"]:
                category = Category(category_data["name"])
                for expense_data in category_data["expenses"]:
                    expense = Expense(
                        category.name, expense_data["amount"], expense_data["date"]
                    )
                    category.expenses.append(expense)
                self.categories.append(category)

            print(f"Expenses loaded from {filename}.")
        except FileNotFoundError:
            print(f"File '{filename}' not found. No expenses loaded.")


def main():
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Category")
        print("2. Add Expense")
        print("3. View Category Expenses")
        print("4. Save Expenses")
        print("5. Load Expenses")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            category_name = input("Enter category name: ")
            tracker.add_category(category_name)

        elif choice == "2":
            category_name = input("Enter category name: ")
            amount = float(input("Enter expense amount: "))
            tracker.add_expense(category_name, amount)

        elif choice == "3":
            category_name = input("Enter category name to view expenses: ")
            tracker.view_category_expenses(category_name)

        elif choice == "4":
            tracker.save_expenses()

        elif choice == "5":
            tracker.load_expenses()

        elif choice == "6":
            print("Exiting Expense Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
