cmake_minimum_required(VERSION 3.10)
project(utp LANGUAGES CXX)

add_library(utp STATIC
    trajectory.cpp
    trajectory_io.cpp
)

# Set C++ standard
set_target_properties(utp PROPERTIES CXX_STANDARD 11 CXX_STANDARD_REQUIRED YES)

# Include Eigen3
include_directories(/usr/include/eigen3)