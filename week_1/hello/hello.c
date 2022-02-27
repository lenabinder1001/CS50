#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get input (name) from users and greet them
    string name = get_string("What´s your name? ");
    printf("hello, %s\n", name);
}