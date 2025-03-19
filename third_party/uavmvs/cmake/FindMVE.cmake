include(FindPackageHandleStandardArgs)

# Allow users to specify the MVE root directory manually
set(MVE_ROOT "" CACHE PATH "Root directory of MVE")

# If not provided, check common locations
if(NOT MVE_ROOT OR MVE_ROOT STREQUAL "")
    set(POSSIBLE_PATHS "${CMAKE_SOURCE_DIR}/../../../mve" "${CMAKE_SOURCE_DIR}/../../mve")
    foreach(POSSIBLE_PATH ${POSSIBLE_PATHS})
        if(EXISTS "${POSSIBLE_PATH}/libs")
            set(MVE_ROOT ${POSSIBLE_PATH})
            break()
        endif()
    endforeach()
endif()

if(NOT EXISTS "${MVE_ROOT}/libs")
    message(FATAL_ERROR "Could not find MVE. Please specify with -DMVE_ROOT=<path>")
    else()
    message(STATUS "Found MVE in ${MVE_ROOT}")
endif()


# Include directories
set(MVE_INCLUDE_DIRS ${MVE_ROOT}/libs)

# Link directories
set(MVE_LIB_DIRS ${MVE_ROOT}/mve_libs)
set(MVE_LIBS mve mve_dmrecon mve_fssr mve_ogl mve_sfm mve_util jpeg png tiff)

function(link_MVE_libraries target_name)
    target_include_directories(${target_name} PUBLIC ${MVE_INCLUDE_DIRS})
    target_link_directories(${target_name} PUBLIC ${MVE_LIB_DIRS})
    target_link_libraries(${target_name} PUBLIC ${MVE_LIBS})
endfunction()

find_package_handle_standard_args(MVE DEFAULT_MSG MVE_INCLUDE_DIRS MVE_LIB_DIRS)
