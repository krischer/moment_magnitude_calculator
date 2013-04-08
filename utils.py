#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility functions and classes.

:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2012
:license:
    GNU General Public License, Version 3
    (http://www.gnu.org/copyleft/gpl.html)
"""
from PyQt4 import QtCore, QtGui, QtWebKit

import glob
import math
import numpy as np
from obspy.core import Stream, Trace, UTCDateTime
import os
import scipy.optimize


class GoogleMapsWebView(QtWebKit.QWebPage):
    """
    Subclass QWebPage to implement a custom user agent string and be able to
    debug Javascript.
    """
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


def lat_long_to_distance(lat1, lng1, depth1, lat2, lng2, depth2):
    """
    Calculates the distance in km between two points in lat/lng/depth. Only
    works for small distances as it simply converts to a x, y, z coordinate
    system.

    Dephts are in kilometer.
    """
    # Some constants. From wikipedia
    # (http://en.wikipedia.org/wiki/Longitude#Length_of_a_degree_of_longitude)
    a = 6378.1370
    b = 6356.7523142
    # Ellicpticity
    e = (a ** 2 - b ** 2) / (a ** 2)

    lats = [lat2, lat1]
    lats.sort()
    lngs = [lng2, lng1]
    lngs.sort()
    lat = lats[1] - lats[0]
    lng = lngs[1] - lngs[0]
    if lat > 180:
        lat = 360 - lat
    if lng > 180:
        lng = 360 - lng
    depth = abs(depth2 - depth1)
    # Just choose the first latitude for the longitude calculation.
    one_degree_lng = (math.pi * a * math.cos(math.radians(lat1))) / \
        (180.0 * (1.0 - e ** 2 * math.sin(math.radians(lat1)) ** 2) ** 0.5)

    # Now calculate the distance as a simple euclidean distance.
    # XXX: Approximate value. Calculate one.
    lat = 111.132 * lat
    lng = one_degree_lng * lng
    return math.sqrt((lat) ** 2 + (lng) ** 2 + (depth) ** 2)


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


def brune_source(duration, sampling_rate=200, variation_signal=0.625,
    stress_drop=50.0, shear_module=3.0E10, v_s=3.5, depth=20, distance=1):
    """
    Calculate a theoretical source after (Brune, 1970) as has been done in the
    PITSA source code.

    :param duration: How long the resulting signal should in [s].
    :param npts: Number of sample points of the resulting signal
    :param variation signal: The radiation pattern of the source.
    :param stress_drop: The stress drop in [bar].
    :param shear_module: The shear module in [Pa].
    :param v_s: The shear wave velocity in [km/s].
    :param depth: The depth in [km].
    :param distance: The distance in [km].

                sigma = 50.0;
                mu = 3.0e10;
                vs = 3.5;
                r = 1.0;
                z = 20.0;
    """
    # Convert some units.
    stress_drop *= 1.0E5  # bar -> Pa
    v_s *= 1000.0  # km/sec -> m/sec
    distance *= 1000.0  # km -> m
    depth *= 1000.0  # km -> m

    # Init time array.
    t = np.linspace(0, duration, duration * sampling_rate)

    # Calculate brune source.
    brune = 2.0 * variation_signal * stress_drop / shear_module * v_s * \
        distance / depth * t * np.exp(-2.34 * (v_s / distance) * t)
    brune = brune.astype("float64")

    # Create a ObsPy Stream object.
    trace = Trace(data=brune)
    trace.stats.sampling_rate = sampling_rate
    trace.stats.network = "SYN"
    trace.stats.station = "NTHET"
    trace.stats.location = "IC"
    trace.stats.channel = "ESZ"
    return Stream(traces=[trace])


def _three_values(value):
    """
    Will always return a list of three values. If value is already a list of
    three values, nothing will happen. If it is one, a list of three copies
    will be returned. If it is two, the third value will be the mean of the
    other two values.
    """
    # Try to convert to float and return with 3 copies
    try:
        value = 3 * [float(value)]
        return value
    except:
        pass
    if len(value) == 1:
        return 3 * value
    if len(value) > 3:
        msg = "Only up to three values possible."
        raise ValueError(msg)
    # Nothing to be done.
    if len(value) == 3:
        return list(value)
    if len(value) != 2:
        msg = "This should not happen."
        raise ValueError(msg)
    # If this point is reached, value will always contain 2 values.
    value = list(value)
    value.append((value[0] + value[1]) / 2.0)
    return value


def moment_from_low_freq_amplitude(low_freq_amplitude, density, wavespeed,
    distance, phase):
    """
    Calculates the seimic moment M_0 from the low frequency amplitude
    of a seismic source displacement spectrum. After (Brune, 1970).

    The used radiation pattern is the average radiation pattern over
    the focal sphere.

    :param low_freq_amplitude:  List of 3 low frequency amplitude in [m/s].
    :param density: Rock density in [kg/m^3].
    :param wavespeed: P-or S-wave speed in [m/s].
    :param distance: Hypocentral distance in [m].
    :phase: 'P' or 'S'. Determines the radiation pattern coefficient.
    :rtype: The Seismic moment in [Nm].
    """
    low_freq_amplitude = _three_values(low_freq_amplitude)
    # After Abercrombie and also Tsuboi
    if phase.lower() == "p":
        radiation_pattern = 0.52
    elif phase.lower() == "s":
        radiation_pattern = 0.63
    else:
        msg = "Unknown phase '%s'." % phase
        raise ValueError(msg)
    omega_0 = np.sqrt(low_freq_amplitude[0] ** 2 + \
        low_freq_amplitude[1] ** 2 + \
        low_freq_amplitude[2] ** 2)
    return 4 * np.pi * density * wavespeed ** 3 * distance * \
        omega_0 / radiation_pattern


def moment_to_moment_magnitude(seismic_moment):
    return 2.0 / 3 * (np.log10(seismic_moment) - 9.1)


def source_radius_from_corner_frequency(corner_frequencies, s_wave_vel, phase):
    """
    Calculates the source radius from the spectral corner
    frequency assuming a circular rupture.

    After (Madariaga, 1976).

    :param corner_frequency: Spectral corner frequency in [Hz].
        Can either be one or a list of three for all three components.
    :param s_wave_vel: The S-wave velocity.
    :phase: 'P' or 'S'. Determines the factor k.
    """
    corner_frequencies = _three_values(corner_frequencies)

    # According to (Madariaga, 1976).
    if phase.lower() == "p":
        k = 0.32
    elif phase.lower() == "s":
        k = 0.21
    else:
        msg = "Unknown phase '%s'." % phase
        raise ValueError(msg)
    return 3 * k * s_wave_vel / sum(corner_frequencies)


def calculate_stress_drop(seismic_moment, source_radius):
    """
    Calculate the stress drop after Eshelby, 1957.

    :param seismic_moment: The seismic moment in [Nm].
    :param source_radius: The source radius assuming circular rupture in [m].
    :rtype: Stress drop in [Pa].
    """
    return (7 * seismic_moment) / (16 * source_radius ** 3)


def calculate_source_spectrum(frequencies, omega_0, corner_frequency, Q,
    traveltime):
    """
    After Abercrombie and Boatwright.

    :param frequencies: Input array to perform the calculation on.
    :param omega_0: Low frequency amplitude in [meter x second].
    :param corner_frequency: Corner frequency in Hz.
    :param Q: Quality factor.
    :param traveltime: Hypocentral traveltime in [s].
    """
    num = omega_0 * np.exp(-np.pi * frequencies * traveltime / Q)
    denom = (1 + (frequencies / corner_frequency) ** 4) ** 0.5
    return num / denom


def fit_spectrum(spectrum, frequencies, traveltime, initial_omega_0,
    initial_f_c, Q):
    """
    """
    def f(frequencies, omega_0, f_c):
        return calculate_source_spectrum(frequencies, omega_0, f_c, Q,
        traveltime)
    popt, pcov = scipy.optimize.curve_fit(f, frequencies, spectrum, \
        p0=[initial_omega_0, initial_f_c], maxfev=100000)
    return popt[0], popt[1], pcov[0, 0], pcov[1, 1]
