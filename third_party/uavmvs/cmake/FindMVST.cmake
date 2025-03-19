include(FindPackageHandleStandardArgs)

# Allow users to specify the MVS-Texturing root directory manually
set(MVST_ROOT "" CACHE PATH "Root directory of MVS-Texturing")

# If not provided, check common locations
if(NOT MVST_ROOT OR MVST_ROOT STREQUAL "")
    set(POSSIBLE_PATHS "${CMAKE_SOURCE_DIR}/../../../mvs-texturing" "${CMAKE_SOURCE_DIR}/../../mvs-texturing")
    foreach(POSSIBLE_PATH ${POSSIBLE_PATHS})
        if(EXISTS "${POSSIBLE_PATH}/libs")
            set(MVST_ROOT ${POSSIBLE_PATH})
            break()
        endif()
    endforeach()
endif()

if(NOT EXISTS "${MVST_ROOT}/libs")
    message(FATAL_ERROR "Could not find MVS-Texturing. Please specify with -DMVST_ROOT=<path>")
endif()

# Include directories
set(MVST_INCLUDE_DIRS ${MVST_ROOT}/libs)

# Link directories
set(MVST_LIB_DIRS ${MVST_ROOT}/build/libs)

function(use_mvst target_name)
    target_include_directories(${target_name} PUBLIC ${MVST_INCLUDE_DIRS})
    target_link_directories(${target_name} PUBLIC ${MVST_LIB_DIRS})
    
    foreach(LIB_NAME ${ARGN})
        target_link_libraries(${target_name} PUBLIC ${LIB_NAME})
    endforeach()
    
    find_package(MVE REQUIRED)
    use_mve(${target_name})
endfunction()

find_package_handle_standard_args(MVST DEFAULT_MSG MVST_INCLUDE_DIRS MVST_LIB_DIRS)
