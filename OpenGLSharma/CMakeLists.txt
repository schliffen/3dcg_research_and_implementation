

set(LIBS GL GLU glut )
set(SOILLIB /home/ek/install/soil/build/lib)
find_package(OpenGL REQUIRED )
find_package(OpenCV REQUIRED )
#find_package(SDL2 REQUIRED)

include_directories(${OpenCV_INCLUDE_DIR})
include_directories(${OpenGL_INCLUDE_DIR})
#opengl math lib
include_directories( /home/ek/install/glm-master )
include_directories(  /home/ek/install/soil/build/include/ )

link_directories(${OpenCV_LIBRARY_DIR})
link_directories(${OpenGL_LIBRARY_DIR})
link_directories(SOILLIB)


add_executable( ${PROJECT_NAME}  main.cpp
        libs.h
        Display.cpp Display.h)


target_link_libraries(${PROJECT_NAME} ${LIBS})
target_link_libraries( ${PROJECT_NAME} ${OpenCV_LIBS} )
target_link_libraries(${PROJECT_NAME} )
target_link_libraries(${PROJECT_NAME} PRIVATE ${libSOIL})
