#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // If program is not executed with 1 command-line argument, inform user and return 1
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE");
        return 1;
    }

    // Open file
    FILE *file = fopen(argv[1], "r");

    // Inform user if file cannot be openend and return 1
    if (file == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    // Initialise variables
    BYTE buffer[512];
    int count = 0;
    FILE *img_pointer = NULL;
    char filename[8];

    // Repeat until end of card
    while (fread(&buffer, 512, 1, file))
    {
        // If new JPG starts
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If not first JPEG, close previous
            if (!(count == 0))
            {
                fclose(img_pointer);
            }
            // Initialise file
            sprintf(filename, "%03i.jpg", count);
            img_pointer = fopen(filename, "w");
            count++;
        }
        // If JPEG has been found, write to file
        if (!(count == 0))
        {
            fwrite(&buffer, 512, 1, img_pointer);
        }
    }
    fclose(file);
    fclose(img_pointer);
    return 0;
}
