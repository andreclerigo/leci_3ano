/**
 *  \file
 *  \brief Some sofs21 global constants 
 *
 *  \author Artur Pereira - 2016-2020
 */

#ifndef __SOFS21_CONSTANTS__
#define __SOFS21_CONSTANTS__

#include <inttypes.h>

namespace sofs21
{
    /** \defgroup constants constants 
     * \brief Core constants
     * \ingroup core
     */

    /** @{ */

    /** \brief block size (in bytes) */
#define BlockSize 1024U

    /** \brief number of inodes per block */
#define IPB (BlockSize / sizeof(SOInode))

    /** \brief number of references per block */
#define RPB (BlockSize / sizeof (uint32_t))

    /** \brief number of direntries per block */
#define DPB (BlockSize / sizeof(SODirectorySlot))

    /** \brief null reference to a block */
#define NullBlockReference 0xFFFFFFFF

    /** \brief null reference to an inode */
#define NullInodeReference 0xFFFF

    /** \brief maximum number of inodes in a sofs21 disk */
#define MAX_INODES (8*4*100)

    /** 
     * \brief maximum length of a file name (in characters)
     */
#define SOFS21_FILENAME_LEN 61

    /** @} */

};

#endif /* __SOFS21_CONSTANTS__ */
