from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from data.data_manager import DataManager
from widgets.data_picker import DataPicker
from widgets.central_widget.tabs.data_tabs import DataTabs

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Importer")

        self.data_picker = DataPicker()
        # Menu
        self.setup_menu()

        # Status Bar
        # self.status = self.statusBar()
        # self.status.showMessage("Data loaded and plotted")
        # self.status.show()

        # central widget
        data_tabs = DataTabs(self)
        self.setCentralWidget(data_tabs)

        # Show window maximized
        self.showMaximized()

    def setup_menu(self):
        self.menu = self.menuBar()
        self.data_menu = self.menu.addMenu("Data")
        self.controls_menu = self.menu.addMenu("Controls")

        ## load data QAction
        load_data_action = QAction("Load Data", self)
        load_data_action.triggered.connect(self.data_picker.exec)
        self.data_menu.addAction(load_data_action)

        ## Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        self.controls_menu.addAction(exit_action)
