#include "grp_mksofs.h"

#include "rawdisk.h"
#include "core.h"
#include "devtools.h"
#include "bin_mksofs.h"

#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/stat.h>
#include <inttypes.h>

namespace sofs21
{
    void grpFillInInodeTable(uint16_t itsize, bool date)
    {
        soProbe(604, "%s(%u)\n", __FUNCTION__, itsize);

        /* replace this comment and following line with your code */
        binFillInInodeTable(itsize, date);
    }
};

