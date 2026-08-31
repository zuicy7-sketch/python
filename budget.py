import json
from datetime import datetime

FILE_NAME = "budget_data.json"

def load_data():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Data file has a problem. Starting with empty data.")
        return []

def save_data(transactions):
    with open(FILE_NAME, "w") as file:
        json.dump(transactions, file, indent=4)

def show_transactions(transactions):
    if len(transactions) == 0:
        print("No transactions found.")
        return False

    print("\n--- Transactions ---")
    for i in range(len(transactions)):
        item = transactions[i]
        print(str(i + 1) + ". " + item["date"] + " | " + item["type"] +
              " | " + str(item["amount"]) + " | " + item["category"] +
              " | " + item["note"])
    return True

def add_transaction(transactions):
    print("\n--- Add Transaction ---")

    while True:
        transaction_type = input("Type (income/expense): ").lower().strip()
        if transaction_type == "income" or transaction_type == "expense":
            break
        print("Please enter income or expense.")

    while True:
        try:
            amount = float(input("Amount: "))
            if amount > 0:
                break
            print("Amount must be more than 0.")
        except ValueError:
            print("Please enter a number.")

    while True:
        category = input("Category: ").strip()
        if category != "":
            break
        print("Category cannot be empty.")

    date = input("Date (DD-MM-YYYY) [today]: ").strip()
    if date == "":
        date = datetime.today().strftime("%d-%m-%Y")
    else:
        try:
            datetime.strptime(date, "%d-%m-%Y")
        except ValueError:
            print("Invalid date. Today's date will be used.")
            date = datetime.today().strftime("%d-%m-%Y")

    note = input("Note (optional): ").strip()

    transaction = {
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "date": date,
        "note": note
    }
    transactions.append(transaction)
    save_data(transactions)
    print("Transaction added and saved.")

def view_summary(transactions):
    income = 0
    expense = 0

    for item in transactions:
        if item["type"] == "income":
            income = income + item["amount"]
        else:
            expense = expense + item["amount"]

    print("\n--- Summary ---")
    print("Total Income:   Rs.", format(income, ".2f"))
    print("Total Expenses: Rs.", format(expense, ".2f"))
    print("Net Balance:    Rs.", format(income - expense, ".2f"))

def view_by_category(transactions):
    categories = {}

    for item in transactions:
        key = item["type"] + " - " + item["category"]
        if key not in categories:
            categories[key] = 0
        categories[key] = categories[key] + item["amount"]

    print("\n--- By Category ---")
    if len(categories) == 0:
        print("No transactions found.")
    else:
        for key in categories:
            print(key + ": Rs. " + format(categories[key], ".2f"))

def manage_transaction(transactions):
    if not show_transactions(transactions):
        return

    action = input("Enter d to delete or e to edit: ").lower().strip()
    if action != "d" and action != "e":
        print("Invalid choice.")
        return

    try:
        number = int(input("Enter transaction number: "))
        index = number - 1
        if index < 0 or index >= len(transactions):
            print("Transaction number not found.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    if action == "d":
        transactions.pop(index)
        save_data(transactions)
        print("Transaction deleted.")
    else:
        item = transactions[index]
        print("Press Enter to keep the old value.")

        new_category = input("Category [" + item["category"] + "]: ").strip()
        if new_category != "":
            item["category"] = new_category

        new_note = input("Note [" + item["note"] + "]: ").strip()
        if new_note != "":
            item["note"] = new_note

        save_data(transactions)
        print("Transaction updated.")

def main():
    transactions = load_data()
    print("Welcome to Budget Tracker!")

    while True:
        print("\n1. Add transaction")
        print("2. View summary")
        print("3. View by category")
        print("4. Delete/Edit transaction")
        print("5. Exit")

        choice = input("> ").strip()

        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_summary(transactions)
        elif choice == "3":
            view_by_category(transactions)
        elif choice == "4":
            manage_transaction(transactions)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Please choose a number from 1 to 5.")

main()
