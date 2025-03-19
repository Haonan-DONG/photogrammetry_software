cmake_minimum_required(VERSION 3.10)
project(mesh_tools)

# Set the language to C++
enable_language(CXX)

# Add the 'convert-mesh' executable
add_executable(convert-mesh convert.cpp)
link_mve_libraries(convert-mesh)

# Now for the 'normalize-mesh' project
add_executable(normalize-mesh normalize.cpp)
link_mve_libraries(normalize-mesh)

# Now for the 'colorize-mesh' project
add_executable(colorize-mesh colorize.cpp)
link_mve_libraries(colorize-mesh)

# Now for the 'estimate_transform-mesh' project
add_executable(estimate_transform-mesh estimate_transform.cpp)

# Add OpenMP flags for 'estimate_transform-mesh'
find_package(OpenMP REQUIRED)
target_compile_options(estimate_transform-mesh PRIVATE ${OpenMP_CXX_FLAGS})

# Link with 'gomp' and 'util'
target_link_libraries(estimate_transform-mesh PRIVATE gomp pthread)
link_mve_libraries(estimate_transform-mesh)