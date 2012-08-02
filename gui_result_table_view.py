#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2012
:license:
    GNU General Public License, Version 3
    (http://www.gnu.org/copyleft/gpl.html)
"""
from PyQt4 import QtCore, QtGui


class ResultsTableView(QtCore.QAbstractTableModel):
    """
    The results table view.
    """
    def __init__(self, results):
        """
        :param result: A list of result objects
        """
        QtCore.QAbstractTableModel.__init__(self)
        self.results = results
        self.header_value_map = { \
            "Channel": "channel",
            u"Ω₀": "omega_0",
            "f_c": "corner_frequency",
            "Q": "quality_factor",
            "Phase": "phase",
            "": ""}

        self.header_values = ["Channel", u"Ω₀", "f_c", "Q", "Phase", ""]

    def rowCount(self, *args):
        return len(self.results)

    def columnCount(self, *args):
        return len(self.header_values)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole:
            column = index.column()
            result_type = self.header_values[column]
            if result_type == "":
                return QtCore.QVariant("Delete")
            value = \
                self.results[index.row()][self.header_value_map[result_type]]
            if isinstance(value, basestring):
                pass
            elif value < 100.0 and value >= 0.1:
                value = "%.2f" % value
            else:
                value = "%.2e" % value
            return QtCore.QVariant(value)
        # Set the background color for column id 4
        elif role == QtCore.Qt.BackgroundRole and index.column() == 5:
            return QtGui.QBrush(QtGui.QColor("#ff6060"))

    def headerData(self, column, orientation, role):
            if orientation != QtCore.Qt.Horizontal or \
                role != QtCore.Qt.DisplayRole:
                return QtCore.QVariant()
            return QtCore.QVariant(self.header_values[column])
