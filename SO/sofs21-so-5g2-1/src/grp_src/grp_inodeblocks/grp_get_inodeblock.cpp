/*
 *  \authur Artur Pereira - 2016-2021
 */

#include "inodeblocks.h"
#include "bin_inodeblocks.h"
#include "grp_inodeblocks.h"

#include "daal.h"
#include "core.h"
#include "devtools.h"

#include <errno.h>

namespace sofs21
{
    /* ********************************************************* */

#if true
    /* Considering bn is the number of a data block containing references to
     * data blocks, return the value of its idx position
     */
    static uint32_t grpGetIndirectInodeBlock(uint32_t bn, uint32_t idx);

    /* Considering bn is the number of a data block containing references
     * to data blocks containing references to data blocks (double indirection),
     * return the value of its idx position
     */
    static uint32_t grpGetDoubleIndirectInodeBlock(uint32_t bn, uint32_t idx);
#endif

    /* ********************************************************* */

    uint32_t grpGetInodeBlock(int ih, uint32_t ibn)
    {
        soProbe(301, "%s(%d, %u)\n", __FUNCTION__, ih, ibn);
        if (ibn > RPB*RPB + RPB + N_DIRECT || ibn < 0 ) {
            throw SOException(EINVAL, __FUNCTION__);
        }
        if(!soGetInodePointer(ih)){
            throw SOException(EINVAL, __FUNCTION__);
        }
            
        
        SOInode* Inode = soGetInodePointer(ih);
        if (ibn < N_DIRECT) {
            return Inode->d[ibn];
        } else if (ibn < RPB + N_DIRECT) {
            return grpGetIndirectInodeBlock(Inode->i1, ibn - N_DIRECT);
        } else {
            return grpGetDoubleIndirectInodeBlock(Inode->i2, ibn - RPB - N_DIRECT);
        }
        
    }

    /* ********************************************************* */

#if true
    static uint32_t grpGetIndirectInodeBlock(uint32_t bn, uint32_t idx)
    {
        soProbe(301, "%s(%d, %d)\n", __FUNCTION__, bn, idx);
        if (bn == NullBlockReference) {
            return NullBlockReference;
        }
        uint32_t array[RPB];
        soReadDataBlock(bn, array);
        return array[idx];
        
    }
#endif

    /* ********************************************************* */

#if true
    static uint32_t grpGetDoubleIndirectInodeBlock(uint32_t bn, uint32_t idx)
    {
        soProbe(301, "%s(%d, %d)\n", __FUNCTION__, bn, idx);
        if (bn == NullBlockReference) {
            return NullBlockReference;
        }
        
        uint32_t bn2 = idx / RPB;
        uint32_t array[RPB];
        soReadDataBlock(bn, array);
        return grpGetIndirectInodeBlock(array[bn2],idx);
        
        
    }
#endif
};