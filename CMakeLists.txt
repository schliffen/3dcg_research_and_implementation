cmake_minimum_required(VERSION 3.17)
project(3dcg_research_and_implementation)

set(CMAKE_CXX_STANDARD 14)
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
set(LIBS  GL GLU glut  )



add_executable(3dcg_research_and_implementation main.cpp)
# Define the link libraries
target_link_libraries(${PROJECT_NAME} ${LIBS})

