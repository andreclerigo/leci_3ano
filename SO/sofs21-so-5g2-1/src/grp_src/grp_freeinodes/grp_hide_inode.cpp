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
    bool grpHideInode(uint16_t in)
    {
        soProbe(403, "%s(%u)\n", __FUNCTION__, in);
        //Acess to SuperBlock

        if(in <=0 || in >= MAX_INODES){
            throw SOException(EINVAL,__FUNCTION__);
        }


        SOSuperblock* sb=soGetSuperblockPointer();
        uint16_t ih = soOpenInode(in);
        SOInode* Inode=soGetInodePointer(ih);
        
        if (sb->iqcount==DELETED_QUEUE_SIZE)return false;
        
        Inode->mode=~(Inode->mode); //complementar o mode

        sb->iqueue[sb->iqhead+sb->iqcount]=in;
        sb->iqcount+=1;
        soSaveSuperblock();
        soSaveInode(ih);
        soCloseInode(ih);
        return true;
        
    }
};

