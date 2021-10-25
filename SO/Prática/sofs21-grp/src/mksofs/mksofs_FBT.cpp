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
    void soFillInBitmapTable(uint32_t ntotal, uint16_t itsize, uint32_t dbtotal)
    {
        if (soBinSelected(605))
            binFillInBitmapTable(ntotal, itsize, dbtotal);
        else
            grpFillInBitmapTable(ntotal, itsize, dbtotal);
    }

};
