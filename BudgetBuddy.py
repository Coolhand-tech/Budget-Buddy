import json
import matplotlib.pyplot as plt
from datetime import datetime

class BudgetBuddy:
    def __init__(self):
        self.transactions = []
        self.categories = ["Food", "Rent", "Entertainment", "Other"]
        self.load_data()

    def add_transaction(self, amount, category, description):
        if category not in self.categories:
            raise ValueError(f"Invalid category. Use: {', '.join(self.categories)}")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        transaction = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.transactions.append(transaction)
        self.save_data()
        print("Transaction added successfully!")

    def summary(self):
        if not self.transactions:
            print("No transactions yet.")
            return
        total = sum(t["amount"] for t in self.transactions)
        by_category = {cat: sum(t["amount"] for t in self.transactions if t["category"] == cat) for cat in self.categories}
        print(f"Total Spent: ${total:.2f}")
        for cat, amt in by_category.items():
            print(f"{cat}: ${amt:.2f} ({(amt/total)*100:.1f}%)")

    def plot(self):
        if not self.transactions:
            print("No data to plot.")
            return
        by_category = {cat: sum(t["amount"] for t in self.transactions if t["category"] == cat) for cat in self.categories}
        plt.pie(by_category.values(), labels=by_category.keys(), autopct='%1.1f%%')
        plt.title("Spending by Category")
        plt.show()

    def save_data(self):
        with open("transactions.json", "w") as f:
            json.dump(self.transactions, f)

    def load_data(self):
        try:
            with open("transactions.json", "r") as f:
                self.transactions = json.load(f)
        except FileNotFoundError:
            self.transactions = []

def main():
    bb = BudgetBuddy()
    while True:
        print("\n1. Add Transaction\n2. View Summary\n3. Plot Spending\n4. Exit")
        choice = input("Choose an option: ")
        try:
            if choice == "1":
                amount = float(input("Amount: "))
                category = input(f"Category ({', '.join(bb.categories)}): ")
                desc = input("Description: ")
                bb.add_transaction(amount, category, desc)
            elif choice == "2":
                bb.summary()
            elif choice == "3":
                bb.plot()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()