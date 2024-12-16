import csv


TRANSACTIONS = "transactions.csv"  # File to store transactions
BUDGETS = "budgets.csv"  # File to store budget data
USERS = "users.csv"  # File to store users data with passwords


# Function to save user data (username and password)
def save_user_data(user_name, password):
    try:
        with open(USERS, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == user_name:
                    print(f"User {user_name} already exists.")
                    return  # Skip saving if user exists
    except FileNotFoundError:
        pass  # if the file doesn't exist it proceeds to save the user

    with open(USERS, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_name, password])  # Stores username and password
    print(f"User {user_name} saved successfully.")


# Function to check if the password matches the stored password
def check_password(stored_password, entered_password):
    return stored_password == entered_password  # checks to see if the password entered is correct


# Function to check if the user exists and authenticate using the password
def user_exists_and_authenticated(user_name, password):
    try:
        with open(USERS, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:  # Checks if the row has both username and password
                    stored_user_name, stored_password = row
                    if stored_user_name == user_name:
                        if check_password(stored_password, password):
                            return True 
                        else:
                            return False  # Password does not match
    except FileNotFoundError:
        print("No users file found.")
    return False  # If user doesn't exist or password is incorrect


# Function for user login
def login():
    user_name = input("Please enter your username: ").strip()
    password = input("Please enter your password: ").strip()
    
    if user_exists_and_authenticated(user_name, password):
        print(f"Welcome back, {user_name}!")
        return user_name  # Returns the authenticated user's name
    else:
        print("Login failed. Please try again.")
        return None


# Function for user registration
def register():
    user_name = input("Please enter your username: ").strip() # strip method removes any leading or trailing whitespace
    password = input("Please enter your password: ").strip() 
    save_user_data(user_name, password)


# Function to set a budget for a category
def set_budget(user_name, budgets):
    category = input("Enter category to budget for: ").lower()  # Ask user which category to set a budget for.
    try:
        amount = float(input("Enter the budget amount: "))  # User inputs the amount they want as budget.
    except ValueError:
        print("Error: Enter a valid number.")  # Error message for incorrect input value.
        return
    budgets[category] = amount  # Sets the budget
    print(f"Budget this amount ${amount} for {category}. \n")  # Prints the budget set message for user.
    save_budget(user_name, budgets)  # Saves the updated budget to the file.

# Function to clear the budget for a user
def clear_budget(user_name, budgets):
    confirmation = input("Are you sure you want to clear your entire budget? (yes/no): ").lower()
    if confirmation == 'yes':
        budgets.clear()  # Clears the budget dictionary
        save_budget(user_name, budgets)  # Saves the empty budget to the file
        print("Your budget has been cleared.")
    else:
        print("Budget clearing operation cancelled.")

# Function to save the budget to the file 
def save_budget(user_name, budgets):
    file_name = f"budgets_{user_name}.csv"  # User-specific budget file
    with open(file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["category", "amount"])
        writer.writeheader()  # Write the header row
        for category, amount in budgets.items():
            writer.writerow({"category": category, "amount": amount})  # Writes each budget entry
    print("Budget Saved")


# Function to load the budget from the file
def load_budget(user_name):
    budgets = {}
    file_name = f"budgets_{user_name}.csv"  # User specific budget file
    try:
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                budgets[row["category"]] = float(row["amount"])  # Loads each budget entry
    except FileNotFoundError:
        print("No budgets file found. Starting fresh.")  # Handles error of missing budget file
    return budgets

# Function to check if expenses are within the user's budget
def check_budget(transactions, budgets):
    print("Budget Summary")
    for category, budget_amount in budgets.items():
        total_spent = sum(
            t["amount"] for t in transactions
            if t["type"] == "expense" and t["category"] == category
        )  # Calculates total spending for the category
        remaining = budget_amount - total_spent  # Calculates the remaining budget
        
        if remaining >= 0:
            print(f"{category.capitalize()}: Remaining: ${remaining:.2f}")  # Shows remaining for the category
        else:
            print(f"{category.capitalize()}: Over Budget by: ${-remaining:.2f}")  # Shows over budget for the category
    print()


# Function to save transactions to the file
def save_transactions(user_name, transactions):
    file_name = f"transactions_{user_name}.csv"  # User-specific transactions file
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


# Function to add transactions
def add_transaction(user_name, transactions, budgets):
    category = input("Enter a category: ").lower()  # Asks user for category of the transaction
    try:
        amount = float(input("Enter the amount: $"))  # Asks user for price of transaction
    except ValueError:
        print("Error: Please enter a number.")  # Error message for if user does not enter a number
        return
    
    transaction_type = input("Income or expense? (type 'i' for income, 'e' for expense): ").lower()  # Asks user to choose if transaction was income or an expense
    if transaction_type not in ['i', 'e']:
        print("Invalid transaction type.")  # Error message for if user did not type i or e
        return
    
    transactions.append({
        "category": category,
        "amount": amount,
        "type": "income" if transaction_type == 'i' else "expense"  # Adds the transaction to the list 
    })
    save_transactions(user_name, transactions)  # Save the updated transactions to the file



def main():
    choice = input("Do you want to (1) Login or (2) Register? (1/2): ")
        
    if choice == "1":
        user_name = login()  # Logs in the user
        if not user_name:
            print("Login failed. Exiting...")
            return  # Exits the program if login fails
    elif choice == "2":
        register()  # Registers a new user
        user_name = input("Please enter your username to continue: ").strip()  # Asks for username after registration
        # Direct login after registration 
        if not user_exists_and_authenticated(user_name, input("Please enter your password: ").strip()):
            print("Login failed after registration. Exiting...")
            return  # Exit if login fails
    else:
        print("Invalid choice. Please choose 1 or 2.")
        return
    
    transactions = load_transactions(user_name)  # Load transactions for the user
    budgets = load_budget(user_name)  # Load budgets for the user

    while True:
        print("<Budget Tracker>") # Menu for user to select what they want to do
        print("1. View Transactions") 
        print("2. Add Transaction")
        print("3. Set Budget")
        print("4. Check Budget")
        print("5. Clear Budget")  
        print("6. Exit") 
        
        selection = input("Choose an option (1-6): ")  # Prompt user to choose what to do

        if selection == "1":
            if not transactions:
                print("No transactions recorded.")
            else:
                for t in transactions:
                    print(f"You recorded a {t['type']} of ${t['amount']} for {t['category']}.")
        elif selection == "2":
            add_transaction(user_name, transactions, budgets)
        elif selection == "3":
            set_budget(user_name, budgets)
        elif selection == "4":
            check_budget(transactions, budgets)
        elif selection == "5":
            clear_budget(user_name, budgets)  
        elif selection == "6":
            print("Exiting Budget Tracker. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose a valid option.") # handles error incase of invalid option being selected

if __name__ == "__main__":
    main()
