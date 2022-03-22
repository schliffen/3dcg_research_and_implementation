cmake_minimum_required(VERSION 3.17)
project(3dcg_research_and_implementation)

set(CMAKE_CXX_STANDARD 17)

#OpenCV
find_package(OpenCV REQUIRED)
# OpenGL
find_package(OpenGL REQUIRED)

# GLM
#find_package(GLM REQUIRED)
#message(STATUS "GLM included at ${GLM_INCLUDE_DIR}")

# GLFW
#find_package(GLFW3 REQUIRED)
#message(STATUS "Found GLFW3 in ${GLFW3_INCLUDE_DIR}")

# ASSIMP
#find_package(ASSIMP REQUIRED)
# Put all libraries into a variable
#set(LIBS glfw3 opengl32 assimp STB_IMAGE GLAD)
#set(LIBS  GL GLU glut  )

include_directories(${OpenCV_INCLUDE_DIR})
include_directories(${OpenGL_INCLUDE_DIR})

#link_directories(${OpenCV_LIBRARY_DIR})
#link_directories(${OpenGL_LIBRARY_DIR})

include_directories(${PROJECT_SOURCE_DIR}/src_v1)
add_subdirectory(src_v1)

# add shared library

#add_library( arlib
#        SHARED
#        src_v1/ARDrawingContext.cpp
#        src_v1/ARDrawingContext.hpp
#        src_v1/ARPipeline.cpp
#        src_v1/ARPipeline.hpp
#        src_v1/CameraCalibration.cpp
#        src_v1/CameraCalibration.hpp
#        src_v1/GeometryTypes.cpp
#        src_v1/GeometryTypes.hpp
#        src_v1/PatternDetector.cpp
#        src_v1/PatternDetector.hpp
#        src_v1/Pattern.cpp
#        src_v1/Pattern.hpp
#        src_v1/DebugHelpers.hpp
#        )




#add_executable(3dcg_research_and_implementation main.cpp)
# Define the link libraries
#target_link_libraries(${PROJECT_NAME} ${OpenGL_LIBS} GL GLU glut)
#target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})
#target_link_libraries(${PROJECT_NAME} arlib)
