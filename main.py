#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Launching the Moment Magnitude Calculator.

:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2012
:license:
    GNU General Public License, Version 3
    (http://www.gnu.org/copyleft/gpl.html)
"""
# Compile the .ui files if necessary. Needs to happen first before the compiled
# .py files are possibly imported by other modules.
import inspect
import os
current_directory = os.path.dirname(inspect.getfile( \
    inspect.currentframe()))
ui_file_directory = os.path.join(current_directory, "resources",
    "ui_files")
from utils import compile_ui_files
compile_ui_files(ui_file_directory, current_directory)


from PyQt4 import QtGui

import sys

from gui_main_window import MainWindow


def main():
    """
    Gets executed when the program starts.
    """
    # Launch and open the main window.
    app = QtGui.QApplication(sys.argv, QtGui.QApplication.GuiClient)
    window = MainWindow()
    # Show the main window and bring it to the foreground.
    window.show()
    window.raise_()

    os._exit(app.exec_())


if __name__ == "__main__":
    main()
