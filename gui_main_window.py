from PyQt4 import QtCore, QtGui

from matplotlib import rcParams
rcParams["figure.dpi"] = 80
rcParams["figure.figsize"] = (8, 6)

import matplotlib.patches
import matplotlib.widgets
import mtspec
import numpy as np
from obspy.seishub import Client

from gui_select_event_window import SelectEventWindow
import ui_main_window
from utils import center_Qt_window, lat_long_to_distance, \
    calculate_source_spectrum, fit_spectrum


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


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Store all station information in there.
        self.station_information = {}

        self.ui = ui_main_window.Ui_MainWindow()
        self.ui.setupUi(self)
        center_Qt_window(self)

        # Shortcut to the central matplotlib figure canvas.
        self.spectrum_figure = self.ui.mpl_canvas.fig
        self.waveform_figure = self.ui.waveform_canvas.fig

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
        self.ui.pick_table.doubleClicked.connect( \
            self._load_pick)
        self.ui.load_missing_data.clicked.connect( \
            self.download_data)
        self.ui.fit_button.clicked.connect(self.fit_spectrum)
        # Connect the matplotlib events.
        self.waveform_figure.canvas.mpl_connect("button_press_event",
            self._on_waveform_mouse_button_press)
        self.spectrum_figure.canvas.mpl_connect("button_press_event",
            self._on_spectrum_mouse_button_press)
        self.spectrum_figure.canvas.mpl_connect("scroll_event",
            self._on_spectrum_mouse_scroll)
        # Object to collect keep track of the button presses.
        self.waveform_canvas_button_presses = {}

    def _on_waveform_mouse_button_press(self, event):
        obj = self.waveform_canvas_button_presses
        if "second_press" in obj.keys():
            obj.clear()
        if not "first_press" in obj.keys():
            obj.clear()
            obj["first_press"] = event
            return
        if obj["first_press"].inaxes is event.inaxes:
            obj["second_press"] = event
            self.timeframe_selected()
        else:
            obj.clear()
            obj["first_press"] = event


    def timeframe_selected(self):
        """
        Fired if a timeframe has successfully been selected. The information is
        stored in self.waveform_canvas_button_presses.
        """
        obj = self.waveform_canvas_button_presses
        # Remove any previous boxes
        for ax in self.waveform_figure.axes:
            if hasattr(ax, "selection_rectangle_patch"):
                ax.selection_rectangle_patch.remove()
                del ax.selection_rectangle_patch
        current_ax = obj["first_press"].inaxes
        x1 = obj["first_press"].xdata
        x2 = obj["second_press"].xdata
        ylim = current_ax.get_ylim()
        p = matplotlib.patches.Rectangle((min(x1, x2), ylim[0]),
            abs(x2 - x1), ylim[1] - ylim[0], facecolor="orange",
            edgecolor="red")
        current_ax.add_patch(p)
        current_ax.set_ylim(*ylim)
        # Only add it now in case something goes wrong earlier on.
        current_ax.selection_rectangle_patch = p
        self.waveform_figure.canvas.draw()

        selection = [x1, x2]
        selection.sort()

        # Now calculate and plot the spectrum.
        self.calculate_spectrum(current_ax.waveform_trace, selection)

    def calculate_spectrum(self, trace, selection_indices):
        """
        Calculates the multitaper spectrum of the trace going from
        selection_indices[0] to selection_indices[1].
        """
        data = trace.data[selection_indices[0]: selection_indices[1]]
        spec, freq, jackknife_errors, _, _ = mtspec.mtspec(data,
            trace.stats.delta, 3, quadratic=True, statistics=True)
        spec = np.sqrt(spec * trace.stats.sampling_rate * trace.stats.npts)
        jackknife_errors = np.sqrt(jackknife_errors * \
            trace.stats.sampling_rate * trace.stats.npts)

        self.spectrum_figure.clear()
        ax = self.spectrum_figure.add_subplot(111)
        ax.loglog(freq, spec, color="black")
        ax.frequencies = freq
        ax.spectrum = spec
        ax.fill_between(freq, jackknife_errors[:, 0], jackknife_errors[:, 1],
            facecolor="0.75", alpha=0.5, edgecolor="0.5")
        # Keep it around to avoid it being garbage collected.
        ax.cursor = matplotlib.widgets.Cursor(ax, True,
            color="#4c7412", linestyle="-")
        ax.pick_text = ax.text(0.99, 0.95, "Pick plateau value",
            horizontalalignment="right", verticalalignment="top",
            transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.5))
        ax.pick_values = {}
        ax.set_ylim(10E-10, 10E0)
        ax.set_xlim(1.0, 100)
        self.spectrum_figure.canvas.draw()

    def _on_spectrum_mouse_scroll(self, event):
        # Invert it because it has the opposite effect in the formula.
        if event.button == "down":
            self.quality_factor += self.quality_factor * 0.1
        if event.button == "up":
            self.quality_factor -= self.quality_factor * 0.1
        print "Scrolling ..."
        self.plot_spectrum()

    def _on_spectrum_mouse_button_press(self, event):
        """
        Fired upon clicking in the spectrum figure.
        """
        try:
            ax = self.spectrum_figure.axes[0]
        except:
            return
        if not hasattr(ax, "pick_values"):
            return
        # On right mouse button press, clear all picks.
        if event.button == 3:
            ax.pick_values.clear()
            ax.pick_text.set_text("Pick plateau value")
            if hasattr(ax, "theoretical_spectrum"):
                ax.theoretical_spectrum.pop(0).remove()
                del ax.theoretical_spectrum
            self.spectrum_figure.canvas.draw()
            return
        if "plateau_value" not in ax.pick_values.keys():
            ax.pick_values["plateau_value"] = event.ydata
            ax.pick_text.set_text("Pick corner frequency")
            self.spectrum_figure.canvas.draw()
            return
        if "corner_frequency" in ax.pick_values.keys():
            return
        ax.pick_values["corner_frequency"] = event.xdata
        self.plateau_value = ax.pick_values["plateau_value"]
        self.corner_frequency = ax.pick_values["corner_frequency"]
        ax.pick_text.set_text("Right click to start over")
        self.quality_factor = 100
        self.plot_spectrum()

    def plot_spectrum(self):
        """
        Plots the spectrum.
        """
        ax = self.spectrum_figure.axes[0]
        if hasattr(ax, "theoretical_spectrum"):
            ax.theoretical_spectrum.pop(0).remove()
            del ax.theoretical_spectrum
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        freqs = np.linspace(0, 100, 10000)
        theoretical_spectrum = calculate_source_spectrum(freqs,
            self.plateau_value, self.corner_frequency, self.quality_factor,
            self.current_pick.time - self.current_event.origins[0].time)
        ax.theoretical_spectrum = ax.loglog(freqs,
            theoretical_spectrum, color="red", lw=2)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        self.spectrum_figure.canvas.draw()

    def fit_spectrum(self):
        ax = self.spectrum_figure.axes[0]
        self.plateau_value, self.corner_frequency, self.quality_factor, \
            var_omega_0, var_f_c, var_Q = fit_spectrum(ax.spectrum, \
            ax.frequencies, \
            self.current_pick.time - self.current_event.origins[0].time, \
            self.plateau_value, \
            self.corner_frequency, self.quality_factor)
        self.plot_spectrum()

    def _load_pick(self, model_index):
        """
        Slot if a pick has been double clicked in the table view.
        """
        if not hasattr(self, "current_event"):
            return
        pick = self.current_event.picks[model_index.row()]
        if not hasattr(pick, "data"):
            QtGui.QMessageBox.critical(self, "Error",
                "No data available for pick. Please load it first.")
            return

        # Plot the data.
        pick.data.sort()
        self.current_pick = pick
        self.waveform_figure.clear()
        for _i, trace in enumerate(pick.data):
            ax = self.waveform_figure.add_subplot(len(pick.data), 1, _i + 1)
            ax.plot(trace.data, color="black")
            ylim = ax.get_ylim()
            ax.text(0.99, 0.95, trace.id,
                horizontalalignment="right", verticalalignment="top",
                transform=ax.transAxes, bbox=dict(facecolor='red', alpha=0.5))
            # Figure out the pick position.
            pick_pos = (pick.time - trace.stats.starttime) / \
                (trace.stats.endtime - trace.stats.starttime) * \
                trace.stats.npts
            ax.vlines(pick_pos, ylim[0], ylim[1], color="blue", lw="2")
            ax.set_ylim(*ylim)
            # Append a reference of the trace to the axis.
            ax.waveform_trace = trace
        self.waveform_figure.canvas.draw()

    def download_data(self):
        """
        Downloads the data for all picks in self.event.
        """
        if not hasattr(self, "current_event"):
            return

        event = self.current_event
        client = Client(base_url=str(self.ui.seishub_server.text()),
            timeout=60)

        progress_dialog = QtGui.QProgressDialog( \
            "Downloading waveform data...", "Cancel", 0,
            len(event.picks))
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        progress_dialog.forceShow()
        # Attempt to load all the station information for all picks.
        for _i, pick in enumerate(event.picks):
            progress_dialog.setValue(_i)
            if progress_dialog.wasCanceled():
                break
            # Do not download it if it is already available.
            if hasattr(pick, "data"):
                # Check if enough data is available.
                if abs((pick.data[0].stats.endtime - \
                    pick.data[0].stats.starttime) - \
                    2.0 * float(self.ui.buffer_seconds.value())) < 0.1:
                    continue
            try:
                st = client.waveform.getWaveform( \
                    network=pick.waveform_id.network_code,
                    station=pick.waveform_id.station_code,
                    location=pick.waveform_id.location_code,
                    channel=pick.waveform_id.channel_code[:-1] + "*",
                    starttime=pick.time - \
                        float(self.ui.buffer_seconds.value()),
                    endtime=pick.time + \
                        float(self.ui.buffer_seconds.value()),
                    getPAZ=True,
                    getCoordinates=True)
            except Exception, e:
                error_type_str = e.__class__.__name__
                print "Problem while downloading waveform data:", \
                    "{err_type}({message})".format( \
                    err_type=error_type_str,
                    message=str(e))
                continue
            for trace in st:
                trace.simulate(paz_remove=trace.stats.paz)
            pick.data = st
        # Finish the progress dialog.
        progress_dialog.setValue(len(event.picks))

        # Display all picks in a table view.
        model = PickTableView(event)
        self.ui.pick_table.setModel(model)
        self.ui.pick_table.resizeRowsToContents()
        self.ui.pick_table.resizeColumnsToContents()
        self.ui.pick_table.horizontalHeader().setStretchLastSection(True)

    def event_chosen(self, event):
        """
        This is called when a new event has been selected.

        :type event: :class:`~obspy.core.event.Event`
        """
        # The window might be hidden when this function is called.
        self.show()
        self.current_event = event
        # Set some labels.
        self.ui.selected_event_id_label.setText(event.resource_id.resource_id)
        self.ui.selected_latitude_label.setText("%.4f" % \
            event.origins[0].latitude)
        self.ui.selected_longitude_label.setText("%.4f" % \
            event.origins[0].longitude)
        self.ui.selected_depth_label.setText("%.4f" % \
            event.origins[0].depth)
        self.ui.selected_origin_time_label.setText(str(event.origins[0].time))
        # It might be possible that the event has no magnitude so far. We want
        # to determine it after all ...
        if len(event.magnitudes):
            self.ui.selected_magnitude_label.setText("%.3f %s" % \
                (event.magnitudes[0].mag, event.magnitudes[0].magnitude_type))
        else:
            self.ui.selected_magnitude_label.setText("None")
        # Download the data upon loading.
        self.download_data()

    def _launch_select_event_window(self):
        """
        Launches the select event window.
        """
        # XXX: Only for development.
        import pickle
        with open("./pickled_data.pickle", "rb") as open_file:
            event = pickle.load(open_file)
        self.event_chosen(event)
        return

        window = SelectEventWindow()
        window.closed.connect(self.show)
        window.event_chosen.connect(self.event_chosen)
        # Show the main window and bring it to the foreground.
        window.show()
        window.raise_()
        self.hide()
