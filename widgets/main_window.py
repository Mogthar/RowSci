from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from data.data_manager import DataManager
from widgets.data_picker import DataPicker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Importer")

        self.data_manager = DataManager()
        self.data_picker = DataPicker(self.data_manager)
        # Menu
        self.setup_menu()

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")
        self.status.show()

        # central widget
        # self.setCentralWidget(widget)


        # Window dimensions
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

    def setup_menu(self):
        self.menu = self.menuBar()
        self.data_menu = self.menu.addMenu("Data")
        self.controls_menu = self.menu.addMenu("Controls")

        ## load data QAction
        load_data_action = QAction("Load Data", self)
        load_data_action.triggered.connect(self.data_picker.show)
        self.data_menu.addAction(load_data_action)

        ## Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        self.controls_menu.addAction(exit_action)
