#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

bool key_valid(string text);
string get_ciphertext(string text, string key);

int main(int argc, string argv[])
{
    // Check, if the program was run with a single command-line argument
    if (argc == 2)
    {
        // Check, if key is valid (26 individual alphabetical characters)
        if (key_valid(argv[1]) == true)
        {
            // Ask for plaintext
            string plaintext = get_string("plaintext:  ");

            // Convert to ciphertext
            string ciphertext = get_ciphertext(plaintext, argv[1]);
            printf("ciphertext: %s\n", ciphertext);
            return 0;
        }
        // If not, print error message
        else
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
    }
    // If not, print error message
    else
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

}

// Check, if key is valid (26 individual alphabetical characters)
bool key_valid(string text)
{
    bool valid_key = true;

    // Check if key contains 26 characters
    if (strlen(text) == 26)
    {
        // Check, if characters are alphabetical
        for (int i = 0; i < strlen(text); i++)
        {
            if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
            {
                // Check, if key only contains unique values
                for (int j = 0; j < strlen(text); j++)
                {
                    for (int k = j + 1; k < strlen(text); k++)
                    {
                        if (text[j] == text[k])
                        {
                            valid_key = false;
                        }
                    }
                }
            }
            else
            {
                valid_key = false;
            }
        }
    }
    else
    {
        valid_key = false;
    }
    return valid_key;
}

string get_ciphertext(string text, string key)
{
    // Iterate over every character in key
    for (int i = 0; i < strlen(text); i++)
    {
        // Check, if character is alphabetical
        if (text[i] >= 'a' && text[i] <= 'z')
        {
            // Change character to related character in key
            text[i] = tolower(key[(int) text[i] - 97]);
        }
        if (text[i] >= 'A' && text[i] <= 'Z')
        {
            // Change character to related character in key
            text[i] = toupper(key[(int) text[i] - 65]);
        }
    }
    return text;
}