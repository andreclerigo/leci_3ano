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
    void soComputeDiskStructure(uint32_t ntotal, uint16_t itotal, uint16_t & itsize, uint32_t & dbtotal)
    {
        if (soBinSelected(601))
            binComputeDiskStructure(ntotal, itotal, itsize, dbtotal);
        else
            grpComputeDiskStructure(ntotal, itotal, itsize, dbtotal);
    }

};
