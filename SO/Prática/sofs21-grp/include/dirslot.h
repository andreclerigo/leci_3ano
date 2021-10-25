/**
 *  \file
 *  \brief Definition of the directory entry data type.
 *
 *  \author Artur Pereira - 2008-2009, 2016-2020
 *  \author Miguel Oliveira e Silva - 2009, 2017
 *  \author António Rui Borges - 2010-2015
 */

#ifndef __SOFS21_DIRECTORY_SLOT__
#define __SOFS21_DIRECTORY_SLOT__

#include "constants.h"

#include <inttypes.h>

#define DIRECTORY_SLOT 30

namespace sofs21
{

    /** 
     * \brief Definition of the directory slot data type. 
     * \ingroup dirslot
     * \details
     *   A directory slot is a fixed-size data type composed of 
     *   space for a string and an inode number.
     *   It allows to implement the typical hierarchical view of a disk content.
     */
    struct SODirectorySlot
    {

        /** \brief the associated inode number */
        uint16_t in;

        /** \brief buffer to hold the name or part of the name of a directory entry */
        char nameBuffer[DIRECTORY_SLOT];
    };

};

#endif /* __SOFS21_DIRECTORY_SLOT__ */
