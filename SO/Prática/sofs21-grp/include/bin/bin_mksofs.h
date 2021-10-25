/**
 *  \file
 *  \brief Binary version of the \b sofs21 formatting functions.
 *
 *  \author Artur Pereira - 2007-2009, 2016-2020
 *  \author Miguel Oliveira e Silva - 2009, 2017
 *  \author António Rui Borges - 2010-2015
 */

#ifndef __SOFS21_MKSOFS_BIN__
#define __SOFS21_MKSOFS_BIN__

#include <inttypes.h>

namespace sofs21
{
    void binComputeDiskStructure(uint32_t ntotal, uint16_t itotal, uint16_t & itsize, uint32_t & dbtotal);

    void binFillInSuperblock(const char *name, uint32_t ntotal, uint16_t itsize, uint32_t dbtotal);

    void binFillInInodeTable(uint16_t itsize, bool date = true);

    void binFillInRootDir(uint32_t ntotal, uint16_t itsize, uint32_t dbtotal);

    void binFillInBitmapTable(uint32_t ntotal, uint16_t itsize, uint32_t dbtotal);

    void binZeroFreeDataBlocks(uint32_t ntotal, uint16_t itsize, uint32_t dbtotal);
};

#endif /* __SOFS21_MKSOFS_BIN__ */
