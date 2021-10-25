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
    void soFillInInodeTable(uint16_t itsize, bool date)
    {
        if (soBinSelected(604))
            binFillInInodeTable(itsize, date);
        else
            grpFillInInodeTable(itsize, date);
    }

};
