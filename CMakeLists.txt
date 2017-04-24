cmake_minimum_required(VERSION 2.8.9)
project(torus)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Prepare the build environment
include_directories(include)
include_directories(source)
include_directories(/usr/local/include)
link_directories(/usr/local/lib)

# Add your project files
FILE(GLOB SRCFILES *.cpp)
add_executable(${PROJECT_NAME} ${SRCFILES})
target_link_libraries(${PROJECT_NAME})
