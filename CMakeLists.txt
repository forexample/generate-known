cmake_minimum_required(VERSION 2.8.11)
project(GenerateSources)

find_package(PythonInterp 3.2 REQUIRED)

set(gen_dir "${PROJECT_BINARY_DIR}/generated")

add_custom_command(
    OUTPUT "${gen_dir}/A.cpp" "${gen_dir}/B.cpp" "${gen_dir}/C.cpp"
    COMMAND
        "${PYTHON_EXECUTABLE}"
        "${CMAKE_CURRENT_LIST_DIR}/script.py"
        --dir "${gen_dir}"
        --smart
        --check-changes
    DEPENDS "${CMAKE_CURRENT_LIST_DIR}/script.py"
    COMMENT "Generate (custom command)"
)

add_custom_target(
    Generated
    DEPENDS "${gen_dir}/A.cpp" "${gen_dir}/B.cpp" "${gen_dir}/C.cpp"
    COMMENT "Generate (target)"
)

add_library(A "${gen_dir}/A.cpp")
add_library(B "${gen_dir}/B.cpp")
add_library(C "${gen_dir}/C.cpp")

add_dependencies(A Generated)
add_dependencies(B Generated)
add_dependencies(C Generated)

add_executable(foo main.cpp)
target_link_libraries(foo A B C)

enable_testing()
add_test(NAME RunFoo COMMAND foo)
