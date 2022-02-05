#include "grp_mksofs.h"

#include "rawdisk.h"
#include "core.h"
#include "devtools.h"
#include "bin_mksofs.h"

#include <string.h>
#include <inttypes.h>

namespace sofs21
{
    void grpFillInSuperblock(const char *name, uint32_t ntotal, uint16_t itsize, uint32_t dbtotal)
    {
        soProbe(602, "%s(%s, %u, %u, %u)\n", __FUNCTION__, name, ntotal, itsize, dbtotal);
        SOSuperblock* sb=(SOSuperblock*) malloc(sizeof(*sb));
        sb->magic=0xFFFF;
        sb->version=VERSION_NUMBER;
        strncpy(sb->name,name,PARTITION_NAME_LEN+1); 
        sb->itotal=itsize*16;
        sb->ifree=sb->itotal-1;
        sb->ntotal=ntotal;
        sb->iidx=1;
        
        uint16_t i;
        for (i = 0; i < (sb->itotal)/32; i++)
        {
            sb->ibitmap[i]=0xFFFFFFFF; //colocar os bits do bitmap todos a 1.
        
        }
        
        if ((sb->itotal % 32) ==0) {
            sb->ibitmap[i] = 0x00000000;
        } else {
            sb->ibitmap[i] = 0xFFFFFFFF >> (32 - (sb->itotal % 32));
        }
        sb->ibitmap[0] = sb->ibitmap[0] & 0xFFFFFFFE;// inode 0 =0 e manter os outros bits do bitmap a como estavam
        
        for (uint16_t i = 0; i < DELETED_QUEUE_SIZE*8; i++)
        {
            sb->iqueue[i]=NullInodeReference;
        }
        sb->iqcount=0;
        sb->iqhead=sb->iqcount;
        
        sb->dbp_start=ntotal-dbtotal;
        sb->dbtotal=dbtotal;
        sb->dbfree=dbtotal-1;
        
        sb->rbm_start=itsize+1;
        sb->rbm_size=sb->dbp_start-sb->rbm_start;
        sb->rbm_idx=0;
        

        sb->retrieval_cache.idx = REF_CACHE_SIZE;
        sb->insertion_cache.idx = 0;
        for(unsigned int i = 0; i < REF_CACHE_SIZE; i++) {
            sb->retrieval_cache.ref[i] = NullBlockReference;
            sb->insertion_cache.ref[i] = NullBlockReference;
        }
        

        
        soWriteRawBlock(0,sb);
    
        /* replace this comment and following line with your code */
        //binFillInSuperblock(name, ntotal, itsize, dbtotal);
    }
};

