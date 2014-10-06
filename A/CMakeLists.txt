set_source_files_properties("${gen_dir}/A.cpp" PROPERTIES GENERATED YES)
add_library(A "${gen_dir}/A.cpp")
add_dependencies(A Generate)
