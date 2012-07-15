from PyQt4 import QtGui

from gui_select_event_window import SelectEventWindow
import ui_main_window
from utils import center_Qt_window


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.ui = ui_main_window.Ui_MainWindow()
        self.ui.setupUi(self)
        center_Qt_window(self)

        # Shortcut to the central matplotlib figure canvas.
        self.mpl_figure = self.ui.mpl_canvas.fig

        self.init_widgets()
        self.connect_signals_and_slots()

    def init_widgets(self):
        """
        """
        pass

    def connect_signals_and_slots(self):
        """
        """
        self.ui.load_event_button.clicked.connect( \
            self._launch_select_event_window)

    def _enable_window(self):
        self.setEnabled(True)

    def _launch_select_event_window(self):
        """
        Launches the select event window.
        """
        window = SelectEventWindow()
        window.closed.connect(self._enable_window)
        # Show the main window and bring it to the foreground.
        window.show()
        window.raise_()
        self.setEnabled(False)
