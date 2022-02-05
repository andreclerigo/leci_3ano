/*
 *  \authur Artur Pereira - 2016-2021
 */

#include "inodeblocks.h"
#include "bin_inodeblocks.h"
#include "grp_inodeblocks.h"

#include "daal.h"
#include "core.h"
#include "devtools.h"

#include <string.h>
#include <inttypes.h>
#include <assert.h>

namespace sofs21
{
    void grpWriteInodeBlock(int ih, uint32_t ibn, void *buf)
    {
        soProbe(332, "%s(%d, %u, %p)\n", __FUNCTION__, ih, ibn, buf);

        /* replace this comment and following line with your code */
        //binWriteInodeBlock(ih, ibn, buf);
        
        // check if the buf pointer is null
        assert(buf != NULL);

        uint32_t inode_block = soGetInodeBlock(ih, ibn);

        // if the referred inode block has not been allocated yet (reference equal to NullBlockReference) nothing is done
        if (inode_block == NullBlockReference) inode_block = soAllocInodeBlock(ih, ibn); 
        soWriteDataBlock(inode_block, buf);
    }
};

