#########-Expense track manager-##########
import sqlite3 
from user_auth import register_user, login_user

def display_menu():
    '''Display the main menu option'''
    print("\nExpense Tracker system")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. total_sum_of_expenses")
    print("5. total_by_category")
    print("6. Exit")
    
#function to add expense
def add_expense(amount,category,description,user_id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    # Insert the expense into the database
    add_query = "INSERT INTO expenses (amount, category, description, user_id) VALUES (?, ?, ?, ?)"
    cursor.execute(add_query,(amount,category,description,user_id))
    # Commit the changes and close the connection
    conn.commit()
    print(f"Added expense: ${amount} for {category} ({description})")
    conn.close()

#function to view expense by category
def veiw_expense(user_id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    # Fetch all expenses
    view_query = "SELECT * FROM expenses WHERE user_id = ?"
    cursor.execute(view_query,(user_id,))
    rows = cursor.fetchall()

    # Display the expenses
    if rows:
        # print(f"{'ID':<5} {'Amount':<10} {'Category':<20} {'description':<20} {'date':<20}")
        # print("-" * 70)
        # for row in rows:
        #     print(f"{row[0]:<5} {row[1]:<10.2f} {row[2]:<15} {row[3]:<20} {row[4]:<20}")
        expense = [{"id": row[0], "amount": row[1], "category": row[2], "description": row[3], "date": row[4]} for row in rows]
        return expense

    else:
        return "No expenses found."

#function to delete expense by category           
def delete_expense(expenses_id,user_id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE id = ? AND user_id = ?",(expenses_id,user_id))
    expense = cursor.fetchone()
    if expense:
        # Delete the expense by ID
        delete_query = "DELETE FROM expenses WHERE id = ? AND user_id"
        cursor.execute(delete_query,(expenses_id,))
        conn.commit()
        print(f"Expense with ID {expenses_id} deleted successfully.")
    else:
        print(f"No expense found with ID {expenses_id}.")

    conn.close()
        
def total_sum_of_expenses(user_id, category=None, start_date=None, end_date=None):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    # Sum all the expenses
    total_expense_query = "SELECT SUM(amount) FROM expenses WHERE user_id = ?"
    params = [user_id]
    # Add filters for category
    if category:
        total_expense_query+= " AND category = ?"
        params.append(category)
    # Add filters for date range
    if start_date and end_date:
        total_expense_query+= " AND DATE(created_at) BETWEEN ? and ?"
        params.extend([start_date, end_date])
    cursor.execute(total_expense_query,params)
    total = cursor.fetchone()[0] or 0.0
    # Display the total expenses
    print(f"Total expenses: ${total:.2f}")
    conn.close()
    return total

def total_by_category(user_id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    total_category_query = "SELECT category, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY category"
    cursor.execute(total_category_query,(user_id,))
    rows = cursor.fetchall()
    print("\nExpenses by Category:")
    print(f"{'Category':<15} {'Total':<10}")
    print("-" * 25)
    for row in rows:
        print(f"{row[0]:<15} ${row[1]:<10.2f}")
    conn.close()

##Main function to run the program is
def main():
    print("\n######### Welcome to the Expense Tracker #########")
    print("1. Register")
    print("2. Login")
    choice = input("Choose an option (1-2): ").strip()

    user_id = None
    if choice == "1":
        username = input("Enter a username: ").strip()
        password = input("Enter a password: ").strip()
        user_id = register_user(username,password)
        if user_id is None:  # If registration failed
            print("Registration failed. Exiting...")
            exit(1)  # Exit with an error code
        print("Registration completed successfully.")

    elif choice == "2":
        username = input("Enter a username: ").strip()
        password = input("Enter a password: ").strip()
        user_id = login_user(username, password)
    else:
        print("Invalid choice. Exiting...")
        return

    if user_id is None:
        print("Authentication failed. Exiting...")
        return

    print("\nLogin successful!")
    while  True:
        display_menu()
        choice = input("Enter your choice (1-6):")
        
        if choice == "1":
            try :
                amount = float(input("\nenter the amount:"))
                category = input("\n enter the category:")
                description = input("\n enter the description:")
                add_expense(amount,category,description,user_id)
            except ValueError:
                print("Invalid input. Amount should be a number.")
                
        elif choice == "2":
            veiw_expense(user_id)
        
        elif choice == "3":
            try:
                expenses_id = int(input(f"Enter expense ID to delete: "))
                delete_expense(expenses_id,user_id)
                print(f"\nSucessfully delete the {expenses_id}")
            except ValueError:
                print("Invalid input for expense ID. Please enter a valid number.")

        elif choice == "4":
            category = input("Filter by category (press Enter to skip): ").strip() or None
            start_date = input("Start date (YYYY-MM-DD) (press Enter to skip): ").strip() or None
            end_date = input("End date (YYYY-MM-DD) (press Enter to skip): ").strip() or None
            total_sum_of_expenses(user_id,category,start_date,end_date)

        elif choice == "5":
            total_by_category(user_id)
            
        elif choice == "6":
            print("\nGoodbye!..")
            break
        
        else:
            print("Invalid choice, please try again.") 

    
            
if __name__=="__main__":
    main()