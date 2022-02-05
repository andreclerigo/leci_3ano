/*
 *  \author António Rui Borges - 2012-2015
 *  \authur Artur Pereira - 2016-2021
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
    void grpReplenishFromBitmap(void)
    {
        soProbe(445, "%s()\n", __FUNCTION__);

        /* replace this comment and following line with your code */
        //binReplenishFromBitmap();
        
        SOSuperblock* sb = soGetSuperblockPointer();                                // create a pointer for the SuperBlock
        bool cache_empty;                                                           // flag to check if the cache is empty
        int free_bits = sb->dbfree - sb->insertion_cache.idx;                       // get the number of bits at 1 in the bitmap
        if (free_bits >= REF_CACHE_SIZE) free_bits = REF_CACHE_SIZE;                // if there are more than or equal to REF_CACHE_SIZE free data blocks, 
                                                                                    // only REF_CACHE_SIZE will be retrieved
        
        // check if the cache is empty
        if (sb->retrieval_cache.idx == REF_CACHE_SIZE) 
            cache_empty = true; 
        else 
            cache_empty = false;

        if (cache_empty == true) {
            // if the retrieval cache is empty, retrieve references from bitmap
            for (int block = free_bits; block > 0;) {
                int num_block = sb->rbm_idx / (BlockSize*8);                        
                int bit_on_block = sb->rbm_idx % (BlockSize*8);                     // auxiliary variable
                int word = bit_on_block / 32;
                int bit = bit_on_block % 32;

                uint32_t* bitmap = soGetBitmapBlockPointer(num_block);              // load bitmapblock
                uint32_t mask = 1 << bit;                                           // create a mask to check if the bit is at 1

                // if the bit is at 1, the block is free
                if ( (bitmap[word] & mask) ) {
                    sb->retrieval_cache.ref[REF_CACHE_SIZE - block] = sb->rbm_idx;  // save the reference in the retrieval cache

                    bitmap[word] &= ~mask;                                          // set the bit to 0 (sinalizing that the block is used)
                    soSaveBitmapBlock();                                            // save the bitmapblock

                    sb->retrieval_cache.idx--;                                      // decrement the number of free data blocks
                    block--;                                                        // decrement the number of blocks to be retrieved
                }
                sb->rbm_idx++;
            }
        }
        
        // check if bitmap is empty
        if (sb->dbfree - sb->insertion_cache.idx == REF_CACHE_SIZE) sb->rbm_idx = NullBlockReference;

        soSaveSuperblock();
    }
};
