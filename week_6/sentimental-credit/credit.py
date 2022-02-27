from cs50 import get_string

# Get credit card number from user
card_number = get_string("Number: ")

# Get first digit of number
first_digit = card_number[0]

# Get first two digits of number
first_two_digits = card_number[:2]

# Sum digits from card number
sum = 0
counter = 0

