

set(LIBS GL GLU glut )
find_package(OpenGL REQUIRED )
find_package(OpenCV REQUIRED )

include_directories(${OpenCV_INCLUDE_DIR})
include_directories(${OpenGL_INCLUDE_DIR})
#opengl math lib
include_directories( /home/ek/install/glm-master )

link_directories(${OpenCV_LIBRARY_DIR})
link_directories(${OpenGL_LIBRARY_DIR})

add_library( geometry
        SHARED
        geometryShape.cpp
        geometryShape.h
        )

add_executable( ${PROJECT_NAME}
        main.cpp

)


target_link_libraries(${PROJECT_NAME} ${LIBS})
target_link_libraries( ${PROJECT_NAME} ${OpenCV_LIBS} )
#install (TARGETS ARProject DESTINATION bin)
