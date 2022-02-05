#include "grp_mksofs.h"

#include "rawdisk.h"
#include "core.h"
#include "devtools.h"
#include "bin_mksofs.h"

#include <inttypes.h>
#include <string.h>

namespace sofs21
{
    void grpFillInBitmapTable(uint32_t ntotal, uint16_t itsize, uint32_t dbtotal)
    {
        soProbe(605, "%s(%u, %u, %u)\n", __FUNCTION__, ntotal, itsize, dbtotal);

        /* replace this comment and following line with your code */
        //binFillInBitmapTable(ntotal, itsize, dbtotal);

        int bitmap_index = 1 + itsize;                                                      // index of the first bitmap block
        int bitmap_size = ntotal - dbtotal - itsize - 1;                                    // bitmap size in blocks
        int words_needed = (dbtotal + (32 - 1)) / 32;                                       // words needed to store the bitmap (round up)
        int exceed_bits = dbtotal % 32;                                                     // bits that are used in the last word
        u_int32_t bitmap_block[RPB];                                                        // bitmap block used to write the bitmap
        memset(bitmap_block, 0xff, RPB*4);                                                  // initialize bitmap with all 1s

        // iterate through the bitmap and set the bits that are used
        for (int b = 0; b < bitmap_size; b++)
        {   
            if (b == 0)
                bitmap_block[0] = bitmap_block[0] << 1;                                     // set datablock0 with 0
            else if (b == 1)
                bitmap_block[0] = 0xffffffff;                                               // set datablock0 with 1

            // last block, take the data size in consideration
            if (b == bitmap_size - 1) {
                
                words_needed = words_needed - ((bitmap_size - 1)* 256);                     // update words needed take into consideration the other blocks
                
                // set the bits on the last word used
                if (exceed_bits != 0) 
                    bitmap_block[words_needed - 1] = bitmap_block[words_needed] >> (32 - exceed_bits);
                
                // set the bits on the rest of the words as 0
                for (u_int32_t i = words_needed; i < RPB; i++) bitmap_block[i] = 0;
            }
            
            soWriteRawBlock(bitmap_index + b, bitmap_block);
        }
    }
};
