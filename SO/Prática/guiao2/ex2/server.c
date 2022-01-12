#include "buffer.h"
#include "server.h"
#include "fifo.h"

#define N_BUFFERS 6

BUFFER pool[N_BUFFERS];

int main(int argc, char *argv[]) {

    FIFO* freebuffers = fifoInit();
    FIFO* pendingRequests = fifoInit();



    return 0;
}