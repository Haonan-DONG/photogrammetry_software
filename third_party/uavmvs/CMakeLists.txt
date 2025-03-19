project(mission_planning)

cmake_minimum_required(VERSION 3.10)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Build configurations
set(CMAKE_CONFIGURATION_TYPES "Debug;Release;Profile" CACHE STRING "Build types" FORCE)

# Set output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

# Root definition
add_definitions(-D__ROOT__="${CMAKE_SOURCE_DIR}")

# Pthread linking for Linux
if(UNIX AND NOT CMAKE_CUDA_COMPILER)
    set(THREADS_PREFER_PTHREAD_FLAG ON)
    find_package(Threads REQUIRED)
    set(LINUX_LINK_FLAGS "-pthread")
endif()

# CUDA-specific settings
if(CMAKE_CUDA_COMPILER)
    set(CMAKE_CUDA_ARCHITECTURES 86)
endif()

# Define build types
set(CMAKE_CXX_FLAGS_RELEASE "-O3")
set(CMAKE_CXX_FLAGS_DEBUG "-g")

# Git submodule initialization
execute_process(COMMAND git submodule init WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})
execute_process(COMMAND git submodule update WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})

find_package(MVE)
find_package(MVST)

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/libs
    ${MVE_INCLUDE_DIRS}
    )


# Add external libraries
add_subdirectory(libs/fmt)
add_subdirectory(libs/sim)
add_subdirectory(libs/utp)
add_subdirectory(libs/eval)

# # Add applications
add_subdirectory(apps/template)
add_subdirectory(apps/testing)

add_subdirectory(apps/mesh_utils)
add_subdirectory(apps/mesh_tools)
# add_subdirectory(apps/image_tools)
# add_subdirectory(apps/scene_tools)
# add_subdirectory(apps/cloud_tools)
# add_subdirectory(apps/volume_tools)
add_subdirectory(apps/trajectory_tools)
add_subdirectory(apps/generate_proxy_mesh)
add_subdirectory(apps/generate_proxy_cloud)
add_subdirectory(apps/optimize_trajectory)
add_subdirectory(apps/evaluate_trajectory)


# add_subdirectory(apps/determine_matching_mask)
# add_subdirectory(apps/estimate_ground_plane)

# add_subdirectory(apps/generate_texture)
# add_subdirectory(apps/generate_gcp_bundle)

# add_subdirectory(apps/generate_guidance_volume)
# add_subdirectory(apps/generate_initial_trajectory)

# add_subdirectory(apps/selector)
# add_subdirectory(apps/simulator)
# add_subdirectory(apps/visualizer)

# add_subdirectory(apps/plan_trajectory)
# add_subdirectory(apps/capture_trajectory)
# add_subdirectory(apps/evaluate_heuristic)
# add_subdirectory(apps/evaluate_reconstruction)
# add_subdirectory(apps/evaluate_ground_sampling)
# add_subdirectory(apps/estimate_capture_difficulty)