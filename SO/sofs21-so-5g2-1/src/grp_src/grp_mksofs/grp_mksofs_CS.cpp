#include "grp_mksofs.h"

#include "core.h"
#include "devtools.h"
#include "bin_mksofs.h"
#include <cmath>

namespace sofs21
{
    void grpComputeDiskStructure(uint32_t ntotal, uint16_t itotal, uint16_t & itsize, uint32_t & dbtotal)
    {
        soProbe(601, "%s(%u, %u, ...)\n", __FUNCTION__, ntotal, itotal);

        /* replace this comment and following line with your code */
        //binComputeDiskStructure(ntotal, itotal, itsize, dbtotal);

        //if, at entry, the proposed value for \c itotal is 0, value ntotal/20
        // should be used as the proposed value
		if (itotal == 0){
			itotal = (uint16_t)(ntotal/20);
		}

        //itotal must be lower than or equal to MAX_INODES
        if(itotal > MAX_INODES){
            itotal=MAX_INODES;
        }

        //itotal must be greater than or equal to IPB
        if(itotal < IPB){
            itotal = IPB;
        }

        //itotal must be lower than or equal to the rounded up value of ntotal/8
        if(itotal > (uint16_t) ceil((double)ntotal/8)){
            itotal = (uint16_t) ceil((double) ntotal / 8);
        }

        //itotal must be rounded up to a multiple of IPB
        if(itotal % IPB != 0){
			itotal = itotal + IPB - (itotal % IPB);
		}

        itsize = (uint16_t)ceil(itotal/IPB);
        uint16_t rem = ntotal - (itsize+1);
        dbtotal = rem - (uint16_t) ceil((double)rem/(BlockSize*8));

    }
};

