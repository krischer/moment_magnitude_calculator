#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility functions and classes.

:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2012
:license:
    GNU General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)
"""
from PyQt4 import QtCore, QtGui, QtWebKit

import glob
from obspy.core import UTCDateTime
import os


class GoogleMapsWebView(QtWebKit.QWebPage):
    """
    Subclass QWebPage to implement a custom user agent string and be able to
    debug Javascript.
    """
    def userAgentForUrl(self, *args, **kwargs):
        # Dirty hack required to not get the multitouch version of google
        # maps...
        # See http://qt-project.org/forums/viewthread/1643
        return "Chrome/1.0"

    def javaScriptConsoleMessage(self, msg, line, source):
        """
        Print all Javascript Console Messages as a red string.
        """
        print "\033[1;31m" + \
            "[JavaScript Console - {source} line {line}] {msg}".format( \
            source=source, line=line, msg=msg) + \
            "\033[1;m"


def UTCtoQDateTime(dt):
    """
    Converts a UTCDateTime object to a QDateTime object.
    """
    return QtCore.QDateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute,
            dt.second, dt.microsecond // 1000, QtCore.Qt.TimeSpec(1))


def QDatetoUTCDateTime(dt):
    """
    Converts a QDateTime to a UTCDateTime object.
    """
    # XXX: Microseconds might be lost.
    return UTCDateTime(dt.toPyDateTime())


def center_Qt_window(window):
    """
    Centers the given window on the screen.
    """
    resolution = QtGui.QDesktopWidget().screenGeometry()
    window.move((resolution.width() / 2) - (window.frameSize().width() / 2),
        (resolution.height() / 2) - (window.frameSize().height() / 2))


def compile_ui_files(ui_directory, destination_directory):
    """
    Automatically compiles all .ui files found in the given ui_directory to .py
    files which will be stored in the destination_directory. The filenames will
    be identical apart from the extension

    The files will only be compiled if the last-modified time of the .ui file
    is later/larger than the one of the corresponding .py file.
    """
    for filename in glob.glob(os.path.join(ui_directory, '*.ui')):
        ui_file = filename
        py_ui_file = os.path.splitext(ui_file)[0] + os.path.extsep + 'py'
        py_ui_file = os.path.join(destination_directory,
            os.path.basename(py_ui_file))
        if not os.path.exists(py_ui_file) or \
            (os.path.getmtime(ui_file) >= os.path.getmtime(py_ui_file)):
            from PyQt4 import uic
            print "Compiling ui file: %s" % ui_file
            with open(py_ui_file, 'w') as open_file:
                uic.compileUi(ui_file, open_file)
