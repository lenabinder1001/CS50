import csv
import sys
import re


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py FILENAME FILENAME")

    # Read database file into a variable
    databases = []

    with open(sys.argv[1], "r") as csvfile:
        reader = csv.DictReader(csvfile)
        databases = list(reader)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as txtfile:
        sequence = txtfile.read()

    # Find longest match of each STR in DNA sequence
    repeats_agatc = longest_match(sequence, 'AGATC')
    repeats_aatg = longest_match(sequence, 'AATG')
    repeats_tatc = longest_match(sequence, 'TATC')
    repeats_ttttttct = longest_match(sequence, 'TTTTTTCT')
    repeats_tctag = longest_match(sequence, 'TCTAG')
    repeats_gata = longest_match(sequence, 'GATA')
    repeats_gaaa = longest_match(sequence, 'GAAA')
    repeats_tctg = longest_match(sequence, 'TCTG')

    # Check database for matching profiles
    match = 0
    name_match = ""

    if sys.argv[1].startswith("databases/large"):
        for element in databases:
            if int(element["AGATC"]) == repeats_agatc and int(element["AATG"]) == repeats_aatg and int(element["TATC"]) == repeats_tatc and int(element["TTTTTTCT"]) == repeats_ttttttct and int(element["TCTAG"]) == repeats_tctag and int(element["GATA"]) == repeats_gata and int(element["GAAA"]) == repeats_gaaa and int(element["TCTG"]) == repeats_tctg:
                match = 1
                name_match = element["name"]
    else:
        for element in databases:
            if int(element["AGATC"]) == repeats_agatc and int(element["AATG"]) == repeats_aatg and int(element["TATC"]) == repeats_tatc:
                match = 1
                name_match = element["name"]

    if match == 1:
        print(name_match)
    else:
        print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
