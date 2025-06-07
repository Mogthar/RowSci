from widgets.central_widget.tabs.common_tab import CommonTab
from event_manager.event_manager import event_manager, Event
from data.data_source import DataSource


class CortexTab(CommonTab):
    def __init__(self):
        super().__init__(DataSource.CORTEX)
        event_manager.register_event_listener(Event.CORTEX_DATA_LOADED, self.update)