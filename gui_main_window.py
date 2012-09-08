#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Moment magnitude calculator hooked up to a SeisHub database.

:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2012
:license:
    GNU General Public License, Version 3
    (http://www.gnu.org/copyleft/gpl.html)
"""
from PyQt4 import QtCore, QtGui

# Make sure to overwrite a possible matplotlibrc file.
from matplotlib import rcParams
rcParams["figure.dpi"] = 80
rcParams["figure.figsize"] = (8, 6)

import copy
import matplotlib.patches
import matplotlib.widgets
import mtspec
import numpy as np
from obspy.core.event import Comment, Magnitude, Catalog
from obspy.seishub import Client
import os

from gui_select_event_window import SelectEventWindow
from gui_pick_table_view import PickTableView
from gui_result_table_view import ResultsTableView
import ui_main_window
from utils import center_Qt_window, calculate_source_spectrum, fit_spectrum, \
    moment_from_low_freq_amplitude, lat_long_to_distance, \
    moment_to_moment_magnitude, source_radius_from_corner_frequency, \
    calculate_stress_drop


class MainWindow(QtGui.QMainWindow):
    """
    The main window of the moment magnitude calculator.
    """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Load the .ui file.
        self.ui = ui_main_window.Ui_MainWindow()
        self.ui.setupUi(self)
        center_Qt_window(self)

        # Setup shortcuts to the matplotlib figures.
        self.ui.spectrum_figure = self.ui.mpl_canvas.fig
        self.ui.waveform_figure = self.ui.waveform_canvas.fig

        # Keep one dictionary that stores information about the current state
        # of the application.
        self.current_state = {}
        # Setup velocities and the rock density.
        self.current_state["density"] = 2700.0
        self.current_state["p_wave_speed"] = (5800 + 3800) / 2.0
        self.current_state["s_wave_speed"] = (2200 + 3220) / 2.0
        self.ui.density.setValue(self.current_state["density"])
        self.ui.v_p.setValue(self.current_state["p_wave_speed"])
        self.ui.v_s.setValue(self.current_state["s_wave_speed"])
        self.results = []

        # Connect all necessary signals and slots.
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        """
        Central method called at initialization time to bind all slots and
        signals.
        """
        # Connect some buttons with their corresponding functions.
        self.ui.load_event_button.clicked.connect( \
            self._open_event_selection_window)
        self.ui.load_missing_data.clicked.connect(self._on_download_data)
        self.ui.fit_button.clicked.connect(self._on_fit_spectrum)
        self.ui.accept_values_button.clicked.connect(self._on_accept_values)
        self.ui.save_file_button.clicked.connect(self._on_file_save)

        # Connect the fit table delte button.
        self.ui.fit_table.clicked.connect(self._on_pick_table_click)

        # Double clicking on a pick load it.
        self.ui.pick_table.doubleClicked.connect(self._on_load_pick)

        # Monitor the three spin boxes for changes. Use a lambda function hack
        # to avoid having to write real methods.
        def update_value(key, value):
            self.current_state[key] = value
            self._calculate_final_values()
        self.ui.density.valueChanged.connect( \
            lambda x: update_value("density", x))
        self.ui.v_p.valueChanged.connect( \
            lambda x: update_value("p_wave_speed", x))
        self.ui.v_s.valueChanged.connect( \
            lambda x: update_value("s_wave_speed", x))

        # Connect the matplotlib events.
        self.ui.waveform_figure.canvas.mpl_connect("button_press_event",
            self._on_waveform_canvas_mouse_button_press)
        self.ui.spectrum_figure.canvas.mpl_connect("button_press_event",
            self._on_spectrum_canvas_mouse_button_press)
        self.ui.spectrum_figure.canvas.mpl_connect("scroll_event",
            self._on_spectrum_canvas_mouse_scroll)
        # Dict to keep track of the button presses on the waveform canvas.
        self.current_state["waveform_canvas_button_presses"] = {}

    def _on_file_save(self):
        """
        Creates a new obspy.core.event.Magnitude object and writes the moment
        magnitude to it.
        """
        # Get the save filename.
        filename = QtGui.QFileDialog.getSaveFileName(caption="Save as...")
        filename = os.path.abspath(str(filename))
        mag = Magnitude()
        mag.mag = self.final_result["moment_magnitude"]
        mag.magnitude_type = "Mw"
        mag.station_count = self.final_result["station_count"]
        mag.evaluation_mode = "manual"
        # Link to the used origin.
        mag.origin_id = self.current_state["event"].origins[0].resource_id
        mag.method_id = "Magnitude picker Krischer"
        # XXX: Potentially change once this program gets more stable.
        mag.evaluation_status = "preliminary"
        # Write the other results as Comments.
        mag.comments.append( \
            Comment("Seismic moment in Nm: %g" % \
            self.final_result["seismic_moment"]))
        mag.comments.append( \
            Comment("Circular source radius in m: %.2f" % \
            self.final_result["source_radius"]))
        mag.comments.append( \
            Comment("Stress drop in Pa: %.2f" % \
            self.final_result["stress_drop"]))
        mag.comments.append( \
                Comment("Very rough Q estimation: %.1f" % \
            self.final_result["quality_factor"]))

        event = copy.deepcopy(self.current_state["event"])
        event.magnitudes.append(mag)
        cat = Catalog()
        cat.events.append(event)
        cat.write(filename, format="quakeml")

    def _on_pick_table_click(self, index):
        row = index.row()
        column = index.column()
        if column != 5 or (row + 1) > len(self.results):
            return
        self.results.pop(row)
        model = ResultsTableView(self.results)
        self.ui.fit_table.setModel(model)
        self.ui.fit_table.resizeRowsToContents()
        self.ui.fit_table.resizeColumnsToContents()
        self.ui.fit_table.horizontalHeader().setStretchLastSection(True)
        self._calculate_final_values()

    def _on_waveform_canvas_mouse_button_press(self, event):
        """
        Handle the mouse button presses on the waveform plots canvas. Only
        accept a time-frame selection if start-and endtime have been selected
        on the waveform canvas.
        """
        state = self.current_state["waveform_canvas_button_presses"]
        if "second_press" in state.keys():
            state.clear()
        if not "first_press" in state.keys():
            state.clear()
            state["first_press"] = event
            return
        if state["first_press"].inaxes is event.inaxes:
            state["second_press"] = event
            self._on_timeframe_selected()
        else:
            state.clear()
            state["first_press"] = event

    def _on_timeframe_selected(self):
        """
        Fired if a timeframe has successfully been selected. The information is
        stored in self.waveform_canvas_button_presses.
        """
        state = self.current_state["waveform_canvas_button_presses"]
        # Remove any previous boxes
        for ax in self.ui.waveform_figure.axes:
            if hasattr(ax, "selection_rectangle_patch"):
                ax.selection_rectangle_patch.remove()
                del ax.selection_rectangle_patch
        current_ax = state["first_press"].inaxes
        x1 = state["first_press"].xdata
        x2 = state["second_press"].xdata
        ylim = current_ax.get_ylim()
        p = matplotlib.patches.Rectangle((min(x1, x2), ylim[0]),
            abs(x2 - x1), ylim[1] - ylim[0], facecolor="orange",
            edgecolor="red")
        current_ax.add_patch(p)
        current_ax.set_ylim(*ylim)
        # Only add it now in case something goes wrong earlier on.
        current_ax.selection_rectangle_patch = p
        self.ui.waveform_figure.canvas.draw()

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
            trace.stats.delta, 2, statistics=True)
        spec = np.sqrt(spec)
        jackknife_errors = np.sqrt(jackknife_errors)

        self.current_state["channel"] = trace.id

        self.ui.spectrum_figure.clear()
        self.ui.spectrum_figure.subplots_adjust(left=0.1, bottom=0.1)
        ax = self.ui.spectrum_figure.add_subplot(111)
        ax.loglog(freq, spec, color="black")
        ax.frequencies = freq
        ax.spectrum = spec
        ax.fill_between(freq, jackknife_errors[:, 0], jackknife_errors[:, 1],
            facecolor="0.75", alpha=0.5, edgecolor="0.5")
        # Keep it around to avoid it being garbage collected.
        ax.cursor = matplotlib.widgets.Cursor(ax, True,
            color="#4c7412", linestyle="-")
        ax.pick_text = ax.text(0.05, 0.05, ("Left click to adjust plateau "
            "value\nRight click to adjust corner frequency\n"
            "Scroll to adjust quality factor"),
            horizontalalignment="left", verticalalignment="bottom",
            multialignment="left",
            transform=ax.transAxes, bbox=dict(facecolor='orange', alpha=0.5))
        ax.pick_values = {}
        ax.set_ylim(spec.min() / 10.0, spec.max() * 100.0)
        ax.set_xlim(1.0, 100)
        self.ui.spectrum_figure.canvas.draw()

        # Now guess guess some values, and fit the curve. Setting it to 10 is
        # reasonable.
        self.current_state["corner_frequency"] = 10.0
        # Set omega_0 to the mean value of all values lower than the corner
        # frequency.
        corn_freq_index = \
            np.abs(freq - self.current_state["corner_frequency"]).argmin()
        self.current_state["omega_0"] = spec[:corn_freq_index].mean()
        self.current_state["quality_factor"] = 100.0
        self._on_fit_spectrum()

    def _on_spectrum_canvas_mouse_scroll(self, event):
        """
        Scrolling the mouse wheel fits the Q value.
        """
        # Invalidate all variances.
        self.current_state["omega_0_var"] = None
        self.current_state["corner_frequency_var"] = None
        if event.button == "up":
            self.current_state["quality_factor"] += \
                self.current_state["quality_factor"] * 0.1
        if event.button == "down":
            self.current_state["quality_factor"] -= \
                self.current_state["quality_factor"] * 0.1
        self.plot_theoretical_spectrum()

    def _on_spectrum_canvas_mouse_button_press(self, event):
        """
        Fired upon clicking in the spectrum figure.
        """
        if event.button not in  (1, 3):
            return
        # Invalidate all variances.
        self.current_state["omega_0_var"] = None
        self.current_state["corner_frequency_var"] = None
        # On left mouse click, set a new omega_0.
        if event.button == 1:
            self.current_state["omega_0"] = event.ydata
        # On right mouse button click, set new corner frequency.
        elif event.button == 3:
            self.current_state["corner_frequency"] = event.xdata
        # Plot the spectrum
        self.plot_theoretical_spectrum()

    def plot_theoretical_spectrum(self):
        """
        Plots the spectrum.
        """
        ax = self.ui.spectrum_figure.axes[0]
        if hasattr(ax, "theoretical_spectrum"):
            ax.theoretical_spectrum.pop(0).remove()
            del ax.theoretical_spectrum
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        freqs = np.linspace(0, 100, 10000)
        theoretical_spectrum = calculate_source_spectrum(freqs,
            self.current_state["omega_0"], \
            self.current_state["corner_frequency"], \
            self.current_state["quality_factor"], \
            self.current_state["pick"].time - \
            self.current_state["event"].origins[0].time)
        ax.theoretical_spectrum = ax.loglog(freqs,
            theoretical_spectrum, color="red", lw=2)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        self.ui.spectrum_figure.canvas.draw()
        # Update the values.
        self._update_spectral_parameter_display()

    def _update_spectral_parameter_display(self):
        labels = ["omega_0", "quality_factor", "corner_frequency"]
        for label in labels:
            var_label = "%s_var" % label
            if label == "quality_factor":
                ll = [label]
            else:
                ll = [label, var_label]
            for _i in ll:
                if _i not in self.current_state or not self.current_state[_i]:
                    getattr(self.ui, _i + "_label").setText("-")
                else:
                    value = self.current_state[_i]
                    if value < 100.0 and value >= 0.1:
                        value = "%.2f" % value
                    else:
                        value = "%.2e" % value
                    getattr(self.ui, _i + "_label").setText(value)

    def _on_fit_spectrum(self):
        """
        Use the current spectrum parameters to get a better fit using a
        Levenberg-Marquardt algorithm.
        """
        ax = self.ui.spectrum_figure.axes[0]
        self.current_state["omega_0"], \
            self.current_state["corner_frequency"], \
            self.current_state["omega_0_var"], \
            self.current_state["corner_frequency_var"] = \
            fit_spectrum(ax.spectrum, ax.frequencies, \
                self.current_state["pick"].time - \
                self.current_state["event"].origins[0].time, \
                self.current_state["omega_0"], \
                self.current_state["corner_frequency"], \
                self.current_state["quality_factor"])
        self.plot_theoretical_spectrum()

    def _on_load_pick(self, model_index):
        """
        Slot if a pick has been double clicked in the table view.
        """
        if not "event" in self.current_state:
            return
        pick = self.current_state["event"].picks[model_index.row()]
        if not hasattr(pick, "data"):
            QtGui.QMessageBox.critical(self, "Error",
                "No data available for pick. Please load it first.")
            return

        # Plot the data.
        pick.data.sort()
        self.current_state["pick"] = pick
        self.ui.waveform_figure.clear()
        self.ui.waveform_figure.subplots_adjust(left=0.1)
        for _i, trace in enumerate(pick.data):
            ax = self.ui.waveform_figure.add_subplot(len(pick.data), 1, _i + 1)
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
        self.ui.waveform_figure.canvas.draw()

    def _on_download_data(self):
        """
        Downloads the data for all picks in self.event.
        """
        if "event" not in self.current_state:
            return

        event = self.current_state["event"]
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
                # Convert to ground motion.
                trace.stats.paz["zeros"].append(0 + 0j)
            st.merge(-1)
            st.detrend()
            st.simulate(paz_remove="self", water_level=10.0)
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
        self.current_state["event"] = event
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
        self._on_download_data()

    def _on_accept_values(self):
        values = ["omega_0", "quality_factor", "corner_frequency", "channel"]
        for value in values:
            if value not in self.current_state or \
                not self.current_state[value]:
                return
        result = { \
            "omega_0": self.current_state["omega_0"],
            "corner_frequency": self.current_state["corner_frequency"],
            "quality_factor": self.current_state["quality_factor"],
            "phase": self.current_state["pick"].phase_hint,
            "channel": self.current_state["channel"]}
        done = False
        for res in self.results:
            if res["channel"] == result["channel"] and \
                res["phase"] == result["phase"]:
                res.update(result)
                done = True
                break
        if done is False:
            self.results.append(result)
        model = ResultsTableView(self.results)
        self.ui.fit_table.setModel(model)
        self.ui.fit_table.resizeRowsToContents()
        self.ui.fit_table.resizeColumnsToContents()
        self.ui.fit_table.horizontalHeader().setStretchLastSection(True)

        self._calculate_final_values()

    def _calculate_final_values(self):
        """
        Takes every dict stored in self.results and produces the final output.
        """
        # If no results are available, nothing is to be done.
        if len(self.results) == 0:
            self.ui.mean_parameter_line_1.setText("-")
            self.ui.mean_parameter_line_2.setText("-")
            if hasattr(self, "current_status"):
                self.current_status["final_results"] = {}
            self.ui.save_file_button.setEnabled(False)
            return
        # Do all the calculations per station and phase.
        stations = {}
        for result in self.results:
            station = ".".join(result["channel"].split(".")[:2])
            if not station in stations:
                stations[station] = { \
                    "p": [],
                    "s": []}
            # The conditional is not strictly necessary but takes care that no
            # other phases slip in.
            if result["phase"].lower() == "p":
                stations[station]["p"].append(result)
            elif result["phase"].lower() == "s":
                stations[station]["s"].append(result)
        # Save the station count for later inclusion in the QuakeML file.
        station_count = len(stations.keys())
        # For every phase, calculate the seismic source parameters M_0 and r.
        # Also take the mean of all Q values, just because they are available.
        final_results = { \
            "M_0": [],
            "r": [],
            "Q": []}
        # Loop over all picks and calculate the values.
        for station_id, phases in stations.iteritems():
            for phase, results in phases.iteritems():
                if len(results) == 0:
                    continue
                # Collect the three variables extracted from the spectra.
                omega_0 = [_i["omega_0"] for _i in results]
                f_c = [_i["corner_frequency"] for _i in results]
                Q = [_i["quality_factor"] for _i in results]

                # The traveltime is necessary for the seismic moment
                # calculation.
                # XXX: This is also calculated for the pick table. Get it from
                # there!
                coordinates = None
                for pick in self.current_state["event"].picks:
                    if ("%s.%s" % (pick.data[0].stats.network,
                        pick.data[0].stats.station)) == station_id:
                        coordinates = pick.data[0].stats.coordinates
                if coordinates is None:
                    print "Warning: No coordinates for the station found."
                    continue
                # Hypocentral distance in meter.
                distance = lat_long_to_distance( \
                    self.current_state["event"].origins[0].latitude,
                    self.current_state["event"].origins[0].longitude,
                    self.current_state["event"].origins[0].depth,
                    coordinates.latitude,
                    coordinates.longitude,
                    coordinates.elevation / 1000.0) * 1000.0
                # Now everything necessary is available. Call the function
                # necessary to calculate everything.
                M_0 = moment_from_low_freq_amplitude(omega_0,
                    self.current_state["density"],
                    self.current_state["p_wave_speed"],
                    distance, phase)
                source_radius = source_radius_from_corner_frequency(f_c,
                    self.current_state["s_wave_speed"], phase)
                # Append it to the final result.
                final_results["M_0"].append(M_0)
                final_results["r"].append(source_radius)
                final_results["Q"].extend(Q)
        # Now calculate the composite result.
        station_count = len(final_results["M_0"])
        M_0 = sum(final_results["M_0"]) / float(len(final_results["M_0"]))
        mag = moment_to_moment_magnitude(M_0)
        source_radius = \
            sum(final_results["r"]) / float(len(final_results["r"]))
        stress_drop = calculate_stress_drop(M_0, source_radius)
        quality_factor = sum(final_results["Q"]) / \
            float(len(final_results["Q"]))
        self.final_result = { \
            "seismic_moment": M_0,
            "moment_magnitude": mag,
            "source_radius": source_radius,
            "stress_drop": stress_drop,
            "quality_factor": quality_factor,
            "station_count": station_count}
        string = u"M₀: %.3e [Nm] || Mw: %.3f || Q: %.1f" % \
            (M_0, mag, quality_factor)
        self.ui.mean_parameter_line_1.setText(string)
        string = u"Source radius: %.1f || Stress drop: %.2f" % \
            (source_radius, stress_drop / 1E5)
        self.ui.mean_parameter_line_2.setText(string)
        self.ui.save_file_button.setEnabled(True)

    def _open_event_selection_window(self):
        """
        Launches the select event window.
        """
        window = SelectEventWindow(str(self.ui.seishub_server.text()))
        window.closed.connect(self.show)
        window.event_chosen.connect(self.event_chosen)
        # Show the main window and bring it to the foreground.
        window.show()
        window.raise_()
        self.hide()
