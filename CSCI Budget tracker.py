import csv

TRANSACTIONS = "transactions.csv" #file to store transactions
BUDGETS = "budgets.csv" # file to store budget data
USERS = "users.csv"  #file to store users data

#function to set a budget for a category
def set_budget(user_name, budgets): 
    category = input("Enter category to budget for: ").lower() #asks user which category they want to set budget for. 
    try:
        amount = float(input("Enter the budget amount: ")) #user inputs the amount they want as budget 
    except ValueError:
        print("Error: Enter a valid number")#error message for wrong input value
        return
    budgets[category] = amount #sets the budget 
    print(f"Budget this amount ${amount} for {category}. \n")#prints the budget set message for user
    save_budget(budgets) #saves the updated budget to the file
    
#function to save the budget to the file 
def save_budget(user_name, budgets):
    file_name = f"budgets_{user_name}.csv"  # User-specific budget file
    with open(file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["category", "amount"])
        writer.writeheader()  # Write the header row
        for category, amount in budgets.items():
            writer.writerow({"category": category, "amount": amount})  # Write each budget entry
    print("Budget Saved")

    
# Function to load the budget from the file
def load_budget(user_name):
    budgets = {}
    file_name = f"budgets_{user_name}.csv"  # User-specific budget file
    try:
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                budgets[row["category"]] = float(row["amount"])  # Load each budget entry
    except FileNotFoundError:
        print("No budgets file found. Starting fresh.")  # Handle missing budget file
    return budgets


#function to check if expenses are within the users budget
def check_budget(transactions, budgets):
    print("Budget Summary")
    for category, budgets_amount in budgets.items():
        total_spent = sum(t["amount"] for t in transactions
            if t["type"] == "expense" and t["category"] == category) #calculates total spending of whichever category the user selects
        remaining = budgets_amount - total_spent # calculates users remaining budget
        if remaining >=0:
                print(f" remaining: ${remaining: }")
        else:
                print(f"Over Budget by $ {-remaining: }")
    print()
    
    
#function to save transactions to the file
def save_transactions(user_name, transactions):
    file_name = f"transactions_{user_name}.csv"  # User specific transactions file
    with open(file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["category", "amount", "type"])
        writer.writeheader()  
        for transaction in transactions:
            writer.writerow(transaction)  # Writes each transaction
    print("Transactions Saved")


# Function to load transactions from the file
def load_transactions(user_name):
    transactions = []
    file_name = f"transactions_{user_name}.csv"  # User specific transactions file
    try:
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append({"category": row["category"], "amount": float(row["amount"]), "type": row["type"]})  # Load each transaction
    except FileNotFoundError:
        print("No transactions file found. Starting fresh.")  # Handle missing transaction file/exception handling
    return transactions

#function to add transactions
def add_transaction(user_name, transactions, budgets):
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
        "type": "income" if transaction_type == 'i' else "expense" # adds the transaction to the list 
    })
    save_transactions(user_name, transactions)  # Save the updated transactions to the file

    
 # Function to save user data
def save_user_data(user_name):
    try:
        with open(USERS, 'r') as file: #file handling
            if any(row[0] == user_name for row in csv.reader(file)):
                return  # Skips saving if user already exists
    except FileNotFoundError: #exception handling
        pass

    with open(USERS, 'a', newline='') as file: #adds the user's name to the file
        writer = csv.writer(file)
        writer.writerow([user_name])  # writes the new user's name as a new row in the file

# Function to check if the user exists
def user_exists(user_name):
    try:
        with open(USERS, 'r') as file:
            reader = csv.reader(file)
            return any(row[0] == user_name for row in reader)  # Check if the user's name is in the file
    except FileNotFoundError: #exception handling
        return False

# Main program function
def main():
    user_name = input("Please enter your name: ").strip() #asks user to enter their name and removes any leading or trailing whitespace with the strip() method.
    if user_exists(user_name): 
        print(f"Welcome back, {user_name}!")
        transactions = load_transactions(user_name)  # Load transactions for the user
        budgets = load_budget(user_name)  # Load budgets for the user
    else:
        print(f"Hello, {user_name}! Starting a new budget tracker for you.")
        transactions = []
        budgets = {}
        save_user_data(user_name)  # Save the new user's name

    
    while True:
        print("<Budget Tracker>")  #menu for user to select what they want to do
        print("1. View Transactions") 
        print("2. Add Transaction")
        print("3. Set Budget")
        print("4. Check Budget")
        print("5. Exit") 
        
        selection = input("Choose an option (1-5): ") #prompt user to choose what to do

        if selection == "1":
            if not transactions:
                print("No transactions recorded.") #message for if no transactions have been added yet
            else:
                for t in transactions:
                    print(f"You recorded a {t['type']} of ${t['amount']} for {t['category']}.")
        elif selection == "2":
            add_transaction(user_name, transactions, budgets)
        elif selection == "3":
            set_budget(budgets) 
        elif selection == "4":
            check_budget(user_name, transactions, budgets)
        elif selection == "5":
            print("Exiting Budget Tracker. Goodbye have a good day!")  # Exit message closing the program
            break
        else:
            print("Invalid selection. Please choose a valid option.")  # Handles error of invalid menu selection

if __name__ == "__main__":
    main()
