cmake_minimum_required(VERSION 3.10)
project(template)

# Set the language to C++
enable_language(CXX)

# Add the source file
add_executable(template template.cpp)
link_mve_libraries(template)