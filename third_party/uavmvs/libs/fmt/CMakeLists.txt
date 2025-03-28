cmake_minimum_required(VERSION 3.10)
project(fmt LANGUAGES CXX)

add_library(fmt STATIC
    format.cc
    ostream.cc
    posix.cc
)

# Set C++ standard
set_target_properties(fmt PROPERTIES CXX_STANDARD 11 CXX_STANDARD_REQUIRED YES)
