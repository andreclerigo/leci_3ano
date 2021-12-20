#include "thread.h"
#include <stdio.h>
#include <unistd.h>

void* thread_main(void* arg)
{
    for (int i = 1; i <= 10; i++)
    {
        printf("Iter: %d\n", i);
        usleep(100000);
    }
    return NULL;
}

int main(int argc, char *argv[])
{
    pthread_t mythread;

    thread_create(&mythread, NULL, &thread_main, NULL);
    thread_join(mythread, NULL);

    return 0;
}
