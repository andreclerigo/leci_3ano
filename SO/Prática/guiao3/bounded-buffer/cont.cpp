#include "process.h"
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>


void* process_main(void* arg)
{
    srand(time(NULL));   // Initialization, should only be called once.
    
    for (int i = 1; i <= 10; i++)
    {
        printf("Iter: %d\n", i);
        usleep((rand()%1)*100000);
    }

    printf("Process %d exiting\n", getpid());
    return NULL;
}


int main(int argc, char *argv[])
{
    pid_t proc;
    
    int pid = fork();

    // Check if the pid is from the child
    if (pid == 0) {
        process_main(NULL);
        // exit child process
        exit(0);
    }

    int pid2 = fork();

    // Check if the pid2 is from the child
    if (pid2 == 0) {
        process_main(NULL);
        // exit child process
        exit(0);
    }
    
    proc = pwaitpid(pid, &proc, 0);
    printf("One child done\n");
    proc = pwaitpid(pid2, &proc, 0);
    printf("Two childs done\n");

    return 0;
}
