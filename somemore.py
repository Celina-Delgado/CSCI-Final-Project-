import csv

TRANSACTIONS = "transactions.csv" #not being used yet


# Add transactions
def add_transaction(transactions):
    category = input("Enter a category: (food, rent, etc..) ").lower()
    try:
        amount = float(input("Enter the amount: $"))
    except ValueError:
        print("Error: Please enter a number")
        return
    
    transaction_type = input("Income or expense? (type 'i' for income, 'e' for expense): ").lower()
    if transaction_type not in ['i', 'e']:
        print("Invalid transaction type.")
        return
    
    print("Data saved")
    transactions.append({
        "category": category,
        "amount": amount,
        "type": "income" if transaction_type == 'i' else "expense"
    })



def main():
    transactions = []

    while True:
        print("--- Budget Tracker ---")
        print("1. View Transactions")
        print("2. Add Transaction")
        
        selection = input("Choose an option (1-2): ")

        if selection == "1":
            if not transactions:
                print("No transactions recorded.")
            else:
                for t in transactions:
                    print(f"You recorded a {t['type']} of ${t['amount']} for {t['category']}.")
        elif selection == "2":
                add_transaction(transactions)
    

if __name__ == "__main__":
        main()
