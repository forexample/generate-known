cmake_minimum_required(VERSION 2.8.11)
project(GenerateSources)

find_package(PythonInterp 3.2 REQUIRED)

set(gen_dir "${PROJECT_BINARY_DIR}/generated")
set(gen_src "${gen_dir}/A.cpp")

add_custom_command(
    OUTPUT ${gen_src}
    COMMAND
        "${PYTHON_EXECUTABLE}"
        "${CMAKE_CURRENT_LIST_DIR}/script.py"
        --dir "${gen_dir}"
    DEPENDS "${CMAKE_CURRENT_LIST_DIR}/script.py"
    COMMENT "Generate (custom command)"
)

add_library(A "${gen_dir}/A.cpp")

add_executable(foo main.cpp)
target_link_libraries(foo A)

enable_testing()
add_test(NAME RunFoo COMMAND foo)
