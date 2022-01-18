#include "thread.h"
#include "buffer.h"
#include "fifo.h"
#include "shared_data.h"
#include <stdio.h>
#include <unistd.h>
#include <string.h>


SharedData sharedData;

void* client(void* arg) {
    int id;
    char* data = "Hello World!";
    
    // id = getFreeBuffer();                /* take a buffer out of fifo of free buffers */
    fifoOut(&id, &sharedData.freebuffers);

    // putRequestData(data, id);            /* put request data on buffer */
    ServiceRequest request;
    strncpy(&request.msg, data, 1023);

    sharedData.pool[id].req = request;
    // addNewPendingRequest (id);           /* add buffer to fifo of pending requests */
    fifoIn(id, &sharedData.pendingRequests);

    // waitForResponse (id);                /* wait (blocked) until a response is available */

    // while(cond)
    //      wait(vcond, mutex)

    // resp = getResponseData (id);         /* take response out of buffer */
    // releaseBuffer (id);                  /* buffer is free, so add it to fifo of free buffers */
    fifoIn(id, &sharedData.freebuffers);
}

void* server(void* arg) {}


int main(int argc, char *argv[]) {
    pthread_t client_thread;
    pthread_t server_thread;

    thread_create(&client_thread, NULL, &client, NULL);
    thread_create(&server_thread, NULL, &server, NULL);
    
    thread_join(client_thread, NULL);
    thread_join(server_thread, NULL);

    return 0;
}
