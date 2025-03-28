cmake_minimum_required(VERSION 3.10)
project(mesh_utils)

# Set the language to C++
enable_language(CXX)

# Add the source file for the first project
add_executable(generate_sphere_mesh generate_sphere_mesh.cpp)
link_mve_libraries(generate_sphere_mesh)

# Add the source file for the second project
add_executable(generate_aabb_mesh generate_aabb_mesh.cpp)
link_mve_libraries(generate_aabb_mesh)