from .strokeListener import StrokeListenerDocker
from krita import DockWidgetFactory,  DockWidgetFactoryBase # type: ignore

__ver__ = "v1.0.0"

DOCKER_NAME = 'Stroke Listener'
DOCKER_ID = 'pykrita_strokelistenerDocker'

# Register the Docker with Krita
instance = Krita.instance() # type: ignore
dock_widget_factory = DockWidgetFactory(DOCKER_ID, DockWidgetFactoryBase.DockRight, StrokeListenerDocker)

instance.addDockWidgetFactory(dock_widget_factory)
