import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get purchases with matching user id
    purchases = db.execute("SELECT * FROM purchases WHERE user_id = ?", session["user_id"])

    # New dictionary for purchases
    purchases_dict = {}

    i = 0

    # Get content into new dict and add aditional information
    for purchase in purchases:
        quote = lookup(purchase["symbol"])

        # Get correct name from symbol
        name = quote["name"]

        # Get current price of holding
        price = quote["price"]

        # Calculate total holding sum
        total_holding = int(purchase["shares"]) * float(price)

        # Add information to dictionary
        purchases_dict[i] = {"symbol": purchase["symbol"], "name": name,
                             "shares": purchase["shares"], "price": price, "total": total_holding}

        i += 1

    # Get current cash from user
    get_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = round(get_cash[0]["cash"], 2)

    # Calculate total
    sum = 0

    for purchase in purchases_dict.values():
        sum += float(purchase["total"])

    total = cash + sum

    # Render template
    return render_template("index.html", purchases=purchases_dict, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST
    if request.method == "POST":

        # Get stock symbol
        quote = lookup(request.form.get("symbol"))

        # Ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        # Ensure stock symbol is correct
        elif not quote:
            return apology("stock not found", 400)

        elif (request.form.get("shares").isdigit() == False):
            return apology("must provide correct number of shares", 400)

        # Ensure number of shares was submitted
        elif not request.form.get("shares") or int(request.form.get("shares")) < 1:
            return apology("must provide number of shares", 400)

        # Get current stock price
        price = quote["price"]

        # Get current amount of cash from user
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        # Check if user can purchase number of shares
        total = int(request.form.get("shares")) * price

        if (cash[0]["cash"] - total) >= 0:

            # Check if user already has shares of the same stock
            owned_stocks = db.execute("SELECT * FROM purchases WHERE user_id = ? AND symbol = ?",
                                      session["user_id"], request.form.get("symbol"))

            # If shares owned -> update database entry
            if len(owned_stocks) > 0:
                # Get current number of shares
                current_shares = db.execute("SELECT shares FROM purchases WHERE user_id = ? AND symbol = ?",
                                            session["user_id"], request.form.get("symbol"))
                new_shares = int(request.form.get("shares")) + int(current_shares[0]["shares"])
                db.execute("UPDATE purchases SET shares = ? WHERE user_id = ? AND symbol = ?",
                           new_shares, session["user_id"], request.form.get("symbol"))

            # If no shares owned -> new database entry
            else:
                db.execute("INSERT INTO purchases (user_id, symbol, shares, price, total) VALUES (?, ?, ?, ?, ?)",
                           session["user_id"], request.form.get("symbol"), request.form.get("shares"), price, total)

            # Update users cash
            new_cash = cash[0]["cash"] - total
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])

            # Add to transactions
            transaction_type = "buy"
            date = datetime.now()
            db.execute("INSERT INTO transactions (user_id, transaction_type, symbol, shares, price, datetime) VALUES(?, ?, ?, ?, ?, ?)",
                       session["user_id"], transaction_type, request.form.get("symbol"), request.form.get("shares"), price, date)

            # Redirect user to home page
            return redirect("/")

        else:
            return apology("cant buy shares", 400)

    # User reached route via GET
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get transaction with matching user id
    transactions = db.execute("SELECt * FROM transactions WHERE user_id = ?", session["user_id"])

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # Return form when user reached via GET
    if request.method == "GET":
        return render_template("quote.html")

    # Return values from lookup when user reached via POST
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        else:
            quote = lookup(request.form.get("symbol"))
            if not quote:
                return apology("stock not found", 400)
            else:
                return render_template("quoted.html", quote=quote)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via GET
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST
    else:

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
        usernames = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Insert new user into database
        if len(usernames) == 0:
            password = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), password)
        else:
            return apology("username already in database", 400)

        # Remember user logged in
        users_row = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = users_row[0]["id"]

        # Redirect user to home page
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Get all symbols the user owns for select menu
    get_symbols = db.execute("SELECT symbol FROM purchases WHERE user_id = ?", session["user_id"])

    # List for symbols
    symbols = []

    for entry in get_symbols:
        symbols.append(entry["symbol"])

    # User reached route via GET
    if request.method == "GET":

        # Return template
        return render_template("sell.html", symbols=symbols)

    # User reached route vis POST
    if request.method == "POST":

        # Ensure symbol was submitted
        if request.form.get("symbol") not in symbols:
            return apology("must provide correct symbol", 400)

        # Ensure number of shares  was submitted and positive integer
        elif not request.form.get("shares") or int(request.form.get("shares")) < 1:
            return apology("must provide correct number of shares", 400)

        # Ensure user has enough shares to sell
        get_shares = db.execute("SELECT shares FROM purchases WHERE user_id = ? AND symbol = ?",
                                session["user_id"], request.form.get("symbol"))

        if int(request.form.get("shares")) <= int(get_shares[0]["shares"]):

            # Update cash of user with shares and current price
            # Get current cash from user
            get_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

            # Calculate sum of selled shares
            quote = lookup(request.form.get("symbol"))
            price = quote["price"]

            new_cash = get_cash[0]["cash"] + (int(request.form.get("shares")) * price)

            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])

        # Delete database entry if user wants to sell all shares
            if int(request.form.get("shares")) == int(get_shares[0]["shares"]):
                db.execute("DELETE FROM purchases WHERE user_id = ? AND symbol = ?", session["user_id"], request.form.get("symbol"))

        # Update entry is user does not want to sell all shares
            else:
                new_shares = int(get_shares[0]["shares"]) - int(request.form.get("shares"))
                db.execute("UPDATE purchases SET shares = ? WHERE user_id = ? AND symbol = ?",
                           new_shares, session["user_id"], request.form.get("symbol"))

                get_price = db.execute("SELECT price FROM purchases WHERE user_id = ? AND symbol = ?",
                                       session["user_id"], request.form.get("symbol"))

                new_total = get_price[0]["price"] * new_shares

                db.execute("UPDATE purchases SET total = ? WHERE user_id = ? AND symbol = ?",
                           new_total, session["user_id"], request.form.get("symbol"))

            # Add to transactions
            transaction_type = "sell"
            date = datetime.now()
            db.execute("INSERT INTO transactions (user_id, transaction_type, symbol, shares, price, datetime) VALUES(?, ?, ?, ?, ?, ?)",
                       session["user_id"], transaction_type, request.form.get("symbol"), request.form.get("shares"), price, date)

            # Redirect user to home page
            return redirect("/")

        else:
            return apology("not enough shares", 400)


@app.route("/password", methods=["GET", "POST"])
def password():
    """Change user password"""

    # User reached route via GET
    if request.method == "GET":
        return render_template("password.html")

    # User reached route via POST
    if request.method == "POST":

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide new password", 403)

        # Ensure password is confirmed
        elif not request.form.get("confirmation"):
            return apology("must confirm new password", 403)

        # Ensure both passwords are the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords are not equal", 403)

        # Update password in database
        password = generate_password_hash(request.form.get("password"))
        db.execute("UPDATE users SET hash = ? WHERE id = ?", password, session["user_id"])

    # Redirect user to home page
    return redirect("/")