/*
 *  \author António Rui Borges - 2012-2015
 *  \authur Artur Pereira - 2016-2021
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

#include "core.h"
#include "devtools.h"
#include "daal.h"

namespace sofs21
{
    void grpFreeInode(uint16_t in)
    {
        soProbe(402, "%s(%u)\n", __FUNCTION__, in);

        /* replace this comment and following line with your code */
        //binFreeInode(in);

        SOSuperblock* psb = soGetSuperblockPointer();

        if(in>=psb->itotal || in < 0){
            throw SOException(EINVAL, __FUNCTION__);
        }

        uint16_t inode_handler = soOpenInode(in);
        SOInode* pinode = soGetInodePointer(inode_handler);

        //mode onwer group at 0
        pinode->mode=0;
        pinode->owner=0;
        pinode->group=0;

        //other field methods
        pinode->size = 0;
        pinode->blkcnt = 0;
        pinode->atime = 0;
        pinode->ctime = 0;
        pinode->mtime = 0;

        //refences put at null
        for (uint32_t i = 0; i < N_DIRECT; i++){
            pinode->d[i] = NullBlockReference;    
        }
        pinode->i1 = NullBlockReference; 
        pinode->i2 = NullBlockReference; 

        soSaveInode(inode_handler);
        soCloseInode(inode_handler);

        //array of 32-bit words
        uint32_t block = in/32;
        uint32_t position = in%32;

        psb->ibitmap[block] = psb->ibitmap[block] | (0x1<<position);
        psb->ifree = psb->ifree +1;
        psb->iidx = in+1;

        soSaveSuperblock();
    }
};

