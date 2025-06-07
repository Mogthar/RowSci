from widgets.central_widget.tabs.common_tab import CommonTab
from event_manager.event_manager import event_manager, Event
from data.data_source import DataSource


class ArtinisTab(CommonTab):
    def __init__(self):
        super().__init__(DataSource.ARTINIS)
        event_manager.register_event_listener(Event.ARTINIS_DATA_LOADED, self.update)
