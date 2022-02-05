#include "direntries.h"

#include "core.h"
#include "devtools.h"
#include "daal.h"
#include "inodeblocks.h"
#include "bin_direntries.h"

#include <string.h>
#include <assert.h>
#include <errno.h>
#include <sys/stat.h>

namespace sofs21
{
    void grpRenameDirentry(int pih, const char *name, const char *newName)
    {
        soProbe(204, "%s(%d, %s, %s)\n", __FUNCTION__, pih, name, newName);

        /* replace this comment and following line with your code */
        //binRenameDirentry(pih, name, newName);
        SOInode* pih_pointer = soGetInodePointer(pih);

        // check if pih is a valid inode handler of a directory where the user has write access
        assert((pih_pointer->mode & S_IFDIR) == S_IFDIR);
        assert(soCheckInodeAccess(pih, W_OK) == 1);

        // check if name and newName contains '/
        assert(strchr(name, '/') == NULL); 
        assert(strchr(newName,'/') == NULL);

        uint32_t block_idx = NullBlockReference;        // save the block that have a entrie with the given name
        uint32_t entries_idx = 0;                       // entrie idx with the given name
        uint32_t block_idx_2slots = NullBlockReference; //save the block with 2 consecutive empty slots
        uint32_t entries_idx_2slots = 0;                // first of the two consecutive empty entries
        SODirectorySlot entries[DPB];

        // loop the block
        for (uint32_t i = 0; i < pih_pointer->size/BlockSize; i++)
        {
            soReadInodeBlock(pih,i,entries);
            // loop the entries of that block
            for (unsigned int j = 0; j < DPB; j++)
            {   

                // find the first block where 2 consecutive slots are empty and saves the block idx and the entrie idx
                if( block_idx_2slots == NullBlockReference ){
                    if(entries[j].nameBuffer[0] == '\0' && entries[j+1].nameBuffer[0] == '\0'){
                        block_idx_2slots = i;
                        entries_idx_2slots = j;
                    }
                }
                if(strlen(newName) <= DIRECTORY_SLOT){
                    // if an entry with the given newName already exists, exception EEXIST must be thrown
                    if(strcmp(newName,entries[j].nameBuffer) == 0)
                        throw SOException(EEXIST,__FUNCTION__);
                }
                else{
                    if(strncmp(newName, entries[j].nameBuffer,DIRECTORY_SLOT) == 0 && 
                        strncmp(newName+DIRECTORY_SLOT, entries[j+1].nameBuffer,DIRECTORY_SLOT) == 0){
                        throw SOException(EEXIST,__FUNCTION__);
                    }
                }

                // occupy two slots
                if(strlen(name) > DIRECTORY_SLOT){ 

                    if (entries[j].nameBuffer[29] != '\0')
                    {
                        if(strncmp(name, entries[j].nameBuffer,DIRECTORY_SLOT) == 0 &&
                            strncmp(name+DIRECTORY_SLOT, entries[j+1].nameBuffer,DIRECTORY_SLOT) == 0)
                        {
                            block_idx = i;
                            entries_idx = j; 
                        }
                    }
                }
                // occupies one slot
                else{           
                    if(strcmp(name,entries[j].nameBuffer) == 0)
                    {
                        block_idx = i;
                        entries_idx = j; 
                    }
                }
            }
        }
        // if an entry with the given name does not exist, exception ENOENT must be thrown
        if (block_idx == NullBlockReference)
            throw SOException(ENOENT,__FUNCTION__);

        // if lower, the unused slot must be cleaned
        //(WORKING)
        if(strlen(newName) <= DIRECTORY_SLOT){
            soReadInodeBlock(pih,block_idx,entries);
            if(strlen(name) > DIRECTORY_SLOT){
                strcpy(entries[entries_idx].nameBuffer, newName);
                entries[entries_idx].in = entries[entries_idx+1].in;
                strcpy(entries[entries_idx+1].nameBuffer, "");
                entries[entries_idx+1].in = NullInodeReference;
            }
            else{
                strcpy(entries[entries_idx].nameBuffer, newName);
            }
            soWriteInodeBlock(pih,block_idx,entries);
        }        

        if (strlen(newName) > DIRECTORY_SLOT){
            
            // if bigger and the following slot is empty, the entry extends now to the next slot
            //(WORKING)
            if(entries[entries_idx+1].nameBuffer[0] == '\0')
            {
                soReadInodeBlock(pih,block_idx,entries);
                strncpy(entries[entries_idx].nameBuffer,newName,DIRECTORY_SLOT); 
                strncpy(entries[entries_idx+1].nameBuffer,newName+DIRECTORY_SLOT,DIRECTORY_SLOT); 
                entries[entries_idx+1].in = entries[entries_idx].in;
                entries[entries_idx].in = NullInodeReference;
                soWriteInodeBlock(pih,block_idx,entries);
            }
            // if bigger and the following slot is not empty, the entry must be moved to the first hole big enough to hold it
            //(WORKING)
            else{
                soReadInodeBlock(pih,block_idx,entries);
                uint16_t inode = entries[entries_idx].in;
                memset(entries[entries_idx].nameBuffer, 0x0, DIRECTORY_SLOT);
                entries[entries_idx].in = NullInodeReference;
                soWriteInodeBlock(pih,block_idx,entries);
                // if there are no empty slots in the block, another block must be allocated.
                if(block_idx_2slots == NullBlockReference){
                    pih_pointer->size += BlockSize;
                    soReadInodeBlock(pih, pih_pointer->size/BlockSize - 1, entries);
                    // reset entries values
                    for (long unsigned int i = 0; i < DPB; i++) {
                        memset(entries[i].nameBuffer, 0x0, DIRECTORY_SLOT);
                        entries[i].in = NullInodeReference;
                    }
                    block_idx_2slots = pih_pointer->size/BlockSize - 1;
                    entries_idx_2slots = 0;
                    soWriteInodeBlock(pih, pih_pointer->size/BlockSize - 1, entries);
                }
                if(block_idx_2slots != block_idx)
                    soReadInodeBlock(pih,block_idx_2slots,entries);
                else
                    soReadInodeBlock(pih,block_idx,entries);

                
                strncpy(entries[entries_idx_2slots].nameBuffer,newName,DIRECTORY_SLOT);
                entries[entries_idx_2slots].in = NullInodeReference;
                strncpy(entries[entries_idx_2slots+1].nameBuffer,newName+DIRECTORY_SLOT,DIRECTORY_SLOT); 
                entries[entries_idx_2slots+1].in = inode;
                if (block_idx_2slots != block_idx)
                    soWriteInodeBlock(pih,block_idx_2slots,entries);
                else
                    soWriteInodeBlock(pih,block_idx,entries);
            }
        }
    }
};

