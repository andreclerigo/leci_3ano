#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(void)
{
  printf("Before the fork:\n");
  printf("  PID = %d, PPID = %d.\n", 
      getpid(), getppid());

  int ret = fork();

  printf("After the fork:\n");
  printf("  PID = %d, PPID = %d.\n", 
      getpid(), getppid());
  printf("  ret = %d\n", ret);

  return EXIT_SUCCESS;
}

