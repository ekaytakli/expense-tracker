import json
from datetime import datetime

# File name where expenses will be stored
FILE_NAME = "expenses.json"

# Load existing expenses from file or create an empty list if file doesn't exist
try:
    with open(FILE_NAME, "r") as f:
        expenses = json.load(f)
except FileNotFoundError:
    expenses = []

# Default categories
CATEGORIES = ["Food", "Transport", "Entertainment", "Bills", "Other"]

# ----------------- Add Expense -----------------
def add_expense():
    print("\n📂 Categories:")
    for i, category in enumerate(CATEGORIES, 1):
        print(f"{i} - {category}")
    print(f"{len(CATEGORIES)+1} - Add a new category")

    choice = input("Select category (number): ")
    category = "Other"  # default category

    # Add new category
    if choice == str(len(CATEGORIES) + 1):
        new_cat = input("New category name: ")
        if new_cat.strip() != "":
            CATEGORIES.append(new_cat)
            category = new_cat
            print(f"✅ '{new_cat}' category added!")
    else:
        try:
            category = CATEGORIES[int(choice) - 1]
        except (IndexError, ValueError):
            print("❌ Invalid choice! Default category 'Other' will be used.")

    # Enter expense amount
    try:
        amount = float(input("Amount (USD): "))
    except ValueError:
        print("❌ Invalid amount! Saving as 0.")
        amount = 0.0

    # Enter expense date
    date_input = input("Date (YYYY-MM-DD, leave empty for today): ")
    if date_input.strip() == "":
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            date = date_input
        except ValueError:
            print("❌ Invalid date format! Using today's date.")
            date = datetime.now().strftime("%Y-%m-%d")

    expense = {"category": category, "amount": amount, "date": date}
    expenses.append(expense)
    save()
    print(f"💸 {amount} USD added under '{category}' ({date}).")

# ----------------- View Expenses -----------------
def view_expenses():
    if not expenses:
        print("\n📭 No expenses recorded yet.")
        return

    print("\n📋 Expense List:")
    for i, expense in enumerate(expenses, 1):
        category = expense.get("category", "Unknown")
        amount = expense.get("amount", 0)
        date = expense.get("date", "Unknown")
        print(f"{i}. {category} - {amount} USD - {date}")

# ----------------- Delete Expense -----------------
def delete_expense():
    view_expenses()
    if not expenses:
        return

    try:
        index = int(input("\nEnter the number of the expense to delete: ")) - 1
        if 0 <= index < len(expenses):
            removed = expenses.pop(index)
            save()
            print(f"🗑️ {removed['amount']} USD from '{removed['category']}' deleted.")
        else:
            print("❌ Invalid number!")
    except ValueError:
        print("❌ You must enter a number!")

# ----------------- Update Expense -----------------
def update_expense():
    view_expenses()
    if not expenses:
        return

    try:
        index = int(input("\nEnter the number of the expense to update: ")) - 1
        if 0 <= index < len(expenses):
            expense = expenses[index]
            print(f"\n📝 Updating: {expense['category']} - {expense['amount']} USD - {expense['date']}")

            new_amount = input("New amount (leave empty to keep current): ")
            new_category = input("New category (leave empty to keep current): ")
            new_date = input("New date (YYYY-MM-DD, leave empty to keep current): ")

            if new_amount.strip() != "":
                try:
                    expense["amount"] = float(new_amount)
                except ValueError:
                    print("❌ Invalid amount, not updated.")

            if new_category.strip() != "":
                expense["category"] = new_category

            if new_date.strip() != "":
                try:
                    datetime.strptime(new_date, "%Y-%m-%d")
                    expense["date"] = new_date
                except ValueError:
                    print("❌ Invalid date, not updated.")

            save()
            print("✅ Expense updated successfully.")
        else:
            print("❌ Invalid number!")
    except ValueError:
        print("❌ You must enter a number!")

# ----------------- View Expenses by Category -----------------
def view_by_category():
    print("\n📂 Categories:")
    for i, category in enumerate(CATEGORIES, 1):
        print(f"{i} - {category}")
    
    choice = input("Select category number to view: ")

    try:
        selected_category = CATEGORIES[int(choice) - 1]
    except (IndexError, ValueError):
        print("❌ Invalid choice! Defaulting to 'Other'.")
        selected_category = "Other"

    # Filter expenses by selected category
    filtered = [e for e in expenses if e.get("category") == selected_category]

    if not filtered:
        print(f"\n📭 No expenses recorded in '{selected_category}' category.")
        return

    print(f"\n📋 Expenses in '{selected_category}':")
    total = 0
    for i, expense in enumerate(filtered, 1):
        print(f"{i}. {expense['amount']} USD - {expense['date']}")
        total += expense["amount"]

    print(f"\n💰 Total spent in '{selected_category}': {total:.2f} USD")

# ----------------- Monthly Total -----------------
def monthly_total():
    year = input("Year (e.g., 2025): ")
    month = input("Month (1-12): ")

    total = 0
    for expense in expenses:
        try:
            date = datetime.strptime(expense["date"], "%Y-%m-%d")
            if date.year == int(year) and date.month == int(month):
                total += expense["amount"]
        except Exception:
            continue

    print(f"\n📆 Total expenses for {year}-{month}: {total:.2f} USD")

# ----------------- Save to File -----------------
def save():
    with open(FILE_NAME, "w") as f:
        json.dump(expenses, f, indent=4)

# ----------------- Main Menu -----------------
def menu():
    while True:
        print("\n==== EXPENSE TRACKER ====")
        print("1 - Add Expense")
        print("2 - View Expenses")
        print("3 - Delete Expense")
        print("4 - Update Expense")
        print("5 - Monthly Total")
        print("6 - View Expenses by Category")
        print("7 - Exit")

        choice = input("Choice: ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            update_expense()
        elif choice == "5":
            monthly_total()
        elif choice == "6":
            view_by_category()
        elif choice == "7":
            print("👋 Program exited.")
            break
        else:
            print("❌ Invalid choice!")

menu()
