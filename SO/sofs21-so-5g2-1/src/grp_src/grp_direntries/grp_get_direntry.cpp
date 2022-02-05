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
    uint16_t grpGetDirentry(int pih, const char *name)
    {
        soProbe(201, "%s(%d, %s)\n", __FUNCTION__, pih, name);

        /* replace this comment and following line with your code */
        //return binGetDirentry(pih, name);

        SOInode *inode = soGetInodePointer(pih);

        
        uint32_t i,j;

        for (i = 0; i < inode->size/BlockSize ; i++)
        {
            SODirectorySlot dir[DPB];
            soReadInodeBlock(pih, i, dir);
            
            for (j = 0; j < DPB; j++)
            {
                if(strlen(name) > 30){ 

                    if (dir[j].nameBuffer[29] != '\0')
                    {
                        if(strncmp(name, dir[j].nameBuffer,DIRECTORY_SLOT) == 0 &&
                            strncmp(name + DIRECTORY_SLOT, dir[j+1].nameBuffer,DIRECTORY_SLOT) == 0)
                        {
                            soSaveInode(pih);
                            return dir[j+1].in;
                        }
                    }
                }
                else {
                    if (strcmp(name , dir[j].nameBuffer) == 0){
                        soSaveInode(pih);
                        return dir[j].in;
                    }
                }
                
            }
        }
        //return NullNodeReference if name doesn't exist
        return NullInodeReference;
    }
};
