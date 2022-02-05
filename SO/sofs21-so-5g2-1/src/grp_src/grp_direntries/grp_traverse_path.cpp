#include "direntries.h"

#include "core.h"
#include "devtools.h"
#include "daal.h"
#include "inodeblocks.h"
#include "direntries.h"
#include "bin_direntries.h"

#include <errno.h>
#include <string.h>
#include <libgen.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>

namespace sofs21
{
    uint16_t grpTraversePath(char *path)
    {
        soProbe(221, "%s(%s)\n", __FUNCTION__, path);

        

        char *parent_dirs = dirname(strdup(path));
        char *last = basename(strdup(path));


        if(strcmp(last,"/") == 0){ //-->root inode =0
            return 0;
        }
        
        uint32_t inode = grpTraversePath(parent_dirs);

        if(inode == NullInodeReference){
            throw SOException(ENOTDIR, __FUNCTION__);
        }
        
        int ih = soOpenInode(inode);
        SOInode * Inode = soGetInodePointer(ih);
              
        if(!S_ISDIR(Inode->mode)){
            soCloseInode(ih);      
            throw SOException(ENOTDIR,__FUNCTION__);
        }

        if(!soCheckInodeAccess(ih,X_OK)){
            soCloseInode(ih);  
            throw SOException(EACCES ,__FUNCTION__);
        }

        inode = soGetDirentry(ih,last);
        soCloseInode(ih);
        return inode;
        
    }
};

