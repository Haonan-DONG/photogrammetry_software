cmake_minimum_required(VERSION 3.10)
project(interop LANGUAGES CXX CUDA)

# Set the C++ and CUDA compilers
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CUDA_STANDARD 11)

# Add the source files
set(SOURCE_FILES
    interop.cu
    ../../libs/cacc/bvh_tree.cu
)

# Create the executable
add_executable(interop ${SOURCE_FILES})
use_mve_util(interop)
use_mve_ogl(interop)

# Add compiler options for nvcc
target_compile_options(interop PRIVATE -Xcompiler -fopenmp)


# Link libraries
target_link_libraries(interop PRIVATE
    gomp
    GL
    glfw
    sim
)
