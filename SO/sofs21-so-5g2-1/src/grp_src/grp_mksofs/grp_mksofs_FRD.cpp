#include "grp_mksofs.h"

#include "rawdisk.h"
#include "core.h"
#include "devtools.h"
#include "bin_mksofs.h"

#include <string.h>
#include <inttypes.h>

namespace sofs21
{
    /*
       filling in the contents of the root directory:
       the first 2 entries are filled in with "." and ".." references
       the remainding of the block is filled with zeros.
       */
    void grpFillInRootDir(uint32_t ntotal, uint16_t itsize, uint32_t dbtotal)
    {
        soProbe(606, "%s(%u, %u, %u)\n", __FUNCTION__, ntotal, itsize, dbtotal);

        /* replace this comment and following line with your code */
        //binFillInRootDir(ntotal, itsize, dbtotal);

        SODirectorySlot directory[DPB];                   //SODirectorySlot buffer

        // int bmsize = ntotal - dbtotal - itsize - 1;    // number of bitmap table blocks

        // position of root diretory equals to : 
        // int firstblock = 1 + itsize + bmsize = 1 + itsize + ntotal- dbtotal - itsize -1

        int firstblock = ntotal - dbtotal;

        // it contains two entries, filled in with "." and "..", both pointing to inode 0
        strcpy(directory[0].nameBuffer,".");
        directory[0].in = 0;

        strcpy(directory[1].nameBuffer,"..");
        directory[1].in = 0;

        for(uint32_t i=2; i<DPB; i++) {                 //the remaining of the data block must be empty, meaning:
            //nameBuffer field filled with pattern 0x0
            memset(directory[i].nameBuffer, 0x0, DIRECTORY_SLOT);  
            directory[i].in =  NullInodeReference;      //in field filled with NullInodeReference
        }

        soWriteRawBlock(firstblock,directory);
    }
};

