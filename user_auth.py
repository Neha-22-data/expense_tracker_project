import bcrypt
import sqlite3

def register_user(username, password):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    # Hash the password
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        register_query = """INSERT INTO user(username, password) VALUES(?,?)"""
        cursor.execute(register_query, (username, password))
        conn.commit()
        user_id = cursor.lastrowid  # Get the newly registered user's ID
        print("User registered successfully!")
        return user_id
    except sqlite3.IntegrityError as e:
        # print("Username already exists. Please choose another.")
        print(f"DEBUG: IntegrityError - {e}")
        if "UNIQUE constraint failed" in str(e):
            print("Username already exists. Please choose another.")
        else:
            print("An unexpected database error occurred.")
        return None
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    login_query = "SELECT user_id,password FROM user WHERE username = ?"
    cursor.execute(login_query, (username,))
    user = cursor.fetchone()
    
    if user :
        # Convert stored hashed password (bytes) to string
        stored_hashed_password = user[1] # Already in bytes
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password): 
            print("Login Successful!")
            return user[0] # Return user_id for session tracking
    
    else :
        print("Invalid username or password.")
        return None
  




