cmake_minimum_required(VERSION 3.10)
project(egl_probe)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

find_package(PythonInterp REQUIRED)
find_package(PythonLibs REQUIRED)

include_directories(${PYTHON_INCLUDE_DIRS})
# Add potential header locations
include_directories(.)
include_directories(egl_probe)
include_directories(glad)
include_directories(egl_probe/glad)

# RECURSIVE SEARCH: Find any .cpp file anywhere in the directory tree
file(GLOB_RECURSE SOURCES "*.cpp")

# Debugging: Print exactly what files were found
message(STATUS "DETECTED SOURCES: ${SOURCES}")

add_library(egl_probe SHARED ${SOURCES})

target_link_libraries(egl_probe ${PYTHON_LIBRARIES})
if(UNIX)
    target_link_libraries(egl_probe dl)
endif()

set_target_properties(egl_probe PROPERTIES PREFIX "")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/egl_probe)
