
/*
 *  \author Artur Pereira - 2007-2009, 2016-2020
 *  \author Miguel Oliveira e Silva - 2009, 2017
 *  \author António Rui Borges - 2010-2012
 */

#define  __STDC_FORMAT_MACROS
#include <inttypes.h>
#include <stdio.h>
#include <stdbool.h>
#include <time.h>
#include <sys/stat.h>
#include <string.h>
#include <stdlib.h>

#include <iostream>

#include "core.h"
#include "devtools.h"

namespace sofs21
{

    /* ********************************************************* */

    void printBlockAsHex(void *buf, uint32_t off)
    {
        /* cast buf to appropriate type */
        unsigned char *byte = (unsigned char *)buf;

        /* print cluster */
        for (uint32_t i = 0; i < BlockSize; i++)
        {
            if ((i & 0x1f) == 0)
                printf("%4.4x:", i + off);
            /* print byte */
            printf(" %.2x", byte[i]);
            /* terminate present line, if required */
            if ((i & 0x1f) == 0x1f)
                printf("\n");
        }
    }

    /* ********************************************************* */

    void printBlockAsAscii(void *buf, uint32_t off)
    {
        /* cast buf to appropriate type */
        unsigned char *c = (unsigned char *)buf;

        /* print cluster */
        char line[256];         /* line to be printed */
        char *p_line = line;    /* pointer to a character in the line */
        for (uint32_t i = 0; i < BlockSize; i++)
        {
            if ((i & 0x1f) == 0)
            {
                printf("%4.4d:", i + off);
                p_line = line;
            }
            /* add character to the line */
            switch (c[i])
            {
                case '\a':
                    p_line += sprintf(p_line, " \\a");
                    break;
                case '\b':
                    p_line += sprintf(p_line, " \\b");
                    break;
                case '\f':
                    p_line += sprintf(p_line, " \\f");
                    break;
                case '\n':
                    p_line += sprintf(p_line, " \\n");
                    break;
                case '\r':
                    p_line += sprintf(p_line, " \\r");
                    break;
                case '\t':
                    p_line += sprintf(p_line, " \\t");
                    break;
                case '\v':
                    p_line += sprintf(p_line, " \\v");
                    break;
                default:
                    if ((c[i] >= ' ') && (c[i] != 0x7F) && (c[i] != 0x8F))
                        p_line += sprintf(p_line, " %c ", c[i]);
                    else
                        p_line += sprintf(p_line, " %.2x", c[i]);
            }
            /* terminate and print present line, if required */
            if ((i & 0x1f) == 0x1f)
            {
                *p_line = '\0';
                printf("%s\n", line);
            }
        }
    }

    /* ********************************************************* */

    void printSuperblock(void *buf)
    {
        /* cast buf to appropriate type */
        SOSuperblock *sbp = (SOSuperblock *) buf;

        /* header */
        printf("Header:\n");
        printf("  Magic number: 0x%04x\n", sbp->magic);
        printf("  Version number: 0x%02x\n", sbp->version);
        printf("  Volume name: \"%-s\"\n", sbp->name);
        printf("  Properly unmounted: %s\n", (sbp->mntstat >= 0) ? "yes" : "no");
        printf("  Number of mounts: %u\n", abs(sbp->mntstat));
        printf("  Total number of blocks in the device: %u\n", sbp->ntotal);
        //printf("\n");

        /* ----------------------------------------------------- */

        /* inodes' metadata */
        printf("Inodes' metadata:\n");
        printf("  Total number of inodes: %u\n", sbp->itotal);
        printf("  Number of free inodes: %u\n", sbp->ifree);
        printf("  Inode search index: %u\n", sbp->iidx);
        printf("  Inode allocation bitmap:\n");
        for (uint32_t i = 0; i < MAX_INODES/32; i++)
        {
            if ((i % 10) == 0)
                printf("    %08x", sbp->ibitmap[i]);
            else if ((i % 10) == 9)
                printf(" %08x\n", sbp->ibitmap[i]);
            else
                printf(" %08x", sbp->ibitmap[i]);
        }
        printf("Inode deleted queue:\n");
        printf("  Inode deleted queue head: %u\n", sbp->iqhead);
        printf("  Inode deleted queue count: %u\n", sbp->iqcount);
        printf("  Queue contents:");
        for (int i = 0; i < DELETED_QUEUE_SIZE; i++)
        {
            if ((i % 10) == 0)
                printf("\n    ");
            if (sbp->iqueue[i] == NullInodeReference)
                printf(" (nil)");
            else
                printf(" %5u", sbp->iqueue[i]);
        }
        printf("\n");

        /* ----------------------------------------------------- */

        /* blocks' metadata */
        printf("Data blocks' metadata:\n");
        printf("  First block of the data block pool: %u\n", sbp->dbp_start);
        printf("  Total number of data blocks: %u\n", sbp->dbtotal);
        printf("  Number of free data blocks: %u\n", sbp->dbfree);

        printf("Reference bitmap's metadata:\n");
        printf("  First block of the bitmap table: %u\n", sbp->rbm_start);
        printf("  Number of blocks of the bitmap table: %u\n", sbp->rbm_size);
        printf("  Index of first 32-word to retrieve references: ");
        if (sbp->rbm_idx == NullBlockReference)
            printf("(nil)\n");
        else
            printf("%u\n", sbp->rbm_idx);

        /* ----------------------------------------------------- */

        /* Retrieval cache' contents */
        printf("Retrieval cache:\n");
        printf("  Index of the first occupied cache position: ");
        if (sbp->retrieval_cache.idx == REF_CACHE_SIZE)
            printf("%u\n", sbp->retrieval_cache.idx);
        else
            printf("%u\n", sbp->retrieval_cache.idx);
        printf("  Cache contents:");
        for (uint32_t i = 0; i < REF_CACHE_SIZE; i++)
        {
            if ((i % 10) == 0)
                printf("\n    ");
            if (sbp->retrieval_cache.ref[i] == NullBlockReference)
                printf(" (nil)");
            else
                printf(" %5u", sbp->retrieval_cache.ref[i]);
        }
        printf("\n");

        printf("Insertion cache:\n");
        printf("  Index of the first empty cache position: ");
        if (sbp->insertion_cache.idx == REF_CACHE_SIZE)
            printf("%u\n", sbp->insertion_cache.idx);
        else
            printf("%u\n", sbp->insertion_cache.idx);
        printf("  Cache contents:");
        for (uint32_t i = 0; i < REF_CACHE_SIZE; i++)
        {
            if ((i % 10) == 0)
                printf("\n    ");
            if (sbp->insertion_cache.ref[i] == NullBlockReference)
                printf(" (nil)");
            else
                printf(" %u", sbp->insertion_cache.ref[i]);
        }
        printf("\n");

        /* ----------------------------------------------------- */

    }

    /* ********************************************************* */

    /* \brief Bit pattern description of the mode field in the inode data type */
    static const char *inodetypes[] = {
        "free",
        "INVALID_0x1",
        "INVALID-0x2",
        "INVALID_0x3",
        "directory",
        "deleted symlink",
        "INVALID-0x6",
        "deleted reg file",
        "regular file",
        "INVALID_0x9",
        "symlink",
        "deleted directory",
        "INVALID-0xc",
        "INVALID-0xd",
        "INVALID-0xe",
        "INVALID-0xf"
    };

    static void printInode(void *buf, uint16_t in, bool showtimes = true)
    {
        SOInode *ip = (SOInode *) buf;

        /* print inode number */
        printf("Inode #");
        if (in == NullInodeReference)
            printf("(nil)\n");
        else
            printf("%u\n", in);

        /* decouple and print mode field */
        uint32_t typebits = (ip->mode & S_IFMT) >> 12;

        printf("type = %s, ", inodetypes[typebits]);
        uint32_t permbits = ip->mode & (S_IRWXU | S_IRWXG | S_IRWXO);
        char perm[10] = "rwxrwxrwx";    /* access permissions array */
        for (int i = 0; i < 9; i++)
        {
            if ((permbits % 2) == 0)    // LSB is zero ?
            {
                perm[8 - i] = '-';
            }
            permbits >>= 1;
        }
        printf("permissions = %s, ", perm);

        /* print reference count */
        printf("lnkcnt = %" PRIu16 ", ", ip->lnkcnt);

        /* print owner and group IDs */
        printf("owner = %u, group = %u\n", ip->owner, ip->group);

        /* print file size in bytes and in clusters */
        printf("size in bytes = %u, block count = %u\n", ip->size, ip->blkcnt);

        if (showtimes)
        {
            char timebuf[30];
            time_t t = ip->atime;
            ctime_r(&t, timebuf);
            timebuf[strlen(timebuf) - 1] = '\0';
            printf("atime = %s, ", timebuf);
            t = ip->mtime;
            ctime_r(&t, timebuf);
            timebuf[strlen(timebuf) - 1] = '\0';
            printf("mtime = %s, ", timebuf);
            t = ip->ctime;
            ctime_r(&t, timebuf);
            timebuf[strlen(timebuf) - 1] = '\0';
            printf("ctime = %s\n", timebuf);
        }

        /* print direct references */
        printf(" d[*] = {");
        for (int i = 0; i < N_DIRECT; i++)
        {
            if (i > 0)
                printf(" ");
            if (ip->d[i] == NullBlockReference)
                printf("(nil)");
            else
                printf("%" PRIu32 "", ip->d[i]);
        }
        printf("}");

        /* print single indirect references */
        printf(", i1 = ");
        if (ip->i1 == NullBlockReference)
            printf("(nil)");
        else
            printf("%" PRIu32 "", ip->i1);

        /* print double indirect reference */
        printf(", i2 = ");
        if (ip->i2 == NullBlockReference)
            printf("(nil)");
        else
            printf("%" PRIu32 "", ip->i2);
        printf("\n");

        printf("----------------\n");
    }

    /* ********************************************************* */

    void printBlockOfInodes(void *buf, uint32_t off, bool showtimes)
    {
        /* cast buf to appropriate type */
        SOInode *inode = (SOInode *) buf;

        /* treat each inode stored in the block separately */
        for (uint32_t i = 0; i < IPB; i++)
            printInode(&inode[i], i + off, showtimes);
    }

    /* ********************************************************* */

    void printBlockOfDirectorySlots(void *buf, uint32_t off)
    {
        /* get dir-slots per cluster */
        uint32_t dpb = BlockSize / sizeof (SODirectorySlot);

        /* cast buf to appropriate type */
        SODirectorySlot *dir = (SODirectorySlot *) buf;

        /* print */
        char s[DIRECTORY_SLOT+1];
        s[DIRECTORY_SLOT] = '\0';
        for (uint32_t i = 0; i < dpb; i++)
        {
            memset(s, 0x0, DIRECTORY_SLOT);
            strncpy(s, dir[i].nameBuffer, DIRECTORY_SLOT);
            printf("%-*.*s ", DIRECTORY_SLOT+1, DIRECTORY_SLOT+1, s);
            if (dir[i].in == NullInodeReference)
                printf("(nil)\n");
            else if (s[DIRECTORY_SLOT-1] != '\0') // extended inode
                printf(" --> \n");
            else
                printf("%.10" PRIu32 "\n", dir[i].in);
        }
    }

    /* ********************************************************* */

    void printBlockOfRefs(void *buf, uint32_t off)
    {
        /* get refs per block */
        uint32_t rpb = BlockSize / sizeof (uint32_t);

        /* cast buf to appropriate type */
        uint32_t *ref = (uint32_t *) buf;

        for (uint32_t i = 0; i < rpb; i++)
        {
            if ((i & 0x07) == 0)
                printf("%4.4d:", i + off);
            /* print reference to a cluster */
            if (ref[i] == NullBlockReference)
                printf("   (nil)   ");
            else
                printf(" %.10" PRIu32, ref[i]);
            /* terminate present line, if required */
            if (((i & 0x07) == 0x07) || (i == (rpb - 1)))
                printf("\n");
        }
    }

    /* ********************************************************* */

    void printBlockOfBitmap(void *buf, uint32_t off)
    {
        /* get refs per block */
        uint32_t rpb = BlockSize / sizeof (uint32_t);

        /* cast buf to appropriate type */
        uint32_t *ref = (uint32_t *) buf;

        for (uint32_t i = 0; i < rpb; i++)
        {
            if ((i & 0x07) == 0)
                printf("%4.4d:", i + off);
            /* print reference to a cluster */
            printf(" %08x", ref[i]);
            /* terminate present line, if required */
            if (((i & 0x07) == 0x07) || (i == (rpb - 1)))
                printf("\n");
        }
    }

    /* ********************************************************* */

};
