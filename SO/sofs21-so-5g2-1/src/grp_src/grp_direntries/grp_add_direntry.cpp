#include "direntries.h"

#include "core.h"
#include "devtools.h"
#include "daal.h"
#include "inodeblocks.h"
#include "bin_direntries.h"

#include <errno.h>
#include <string.h>
#include <sys/stat.h>
#include <assert.h>
#include <string.h>

namespace sofs21
{
    void grpAddDirentry(int pih, const char *name, uint16_t cin)
    {
        soProbe(202, "%s(%d, %s, %u)\n", __FUNCTION__, pih, name, cin);

        /* replace this comment and following line with your code */
        // binAddDirentry(pih, name, cin);

        SOInode *pip = soGetInodePointer(pih);
        // check if pih is valid
        assert(pip != NULL);
        // check if pih is a directory
        assert((pip->mode & S_IFDIR) == S_IFDIR);
        // check if cin is valid (cin is less then the number of free inodes)
        SOSuperblock *sb = soGetSuperblockPointer();
        assert(cin < sb->ifree);
        // check if name contains '/
        assert(strchr(name, '/') == NULL);
        

        SODirectorySlot ds[DPB];
        int slots_occupied = (strlen(name) + DIRECTORY_SLOT-1)/DIRECTORY_SLOT;

        // iterate through the directory blocks
        for (unsigned int ibn = 0; ibn < pip->size/BlockSize; ibn++) {
            soReadInodeBlock(pih, ibn, ds);
            
            // check if there is an equal name on the Direntries of the Parent
            for (long unsigned int i = 0; i <= DPB-slots_occupied; i++) {
                if (strncmp(name, ds[i].nameBuffer, DIRECTORY_SLOT) == 0) {
                    if (slots_occupied == 1 && ds[i].in != NullInodeReference)
                        throw SOException(EEXIST, __FUNCTION__);
                    if (slots_occupied == 2 && ds[i].in == NullInodeReference && strncmp(name+DIRECTORY_SLOT, ds[i+1].nameBuffer, DIRECTORY_SLOT) == 0) 
                        throw SOException(EEXIST, __FUNCTION__);
                }
            }
        }

        // iterate through the directory blocks
        for (unsigned int ibn = 0; ibn < pip->size/BlockSize; ibn++) {
            soReadInodeBlock(pih, ibn, ds);

            // check if there is enough space to store the new directory entry
            for (long unsigned int i = 0; i <= DPB-slots_occupied; i++) {
                if ('\0' == (ds[i].nameBuffer)[0]) {
                    if (slots_occupied == 1) {
                        strncpy(ds[i].nameBuffer, name, DIRECTORY_SLOT);
                        ds[i].in = cin;
                        soWriteInodeBlock(pih, ibn, ds);
                        return;
                    }
                    
                    if (slots_occupied == 2 && ('\0' == (ds[i+1].nameBuffer)[0])) {
                        strncpy(ds[i].nameBuffer, name, DIRECTORY_SLOT);
                        strncpy(ds[i+1].nameBuffer, name+DIRECTORY_SLOT, DIRECTORY_SLOT);
                        ds[i].in = NullInodeReference;
                        ds[i+1].in = cin;
                        soWriteInodeBlock(pih, ibn, ds);
                        return;
                    }
                }
            }
        }

        // reset ds values
        for (long unsigned int i = 0; i < DPB; i++) {
            ds[i].nameBuffer[0] = '\0';
            ds[i].in = NullInodeReference;
        }
        
        // new block is allocated
        pip->size += BlockSize;
        ds[slots_occupied-1].in = cin;
        strncpy(ds[0].nameBuffer, name, DIRECTORY_SLOT);
        
        if (slots_occupied == 2) {
            strncpy(ds[1].nameBuffer, name+DIRECTORY_SLOT, DIRECTORY_SLOT);
            ds[0].in = NullInodeReference;
        }
        soWriteInodeBlock(pih, pip->size/BlockSize - 1, ds);
    }
};
