set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_ROOT_DIR}/lib/grp)

add_library(grp_freedatablocks STATIC
    grp_alloc_datablock.cpp
    grp_free_datablock.cpp
    grp_replenish_from_cache.cpp
    grp_replenish_from_bitmap.cpp
    grp_deplete.cpp
)

