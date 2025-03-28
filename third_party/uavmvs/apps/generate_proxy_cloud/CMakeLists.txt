cmake_minimum_required(VERSION 3.10)
project(generate_proxy_cloud)

# Set the language to C++
enable_language(CXX)

add_executable(generate_proxy_cloud generate_proxy_cloud.cpp)

find_package(OpenMP REQUIRED)
target_compile_options(generate_proxy_cloud PRIVATE ${OpenMP_CXX_FLAGS})

target_link_libraries(generate_proxy_cloud PRIVATE gomp)
link_mve_libraries(generate_proxy_cloud)