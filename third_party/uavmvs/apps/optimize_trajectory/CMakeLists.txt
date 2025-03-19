cmake_minimum_required(VERSION 3.10)
project(optimize_trajectory CUDA)

# Enable C++ language
enable_language(CXX)

# Set the CUDA compilation flags
set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} -Xcompiler")

# Add the 'optimize_trajectory' executable (using CUDA)
add_executable(optimize_trajectory optimize_trajectory.cu)

# Link with 'util', 'utp', 'eval', and OpenMP (gomp)
find_package(OpenMP REQUIRED)
target_compile_options(optimize_trajectory PRIVATE ${OpenMP_CXX_FLAGS})
target_link_libraries(optimize_trajectory PRIVATE utp eval gomp)
link_mve_libraries(optimize_trajectory)

# Make sure CUDA is available and correctly set up
if(NOT DEFINED CMAKE_CUDA_COMPILER)
    message(FATAL_ERROR "CUDA compiler (nvcc) is not found.")
endif()
