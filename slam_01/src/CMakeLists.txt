set(slam_01_SRCS
    slam_01.cpp
)

ecm_qt_declare_logging_category(slam_01_SRCS
    HEADER debug.h
    IDENTIFIER PLUGIN_SLAM_01
    CATEGORY_NAME "kdevelop.plugins.slam_01"
)

kdevplatform_add_plugin(slam_01
    JSON slam_01.json
    SOURCES ${slam_01_SRCS}
)

target_link_libraries(slam_01
    KDev::Interfaces
)
