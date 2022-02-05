/*
 *  \author António Rui Borges - 2012-2015
 *  \authur Artur Pereira - 2009-2020
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
    uint32_t grpAllocDataBlock()
    {
        SOSuperblock* sb =  soGetSuperblockPointer(); 

        // throw Exception
        if (sb->dbfree == 0)
            throw SOException(ENOSPC, __FUNCTION__);

        // if the retrieval cache is empty
        if (sb->retrieval_cache.idx == REF_CACHE_SIZE)
            soReplenishFromBitmap();
        else 
            soReplenishFromCache();
        
        uint32_t idx =  sb->retrieval_cache.idx;
        uint32_t ref =  sb->retrieval_cache.ref[idx];

        sb->retrieval_cache.ref[idx] = NullBlockReference;
        sb->retrieval_cache.idx = 1;
        sb->dbfree--;

        return ref;


        /* replace this comment and following line with your code */
        //return binAllocDataBlock();
    }
};

