#include "grp_mksofs.h"

#include "rawdisk.h"
#include "core.h"
#include "devtools.h"
#include "bin_mksofs.h"

#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/stat.h>
#include <inttypes.h>

namespace sofs21
{
    void grpFillInInodeTable(uint16_t itsize, bool date)
    {
        soProbe(604, "%s(%u)\n", __FUNCTION__, itsize);
        /* replace this comment and following lines with your code*/
        // binFillInInodeTable(itsize, date);

        // Fill all blocks
        uint16_t inode;
        uint16_t block;
        for(block = 1; block <= itsize; block++){
            
            // Start 1 block array of inodes
            SOInode inodeBlock[IPB];

            for(inode = 0; inode < IPB; inode++){

                // CLEAN STATE
                // Inicializar  todos os fields
                inodeBlock[inode].mode = 0;
                inodeBlock[inode].lnkcnt = 0;
                inodeBlock[inode].owner = 0;
                inodeBlock[inode].group = 0;
                inodeBlock[inode].size = 0;
                inodeBlock[inode].blkcnt = 0;
                inodeBlock[inode].atime = 0;
                inodeBlock[inode].mtime = 0;
                inodeBlock[inode].ctime = 0;
                inodeBlock[inode].i1 = NullBlockReference;
                inodeBlock[inode].i2 = NullBlockReference;
                //
                // Inicializar all references
                uint32_t i;
                for(i = 0; i < N_DIRECT; i++)
                    inodeBlock[inode].d[i] = NullBlockReference;
                
                if (block == 1 && inode == 0){
                    inodeBlock[0].lnkcnt = 2;
                    inodeBlock[0].owner = getuid();
                    inodeBlock[0].group = getgid();
                    inodeBlock[0].size = BlockSize;
                    inodeBlock[0].blkcnt = 1;
                    inodeBlock[0].mode = S_IFDIR|0755;

                    if  (date==true){
                        time_t system_time;
                        time (&system_time);

                        inodeBlock[0].atime = system_time;
                        inodeBlock[0].mtime = system_time;
                        inodeBlock[0].ctime = system_time;
                    }
                    inodeBlock[0].d[0] = 0;
                }
                
            }
            
            soWriteRawBlock(block,inodeBlock);
        }
    }
};

