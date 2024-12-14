import csv

TRANSACTIONS = "transactions.csv" #not being used yet
BUDGETS = "budgets.csv" #also not in use yet

#function to set a budget for a category
def set_budget(budgets): 
    category = input("Enter category to budget for: ").lower()
    try:
        amount = float(input("Enter the budget amount: "))
    except ValueError:
        print("Error: Enter a valud number")
        return
    budgets[category] = amount
    print(f"Budget this amount ${amount} for {category}. \n")

#function to add transactions
def add_transaction(transactions, budgets):
    category = input("Enter a category: ").lower() #asks user for category of  the transaction
    try:
        amount = float(input("Enter the amount: $")) #asks user for price of transaction
    except ValueError:
        print("Error: Please enter a number") # error message for if user does not enter a number
        return
    
    transaction_type = input("Income or expense? (type 'i' for income, 'e' for expense): ").lower() #asks user to choose if transaction was income or an expense
    if transaction_type not in ['i', 'e']:
        print("Invalid transaction type.") #error message for if user did not type i or e
        return
    
    transactions.append({
        "category": category,
        "amount": amount,
        "type": "income" if transaction_type == 'i' else "expense"
    })
    if category in budgets:
        budget_left = budgets[category] - amount if transaction_type == 'e' else budgets[category] + amount # calculates users reamaining budget for the category based on amount and if transaction was income or expense
        print(f"Your remaining budget for {category} is ${budget_left}") # tells user their remaining budget for the category

def main():
    transactions = []
    budgets = {}
    while True:
        print("<Budget Tracker>")  #menu for user to select what they want to do
        print("1. View Transactions")
        print("2. Add Transaction")
        print("3. Set Budget")
        
        selection = input("Choose an option (1-3): ") #prompt user to choose what to do

        if selection == "1":
            if not transactions:
                print("No transactions recorded.") #messge for if no transactions have been added yet
            else:
                for t in transactions:
                    print(f"You recorded a {t['type']} of ${t['amount']} for {t['category']}.")
        elif selection == "2":
                add_transaction(transactions, budgets) #runs the add transaction method if 2 is selected
        elif selection == "3":
             set_budget(budgets) # runs the set budget method if 3 is selected
                

if __name__ == "__main__":
        main()
