/**
 *  \file
 *  \brief The \b sofs21 formatting functions.
 *
 *  \author Artur Pereira - 2007-2009, 2016-2020
 *  \author Miguel Oliveira e Silva - 2009, 2017
 *  \author António Rui Borges - 2010-2015
 */

#ifndef __SOFS21_MKSOFS__
#define __SOFS21_MKSOFS__

#include <inttypes.h>

#include "bin_mksofs.h"
#include "grp_mksofs.h"

namespace sofs21
{

    /**
     * \defgroup mksofs mksofs
     * \brief Auxiliary formatting functions
     * @{ 
     * */

    /* ******************************************************************* */

    /**
     * \brief Computes the structural partition of the disk
     * \details
     *   Based on the total number of blocks of the disk (\c ntotal) and
     *   on the number of inodes (\c itotal) proposed, 
     *   computes the structural partition, that is, the actual number of inodes,
     *   the number of data blocks and the number blocks for the reference table,
     *   taking into account the following:
     *   - \c itotal must be rounded up to a multiple of \c IPB;
     *   - \c itotal must be lower than or equal to the rounded up value of <tt>ntotal/8</tt>
     *   - \c itotal must be lower than or equal to <tt>MAX_INODES</tt>
     *   - \c itotal must be greater than or equal to \c IPB
     *   - if, at entry, the proposed value for \c itotal is 0,
     *     value <tt>ntotal/20</tt> should be used
     *   - for every data block, there must exist a corresponding bit in the bitmap table
     *   - after making the partition, the last block of the bitmap table can be totally used,
     *     partially used, or not used at all; in such cases, it should be assigned
     *     to the inode table
     *   .
     * \difficulty 3
     *
     * \note This function does not change any block of the disk.
     *
     * \param [in] ntotal Total number of blocks of the disk
     * \param [in] itotal the requested number of inodes
     * \param [out] itsize the number of blocks of the inode table
     * \param [out] dbtotal Total number of data blocks
     */
    void soComputeDiskStructure(uint32_t ntotal, uint16_t itotal, uint16_t & itsize, uint32_t & dbtotal);


    /**
     * \brief Fill in the fields of the superblock.
     * \details
     *   The following nust be considered:
     *   - The magic number must be put at \c 0xFFFF. Afterwards, it will be put with the
     *     correct value.
     *   - the retrieval cache must be left filled (totally, if possible).      
     *   - The insertion cache must be left empty.
     *   - All bits of the inode bitmap must be 0, except the one representing inode 0.
     *   .
     * \difficulty 3
     *
     * \param [in] name volume name
     * \param [in] ntotal the total number of blocks in the device
     * \param [in] itsize the number of blocks of the inode table
     * \param [in] dbtotal Total number of data blocks 
     *
     * \note Access to disk must be done using \ref wrb "soWriteRawBlock" function
     */
    void soFillInSuperblock(const char *name, uint32_t ntotal, uint16_t itsize, uint32_t dbtotal);


    /**
     * \brief Fill in the blocks of the inode table.
     * \details
     *   The following nust be considered:
     *   - The inode table starts on block number 1
     *   - All inodes are free, except inode number 0
     *   - Inode number 0 must be filled knowing it is the root directory, considering:
     *     - its data is composed of 2 directory entries, stored in data block number 0
     *     - its permissions should be 0755
     *     - \c owner and group are given by system calls \c getuid and \c getgid, respectively
     *   - All others inodes must be put in the clean state, meaning:
     *     - all reference fields at \c NullBlockReference
     *     - all other fields at 0.
     *   .
     * \difficulty 3
     *
     * \param [in] itsize the number of blocks of the inode table
     * \param [in] date if \c true current date is set; otherwise date is put at zero
     *
     * \note Access to disk must be done using \ref wrb "soWriteRawBlock" function
     */
    void soFillInInodeTable(uint16_t itsize, bool date = true);


    /** 
     * \brief Fill in the root directory
     * \details
     *   The following nust be considered:
     *   - The root directory occupies a single data block, the first one after the inode table
     *   - It contains two entries, filled in with \c "." and \c "..", both pointing to inode 0
     *   - The remaining of the data block must be cleaned, filled with pattern 0x0 
     *   .
     * \difficulty 2
     *
     * \param [in] ntotal Total number of blocks in the device
     * \param [in] itsize number of blocks of the inode table
     * \param [in] dbtotal Total number of data blocks
     *
     * \note Access to disk must be done using \ref wrb "soWriteRawBlock" function
     */
    void soFillInRootDir(uint32_t ntotal, uint16_t itsize, uint32_t dbtotal);


    /**
     * \brief Fill in the data blocks containing references to free data blocks 
     * \details
     *   The following nust be considered:
     *   - The list of free data blocks must be sorted in ascending order
     *   - The first references of the list are in the retrieval cache, totally filled if possible
     *   - Non-used cells must be filled with pattern NullBlockReference
     *   - Nothing should be done, if there are no reference blocks
     *   .
     * \difficulty 2
     *
     * \param [in] ntotal Total number of blocks in the device
     * \param [in] itsize number of blocks of the inode table
     * \param [in] dbtotal Total number of data blocks
     *
     * \note Access to disk must be done using \ref wrb "soWriteRawBlock" function
     */
    void soFillInBitmapTable(uint32_t ntotal, uint16_t itsize, uint32_t dbtotal);


    /**
     * \brief Fill with zeros the free data blocks
     * \details
     *   The following nust be considered:
     *   - All data blocks, but the one used by the root directory, must be filled with pattern 0x0.
     *   .
     * \difficulty 1
     *
     * \param [in] ntotal Total number of blocks in the device
     * \param [in] itsize number of blocks of the inode table
     * \param [in] dbtotal Total number of data blocks
     *
     * \note Access to disk must be done using \ref wrb "soWriteRawBlock" function
     */
    void soZeroFreeDataBlocks(uint32_t ntotal, uint16_t itsize, uint32_t dbtotal);

    /* ***************************************** */

    /* ******************************************************************* */

    /** @} close group mksofs */
    /* ******************************************************************* */
};

#endif /* __SOFS21_MKSOFS__ */
