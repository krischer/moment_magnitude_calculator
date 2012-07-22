#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyQt4 window handling the event selection.

:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2012
:license:
    GNU General Public License, Version 3
    (http://www.gnu.org/copyleft/gpl.html)
"""
from PyQt4 import QtGui, QtCore

import inspect
from obspy.core import UTCDateTime
from obspy.core.event import Event
import os
import StringIO

# Custom Seishub event file format reading routine.
from seishub_event_format_parser import readSeishubEventFile
from utils import GoogleMapsWebView, UTCtoQDateTime, QDatetoUTCDateTime, \
    center_Qt_window

# Import the ui file.
import ui_select_event_window

SEISHUB_BASE_URL = "http://localhost:7777"


class SelectEventWindow(QtGui.QMainWindow):
    # Give the window a closed signal. This is necessary for the faked
    # multi-window application.
    closed = QtCore.pyqtSignal()

    # A signal that is emitted when the "Choose event" button has been clicked.
    event_chosen = QtCore.pyqtSignal(Event)

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.ui = ui_select_event_window.Ui_SelectEventWindow()
        self.ui.setupUi(self)
        center_Qt_window(self)

        # Init event list and currently selected event.
        self.events = []
        self.currently_selected_event = None
        self.current_selected_event_object = None

        self.init_widgets()

        self.connect_signals_and_slots()

        self.update_plot()

    def init_widgets(self):
        """
        """
        # Set the timeframe to the last two week.
        self.ui.starttime.setDateTime( \
            UTCtoQDateTime(UTCDateTime() - 86000 * 14))
        self.ui.endtime.setDateTime(UTCtoQDateTime(UTCDateTime()))
        self.ui.webView.setPage(GoogleMapsWebView())
        map_file = os.path.join(os.path.dirname(inspect.getfile( \
            inspect.currentframe())), "resources", "html_resources",
            "map.html")
        self.ui.webView.load(QtCore.QUrl(map_file))

        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("pyObj",
                self)

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

    @QtCore.pyqtSlot(str)
    def set_lat_long_bounds(self, bounds):
        """
        Set the latitude longitude bounds as a string, e.g.:
            "((lat_ne, long_ne), (lat_sw, long_sw))"

        Used as a callback in the WebView JavaScript Code.
        """
        self.north_east, self.south_west = [map(float, _i.split(", ")) \
            for _i in str(bounds)[2:-2].split("), (")]
        self.ui.northeast_label.setText("%.3f, %.3f" % (self.north_east[0],
            self.north_east[1]))
        self.ui.southwest_label.setText("%.3f, %.3f" % (self.south_west[0],
            self.south_west[1]))

    @QtCore.pyqtSlot(str)
    def event_selected(self, event_id):
        """
        Called when a new event has been selected. The event_id should be
        enough to identify it.

        Used as a callback in the WebView JavaScript Code.
        """
        # Reset all detail object as soon as a new event is selected. Also
        # disable the "Choose event" button.
        self.ui.choose_event_button.setEnabled(False)
        self.ui.selected_event_p_phase_picks.setText("-")
        self.ui.selected_event_s_phase_picks.setText("-")
        self.ui.selected_event_warning.setText("")

        self.current_selected_event_object = None
        for event in self.events:
            if event["resource_name"] == event_id:
                self.currently_selected_event = event
                break
        # Handle an eventual error.
        if self.currently_selected_event is None:
            QtGui.QMessageBox.critical(self, "Error",
                "Selected event not found on the Python side. Please " + \
                "contact the developer or fix the code yourself...")
            return

        ev = self.currently_selected_event
        self.ui.selected_event_id_label.setText(ev["resource_name"])
        self.ui.selected_latitude_label.setText("%.4f" % ev["latitude"])
        self.ui.selected_longitude_label.setText("%.4f" % ev["longitude"])
        self.ui.selected_depth_label.setText("%.4f" % ev["depth"])
        self.ui.selected_origin_time_label.setText(str(ev["datetime"]))
        self.ui.selected_magnitude_label.setText("%.3f %s" % \
            (ev["magnitude"], ev["magnitude_type"]))

        # Last but not least enable the detail loading button.
        self.ui.selected_event_load_details.setEnabled(True)

    def connect_signals_and_slots(self):
        self.ui.search_events_button.clicked.connect(self.search_for_events)
        self.ui.selected_event_load_details.clicked.connect(\
            self.load_event_object)
        self.ui.choose_event_button.clicked.connect(self.choose_event)
        self.ui.cancel_button.clicked.connect(self.close)

    def choose_event(self):
        if self.current_selected_event_object is None:
            QtGui.QMessageBox.critical(self, "Error",
                "The event object cannot be found... Please " + \
                "contact the developer or fix the code yourself...")
            return
        self.event_chosen.emit(self.current_selected_event_object)
        self.close()

    def load_event_object(self):
        """
        Loads the currently selected event from the Seishub database.
        """
        if self.currently_selected_event is None:
            QtGui.QMessageBox.critical(self, "Error",
                "Selected event not found - something is wrong. Please " + \
                "contact the developer or fix the code yourself...")
            return
        from obspy.seishub import Client
        client = Client(base_url=SEISHUB_BASE_URL)
        try:
            resource = client.event.getResource( \
                self.currently_selected_event["resource_name"])
        except Exception, e:
            error_type_str = e.__class__.__name__
            msg_box = QtGui.QMessageBox()
            msg_box.setIcon(QtGui.QMessageBox.Critical)
            msg_box.setText("Retrieving event from the SeisHub server " + \
                "failed!")
            msg_box.setDetailedText("{err_type}({message})".format( \
                err_type=error_type_str,
                message=str(e)))
            msg_box.exec_()
            return
        file_object = StringIO.StringIO(resource)
        self.current_selected_event_object = \
            readSeishubEventFile(file_object)[0]
        # Get the P and S wave pick counts.
        p_picks = len([_i for _i in self.current_selected_event_object.picks \
            if _i.phase_hint == "P"])
        s_picks = len([_i for _i in self.current_selected_event_object.picks \
            if _i.phase_hint == "S"])
        if p_picks == 0 and s_picks == 0:
            self.ui.selected_event_warning.setText( \
                "Warning: Event has no associated picks.")
            return
        # If all is fine, update the pick count and enable the user to choose
        # the event.
        self.ui.selected_event_p_phase_picks.setText(str(p_picks))
        self.ui.selected_event_s_phase_picks.setText(str(s_picks))
        self.ui.choose_event_button.setEnabled(True)

    def update_plot(self):
        pass
        #self.mpl_figure.clear()
        #self.mpl_figure.canvas.draw()

    def search_for_events(self):
        """
        Read all current values in the GUI and load the requested events.
        """
        # Read all necessary the GUI variables.
        starttime = QDatetoUTCDateTime(self.ui.starttime.dateTime())
        endtime = QDatetoUTCDateTime(self.ui.endtime.dateTime())
        min_mag = self.ui.min_magnitude.value()
        max_mag = self.ui.max_magnitude.value()

        model_box = QtGui.QMessageBox(QtGui.QMessageBox.Information,
            "", "Downloading event index. Please wait...",
            QtGui.QMessageBox.NoButton)
        model_box.show()

        from obspy.seishub import Client
        c = Client(base_url=SEISHUB_BASE_URL)
        try:
            events = c.event.getList(limit=2500, min_datetime=starttime,
                max_datetime=endtime, min_latitude=self.north_east[0],
                max_latitude=self.south_west[0],
                min_longitude=self.north_east[1],
                max_longitude=self.south_west[1], min_magnitude=min_mag,
                max_magnitude=max_mag)
        except Exception, e:
            error_type_str = e.__class__.__name__
            model_box.done(0)
            msg_box = QtGui.QMessageBox()
            msg_box.setIcon(QtGui.QMessageBox.Critical)
            msg_box.setText("Retrieving events from the SeisHub server " + \
                "failed!")
            msg_box.setDetailedText("{err_type}({message})".format( \
                err_type=error_type_str,
                message=str(e)))
            msg_box.exec_()
            return

        # Clear the old events.
        self.ui.webView.page().mainFrame().evaluateJavaScript("clearEvents()")

        for event in events:
            js_call = "addEvent({lat}, {lng}, {depth}, {magnitude}, " + \
                "'{magnitude_type}', '{datetime}', '{event_id}', " + \
                "'{misc_info}', '{server}')"
            js_call = js_call.format( \
                lat=event["latitude"],
                lng=event["longitude"],
                depth=event["depth"],
                magnitude=event["magnitude"],
                magnitude_type=event["magnitude_type"],
                datetime=event["datetime"],
                event_id=event["resource_name"],
                # Misc information in a human readable form. Use ; as
                # delimiter.
                misc_info=("SeisHub account: {account}; " + \
                    "SeisHub user: {user}; Localisation Method: " + \
                    "{localisation_method}").format( \
                    account=event["account"],
                    user=event["user"],
                    localisation_method=event["localisation_method"]),
                server="SeisHub")
            self.ui.webView.page().mainFrame().evaluateJavaScript(js_call)

        # Make it a instance attribute.
        self.events = events
        model_box.done(0)
