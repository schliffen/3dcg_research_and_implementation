#ifndef SLAM_01_H
#define SLAM_01_H

#include <interfaces/iplugin.h>

class slam_01 : public KDevelop::IPlugin
{
    Q_OBJECT

public:
    // KPluginFactory-based plugin wants constructor with this signature
    slam_01(QObject* parent, const QVariantList& args);
};

#endif // SLAM_01_H
