#include "shared_data.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

SharedData* sh_init(void)
{
    SharedData* sh = (SharedData*) malloc(sizeof(SharedData));
    if (sh == NULL) {
        fprintf(stderr, "fifoInit: malloc failed\n");
        exit(1);
    }

    return sh;
}