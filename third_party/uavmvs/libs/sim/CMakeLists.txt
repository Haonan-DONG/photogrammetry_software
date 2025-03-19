cmake_minimum_required(VERSION 3.10)
project(sim LANGUAGES CXX)

add_library(sim STATIC
    window.cpp
    model.cpp
)

# Set C++ standard
set_target_properties(sim PROPERTIES CXX_STANDARD 11 CXX_STANDARD_REQUIRED YES)

# Link against OpenGL and GLFW
find_package(OpenGL REQUIRED)
find_package(glfw3 REQUIRED)

target_link_libraries(sim PUBLIC OpenGL::GL glfw)
