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
    uint16_t grpUnqueueHiddenInode()
    {
        soProbe(404, "%s()\n", __FUNCTION__);

        /* replace this comment and following line with your code */
        //return binUnqueueHiddenInode();
        
        SOSuperblock* sb = soGetSuperblockPointer();

        if(sb->iqcount == 0)
            return NullInodeReference;  // if the queue is empty, do nothing and return NullInodeReference

        uint16_t oldest_inode = sb->iqueue[sb->iqhead]; // reference of the oldest inode

        sb->iqueue[sb->iqhead] = NullInodeReference; // oldest inode fillet with NullInodeReference

        // update the other iqueue fields (iqhead, iqcount)

        if(DELETED_QUEUE_SIZE-1 == sb->iqhead)  // if index os oldest inode is the last position of the queue
            sb->iqhead = 0;                         // next oldest inode index is the first position
        else
            sb->iqhead = sb->iqhead+1;          // else, next oldest inode index is the following index 
        sb->iqcount--;                          // size of the queue decreases
        
        soSaveSuperblock();
        return oldest_inode; // return oldest inode reference
    }
};

