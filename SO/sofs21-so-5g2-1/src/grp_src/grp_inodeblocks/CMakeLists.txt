set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_ROOT_DIR}/lib/grp)

add_library(grp_inodeblocks STATIC
        grp_alloc_inodeblock.cpp
        grp_free_inodeblocks.cpp
        grp_get_inodeblock.cpp
        grp_read_inodeblock.cpp
        grp_write_inodeblock.cpp
        grp_new_inode.cpp
        grp_remove_inode.cpp
)

