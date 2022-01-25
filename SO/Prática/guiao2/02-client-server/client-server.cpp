#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <libgen.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <pthread.h>
#include <cctype>
#include <string>
 
#include "thread.h"

#define FIFOSZ  10

typedef struct FIFO
{
    uint32_t ii;   ///< point of insertion
    uint32_t ri;   ///< point of retrieval
    uint32_t cnt;  ///< number of items stored
    uint32_t ids[FIFOSZ];  ///< storage memory
    pthread_cond_t notEmpty = PTHREAD_COND_INITIALIZER;
    pthread_cond_t notFull = PTHREAD_COND_INITIALIZER;
    pthread_mutex_t accessCR = PTHREAD_MUTEX_INITIALIZER;
}FIFO;

typedef struct ServiceRequest
{   
    uint32_t clientid;
    char *frase;
}ServiceRequest;

typedef struct ServiceResponse
{
    uint32_t len = 0;
    uint32_t alpha = 0;
    uint32_t numbers = 0;
    uint32_t serverid = 0;
}ServiceResponse;

typedef struct SLOT
{
    ServiceRequest req;
    ServiceResponse res;
    bool hasResponse = false;
    pthread_mutex_t accessCR = PTHREAD_MUTEX_INITIALIZER;
    pthread_cond_t available = PTHREAD_COND_INITIALIZER;
}SLOT;

typedef struct ARG
{
    int id;
    int iter;
}ARG;


static SLOT slots[FIFOSZ];
static FIFO frees;
static FIFO pending;

void freesInit(void){
    mutex_lock(&frees.accessCR);
    frees.ii = frees.ri = 0;
    frees.cnt = FIFOSZ;
    uint32_t i;
    for ( i = 0; i < FIFOSZ; i++)
    {
        frees.ids[i] = i;
    }
    cond_signal(&frees.notEmpty);
    mutex_unlock(&frees.accessCR);
}

void pendingInit(void){
    mutex_lock(&pending.accessCR);
    pending.cnt = pending.ii = pending.ri = 0;
    cond_signal(&pending.notFull);
    mutex_unlock(&pending.accessCR);
}

void insert(FIFO *fifo, uint32_t id){
    mutex_lock(&fifo->accessCR);

    while (fifo->cnt == FIFOSZ)
    {
        cond_wait(&fifo->notFull,&fifo->accessCR);
    }

    fifo->ids[fifo->ii] = id;
    fifo->ii = (fifo->ii + 1) % FIFOSZ;
    fifo->cnt++;
    cond_signal(&fifo->notEmpty);
    mutex_unlock(&fifo->accessCR);
}

uint32_t retrive(FIFO *fifo){
    mutex_lock(&fifo->accessCR);

    while (fifo->cnt == 0)
    {
        cond_wait(&fifo->notEmpty, &fifo->accessCR);
    }
    
    uint32_t id = fifo->ids[fifo->ri];
    fifo->ids[fifo->ri] = 99999999;
    fifo->ri = (fifo->ri + 1) % FIFOSZ;
    fifo->cnt--;
    cond_signal(&fifo->notFull);
    mutex_unlock(&fifo->accessCR);
    return id;
}

void signalResponseIsAvailable(uint32_t id){
    slots[id].hasResponse = true;
    cond_signal(&slots[id].available);
}

void waitForResponse(uint32_t id){
    while (!slots[id].hasResponse)
    {
        cond_wait(&slots[id].available, &slots[id].accessCR);
    }
    slots[id].hasResponse = false;
}

void callService(ServiceRequest &req, ServiceResponse &res){
    uint32_t id = retrive(&frees);
    mutex_lock(&slots[id].accessCR);
    slots[id].req = req;
    slots[id].res = res;
    insert(&pending, id);
    printf("Client %u call service\n", req.clientid);
    waitForResponse(id);
    res = slots[id].res;
    printf("Size: %u,  Alpha: %u,  Numbers: %u,  ServerId: %u\n",res.len,res.alpha,res.numbers,res.serverid);
    mutex_unlock(&slots[id].accessCR);
    insert(&frees, id);
}

void processService(uint32_t sid){
    uint32_t id = retrive(&pending);
    mutex_lock(&slots[id].accessCR);
    slots[id].res.serverid = sid;

    char *i;
    for ( i = slots[id].req.frase; *i != '\0'; i++)
    {
        slots[id].res.len++;
        if(isdigit(*i)) slots[id].res.numbers++;
        if(isalpha(*i)) slots[id].res.alpha++; 
    }
    signalResponseIsAvailable(id);
    mutex_unlock(&slots[id].accessCR);
}

void *client(void *arg){
    ARG* x = (ARG*)arg;
    printf("Client %d created\n",x->id);
    int iter = 10;
    int i;
    for (i = 0; i < iter; i++)
    {
        ServiceResponse res; //= new ServiceResponse();
        ServiceRequest req; //= new ServiceRequest();
        req.clientid = x->id;
        req.frase = (char *)"Teste String 123";
        callService(req, res);
    }
    return NULL;
}

void *server(void *arg){
    int x = *((int*)arg);
    printf("Server %d created\n", x);
    while (1)
    {
        processService(x);   
    }
}

int main(void){
    int nservers = 2;
    int nclients = 2;

    freesInit();
    pendingInit();

    pthread_t servers[nservers];
    int sarg[nservers];
    pthread_t clients[nclients];
    ARG carg[nclients];

    int i;
    for ( i = 0; i < nservers; i++)
    {   
        sarg[i] = i;
        thread_create(&servers[i],NULL,server,&sarg[i]);
    }

    int j;
    for ( j = 0; j < nclients; j++)
    {
        carg[j].id = j;
        thread_create(&clients[j],NULL,client,&carg[j]);
    }

    int k;
    for ( k = 0; k < nclients; k++)
    {
        thread_join(clients[k], NULL);
        printf("Client %d terminated\n",k);
    }

    int n;
    for ( n = 0; n < nservers; n++)
    {
        thread_cancel(servers[n]);
        printf("Server %d terminated\n", n);
    }

    return EXIT_SUCCESS;
}