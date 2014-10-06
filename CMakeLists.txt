cmake_minimum_required(VERSION 2.8.11)
project(GenerateSources)

find_package(PythonInterp 3.2 REQUIRED)

set(gen_dir "${PROJECT_BINARY_DIR}/generated")

add_custom_command(
    OUTPUT "${gen_dir}/A.cpp"
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
    Generate
    DEPENDS "${gen_dir}/A.cpp"
    COMMENT "Generate (custom target)"
)

add_subdirectory(A)

add_executable(foo main.cpp)
target_link_libraries(foo A)

enable_testing()
add_test(NAME RunFoo COMMAND foo)
