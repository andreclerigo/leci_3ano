/*
 *  \author António Rui Borges - 2012-2015
 *  \authur Artur Pereira - 2016-2020
 */

#include "freeinodes.h"
#include "bin_freeinodes.h"
#include "grp_freeinodes.h"

#include <stdio.h>
#include <errno.h>
#include <inttypes.h>
#include <time.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>

#include <iostream>

#include "core.h"
#include "devtools.h"
#include "daal.h"

namespace sofs21
{
    uint16_t grpAllocInode()
    {
        soProbe(401, "%s()\n", __FUNCTION__);

        /* replace this comment and following line with your code 
        return binAllocInode();
        */
        
        SOSuperblock* sb = soGetSuperblockPointer();
        if (sb->ifree == 0){    
            return NullInodeReference;  // returns NullInodeReference if there is no free inodes
        }      
        uint32_t inode_id = sb->iidx;
        for(; inode_id < sb->itotal; inode_id++){
            if((sb->ibitmap[inode_id/32] >> (inode_id % 32)) & 0b01){ // check at bit_pos if the bit value is 1 or 0
                break;  // if bit == 1, loop breaks
            }
        }
        inode_id %= sb->itotal;

        // change bit at bit_pos to 0
        sb->ibitmap[inode_id/32] = sb->ibitmap[inode_id/32] & ~(0b01<<inode_id%32);  
        sb->ifree--;
        sb->iidx = (inode_id+1)%(sb->itotal);   // search should start at index next to the last allocated inode
                                                // last allocated inode -> inode_idq
        soSaveSuperblock();
        return inode_id;  // returns the number (reference) of the inode allocated
        
    }
};

