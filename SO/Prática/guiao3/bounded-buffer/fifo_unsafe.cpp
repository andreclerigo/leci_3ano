/*
 *  @brief A simple FIFO, whose elements are pairs of integers,
 *      one being the id of the producer and the other the value produced
 *
 * @remarks Unsafe, blocking, busy waiting version
 *
 *  The following operations are defined:
 *     \li insertion of a value
 *     \li retrieval of a value.
 *
 * \author (2016) Artur Pereira <artur at ua.pt>
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <errno.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <stdint.h>

#include "fifo.h"
#include "delays.h"
#include "process.h"



/* ************************************************* */

/* create a FIFO in shared memory, initialize it, and return its id */
int fifoCreate(void)
{
    /* create the shared memory */
    int shmid = pshmget(IPC_PRIVATE, sizeof(FIFO), 0600 | IPC_CREAT | IPC_EXCL);

    /*  attach shared memory to process addressing space */
    FIFO * fifo = (FIFO*)pshmat(shmid, NULL, 0);

    /* init fifo */
    uint32_t i;
    for (i = 0; i < FIFOSZ; i++)
    {
        fifo->slot[i].id = 99999999;
        fifo->slot[i].value = 99999999;
    }
    fifo->ii = fifo->ri = 0;
    fifo->cnt = 0;


    pshmdt(fifo);
    return shmid;
}

/* ************************************************* */

FIFO *fifoMap(int shmid)
{
    /* attach shared memory to process addressing space */ 
    return (FIFO*)pshmat(shmid, NULL, 0);
}

/* ************************************************* */

void fifoUnmap(FIFO *fifo)
{
    /* detach shared memory from process addressing space */
    if (fifo == NULL) return;
    pshmdt(fifo);
}

/* ************************************************* */

void fifoDestroy(int shmid)
{
    /*  attach shared memory to process addressing space */
    FIFO * fifo = (FIFO*)pshmat(shmid, NULL, 0);

    /* detach shared memory from process addressing space */
    pshmdt(fifo);

    /* destroy the shared memory */
    pshmctl(shmid, IPC_RMID, NULL);
}

/* ************************************************* */

/* Insertion of a pair <id, value> into the FIFO  */
static bool fifoFull(FIFO *fifo)
{
    return fifo->cnt == FIFOSZ;
}

/* ************************************************* */

/* Check if FIFO is empty */
static bool fifoEmpty(FIFO *fifo)
{
    return fifo->cnt == 0;
}

/* ************************************************* */

/* Insertion of a pait <id, value> into the FIFO  */
void fifoIn(FIFO *fifo, uint32_t id, uint32_t value)
{
    /* wait while fifo is full */
    while (fifoFull(fifo))
    {
        usleep(1000);
    }

    /* Insert pair */
    fifo->slot[fifo->ii].value = value;
    gaussianDelay(1, 0.5);
    fifo->slot[fifo->ii].id = id;
    fifo->ii = (fifo->ii + 1) % FIFOSZ;
    fifo->cnt++;
}

/* ************************************************* */

/* Retrieval of a pair <id, value> from the FIFO */

void fifoOut(FIFO *fifo, uint32_t * idp, uint32_t * valuep)
{
    /* wait while fifo is empty */
    while (fifoEmpty(fifo))
    {
        usleep(1000);
    }

    /* Retrieve pair */
    *valuep = fifo->slot[fifo->ri].value;
    fifo->slot[fifo->ri].value = 99999999;
    *idp = fifo->slot[fifo->ri].id;
    fifo->slot[fifo->ri].id = 99999999;
    fifo->ri = (fifo->ri + 1) % FIFOSZ;
    fifo->cnt--;
}

/* ************************************************* */

