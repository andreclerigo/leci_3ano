/*
 *  \author António Rui Borges - 2012-2015
 *  \authur Artur Pereira - 2016-2020
 */

#include "freedatablocks.h"
#include "bin_freedatablocks.h"
#include "grp_freedatablocks.h"

#include <string.h>
#include <errno.h>
#include <iostream>

#include "core.h"
#include "devtools.h"
#include "daal.h"

namespace sofs21
{
    void grpReplenishFromCache(void)
    {
        soProbe(443, "%s()\n", __FUNCTION__);

        SOSuperblock* sb = soGetSuperblockPointer();

        if (sb->retrieval_cache.idx == REF_CACHE_SIZE){
            sb->retrieval_cache.idx = 0;
            for (int i = 0; i < REF_CACHE_SIZE; i++) {
                if (sb->insertion_cache.idx == 0) {
                    break;
                }

                sb->retrieval_cache.ref[i] = sb->insertion_cache.ref[i];
                sb->insertion_cache.ref[i] = NullBlockReference;

                sb->retrieval_cache.idx++;
                sb->insertion_cache.idx--;
            }
            soSaveSuperblock();
        }

        /* replace this comment and following line with your code */
        //binReplenishFromCache();
    }
};

