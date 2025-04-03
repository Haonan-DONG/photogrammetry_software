set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

find_package(PROJ REQUIRED)
if(PROJ_FOUND)
    message(STATUS "Found valid PROJ.")
else()
    message(FATAL "Not found valid PROJ")
endif()

find_package(Eigen3 REQUIRED)

include_directories(
    ${PROJ_INCLUDE_DIRS}
    ${EIGEN3_INCLUDE_DIRS}
)

add_executable(utm2wgs84 utm2wgs84_uavmvs.cpp)
target_link_libraries(utm2wgs84 ${PROJ_LIBRARIES})