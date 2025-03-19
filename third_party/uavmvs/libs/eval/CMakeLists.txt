cmake_minimum_required(VERSION 3.10)
project(eval LANGUAGES CXX CUDA)

add_library(eval STATIC
    kernels.cu
    ../cacc/kd_tree.cu
    ../cacc/bvh_tree.cu
)

# Set C++ and CUDA standards
set_target_properties(eval PROPERTIES CXX_STANDARD 11 CXX_STANDARD_REQUIRED YES)
set_target_properties(eval PROPERTIES CUDA_STANDARD 11 CUDA_STANDARD_REQUIRED YES)

# Set CUDA architecture
set(CMAKE_CUDA_ARCHITECTURES 86)