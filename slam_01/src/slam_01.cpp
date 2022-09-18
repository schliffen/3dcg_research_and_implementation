#include "slam_01.h"

#include <debug.h>

#include <KPluginFactory>

K_PLUGIN_FACTORY_WITH_JSON(slam_01Factory, "slam_01.json", registerPlugin<slam_01>(); )

slam_01::slam_01(QObject *parent, const QVariantList& args)
    : KDevelop::IPlugin(QStringLiteral("slam_01"), parent)
{
    Q_UNUSED(args);

    qCDebug(PLUGIN_SLAM_01) << "Hello world, my plugin is loaded!";
}

// needed for QObject class created from K_PLUGIN_FACTORY_WITH_JSON
#include "slam_01.moc"
