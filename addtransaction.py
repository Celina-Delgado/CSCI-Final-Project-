import csv

TRANSACTIONS = "transactions.csv"


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
    
    print("Data saved (not really)")
    transactions.append({
        "category": category,
        "amount": amount,
        "type": "income" if transaction_type == 'i' else "expense"
    })


transactions = []
while True:
    add_transaction(transactions)
