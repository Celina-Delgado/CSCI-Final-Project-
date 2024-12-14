import csv

TRANSACTIONS = "transactions.csv" #not being used yet
BUDGETS = "budgets.csv" #also not in use yet

#function to set a budget for a category
def set_budget(budgets): 
    category = input("Enter category to budget for: ").lower()#asks user which category they want to set budget for. 
    try:
        amount = float(input("Enter the budget amount: "))#user inputs the amount they want as budget 
    except ValueError:
        print("Error: Enter a valid number")#error message for wrong input value
        return
    budgets[category] = amount#sets the budget 
    print(f"Budget this amount ${amount} for {category}. \n")#prints the budget set message for user

#function to save the budget to the file 
def save_budget(budgets): #not in use yet 
    with open(BUDGETS,'w') as file:
        writer = csv.DictWriter(file, fieldnames=["category", "amount"])
        writer.writeheader()
        for category, amount in budgets.items():
            writer.writerow({"category": category, "amount": amount})
    print("Budget Saved")

def check_budget(transactions, budgets):
    print("Budget Summary")
    for category, budgets_amount in budgets.items():
        total_spent = sum(t["amount"] for t in transactions
        if t["type"] == "expense" and t["category"] == category)
        remaining = budgets_amount - total_spent
        if remaining >=0:
            print(f" remaining: ${remaining: }")
        else:
            print(f"Over Budget by $ {-remaining: }")
    print()



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
    

def main():
    transactions = []
    budgets = {}
    while True:
        print("<Budget Tracker>")  #menu for user to select what they want to do
        print("1. View Transactions")
        print("2. Add Transaction")
        print("3. Set Budget")
        print("4. Check Budget")
        
        selection = input("Choose an option (1-4): ") #prompt user to choose what to do

        if selection == "1":
            if not transactions:
                print("No transactions recorded.") #message for if no transactions have been added yet
            else:
                for t in transactions:
                    print(f"You recorded a {t['type']} of ${t['amount']} for {t['category']}.")
        elif selection == "2":
            add_transaction(transactions, budgets) #runs the add transaction method if 2 is selected
        elif selection == "3":
            set_budget(budgets) # runs the set budget method if 3 is selected
        elif selection == "4":
            check_budget(transactions, budgets)
            
                

if __name__ == "__main__":
        main()
