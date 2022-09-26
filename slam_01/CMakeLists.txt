cmake_minimum_required(VERSION 3.0)

project(slam_01)






find_package(OpenCV REQUIRED)
find_package(Pangolin 0.4 REQUIRED)


include_directories(
        ${OpenCV_INCLUDE_DIRS}
        ${Pangolin_INCLUDE_DIRS}
        #${G2O_INCLUDE_DIRS}
        #${Sophus_INCLUDE_DIRS}

)




add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})
target_link_libraries( ${PROJECT_NAME}   ${Pangolin_LIBRARIES} )

install(TARGETS ${PROJECT_NAME} RUNTIME DESTINATION bin)
