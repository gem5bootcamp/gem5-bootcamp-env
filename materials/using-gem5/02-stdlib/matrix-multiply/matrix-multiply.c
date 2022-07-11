#include <stdio.h>

int main()
{
    const int size = 100;
    int first[size][size], second[size][size], multiply[size][size];

    printf("Populating the first and second matrix...\n");
    for(int x=0; x<size; x++)
    {
        for(int y=0; y<size; y++)
        {
            first[x][y] = x + y;
            second[x][y] = (4 * x) + (7 * y);
        }
    }
    printf("Done!\n");

    printf("Multiplying the matrixes...\n");
    for(int c=0; c<size; c++)
    {
        for(int d=0; d<size; d++)
        {
            int sum = 0;
            for(int k=0; k<size; k++)
            {
                sum += first[c][k] * second[k][d];
            }
           multiply[c][d] = sum;
        }
    }
    printf("Done!\n");

    printf("Calculating the sum of all elements in the matrix...\n");
    long int sum = 0;
    for(int x=0; x<size; x++)
        for(int y=0; y<size; y++)
            sum += multiply[x][y];
    printf("Done\n");

    printf("The sum is %ld\n", sum);
}
