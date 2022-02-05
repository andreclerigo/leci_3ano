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
    uint16_t grpDeleteDirentry(int pih, const char *name)
    {
        soProbe(203, "%s(%d, %s)\n", __FUNCTION__, pih, name);

        /* replace this comment and following line with your code */
        //return binDeleteDirentry(pih, name);

        //pih is a valid inode handler of a directory where the user has write access
        soCheckInodeAccess(pih, W_OK);

        //name is a valid base name (it doesn't contain '/')
        if(strchr(name, '/') != NULL){
            throw SOException(ENOENT, __FUNCTION__);
        }

        //access inode 
        SOInode *pinode = soGetInodePointer(pih);

        //access all the directories
        SODirectorySlot pdirentry [DPB];

        //2 slots case
        char name1 [DIRECTORY_SLOT];
        char name2 [DIRECTORY_SLOT];
        if(strlen(name)>DIRECTORY_SLOT){
            strncpy(name1, name, DIRECTORY_SLOT);
            strncpy(name2, name+DIRECTORY_SLOT, DIRECTORY_SLOT);
        }

        unsigned int flag=0;
        uint32_t old_i;
        uint32_t old_j;

        for(uint32_t i=0 ; i<pinode->blkcnt ; i++){
            soReadInodeBlock(pih, i, pdirentry);
            for (uint32_t j = 0 ; j < DPB; j++){
                if(strlen(name)<=DIRECTORY_SLOT){ //1 slot
                    if( (strncmp(name, pdirentry[j].nameBuffer, DIRECTORY_SLOT)==0) && pdirentry[j].in!=NullInodeReference){
                        uint16_t inode_number = pdirentry[j].in;
                        memset(pdirentry[j].nameBuffer, 0x00, DIRECTORY_SLOT);
                        pdirentry[j].in=NullInodeReference;
                        soWriteInodeBlock(pih, i, pdirentry);
                        return inode_number;
                    }
                }else{ //2 slots
                    if (flag==0){
                        if((strncmp(name1, pdirentry[j].nameBuffer, DIRECTORY_SLOT)==0) && pdirentry[j].in==NullInodeReference){
                            flag=1;
                            old_i=i;
                            old_j=j;
                        }
                    }
                    else if (flag==1){
                        if( (strncmp(name2, pdirentry[j].nameBuffer, DIRECTORY_SLOT)==0) && pdirentry[j].in!=NullInodeReference){
                            //bloco atual
                            uint16_t inode_number = pdirentry[j].in;
                            memset(pdirentry[j].nameBuffer, 0x00, DIRECTORY_SLOT);
                            pdirentry[j].in=NullInodeReference;
                            soWriteInodeBlock(pih, i, pdirentry);

                            //read previous block
                            soReadInodeBlock(pih, old_i, pdirentry);
                            memset(pdirentry[old_j].nameBuffer, 0x00, DIRECTORY_SLOT);
                            soWriteInodeBlock(pih, old_i, pdirentry);
                            flag=0;
                            return inode_number;
                        }
                    }
                }
            }
        }
        throw SOException(ENOENT, __FUNCTION__);
    }
};

