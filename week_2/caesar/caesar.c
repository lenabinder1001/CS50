#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

string get_ciphertext(string text, int number);
bool only_digits(string text);

int main(int argc, string argv[])
{
    // Check, if the program was run with a single command-line argument
    if (argc == 2)
    {
        // Check if key only contains digits between 0 and 9
        if (only_digits(argv[1]) == true)
        {
            string plaintext = get_string("plaintext:  ");

            int key = atoi(argv[1]) % 26;

            // Get ciphercode out of plaintext
            string ciphertext = get_ciphertext(plaintext, key);

            printf("ciphertext: %s\n", ciphertext);
            return 0;
        }
        else
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }


}

string get_ciphertext(string text, int number)
{
    printf("Number: %i\n", number);
    // Iterate over every character
    for (int i = 0; i < strlen(text); i++)
    {
        // If character is alphabetical character, rotate it
        if (text[i] >= 'a' && text[i] <= 'z')
        {
            text[i] = (((int)text[i] - 97 + number) % 26) + 97;
        }
        if (text[i] >= 'A' && text[i] <= 'Z')
        {
            text[i] = (((int)text[i] - 65 + number) % 26) + 65;
        }
    }
    return text;
}

// Check if key only contains digits
bool only_digits(string text)
{
    bool only_digits = true;

    // Return true if key only contains digits
    for (int i = 0; i < strlen(text); i++)
    {
        if ((int) text[i] >= 48 && (int) text[i] <= 57)
        {
            ;
        }
        // Return false if key contains other characters
        else
        {
            only_digits = false;
        }
    }
    return only_digits;
}
