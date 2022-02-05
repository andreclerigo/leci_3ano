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

#include <inttypes.h>
#include <errno.h>
#include <assert.h>

#define CHANGED 0x1
#define NOT_EMPTY 0x2

namespace sofs21
{
    /* free all blocks between positions idx and RPB - 1
     * existing in the block of references passed as argument.
     * The return value has the following meaning:
     * - bit CHANGED is raised if the block of references changed
     * - bit NOT_EMPTY is raised if the block of references contains non NullBlockReference references
     */
    static uint32_t grpFreeIndirectInodeBlocks(int ih, uint32_t *ref, uint32_t idx);

    /* free all blocks between positions idx and RPB*RPB - 1
     * covered by the block of indirect references passed as argument.
     * The return value has the following meaning:
     * - bit CHANGED is raised if the block of indirect references changed
     * - bit NOT_EMPTY is raised if the block of indirect references contains non NullBlockReference references
     */
    static uint32_t grpFreeDoubleIndirectInodeBlocks(int ih, uint32_t *iref, uint32_t idx);

    /* ********************************************************* */

    void grpFreeInodeBlocks(int ih, uint32_t fibn)
    {
        soProbe(303, "%s(%d, %u)\n", __FUNCTION__, ih, fibn);

        /* replace this comment and following line with your code */
        // binFreeInodeBlocks(ih, fibn);

        SOInode *inode = soGetInodePointer(ih);     // get inode pointer
        uint16_t ic = 0x0;      // Flag to check if inode d[N_DIRECT], i1 or i2 has changed

        // free blocks in d_direct
        for(uint32_t ibn = fibn; ibn < N_DIRECT; ibn++) {
            if(inode->d[ibn] != NullBlockReference){
                soFreeDataBlock(inode->d[ibn]); // free block
                inode->d[ibn] = NullBlockReference;
                inode->blkcnt--;
                ic = CHANGED;
            }
        }

        uint32_t ref[RPB];
        uint16_t res;

        if(inode->i1 != NullBlockReference && fibn < N_DIRECT + RPB) {
            soReadDataBlock(inode->i1, ref);
 
            if(fibn > N_DIRECT) res = grpFreeIndirectInodeBlocks(ih,ref,fibn-N_DIRECT);
            else res = grpFreeIndirectInodeBlocks(ih,ref,0);

            if( (res&CHANGED) == CHANGED) soWriteDataBlock(inode->i1,ref); // Save data block if references changed
            if( (res&NOT_EMPTY) == 0x0) {
                soFreeDataBlock(inode->i1);        // Free i1 if is empty
                inode->i1 = NullBlockReference;
                inode->blkcnt--;
                ic = CHANGED;
            }
        }

        if(inode->i2 != NullBlockReference && fibn < N_DIRECT + RPB * RPB) {
            soReadDataBlock(inode->i2, ref);

            if(fibn > N_DIRECT + RPB) res = grpFreeDoubleIndirectInodeBlocks(ih,ref,fibn-N_DIRECT-RPB);
            else res = grpFreeDoubleIndirectInodeBlocks(ih,ref,0);

            if( (res&CHANGED) == CHANGED) soWriteDataBlock(inode->i2,ref); // Save data block if references changed
            if( (res&NOT_EMPTY) == 0x0){
                soFreeDataBlock(inode->i2);        // Free i2 if is empty
                inode->i2 = NullBlockReference;
                inode->blkcnt--;
                ic = CHANGED;
            }
        }

        if((ic&CHANGED) == CHANGED) soSaveInode(ih);    // Save inode if d[N_DIRECT], i1 or i2 has changed
    }

    /* ********************************************************* */

    static uint32_t grpFreeIndirectInodeBlocks(int ih, uint32_t *ref, uint32_t idx)
    {
        soProbe(303, "%s(%d, %p, %u)\n", __FUNCTION__, ih, ref, idx);

        /* replace this comment and following line with your code */
        // throw SOException(ENOSYS, __FUNCTION__); 

        SOInode *inode = soGetInodePointer(ih);     // get inode pointer
        uint16_t res = 0x0;                         // return value

        // Check if block of references contains non NullBlockReference references
        for(uint32_t i = 0; i < idx; i++) {
            if(ref[i] != NullBlockReference){
                res |= NOT_EMPTY;
                break;
            }
        }

        // free all blocks between positions idx and RPB - 1
        for(uint32_t i = idx; i < RPB; i++) {
            if(ref[i] != NullBlockReference){
                soFreeDataBlock(ref[i]);
                ref[i] = NullBlockReference;
                inode->blkcnt--;
                res |= CHANGED;
            }
        }

        return res;
    }

    /* ********************************************************* */

    static uint32_t grpFreeDoubleIndirectInodeBlocks(int ih, uint32_t *iref, uint32_t idx)
    {
        soProbe(303, "%s(%d, %p, %u)\n", __FUNCTION__, ih, iref, idx);

        /* replace this comment and following line with your code */
        // throw SOException(ENOSYS, __FUNCTION__);

        SOInode *inode = soGetInodePointer(ih);     // get inode pointer
        uint16_t res = 0x0;                         // return value
        uint32_t ref[RPB];

        for(uint32_t i = 0; i < RPB; i++) {
            if(iref[i] == NullBlockReference) continue; // jump through holes
            if(i*RPB < idx) res |= NOT_EMPTY;   // Check if references are not empty before idx
            
            uint16_t r = 0x0;

            // Free Indirect Inode Blocks
            if(idx - RPB*i < RPB || idx < RPB*i) {
                soReadDataBlock(iref[i], ref);
                if(idx > RPB * i) r = grpFreeIndirectInodeBlocks(ih,ref,idx - RPB*i);
                else r = grpFreeIndirectInodeBlocks(ih,ref,0);

                if( (r&CHANGED) == CHANGED ) soWriteDataBlock(iref[i],ref); // Save data block if references changed
                if( (r&NOT_EMPTY) == 0x0) {
                    soFreeDataBlock(iref[i]);        // Free iref[i] if is empty
                    iref[i] = NullBlockReference;
                    inode->blkcnt--;
                    res |= CHANGED;
                }
            }
        }

        return res;
    }

    /* ********************************************************* */
};

