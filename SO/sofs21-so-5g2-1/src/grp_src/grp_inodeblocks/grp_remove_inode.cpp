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

namespace sofs21
{
    void grpRemoveInode(uint16_t in)
    {
        soProbe(334, "%s(%d)\n", __FUNCTION__, in);

        /* replace this comment and following line with your code */
        //binRemoveInode(in);
        
        //SOSuperblock* sb = soGetSuperblockPointer();
        
        int stat = soHideInode(in);
        if (stat == 0){                                        // check if the deleted queue is full -> stat = 0(false)
            uint16_t oldest_inode = soUnqueueHiddenInode();    // the oldest inode there must removed from the queue
            int oldest_inode_hander = soOpenInode(oldest_inode);                  
            uint32_t fibn = oldest_inode/IPB;                  // if oldest_inode < 16, finb = 0 (inode table first block). 
                                                               // if 16<=oldest_inode<32 and, fibn = 1 (inode table second block)
                                                               // if 32<=oldest_inode<48 and, fibn = 2 (inode table third block)
                                                               // if 48<=oldest_inode<64 and, fibn = 3 (inode table forth block)
            soFreeInodeBlocks(oldest_inode_hander,fibn);       // the oldest inode must be cleaned
            soFreeInode(oldest_inode);                         // the oldest inode must be freed
            soSaveInode(oldest_inode_hander);
            soCloseInode(oldest_inode_hander);                   
            soHideInode(in);
        }

    }
};

