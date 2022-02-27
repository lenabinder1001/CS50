import os
import json
import urllib.request

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import login_required, apology

STATS = ["Todo", "In progress", "Done"]
CATEGORIES = ["Transportation", "Food", "Clothes", "Entertainment", "Rent", "Others"]

# Configurate application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///planner.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Return homepage template"""

    # Code for weather data
    # Source contain json data from api
    source = urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?lat=48.9667&lon=8.75&appid=9976fb8845c810791b4f76c71986868e").read()

    # Converting JSON data to a dictionary
    list_of_data = json.loads(source)

    # Convert kelvin to celsius
    kelvin = float(list_of_data['main']['temp'])
    temp = int(kelvin - 273.15)

    # Code for greeting
    # Get name from user
    name = db.execute("SELECT name FROM users WHERE id = ?", session["user_id"])

    # Code for todos
    # Get 3 prio 1 tasks that are not finished yet
    rows = db.execute("SELECT * FROM todos WHERE priority = '1' AND (status ='Todo' OR status = 'In progress') AND user_id = ?",
                      session["user_id"])

    # Make sure just 3 tasks get to homepage
    todos = []
    if len(rows) >= 3:
        todos.append(rows[0])
        todos.append(rows[1])
        todos.append(rows[2])

    # Code for spendings
    # Get spendings from different categories
    transportation = db.execute("SELECT category, amount FROM spendings WHERE user_id = ? AND category ='Transportation'",
                                session["user_id"])
    food = db.execute("SELECT category, amount FROM spendings WHERE user_id = ? AND category ='Food'",
                      session["user_id"])
    clothes = db.execute("SELECT category, amount FROM spendings WHERE user_id = ? AND category ='Clothes'",
                         session["user_id"])
    entertainment = db.execute("SELECT category, amount FROM spendings WHERE user_id = ? AND category ='Entertainment'",
                               session["user_id"])
    rent = db.execute("SELECT category, amount FROM spendings WHERE user_id = ? AND category ='Rent'",
                      session["user_id"])
    others = db.execute("SELECT category, amount FROM spendings WHERE user_id = ? AND category ='others'",
                        session["user_id"])

    # Sum amount spend per category and calculate totyl spending
    categories = []
    total = 0
    sum = {"Spending": "Amount per month", "Transportation": 0, "Food": 0, "Clothes": 0, "Entertainment": 0, "Rent": 0, "Others": 0}

    for i in [transportation, food, clothes, entertainment, rent, others]:
        categories.append(i)

    for element in categories:
        if len(element) != 0:
            for spending in element:
                total += float(spending["amount"])
                sum[spending["category"]] += float(spending["amount"])

    # Code for today section
    # Get date and weekday
    date = datetime.now()
    year = date.strftime("%y")
    month = date.strftime("%m")
    day = date.strftime("%d")
    date_today = day + "." + month + "." + year
    weekday = date.strftime("%a")

    # User reached route via GET
    return render_template('index.html', temp=temp, name=name[0]["name"], todos=todos, data=sum,
                           total=round(total, 2), date=date_today, weekday=weekday)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        users = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(users) != 1 or not check_password_hash(users[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = users[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user id
    session.clear()

    # User reached route via GET
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST
    else:

        # Ensure name was submitted
        if not request.form.get("name"):
            return apology("must provide name", 403)

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password is confirmed
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure both passwords are the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords are not equal", 400)

        # Check for username in database
        users = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Insert new user into database if username not taken
        if len(users) == 0:
            password = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users (username, hash, name) VALUES(?, ?, ?)",
                       request.form.get("username"), password, request.form.get("name"))
        else:
            return apology("username already taken", 400)

        # Remember user logged in
        users = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = users[0]["id"]

        # Redirect user to homepage
        return redirect("/")


@app.route("/todos")
@login_required
def todos():
    """Show all todos of user"""

    # Get all todos with matching user id
    todos = db.execute("SELECT * FROM todos WHERE user_id = ?", session["user_id"])

    return render_template("todos.html", todos=todos)


@app.route("/add_todo", methods=["GET", "POST"])
@login_required
def add_todo():
    """Add new todo"""

    # User reached route via GET
    if request.method == "GET":
        return render_template("add_todo.html")

    # User reaches route via POST
    else:

        # Ensure task name was submitted
        if not request.form.get("name"):
            return apology("must provide task name", 400)

        # Ensure priority was submitted
        if not request.form.get("priority"):
            return apology("must provide priority", 400)

        # Insert new task into database
        db.execute("INSERT INTO todos (user_id, name, status, priority) VALUES(?, ?, ?, ?)",
                   session["user_id"], request.form.get("name"), "Todo", request.form.get("priority"))

        # Redirect user to todos
        return redirect("/todos")


@app.route("/edit_todo/<int:id>", methods=["GET", "POST"])
@login_required
def edit_todo(id):
    """Change todo"""

    # User reached route via GET
    if request.method == "GET":

        # Get todo from user
        todo = db.execute("SELECT * FROM todos WHERE user_id = ? AND id = ?", session["user_id"], id)

        return render_template("edit_todo.html", stats=STATS, todo=todo[0]["name"], id=id)

    # User reached route via POST
    else:

        # Check if new name was submitted
        if request.form.get("name"):
            # Change name of todo in database
            db.execute("UPDATE todos SET name = ? WHERE user_id = ? AND id = ?",
                       request.form.get("name"), session["user_id"], id)

        # Check if new status was submitted
        if request.form.get("status"):
            # Change status of todo in database
            db.execute("UPDATE todos SET status = ? WHERE user_id = ? AND id = ?",
                       request.form.get("status"), session["user_id"], id)

        # Check if new priority was submitted
        if request.form.get("priority"):
            # Change status of todo in database
            db.execute("UPDATE todos SET priority = ? WHERE user_id = ? AND id = ?",
                       request.form.get("priority"), session["user_id"], id)

        # Redirect user to todos
        return redirect("/todos")


@app.route("/delete_todo/<int:id>")
@login_required
def delete_todo(id):
    """Delete todo"""

    # Delete todo from database
    db.execute("DELETE FROM todos WHERE user_id = ? AND id = ?", session["user_id"], id)

    # Redirect user to todos
    return redirect("/todos")


@app.route("/spendings")
@login_required
def spendings():
    """Show all spendings of user in this month"""

    # Get current month
    date = datetime.now()
    month = date.strftime("%m")

    # Get all spendings with matching user id and month
    spendings = db.execute("SELECT * FROM spendings WHERE user_id = ? AND month = ?", session["user_id"], month)

    return render_template("spendings.html", spendings=spendings)


@app.route("/add_spending", methods=["GET", "POST"])
@login_required
def add_spending():
    """Add new spending"""

    # User reached route via GET
    if request.method == "GET":
        return render_template("add_spending.html", categories=CATEGORIES)

    # User reaches route via POST
    else:

        # Ensure spending name was submitted
        if not request.form.get("name"):
            return apology("must provide spending name", 400)

        # Ensure amount was submitted
        elif not request.form.get("amount"):
            return apology("must provide spending amount", 400)

        # Ensure category was submitted
        elif not request.form.get("category"):
            return apology("must provide category", 400)

        # Ensure amount is correct
        # Check if there is a point in string
        if "." in request.form.get("amount"):
            divided = request.form.get("amount").split(".")
            # Check if second string has length 2 and contains only digits
            if len(divided[1]) == 2 and divided[1].isdigit():
                if divided[0].isdigit():
                    # Get current date
                    date = datetime.now()
                    year = date.strftime("%y")
                    month = date.strftime("%m")
                    day = date.strftime("%d")

                    # Insert new spending into database
                    db.execute("INSERT INTO spendings (user_id, name, amount, category, day, month, year) VALUES(?, ?, ?, ?, ?, ?, ?)",
                               session["user_id"], request.form.get("name"), request.form.get("amount"), request.form.get("category"),
                               day, month, year)

                    # Redirect user to spendings
                    return redirect("/spendings")
                else:
                    return apology("must provide correct amount", 400)
            else:
                return apology("must provide correct amount", 400)
        else:
            return apology("must provide correct amount", 400)


@app.route("/edit_spending/<int:id>", methods=["GET", "POST"])
@login_required
def edit_spending(id):
    """Change spending"""

    # User reached route via GET
    if request.method == "GET":

        # Get todo from user
        spending = db.execute("SELECT * FROM spendings WHERE user_id = ? AND id = ?", session["user_id"], id)

        return render_template("edit_spending.html", categories=CATEGORIES, spending=spending[0]["name"],
                               id=id, amount=spending[0]["amount"])

    # User reached route via POST
    else:

        # Check if new name was submitted
        if request.form.get("name"):
            # Change name of spending in database
            db.execute("UPDATE spendings SET name = ? WHERE user_id = ? AND id = ?",
                       request.form.get("name"), session["user_id"], id)

        # Check if new amount was submitted
        if request.form.get("amount"):
            # Change amount of spending in database
            db.execute("UPDATE spendings SET amount = ? WHERE user_id = ? AND id = ?",
                       request.form.get("amount"), session["user_id"], id)

        # Check if new category was submitted
        if request.form.get("category"):
            # Change category of spending in database
            db.execute("UPDATE spendingd SET category = ? WHERE user_id = ? AND id = ?",
                       request.form.get("category"), session["user_id"], id)

        # Redirect user to todos
        return redirect("/spendings")


@app.route("/delete_spending/<int:id>")
@login_required
def delete_spending(id):
    """Delete spending"""

    # Delete todo from database
    db.execute("DELETE FROM spendings WHERE user_id = ? AND id = ?", session["user_id"], id)

    # Redirect user to todos
    return redirect("/spendings")
