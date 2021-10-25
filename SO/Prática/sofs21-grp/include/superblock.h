/**
 *  \file 
 *  \brief Definition of the superblock data type.
 *
 *  \author Artur Pereira - 2008-2009, 2016-2021
 *  \author Miguel Oliveira e Silva - 2009, 2017
 *  \author António Rui Borges - 2010-2015
 */

#ifndef __SOFS21_SUPERBLOCK__
#define __SOFS21_SUPERBLOCK__

#include "constants.h"

#include <inttypes.h>

namespace sofs21
{
    /** 
     * \defgroup superblock superblock
     * \ingroup core
     * \brief The SOSuperblock data type
     * @{ 
     */

/** \brief sofs21 magic number */
#define MAGIC_NUMBER 0x50F5

/** \brief sofs21 version number */
#define VERSION_NUMBER 0x21

/** \brief maximum length of volume name */
#define PARTITION_NAME_LEN 19

/** \brief capacity of the deleted inode queue */
#define DELETED_QUEUE_SIZE 36

/** \brief reference cache size */
#define REF_CACHE_SIZE 60

    /** \brief Definition of the superblock data type. 
     */
    struct SOSuperblock
    {

        /** \brief magic number - file system identification number */
        uint16_t magic;

        /** \brief version number */
        uint8_t version;

        /** \brief mount status and mount count 
         * - if positive it means properly unmounted
         * - if negative on mount, file system check should be done
         * - absolute value represents the number of mounts
         */
        int8_t mntstat;

        /** \brief volume name */
        char name[PARTITION_NAME_LEN + 1];

        /** \brief total number of blocks in the device */
        uint32_t ntotal;

        /* Inode table's metadata */

        /** \brief total number of inodes */
        uint16_t itotal;

        /** \brief number of free inodes */
        uint16_t ifree;

        /** \brief bit index where search for a free inode should start from 
         */
        uint16_t iidx;

        /** \brief bitmap representing inode allocation states 
         * - All inodes are represented, including inode number 0, which is never free
         * - Inode 0 is represented by bit 0 (LSB) of ibitmap[0], and so forth
         * - A 0 means the corresponding inode is free, and 1 it is in-use.
         */
        uint32_t ibitmap[MAX_INODES/32];

        /** \brief queue of deleted inodes, managed in a circular FIFO
         */
        uint16_t iqueue[DELETED_QUEUE_SIZE];

        /** \brief index of head of iqueue */
        uint8_t iqhead;

        /** \brief number of elements in iqueue */
        uint8_t iqcount;


        /* Data blocks' metadata */

        /** \brief physical number of the block where the data block pool starts */
        uint32_t dbp_start;

        /** \brief total number of data blocks */
        uint32_t dbtotal;

        /** \brief number of free data blocks */
        uint32_t dbfree;


        /* Reference bitmap's metadata */

        /** \brief physical number of the block where the reference bitmap starts */
        uint32_t rbm_start;

        /** \brief number of blocks the reference bitmap comprises */
        uint16_t rbm_size;

        /** \brief index of first 32-word to be used to retrieve references from bitmap */
        uint32_t rbm_idx;

        /** \brief cache of references to free data blocks */
        struct ReferenceCache
        {
            /** \brief index of first free/occupied cell */
            uint32_t idx;
            /** \brief the cache itself */
            uint32_t ref[REF_CACHE_SIZE];
        };

        /** \brief retrieval cache of references to free data blocks */
        ReferenceCache retrieval_cache;

        /** \brief insertion cache of references to free data blocks */
        ReferenceCache insertion_cache;

    };

    /** @} */

};

#endif /*__SOFS21_SUPERBLOCK__ */
