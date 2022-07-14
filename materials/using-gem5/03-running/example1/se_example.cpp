#include <unistd.h>
#include "gem5/m5ops.h"

int main()
{
    m5_reset_stats(0, 0);

    write(1, "This will be output to standard out\n", 36);

    m5_exit(0);
    
    return 0;
}

