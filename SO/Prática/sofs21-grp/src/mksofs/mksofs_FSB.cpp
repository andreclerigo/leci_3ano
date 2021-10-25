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
    void soFillInSuperblock(const char *name, uint32_t ntotal, uint16_t itsize, uint32_t dbtotal)
    {
        if (soBinSelected(602))
            binFillInSuperblock(name, ntotal, itsize, dbtotal);
        else
            grpFillInSuperblock(name, ntotal, itsize, dbtotal);
    }

};
