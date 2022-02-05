/*
 *  \author António Rui Borges - 2012-2015
 *  \authur Artur Pereira - 2016-2020
 */

#include "freedatablocks.h"
#include "bin_freedatablocks.h"
#include "grp_freedatablocks.h"

#include "core.h"
#include "devtools.h"
#include "daal.h"

#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <iostream>
using namespace std;

namespace sofs21
{
    /* only fill the current block to its end */
    void grpDeplete(void)
    {
        soProbe(444, "%s()\n", __FUNCTION__);

        /* replace this comment and following line with your code */
        //binDeplete();

        SOSuperblock* sb = soGetSuperblockPointer();
        
        // do nothing if the insertion cache is not full
        if (sb->insertion_cache.idx != REF_CACHE_SIZE) return;
    
        // if rbm_idx is NullBlockReference, it must be assigned 0
        if (sb->rbm_idx == NullBlockReference) sb->rbm_idx = 0;

        uint32_t br = sb->insertion_cache.ref[0];       // Block reference from cache
        uint32_t rbn = br / (BlockSize*8);              // index, within the bitmap table, of the required reference block
        uint32_t* bitmap = soGetBitmapBlockPointer(rbn);    // Get bitmap table pointer
        for(int i=0; i < REF_CACHE_SIZE; i++) {
            br = sb->insertion_cache.ref[i];            // Block reference from cache
            
            if(br / (BlockSize*8) != rbn){              // check if the block is the same
                rbn = br / (BlockSize*8);
                bitmap = soGetBitmapBlockPointer(rbn);
            }

            uint32_t bit_on_block = br % (BlockSize*8); // bit on reference block
            uint32_t word = bit_on_block / 32;          // index of word on reference block
            uint32_t bit = bit_on_block % 32;           // bit on word

            uint32_t mask = 1 << bit;                   // mask to switch bit to 1
            
            bitmap[word] |= mask;                       // mark bit of block as 1(free)

            sb->insertion_cache.ref[i] = NullBlockReference;    // after transferring a reference from A to B, the value in A must become NullBlockReference
            
            //if(br < sb->rbm_idx) sb->rbm_idx = br;    // updates rbm_idx to the lowest block (positionwise) freed
        }
        soSaveBitmapBlock();
        sb->insertion_cache.idx = 0;
        soSaveSuperblock();
    }
};

