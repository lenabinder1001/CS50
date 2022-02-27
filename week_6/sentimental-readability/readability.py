def main():
    # Ask user for text input
    input_text = input("Text: ")

    # Count letters
    letters = count_letters(input_text)

    # Count words
    words = count_words(input_text)

    # Count sentences
    sentences = count_sentences(input_text)

    # Calculate reading level
    index = 0.0588 * (100 * float(letters) / float(words)) - 0.296 * (100 * float(sentences) / float(words)) - 15.8

    if int(round(index) < 1):
        print("Before Grade 1")
    elif int(round(index) >= 16):
        print("Grade 16+")
    else:
        print("Grade " + str(int(round(index))))

# Funktion for counting letters


def count_letters(text):
    letters = 0

    # Iterate over every character of the text and count letters
    for character in range(len(text)):
        if (text[character] >= "a" and text[character] <= "z") or (text[character] >= "A" and text[character] <= "Z"):
            letters += 1

    return letters

# Function for counting words


def count_words(text):
    words = 0

    # Iterate over every character of the text and count words
    for character in range(len(text)):
        if text[character] == " ":
            words += 1

    # Add 1 for the last word of the text
    words += 1

    return words

# Function for counting sentences


def count_sentences(text):
    sentences = 0

    # Iterate over every character of the text and count sentences
    for character in range(len(text)):
        if text[character] == "." or text[character] == "?" or text[character] == "!":
            sentences += 1

    return sentences


main()
