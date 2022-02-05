#include "direntries.h"

#include "core.h"
#include "devtools.h"
#include "daal.h"
#include "inodeblocks.h"
#include "bin_direntries.h"

#include <errno.h>
#include <string.h>
#include <sys/stat.h>

namespace sofs21
{
    bool grpCheckDirEmpty(int ih)
    {
        soProbe(205, "%s(%d)\n", __FUNCTION__, ih);

        /* replace this comment and following line with your code */
        // return binCheckDirEmpty(ih);

        SOInode *inode = soGetInodePointer(ih);

        // Check if dir
        if( (inode->mode & S_IFDIR) != S_IFDIR) throw SOException(ENOTDIR, __FUNCTION__);

        // Check if ih is a valid inode handler of a directory where the user has read access
        // if(!soCheckInodeAccess(ih, R_OK)) throw SOException(EACCES, __FUNCTION__);

        SODirectorySlot dirs[DPB];

        uint32_t num_blks = inode->size / BlockSize;
        // Check if there are any entries in the allocated blocks
        for(uint32_t blk = 0; blk < num_blks; blk++) {
            soReadInodeBlock(ih, blk, dirs);
            for(uint32_t i = 0; i < DPB; i++) {
                // jump through '.' and '..' entries
                if(strcmp(dirs[i].nameBuffer, ".") == 0 || strcmp(dirs[i].nameBuffer, "..") == 0) continue;
                if(dirs[i].nameBuffer[0] != '\0') return false;
            } 
        }

        return true;
    }
};

