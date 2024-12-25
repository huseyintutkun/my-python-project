import sys
import json
from datetime import datetime

DATA_FILE = "expenses.json"

def load_expenses():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=4)

def add_expense(amount, category, description="", date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    expenses = load_expenses()
    expense = {
        "amount": float(amount),
        "category": category,
        "description": description,
        "date": date
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"{amount} tutarındaki harcama '{category}' kategorisine eklendi.")

def list_expenses(start_date=None, end_date=None):
    expenses = load_expenses()
    filtered = expenses

    if start_date:
        filtered = [e for e in filtered if e["date"] >= start_date]
    if end_date:
        filtered = [e for e in filtered if e["date"] <= end_date]

    for e in filtered:
        print(f"{e['date']} - {e['category']}: {e['amount']} (Açıklama: {e['description']})")

def main():
    args = sys.argv[1:]
    if not args:
        print("Kullanım:")
        print("  python expense_tracker.py add <miktar> <kategori> [--description ...] [--date YYYY-MM-DD]")
        print("  python expense_tracker.py list [--start YYYY-MM-DD] [--end YYYY-MM-DD]")
        sys.exit(0)

    command = args[0]
    if command == "add":
        # Basit arg parse
        amount = args[1]
        category = args[2]
        description = ""
        date = None
        # Ek parametreleri al
        if "--description" in args:
            desc_index = args.index("--description") + 1
            description = args[desc_index]
        if "--date" in args:
            date_index = args.index("--date") + 1
            date = args[date_index]

        add_expense(amount, category, description, date)
    elif command == "list":
        start_date = None
        end_date = None
        if "--start" in args:
            start_index = args.index("--start") + 1
            start_date = args[start_index]
        if "--end" in args:
            end_index = args.index("--end") + 1
            end_date = args[end_index]

        list_expenses(start_date, end_date)
    else:
        print(f"Bilinmeyen komut: {command}")

if __name__ == "__main__":
    main()
