set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_ROOT_DIR}/lib/grp)

add_library(grp_mksofs STATIC
    grp_mksofs_CS.cpp
    grp_mksofs_FSB.cpp
    grp_mksofs_FIT.cpp
    grp_mksofs_FRD.cpp
    grp_mksofs_FBT.cpp
    grp_mksofs_ZDB.cpp
)

