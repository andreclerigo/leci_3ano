/**
 *  \file
 *  \brief Student version of the \b sofs21 formatting functions.
 *
 *  \author Artur Pereira - 2019-2020
 *
 *  \remarks See the main \c mksofs header file for documentation
 */

#ifndef __SOFS21_MKSOFS_GROUP__
#define __SOFS21_MKSOFS_GROUP__

#include <inttypes.h>

namespace sofs21
{
    void grpComputeDiskStructure(uint32_t ntotal, uint16_t itotal, uint16_t & itsize, uint32_t & dbtotal);

    void grpFillInSuperblock(const char *name, uint32_t ntotal, uint16_t itsize, uint32_t dbtotal);

    void grpFillInInodeTable(uint16_t itsize, bool date = true);

    void grpFillInRootDir(uint32_t ntotal, uint16_t itsize, uint32_t dbtotal);

    void grpFillInBitmapTable(uint32_t ntotal, uint16_t itsize, uint32_t dbtotal);

    void grpZeroFreeDataBlocks(uint32_t ntotal, uint16_t itsize, uint32_t dbtotal);
};

#endif /* __SOFS21_MKSOFS_GROUP__ */
