/*
 *  @brief A simple FIFO, whose elements are pairs of integers,
 *      one being the id of the producer and the other the value produced
 *
 * @remarks safe, bust waiting version
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
#include <pthread.h>

#include "fifo.h"
#include "delays.h"
#include "thread.h"


/** \brief internal storage region of FIFO type */
static FIFO fifo;

/** \brief locking flag which warrants mutual exclusion inside the monitor */
static pthread_mutex_t accessCR = PTHREAD_MUTEX_INITIALIZER;

/** \brief condition variable for checking fifo fullness and emptiness */
static pthread_cond_t fifoNotFull = PTHREAD_COND_INITIALIZER;
static pthread_cond_t fifoNotEmpty = PTHREAD_COND_INITIALIZER;

/* ************************************************* */

/* Initialization of the FIFO */
FIFO* fifoInit(void)
{
    FIFO* fifo = (FIFO*) malloc(sizeof(FIFO));
    if (fifo == NULL) {
        fprintf(stderr, "fifoInit: malloc failed\n");
        exit(1);
    }

    mutex_lock(&accessCR);

    unsigned int i;
    for (i = 0; i < FIFOSZ; i++)
    {
        fifo->slot[i] = 99999999;
    }
    fifo->ii = fifo->ri = 0;
    fifo->cnt = 0;

    cond_broadcast(&fifoNotFull);

    mutex_unlock(&accessCR);

    return fifo;
}

/* ************************************************* */

/* Check if FIFO is full */
static bool fifoFull(FIFO* fifo)
{
    return fifo->cnt == FIFOSZ;
}

/* ************************************************* */

/* Check if FIFO is empty */
static bool fifoEmpty(FIFO* fifo)
{
    return fifo->cnt == 0;
}

/* ************************************************* */

/* Insertion of an element into the FIFO  */
void fifoIn(unsigned int id, FIFO* fifo)
{
    mutex_lock(&accessCR);

    /* wait while fifo is full */
    while (fifoFull(fifo))
    {
        cond_wait(&fifoNotFull, &accessCR);
    }

    /* Insert buffer id */
    fifo->slot[fifo->ii] = id;
    fifo->ii = (fifo->ii + 1) % FIFOSZ;
    fifo->cnt++;

    cond_broadcast(&fifoNotEmpty);

    mutex_unlock(&accessCR);
}

/* ************************************************* */

/* Retrieval of the first element avaiable from the FIFO */

void fifoOut(unsigned int *idp, FIFO* fifo)
{
    mutex_lock(&accessCR);

    /* wait while fifo is empty */
    while (fifoEmpty(fifo))
    {
        cond_wait(&fifoNotEmpty, &accessCR);
    }

    /* Retrieve id */
    *idp = fifo->slot[fifo->ri];
    fifo->slot[fifo->ri] = 99999999;
    fifo->ri = (fifo->ri + 1) % FIFOSZ;
    fifo->cnt--;

    cond_broadcast(&fifoNotFull);

    mutex_unlock(&accessCR);
}

/* ************************************************* */
