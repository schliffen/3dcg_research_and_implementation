

set(LIBS GL GLU glut )
find_package(OpenGL REQUIRED )
find_package(OpenCV REQUIRED )

include_directories(${OpenCV_INCLUDE_DIR})
include_directories(${OpenGL_INCLUDE_DIR})
#opengl math lib
include_directories( /home/ek/install/glm-master )

link_directories(${OpenCV_LIBRARY_DIR})
link_directories(${OpenGL_LIBRARY_DIR})

#add_library( game
#        SHARED
#        Game.cpp
#        Game.h
#        )

add_executable( ${PROJECT_NAME}
        main.cpp
        Game.cpp
        Game.h
        States/State.cpp
        States/State.h
        States/GameState.cpp
        States/GameState.h
        Entity/Entity.cpp
        Entity/Entity.h

        States/MainMenuState.cpp
        States/MainMenuState.h
        Resources/Button.cpp
        Resources/Button.h)


target_link_libraries(${PROJECT_NAME} ${LIBS})
target_link_libraries( ${PROJECT_NAME} ${OpenCV_LIBS} )
target_link_libraries(${PROJECT_NAME} sfml-graphics sfml-window sfml-system sfml-audio sfml-network)
#target_link_libraries( ${PROJECT_NAME} game)
#install (TARGETS ARProject DESTINATION bin)
