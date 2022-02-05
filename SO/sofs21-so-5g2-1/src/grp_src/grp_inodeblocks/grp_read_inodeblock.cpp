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
    void grpReadInodeBlock(int ih, uint32_t ibn, void *buf)
    {
        soProbe(331, "%s(%d, %u, %p)\n", __FUNCTION__, ih, ibn, buf);

        /* replace this comment and following line with your code */
        //binReadInodeBlock(ih, ibn, buf);
        
        // check if the buf pointer is null
        assert(buf != NULL);
        
        uint32_t inode_block = soGetInodeBlock(ih, ibn);

        // if the referred inode block has not been allocated yet (reference equal to NullBlockReference), 
        // the returned data will consist of a byte stream filled with the null character (ascii code 0)
        if (inode_block == NullBlockReference)
            memset(buf, 0, BlockSize);
        else
            soReadDataBlock(inode_block, buf); 
    }
};
