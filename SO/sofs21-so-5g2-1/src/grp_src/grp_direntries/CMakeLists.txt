set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_ROOT_DIR}/lib/grp)

add_library(grp_direntries STATIC
        grp_check_dir_empty.cpp
        grp_get_direntry.cpp
        grp_delete_direntry.cpp
        grp_rename_direntry.cpp
        grp_add_direntry.cpp
        grp_traverse_path.cpp
)

