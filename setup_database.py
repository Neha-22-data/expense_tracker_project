import sqlite3

# Connect to SQLite database (this will create the file if it doesn't exist
def setup_database():
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        # Create the expenses table if it doesn't already exist
        expenses_query = """
                CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        """
        cursor.execute(expenses_query)

        # # Insert some default categories if none exist
        # category_query = "select count(*) from a categories"
        # cursor.execute(category_query)
        # if cursor.fetchone()[0] == 0:
        #         default_category = ["Food","Transport","Entertainment","Health","Shopping","Utilities","Other"]
        #         insert_query = "INSERT INTO categories (name) VALUES (?)"
        #         cursor.executemany(insert_query([(cat,) for cat in default_category]))

        ## Commit changes and close the connection
        conn.commit()

        print("Database and expenses table setup complete.")

        conn.close()

def setup_auth_user():
       conn = sqlite3.connect("expenses.db")
       cursor = conn.cursor()

#         # Drop the `users` table if it exists
#        cursor.execute("DROP TABLE IF EXISTS user")
#        print("done")

        # Create the expenses table if it doesn't already exist
       user_query = """
                CREATE TABLE IF NOT EXISTS user(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
                )
        """
       cursor.execute(user_query) 
       # Add user_id column to expenses table to associate with users
       try:
           expenses_alter_query = """ALTER TABLE expenses
                             ADD COLUMN user_id INTEGER REFERENCES users(user_id)"""
           cursor.execute(expenses_alter_query) 

       except sqlite3.OperationalError:
            pass
       
       conn.commit()
       conn.close()
       print("Database setup complete with user authentication!")

if __name__ == "__main__":
        setup_database()
        setup_auth_user()