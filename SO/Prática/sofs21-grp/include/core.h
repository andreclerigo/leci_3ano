/**
 *  \file
 *  \brief aggregation of core header files
 *
 *  \author Artur Pereira - 2016-2020
 */

#ifndef __SOFS21_CORE__
#define __SOFS21_CORE__

/** \defgroup core core
 *  \brief Core constants and core data types
 */

/** 
 * \defgroup superblock superblock
 * \ingroup core
 * \brief The \c SOSuperblock data type
 *
 * \defgroup inode inode
 * \ingroup core
 * \brief The \c SOInode data type
 *
 * \defgroup dirslot dirslot
 * \ingroup core
 * \brief The \c SODirentry data type
 *
 * \defgroup exception exception
 * \ingroup core
 * \brief \c The sofs21 exception data type
 */

#include "constants.h"
#include "exception.h"
#include "superblock.h"
#include "inode.h"
#include "dirslot.h"

#endif /* __SOFS21_CORE__ */
