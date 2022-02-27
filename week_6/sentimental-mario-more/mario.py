from cs50 import get_int

# Get positive integer between 1 and 8 inclusive
while True:
    # Ask for input
    height = get_int("Height: ")
    # Check condition
    if height > 0 and height < 9:
        break

# Draw the pyramide
for i in range(1, height + 1):
    # For loop to add spaces
    for j in range(height - i):
        print(" ", end="")

    # For loop to add hashes
    for k in range(i):
        print("#", end="")

    # Add space between blocks
    print("  ", end="")

    # For loop to add hashes
    for l in range(i):
        print("#", end="")

    print()

