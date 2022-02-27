#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Iterate over 2 dimensional image array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Save original rgb values to int variables
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;
            int red = image[i][j].rgbtRed;

            // Calculate average value
            float average = round((blue + green + red) / 3.0);

            // Change rgb values to average value
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Iterate over 2 dimensional image array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Save original rgb values to int variables
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;
            int red = image[i][j].rgbtRed;

            // Calculate sepia values for each rgb value
            float sepiaRed = round((.393 * red) + (.769 * green) + (.189 * blue));
            float sepiaGreen = round((.349 * red) + (.686 * green) + (.168 * blue));
            float sepiaBlue = round((.272 * red) + (.534 * green) + (.131 * blue));

            // Check, if sepia values (red) are greater than 255
            if (sepiaRed > 255)
            {
                // If true, set them to 255
                sepiaRed = 255;
                image[i][j].rgbtRed = sepiaRed;
            }
            else
            {
                image[i][j].rgbtRed = sepiaRed;
            }

            // Check, if sepia values (green) are greater than 255
            if (sepiaGreen > 255)
            {
                // If true, set them to 255
                sepiaGreen = 255;
                image[i][j].rgbtGreen = sepiaGreen;
            }
            else
            {
                image[i][j].rgbtGreen = sepiaGreen;
            }

            // Check, if sepia values (blue) are greater than 255
            if (sepiaBlue > 255)
            {
                // If true, set them to 255
                sepiaBlue = 255;
                image[i][j].rgbtBlue = sepiaBlue;
            }
            else
            {
                image[i][j].rgbtBlue = sepiaBlue;
            }

        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Iterate over 2 dimensional array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            // Reflect pixels
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    float average_red;
    float average_green;
    float average_blue;

    // Create copy of image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j].rgbtRed = image[i][j].rgbtRed;
            copy[i][j].rgbtGreen = image[i][j].rgbtGreen;
            copy[i][j].rgbtBlue = image[i][j].rgbtBlue;
        }
    }

    // Iterate over image array
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            // Pixel is in the top right corner
            if (w == 0 && h == 0)
            {
                // Calculate average rgb values
                average_red = (float)(copy[h][w].rgbtRed + copy[h][w + 1].rgbtRed + copy[h + 1][w].rgbtRed +
                                      copy[h + 1][w + 1].rgbtRed) / 4;
                average_green = (float)(copy[h][w].rgbtGreen + copy[h][w + 1].rgbtGreen + copy[h + 1][w].rgbtGreen
                                        + copy[h + 1][w + 1].rgbtGreen) / 4;
                average_blue = (float)(copy[h][w].rgbtBlue + copy[h][w + 1].rgbtBlue + copy[h + 1][w].rgbtBlue
                                       + copy[h + 1][w + 1].rgbtBlue) / 4;

                // Round average values
                average_red = round(average_red);
                average_green = round(average_green);
                average_blue = round(average_blue);

                // Copy values into original image array
                image[h][w].rgbtRed = average_red;
                image[h][w].rgbtGreen = average_green;
                image[h][w].rgbtBlue = average_blue;
            }

            // If pixel is in the bottom left corner
            else if (w == 0 && h == (height - 1))
            {
                // Calculate average rgb values
                average_red = (float)(copy[h - 1][w].rgbtRed + copy[h - 1][w + 1].rgbtRed + copy[h][w].rgbtRed
                                      + copy[h][w + 1].rgbtRed) / 4;
                average_green = (float)(copy[h - 1][w].rgbtGreen + copy[h - 1][w + 1].rgbtGreen + copy[h][w].rgbtGreen
                                        + copy[h][w + 1].rgbtGreen) / 4;
                average_blue = (float)(copy[h - 1][w].rgbtBlue + copy[h - 1][w + 1].rgbtBlue + copy[h][w].rgbtBlue
                                       + copy[h][w + 1].rgbtBlue) / 4;

                // Round average values
                average_red = round(average_red);
                average_green = round(average_green);
                average_blue = round(average_blue);

                // Copy values into original image array
                image[h][w].rgbtRed = average_red;
                image[h][w].rgbtGreen = average_green;
                image[h][w].rgbtBlue = average_blue;
            }

            // If pixel is in the tio right corner
            else if (h == 0 && w == (width - 1))
            {
                // Calculate average rgb values
                average_red = (float)(copy[h][w - 1].rgbtRed + copy[h][w].rgbtRed + copy[h + 1][w - 1].rgbtRed
                                      + copy[h + 1][w].rgbtRed) / 4;
                average_green = (float)(copy[h][w - 1].rgbtGreen + copy[h][w].rgbtGreen + copy[h + 1][w - 1].rgbtGreen
                                        + copy[h + 1][w].rgbtGreen) / 4;
                average_blue = (float)(copy[h][w - 1].rgbtBlue + copy[h][w].rgbtBlue + copy[h + 1][w - 1].rgbtBlue
                                       + copy[h + 1][w].rgbtBlue) / 4;

                // Round average values
                average_red = round(average_red);
                average_green = round(average_green);
                average_blue = round(average_blue);

                // Copy values into original image array
                image[h][w].rgbtRed = average_red;
                image[h][w].rgbtGreen = average_green;
                image[h][w].rgbtBlue = average_blue;
            }

            // If pixel is in the bottom right corner
            else if (h == (height - 1) && w == (width - 1))
            {
                // Calculate average rgb values
                average_red = (float)(copy[h - 1][w - 1].rgbtRed + copy[h - 1][w].rgbtRed + copy[h][w - 1].rgbtRed
                                      + copy[h][w].rgbtRed) / 4;
                average_green = (float)(copy[h - 1][w - 1].rgbtGreen + copy[h - 1][w].rgbtGreen + copy[h][w - 1].rgbtGreen
                                        + copy[h][w].rgbtGreen) / 4;
                average_blue = (float)(copy[h - 1][w - 1].rgbtBlue + copy[h - 1][w].rgbtBlue + copy[h][w - 1].rgbtBlue
                                       + copy[h][w].rgbtBlue) / 4;

                // Round average values
                average_red = round(average_red);
                average_green = round(average_green);
                average_blue = round(average_blue);

                // Copy values into original image array
                image[h][w].rgbtRed = average_red;
                image[h][w].rgbtGreen = average_green;
                image[h][w].rgbtBlue = average_blue;
            }

            // Pixel is on the left
            else if (w == 0 && (h > 0 && h < height - 1))
            {
                // Calculate average rgb values
                average_red = (float)(copy[h - 1][w].rgbtRed + copy[h - 1][w + 1].rgbtRed + copy[h][w].rgbtRed
                                      + copy[h][w + 1].rgbtRed + copy[h + 1][w].rgbtRed + copy[h + 1][w + 1].rgbtRed) / 6;
                average_green = (float)(copy[h - 1][w].rgbtGreen + copy[h - 1][w + 1].rgbtGreen + copy[h][w].rgbtGreen
                                        + copy[h][w + 1].rgbtGreen + copy[h + 1][w].rgbtGreen + copy[h + 1][w + 1].rgbtGreen) / 6;
                average_blue = (float)(copy[h - 1][w].rgbtBlue + copy[h - 1][w + 1].rgbtBlue + copy[h][w].rgbtBlue
                                       + copy[h][w + 1].rgbtBlue + copy[h + 1][w].rgbtBlue + copy[h + 1][w + 1].rgbtBlue) / 6;

                // Round average values
                average_red = round(average_red);
                average_green = round(average_green);
                average_blue = round(average_blue);

                // Copy values into original image array
                image[h][w].rgbtRed = average_red;
                image[h][w].rgbtGreen = average_green;
                image[h][w].rgbtBlue = average_blue;
            }

            // Pixel is on the right
            else if (w == (width - 1) && (h > 0 && h < height - 1))
            {
                // Calculate average rgb values
                average_red = (float)(copy[h - 1][w - 1].rgbtRed + copy[h - 1][w].rgbtRed + copy[h][w - 1].rgbtRed
                                      + copy[h][w].rgbtRed + copy[h + 1][w - 1].rgbtRed + copy[h + 1][w].rgbtRed) / 6;
                average_green = (float)(copy[h - 1][w - 1].rgbtGreen + copy[h - 1][w].rgbtGreen + copy[h][w - 1].rgbtGreen
                                        + copy[h][w].rgbtGreen + copy[h + 1][w - 1].rgbtGreen + copy[h + 1][w].rgbtGreen) / 6;
                average_blue = (float)(copy[h - 1][w - 1].rgbtBlue + copy[h - 1][w].rgbtBlue + copy[h][w - 1].rgbtBlue
                                       + copy[h][w].rgbtBlue + copy[h + 1][w - 1].rgbtBlue + copy[h + 1][w].rgbtBlue) / 6;

                // Round average values
                average_red = round(average_red);
                average_green = round(average_green);
                average_blue = round(average_blue);

                // Copy values into original image array
                image[h][w].rgbtRed = average_red;
                image[h][w].rgbtGreen = average_green;
                image[h][w].rgbtBlue = average_blue;
            }

            // Pixel is on the top
            else if (h == 0 && (w > 0 &&  w < width - 1))
            {
                // Calculate average rgb values
                average_red = (float)(copy[h][w - 1].rgbtRed + copy[h][w].rgbtRed + copy[h][w + 1].rgbtRed + copy[h + 1][w - 1].rgbtRed
                                      + copy[h + 1][w].rgbtRed + copy[h + 1][w + 1].rgbtRed) / 6;
                average_green = (float)(copy[h][w - 1].rgbtGreen + copy[h][w].rgbtGreen + copy[h][w + 1].rgbtGreen + copy[h + 1][w - 1].rgbtGreen
                                        + copy[h + 1][w].rgbtGreen + copy[h + 1][w + 1].rgbtGreen) / 6;
                average_blue = (float)(copy[h][w - 1].rgbtBlue + copy[h][w].rgbtBlue + copy[h][w + 1].rgbtBlue + copy[h + 1][w - 1].rgbtBlue
                                       + copy[h + 1][w].rgbtBlue + copy[h + 1][w + 1].rgbtBlue) / 6;

                // Round average values
                average_red = round(average_red);
                average_green = round(average_green);
                average_blue = round(average_blue);

                // Copy values into original image array
                image[h][w].rgbtRed = average_red;
                image[h][w].rgbtGreen = average_green;
                image[h][w].rgbtBlue = average_blue;
            }

            // Pixel is on the bottom
            else if (h == height - 1 && (w > 0 && w < width - 1))
            {
                // Calculate average rgb values
                average_red = (float)(copy[h - 1][w - 1].rgbtRed + copy[h - 1][w].rgbtRed + copy[h - 1][w + 1].rgbtRed
                                      + copy[h][w - 1].rgbtRed + copy[h][w].rgbtRed + copy[h][w + 1].rgbtRed) / 6;
                average_green = (float)(copy[h - 1][w - 1].rgbtGreen + copy[h - 1][w].rgbtGreen + copy[h - 1][w + 1].rgbtGreen
                                        + copy[h][w - 1].rgbtGreen + copy[h][w].rgbtGreen + copy[h][w + 1].rgbtGreen) / 6;
                average_blue = (float)(copy[h - 1][w - 1].rgbtBlue + copy[h - 1][w].rgbtBlue + copy[h - 1][w + 1].rgbtBlue
                                       + copy[h][w - 1].rgbtBlue + copy[h][w].rgbtBlue + copy[h][w + 1].rgbtBlue) / 6;

                // Round average values
                average_red = round(average_red);
                average_green = round(average_green);
                average_blue = round(average_blue);

                // Copy values into original image array
                image[h][w].rgbtRed = average_red;
                image[h][w].rgbtGreen = average_green;
                image[h][w].rgbtBlue = average_blue;
            }

            // Pixel is in the middle and has 9 pixels around
            else
            {
                // Calculate average rgb values
                average_red = (float)(copy[h - 1][w - 1].rgbtRed + copy[h - 1][w].rgbtRed + copy[h - 1][w + 1].rgbtRed
                                      + copy[h][w - 1].rgbtRed + copy[h][w].rgbtRed + copy[h][w + 1].rgbtRed + copy[h + 1][w - 1].rgbtRed
                                      + copy[h + 1][w].rgbtRed + copy[h + 1][w + 1].rgbtRed) / 9;
                average_green = (float)(copy[h - 1][w - 1].rgbtGreen + copy[h - 1][w].rgbtGreen + copy[h - 1][w + 1].rgbtGreen
                                        + copy[h][w - 1].rgbtGreen + copy[h][w].rgbtGreen + copy[h][w + 1].rgbtGreen + copy[h + 1][w - 1].rgbtGreen
                                        + copy[h + 1][w].rgbtGreen + copy[h + 1][w + 1].rgbtGreen) / 9;
                average_blue = (float)(copy[h - 1][w - 1].rgbtBlue + copy[h - 1][w].rgbtBlue + copy[h - 1][w + 1].rgbtBlue
                                       + copy[h][w - 1].rgbtBlue + copy[h][w].rgbtBlue + copy[h][w + 1].rgbtBlue + copy[h + 1][w - 1].rgbtBlue
                                       + copy[h + 1][w].rgbtBlue + copy[h + 1][w + 1].rgbtBlue) / 9;

                // Round average values
                average_red = round(average_red);
                average_green = round(average_green);
                average_blue = round(average_blue);

                // Copy values into original image array
                image[h][w].rgbtRed = average_red;
                image[h][w].rgbtGreen = average_green;
                image[h][w].rgbtBlue = average_blue;
            }
        }
    }
    return;
}