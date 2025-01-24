from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from user_auth import register_user, login_user
from expenses_track_app import add_expense, veiw_expense, delete_expense, total_sum_of_expenses, total_by_category


app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session handling

@app.route('/')
def index():
    if "user_id" in session:
        return render_template("index.html", username=session["username"])
    return redirect(url_for("login"))

# Register Endpoint
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = register_user(username, password)
        if user_id:
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        else:
            flash("Username already exists. Try another one.", "danger")
    return render_template("register.html")

# login Endpoint
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = login_user(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.", "danger")
    return render_template("login.html")

# logout endpoint
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logout.","info")
    return redirect(url_for("login"))

@app.route("/add_expense", methods=["GET", "POST"])
def add_expense_route():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            category = request.form["category"]
            description = request.form["description"]
            add_expense(amount, category, description, session["user_id"])
            flash("Expense added successfully!", "success")
        except ValueError:
            flash("Invalid amount. Please enter a number.", "danger")
        return redirect(url_for("index"))
    return render_template("add_expense.html")

# View Expenses
@app.route("/view_expenses")
def view_expenses():
    user_id = session.get('user_id') 
    if not user_id:
        return redirect(url_for("login"))
    print(session['user_id'])
    expenses = veiw_expense(user_id)  # Returns a list of expenses
    print("Expenses fetched for template:", expenses)
    return render_template("expenses.html", expenses=expenses)

# Delete Expense
@app.route("/delete_expense/<int:expense_id>", methods=["POST"])
def delete_expense_route(expense_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    delete_expense(expense_id, session["user_id"])
    flash(f"Expense with ID {expense_id} deleted successfully.", "success")
    return redirect(url_for("view_expenses"))

if __name__ == "__main__":
    app.run(debug=True)
