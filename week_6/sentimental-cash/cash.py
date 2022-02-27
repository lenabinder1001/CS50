from cs50 import get_float

# Ask user for input
while True:
    amount = get_float("Change owed: ")
    # Check condition
    if amount > 0:
        break

# Round cents to nearest penny
cents = round(amount * 100)

# Dictionary for coins
coins = {"quarter": 25, "dime": 10, "nickel": 5, "pennie": 1}

amount_of_coins = 0
change_left = cents

# Count minimum number of coins until no change is left
while change_left > 0:
    # Subtract quarters as often as possible
    if change_left - coins["quarter"] >= 0:
        change_left -= coins["quarter"]
    elif change_left - coins["dime"] >= 0:
        change_left -= coins["dime"]
    elif change_left - coins["nickel"] >= 0:
        change_left -= coins["nickel"]
    elif change_left - coins["pennie"] >= 0:
        change_left -= coins["pennie"]
    amount_of_coins += 1

# Print out amount of coins
print(amount_of_coins)
