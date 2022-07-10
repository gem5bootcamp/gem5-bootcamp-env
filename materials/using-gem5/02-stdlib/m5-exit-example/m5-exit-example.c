#include <stdio.h>
#include "gem5/m5ops.h"

int main()
{
    printf("The program has started!\n");

    int exit_count = 0;
    while(1)
    {
        exit_count++;
        printf("About to exit the simulation for the %d st/nd/rd/st time\n", exit_count);
        m5_exit(0);
    };

    return 0;
}
