#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(void)
{
    printf("Before the fork:\n");
    printf("  PID = %d, PPID = %d.\n", 
            getpid(), getppid());

    fork();

    printf("After the fork:\n");
    printf("  PID = %d, PPID = %d.\n"
            "  Am I the parent or the child?"
            " How can I know it?\n", 
            getpid(), getppid());

    return EXIT_SUCCESS;
}

