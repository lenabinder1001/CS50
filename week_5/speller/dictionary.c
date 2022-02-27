// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 100000;

// Hash table
node *table[N];

// Integer for the size of the dictionary
int dict_size = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash word to obtain hash value
    int hash_value = hash(word);

    // Access linked list at that index in hash table
    node *n = table[hash_value];

    // Traverse linked list, looking for word (strcasecomp)
    while (n != NULL)
    {
        if (strcasecmp(word, n->word) == 0)
        {
            return true;
        }
        n = n->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Function should take a string and return an index
    // This hash function adds the ASCII values of all characters in the word together
    long sum = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        sum += tolower(word[i]);
    }

    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Read dictionary-file
    FILE *dict = fopen(dictionary, "r");

    // Check, if dictionary is empty
    if (dict == NULL)
    {
        printf("Unable to read %s\n", dictionary);
        return false;
    }

    // Read words from dictionary into hash table
    char word_next[LENGTH + 1];

    while (fscanf(dict, "%s", word_next) != EOF)
    {
        // One node for every word
        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            return false;
        }

        // Copy word into node
        strcpy(n->word, word_next);

        // Hash word to get its hash value
        int hash_val = hash(word_next);

        // Insert node into hash table at the right location
        n->next = table[hash_val];
        table[hash_val] = n;
        dict_size += 1;
    }

    // Close file
    fclose(dict);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Return size of dictionary
    return dict_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Iterate over hash table and free nodes in each linked list
    for (int i = 0; i < N; i++)
    {
        // Assign cursor
        node *n = table[i];
        // Loop through linked list
        while (n != NULL)
        {
            // Make temp equal cursor;
            node *tmp = n;
            // Point cursor to next element
            n = n->next;
            // free temp
            free(tmp);
        }
        if (n == NULL && i == N - 1)
        {
            return true;
        }
    }

    return false;
}
