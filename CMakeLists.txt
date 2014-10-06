cmake_minimum_required(VERSION 2.8.11)
project(GenerateSources)

find_package(PythonInterp 3.2 REQUIRED)

set(gen_dir "${PROJECT_BINARY_DIR}/generated")

add_custom_command(
    OUTPUT "${gen_dir}/A1.cpp" "${gen_dir}/A2.cpp"
    COMMAND
        "${PYTHON_EXECUTABLE}"
        "${CMAKE_CURRENT_LIST_DIR}/script.py"
        --dir "${gen_dir}"
        --smart
        --check-changes
    DEPENDS "${CMAKE_CURRENT_LIST_DIR}/script.py"
    COMMENT "Generate (custom command)"
)

add_library(A "${gen_dir}/A1.cpp" "${gen_dir}/A2.cpp")

add_executable(foo main.cpp)
target_link_libraries(foo A)

enable_testing()
add_test(NAME RunFoo COMMAND foo)
