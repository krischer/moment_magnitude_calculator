#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple script that creates the icons used for displaying earthquakes.

Creates 11 icons in different sizes suitable for displaying hypocenters on a
map.

- icon_magnitude_-1.png
- icon_magnitude_0.png
- icon_magnitude_1.png
    ...
- icon_magnitude_9.png

:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2012
:license:
    GNU General Public License, Version 3
    (http://www.gnu.org/copyleft/gpl.html)
"""
from matplotlib import rc as matplotlibrc
matplotlibrc('figure.subplot', left=0.00, right=1.00, bottom=0.00, top=1.00)
import matplotlib.pylab as plt
import matplotlib.patches as patches


MIN_SIZE = 13
MAX_SIZE = 50
COLOR = 'red'
DPI = 100

# Loop 9 times to create 9 icons.
for i in xrange(-1, 10):
    # Calculate the size of the current icon.
    size = MIN_SIZE + (i + 1) * float(MAX_SIZE - MIN_SIZE) / 10.0

    fig = plt.figure(num=None, dpi=DPI,
                          figsize=(size / DPI, size / DPI))
    fig.set_figwidth(size / DPI)
    fig.set_figheight(size / DPI)
    ax = fig.add_subplot(111)

    circle = patches.Circle((0.5, 0.5), radius=0.45, edgecolor=COLOR,
                           facecolor=COLOR, alpha=0.5)
    plt.setp(ax, frame_on=False)
    ax.set_yticks([])
    ax.set_xticks([])

    ax.add_patch(circle)
    fig.savefig("icon_magnitude_%i.png" % i, transparent=True)
