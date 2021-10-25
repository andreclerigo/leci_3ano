#include <iostream>

#include "core.h"
#include "devtools.h"

using namespace std;
using namespace sofs21;

int main(void)
{
    cout <<
        "BlockSize: " << BlockSize << endl <<
        "sizeof(SOSuperblock): " << sizeof(SOSuperblock) << endl <<
        "sizeof(SOInode): " << sizeof(SOInode) << endl <<
        "sizeof(SODirectorySlot): " << sizeof(SODirectorySlot) << endl <<
        "IPB (inodes per block): " << IPB << endl <<
        "DPB (directory slots per block): " << DPB << endl <<
        "RPB references per block): " << RPB << endl;

    return 0;
}
