cmake_minimum_required(VERSION 3.10)
project(generate_proxy_mesh)

# Set the language to C++
enable_language(CXX)

# Add the 'generate_proxy_mesh' executable
add_executable(generate_proxy_mesh generate_proxy_mesh.cpp)

# Add OpenMP flags for 'generate_proxy_mesh'
find_package(OpenMP REQUIRED)
target_compile_options(generate_proxy_mesh PRIVATE ${OpenMP_CXX_FLAGS})

target_link_libraries(generate_proxy_mesh PRIVATE fmt gomp pthread)
link_mve_libraries(generate_proxy_mesh)