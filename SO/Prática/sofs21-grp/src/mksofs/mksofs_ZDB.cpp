/*
 *  \authur Artur Pereira - 2009-2020
 */

#include "mksofs.h"

#include "core.h"
#include "devtools.h"

#include <inttypes.h>

namespace sofs21
{
    /* see mksofs.h for a description */
    void soZeroFreeDataBlocks(uint32_t ntotal, uint16_t itotal, uint32_t dbtotal)
    {
        if (soBinSelected(607))
            binZeroFreeDataBlocks(ntotal, itotal, dbtotal);
        else
            grpZeroFreeDataBlocks(ntotal, itotal, dbtotal);
    }

};
