/*
 *  \author António Rui Borges - 2012-2015
 *  \authur Artur Pereira - 2016-2020
 */

#include "freedatablocks.h"
#include "bin_freedatablocks.h"
#include "grp_freedatablocks.h"

#include <stdio.h>
#include <errno.h>
#include <inttypes.h>
#include <time.h>
#include <unistd.h>
#include <sys/types.h>

#include "core.h"
#include "devtools.h"
#include "daal.h"

namespace sofs21
{
    void grpFreeDataBlock(uint32_t bn)
    {   
        soProbe(442, "%s(%u)\n", __FUNCTION__, bn);
        SOSuperblock* sb=soGetSuperblockPointer();
        if(bn <=0 || bn >= sb->ntotal){
            throw SOException(EINVAL,__FUNCTION__);
        }

        if (sb->insertion_cache.idx>REF_CACHE_SIZE){
            soDeplete();
        }
        sb->insertion_cache.ref[sb->insertion_cache.idx]=bn;
        sb->dbfree++;
        sb->insertion_cache.idx++;
        soSaveSuperblock();
        /* replace this comment and following line with your code */
        //binFreeDataBlock(bn);
    }
};

