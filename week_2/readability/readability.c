#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Get text from user
    string input_text = get_string("Text: ");

    // Count letters
    int letters = count_letters(input_text);

    // Count words
    int words = count_words(input_text);

    // Count sentences
    int sentences = count_sentences(input_text);

    // Calculate reading level
    float index = 0.0588 * (100 * (float) letters / (float) words) - 0.296 * (100 * (float) sentences / (float) words) - 15.8;

    if ((int) round(index) < 1)
    {
        printf("Before Grade 1\n");
    }
    else if ((int) round(index) >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(index));
    }
}


int count_letters(string text)
{
    int number_of_letters = 0;

    // Iterate over characters of the text and count letters
    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
            number_of_letters += 1;
        }
    }

    return number_of_letters;
}

int count_words(string text)
{
    int number_of_words = 0;

    // Iterate over characters of the text and count words
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            number_of_words += 1;
        }
    }

    // Add 1 for the last word of the text
    number_of_words += 1;

    return number_of_words;
}

int count_sentences(string text)
{
    int number_of_sentences = 0;

    // Iterate over characters of the text and count sentences
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            number_of_sentences += 1;
        }
    }

    return number_of_sentences;
}
