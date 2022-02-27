#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Determine winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    int sum = 0;

    // Check, if character is uppercase or lowercase to get the right
    // integer and get the correct amount of points from the array
    for (int i = 0; i < strlen(word); i++)
        if (isupper(word[i]))
        {
            int str_as_int = (int) word[i] - 65;
            sum += POINTS[str_as_int];
        }
        else if (islower(word[i]))
        {
            int str_as_int = (int) word[i] - 97;
            sum += POINTS[str_as_int];
        }
    // Return sum to determine the winner
    return sum;
}
