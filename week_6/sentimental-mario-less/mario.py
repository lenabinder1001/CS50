from cs50 import get_int

# Ask user for height (number between 1 and 8 inklusive)
while True:
    # Ask for input
    height = get_int("Height: ")
    # Check condition
    if height > 0 and height < 9:
        break

# Draw the pyramide
for i in range(1, height + 1):
    for j in range(height - i):
        print(" ", end="")
    for k in range(i):
        print("#", end="")
    print()

