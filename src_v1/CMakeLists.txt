add_executable(${PROJECT_NAME}
        main.cpp
        CameraCalibration.cpp
        CameraCalibration.hpp


#ARDrawingContext.cpp
#ARDrawingContext.hpp
#GeometryTypes.cpp
#GeometryTypes.hpp
#ARPipeline.hpp
#ARPipeline.cpp
#Pattern.cpp
#Pattern.hpp
#PatternDetector.cpp
#PatternDetector.hpp
#DebugHelpers.hpp
)

target_link_libraries( ${PROJECT_NAME} ${OpenCV_LIBRARIES} )
target_link_libraries( ${PROJECT_NAME} ${OPENGL_LIBRARIES} ) # GL GLU glut
     
install (TARGETS ${PROJECT_NAME} DESTINATION bin)
