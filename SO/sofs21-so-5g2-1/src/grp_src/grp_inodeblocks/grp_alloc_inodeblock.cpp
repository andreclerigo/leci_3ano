/*
 *  \authur Artur Pereira - 2016-2021
 */

#include "inodeblocks.h"
#include "bin_inodeblocks.h"
#include "grp_inodeblocks.h"

#include "freedatablocks.h"
#include "daal.h"
#include "core.h"
#include "devtools.h"

#include <errno.h>

#include <iostream>

namespace sofs21
{

#if true
    static uint32_t grpAllocIndirectInodeBlock(int ih, uint32_t & i1, uint32_t idx);
    static uint32_t grpAllocDoubleIndirectInodeBlock(int ih, uint32_t & i2, uint32_t idx);
#endif

    /* ********************************************************* */

    uint32_t grpAllocInodeBlock(int ih, uint32_t ibn)
    {
        soProbe(302, "%s(%d, %u)\n", __FUNCTION__, ih, ibn);

        /* replace the following two lines with your code */
        //return binAllocInodeBlock(ih, ibn);
 
        //if ih is not a valid handler of a open inodes
        SOInode* pinode = soGetInodePointer(ih);
        
        uint32_t allocBlock;

        //if ibn is not a valid inode block number
        if ( !(ibn<(N_DIRECT + RPB + (RPB*RPB))) || (ibn<0)){
            throw SOException(EINVAL, __FUNCTION__);
        }

        if(ibn < N_DIRECT){
            if (pinode->d[ibn]!=NullBlockReference){
                throw SOException(ESTALE, __FUNCTION__);
            }
            allocBlock = soAllocDataBlock();
            pinode->d[ibn] = allocBlock;
            pinode-> blkcnt ++; 
        }
        else if(ibn < RPB + N_DIRECT){
            allocBlock = grpAllocIndirectInodeBlock(ih, pinode->i1, ibn-N_DIRECT);
        } 
        else{
            allocBlock = grpAllocDoubleIndirectInodeBlock(ih, pinode->i2, ibn-N_DIRECT-RPB);
        }
        soSaveInode(ih);
        return allocBlock;

    }

    /* ********************************************************* */

#if true
    /*
    */
    static uint32_t grpAllocIndirectInodeBlock(int ih, uint32_t & i1, uint32_t idx){
        soProbe(302, "%s(%d, %u, %u)\n", __FUNCTION__, ih, i1, idx);

        /* replace the following two lines with your code */
        /* throw SOException(ENOSYS, __FUNCTION__); 
        return 0 ;*/
        SOInode* pinode = soGetInodePointer(ih);

        //bloco de referencias 
        uint32_t ref [RPB];
        uint32_t allBlock;

        if (i1==NullBlockReference){
            i1=soAllocDataBlock();
            pinode-> blkcnt = pinode-> blkcnt + 1; 
            for (uint32_t i = 0; i < RPB; i++) {
                ref[i] = NullBlockReference;
            }
        }else{
            soReadDataBlock(i1, ref);
            if(ref[idx]!=NullBlockReference){
                throw SOException(ESTALE, __FUNCTION__);
            }
        }

        allBlock = soAllocDataBlock();
        pinode-> blkcnt = pinode-> blkcnt + 1; 
        ref[idx] = allBlock;
        soWriteDataBlock(i1, ref);
        soSaveInode(ih);
        return allBlock;
    }
#endif

    /* ********************************************************* */

#if true
    /*
    */
    static uint32_t grpAllocDoubleIndirectInodeBlock(int ih, uint32_t & i2, uint32_t idx)
    {
        soProbe(302, "%s(%d, %u, %u)\n", __FUNCTION__, ih, i2, idx);

        /* replace the following two lines with your code */
        /* throw SOException(ENOSYS, __FUNCTION__); 
        return 0; */
        SOInode* pinode = soGetInodePointer(ih);

        uint32_t ref [RPB];
        uint32_t allBlock;

        uint32_t index_block = idx / RPB;
        uint32_t index_position = idx % RPB;

        if(i2==NullBlockReference){
            i2=soAllocDataBlock();
            pinode-> blkcnt = pinode-> blkcnt + 1; 
            for (uint32_t i = 0; i < RPB; i++) {
                ref[i] = NullBlockReference;
            }
        }else{
            soReadDataBlock(i2, ref);
        }
        allBlock =  grpAllocIndirectInodeBlock(ih, ref[index_block], index_position);
        soWriteDataBlock(i2, ref);
        soSaveInode(ih);
        return allBlock;
    }
#endif
};

