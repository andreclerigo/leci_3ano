/*
 *  \authur Artur Pereira - 2016-2021
 */

#include "inodeblocks.h"
#include "bin_inodeblocks.h"
#include "grp_inodeblocks.h"
#include "freeinodes.h"

#include "daal.h"
#include "core.h"
#include "devtools.h"

#include <string.h>
#include <inttypes.h>
#include <unistd.h>

namespace sofs21
{
    uint16_t grpNewInode(uint16_t type, uint16_t perm)
    {
        soProbe(333, "%s(%04x, %9o)\n", __FUNCTION__, type, perm);

        if (type != S_IFREG && type != S_IFDIR && type != S_IFLNK)
            throw SOException(EINVAL, __FUNCTION__);

        if (perm < 0 && perm > 0777)
            throw SOException(EINVAL, __FUNCTION__);

        SOSuperblock* sb =  soGetSuperblockPointer();

        uint16_t inode = 0;

        if (sb->ifree > 0)
            inode = soAllocInode();
        else { 
            if (sb->iqcount > 0) {
                inode = soUnqueueHiddenInode();
                soFreeInodeBlocks(soOpenInode(inode), inode / IPB);
            }
            else {
                throw SOException(ENOSPC, __FUNCTION__);
            }
        }

        int inodehandler = soOpenInode(inode);

        SOInode* pointer = soGetInodePointer(inodehandler);

        pointer->mode = type | perm;

        return inode;

        /* replace this comment and following line with your code */
        //return binNewInode(type, perm);
    }
};

