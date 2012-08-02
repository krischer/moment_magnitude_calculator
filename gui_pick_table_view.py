from PyQt4 import QtCore, QtGui

from utils import lat_long_to_distance


class PickTableView(QtCore.QAbstractTableModel):
    """
    A table model used to display all the picks.
    """
    def __init__(self, event):
        """
        :param event: A of :class:`~obspy.core.event.Event` object. Every inner
            pick object can have an additional data attribute. This stores the
            waveform stream and some metadata.
        """
        QtCore.QAbstractTableModel.__init__(self)
        self.event = event
        self.picks = event.picks
        self.header_values = ["Channel", "Phase", "Polarity", "Mode",
            "Distance", "Data available"]

    def rowCount(self, *args):
        return len(self.picks)

    def columnCount(self, *args):
        return 6

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole:
            pick = self.picks[index.row()]
            # Map the column to an attribute.
            column = index.column()
            if column == 0:
                return QtCore.QVariant(pick.waveform_id.getSEEDString())
            elif column == 1:
                phase_hint = pick.phase_hint
                if phase_hint is None:
                    phase_hint = "-"
                return QtCore.QVariant(str(phase_hint))
            elif column == 2:
                polarity = pick.polarity
                if polarity is None:
                    polarity = "-"
                return QtCore.QVariant(str(polarity))
            elif column == 3:
                evaluation_mode = pick.evaluation_mode
                if evaluation_mode is None:
                    evaluation_mode = "-"
                return QtCore.QVariant(str(evaluation_mode))
            # The distance column.
            elif column == 4:
                coods = pick.data[0].stats.coordinates
                distance = lat_long_to_distance(self.event.origins[0].latitude,
                    self.event.origins[0].longitude,
                    self.event.origins[0].depth, coods.latitude,
                    coods.longitude, coods.elevation / 1000.0)
                return QtCore.QVariant("%.3f" % distance)
            elif column == 5:
                if hasattr(pick, "data"):
                    return QtCore.QVariant("Yes")
                return QtCore.QVariant("No")
        # Set the background color for column id 4
        if role == QtCore.Qt.BackgroundRole and index.column() == 5:
            pick = self.picks[index.row()]
            if hasattr(pick, "data"):
                return QtGui.QBrush(QtGui.QColor("#e2ffa4"))
            return QtGui.QBrush(QtGui.QColor("#ff8768"))
        # Some tooltip for everything.
        if role == QtCore.Qt.ToolTipRole:
            pick = self.picks[index.row()]
            coods = pick.data[0].stats.coordinates
            coods = "Lat: %.4f | Lng: %.4f | Elevation: %.1f" % ( \
                coods.latitude, coods.longitude, coods.elevation)
            return QtCore.QVariant(coods)

    def headerData(self, column, orientation, role):
            if orientation != QtCore.Qt.Horizontal or \
                role != QtCore.Qt.DisplayRole:
                return QtCore.QVariant()
            return QtCore.QVariant(self.header_values[column])
