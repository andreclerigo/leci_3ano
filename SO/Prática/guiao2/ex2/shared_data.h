#include "fifo.h"
#include "buffer.h"
#define N_BUFFERS 6

typedef struct{
    BUFFER pool[N_BUFFERS];
    FIFO freebuffers;
    FIFO pendingRequests;
} SharedData;