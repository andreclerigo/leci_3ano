#include "grp_mksofs.h"

#include "core.h"
#include "devtools.h"
#include "bin_mksofs.h"

#include <inttypes.h>
#include <iostream>

namespace sofs21
{
    void grpComputeDiskStructure(uint32_t ntotal, uint16_t itotal, uint16_t & itsize, uint32_t & dbtotal)
    {
        soProbe(601, "%s(%u, %u, ...)\n", __FUNCTION__, ntotal, itotal);

        /* replace this comment and following line with your code */
        binComputeDiskStructure(ntotal, itotal, itsize, dbtotal);
    }
};

