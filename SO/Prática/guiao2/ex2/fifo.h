/**
 *  @file 
 *
 *  @brief A simple FIFO, whose elements are pairs of integers,
 *      one representing the producer and the other the value produced
 *
 *  The following operations are defined:
 *     \li insertion of a value
 *     \li retrieval of a value.
 *
 * \author (2016) Artur Pereira <artur at ua.pt>
 */
/** \brief internal storage size of <em>FIFO memory</em> */
#define FIFOSZ 5

/*
 *  \brief Data structure.
 */

typedef struct FIFO
{
    unsigned int ii;    ///< point of insertion
    unsigned int ri;    ///< point of retrieval
    unsigned int cnt;   ///< number of items stored
    int slot[FIFOSZ];   ///< storage memory
} FIFO;

#ifndef __SO_IPC_PRODUCER_CONSUMER_FIFO_
#define __SO_IPC_PRODUCER_CONSUMER_FIFO_

/**
 * \brief Init the fifo 
 */
FIFO* fifoInit(void);

/**
 *  \brief Insertion of a value into the FIFO.
 *
 * \param id id of the producer
 * \param value value to be stored
 */
void fifoIn (unsigned int id, FIFO* fifo);

/**
 *  \brief Retrieval of a value from the FIFO.
 *
 * \param idp pointer to recipient where to store the producer id
 * \param valuep pointer to recipient where to store the value 
 */
void fifoOut (unsigned int * idp, FIFO* fifo);

#endif /* __SO_IPC_PRODUCER_CONSUMER_FIFO_ */
