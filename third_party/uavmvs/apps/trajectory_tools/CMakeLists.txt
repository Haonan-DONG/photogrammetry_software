cmake_minimum_required(VERSION 3.10)
project(trajectory_tools)

# Set the language to C++
enable_language(CXX)

# Add the 'generate-trajectory' executable
add_executable(generate-trajectory generate.cpp)
link_mve_libraries(generate-trajectory)
target_link_libraries(generate-trajectory PRIVATE utp pthread)


# Now for the 'shorten-trajectory' project
add_executable(shorten-trajectory shorten.cpp)

# Add OpenMP flags for 'shorten-trajectory'
find_package(OpenMP REQUIRED)
target_compile_options(shorten-trajectory PRIVATE ${OpenMP_CXX_FLAGS})

target_link_libraries(shorten-trajectory PRIVATE gomp utp pthread)
link_mve_libraries(shorten-trajectory)


# Now for the 'interpolate-trajectory' project
add_executable(interpolate-trajectory interpolate.cpp)

# Set the system include directory for Eigen3
target_include_directories(interpolate-trajectory PRIVATE /usr/include/eigen3)

link_mve_libraries(interpolate-trajectory )
target_link_libraries(interpolate-trajectory  PRIVATE utp)


add_executable(evaluate-trajectory evaluate.cpp)

# Set the system include directory for Eigen3
target_include_directories(evaluate-trajectory PRIVATE /usr/include/eigen3)
link_mve_libraries(evaluate-trajectory)
target_link_libraries(evaluate-trajectory PRIVATE utp pthread)
