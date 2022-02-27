#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get positive integer between 1 and 8 (inclusive) from user
    int stored;

    do
    {
        stored = get_int("Height: ");
    }
    while (stored < 1 || stored > 8);

    for (int i = 0; i < stored; i++)
    {
        // For-Loop to add spaces
        for (int k = stored - i; k > 1; k--)
        {
            printf(" ");
        }
        // For-Loop to add hashes
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }

}
