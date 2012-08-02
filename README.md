# Moment Magnitude Calculator

### Requirements

 * Python >= 2.6
 * NumPy
 * SciPy
 * matplotlib
 * A recent [ObsPy](http://obspy.org) version
 * PyQt4
 * [mtspec](https://github.com/krischer/mtspec)
 * Access to a [SeisHub](http://www.seishub.org) server

### Installing/Running

It currently has no setup.py, so simply check it out and run it:

```
git clone git://github.com/krischer/moment_magnitude_calculator.git
cd moment_magnitude_calculator
python main.py
```

### Short Usage Guide
![Screenshot 1](https://raw.github.com/krischer/moment_magnitude_calculator/master/img/moment_mag_0.png)


Upon running main.py a window should pop up. Two things need to be done here:

1. Enter the correct SeisHub server in the top right corner.
2. Click the **Load event** button to choose an event.

Additionally you can specify how many buffer seconds of data to load around each pick; also in the top right corner.

---

![Screenshot 2](https://raw.github.com/krischer/moment_magnitude_calculator/master/img/moment_mag_1.png)

In this window you can search the SeisHub database for events.

1. Specify the search parameters.
2. Move the map to choose the search area.
3. Finally press the **Search for Events** button.
4. Pick an event on the map.
5. If the short summary is satisfactory, press the **Load Details** button to
   check for available picks.
6. Finally press the **Choose event** button.

Now the data will be downloaded and you will be returned to the previous window.


---

![Screenshot 3](https://raw.github.com/krischer/moment_magnitude_calculator/master/img/moment_mag_2.png)

Now you can estimate the source parameters and the moment magnitudes at as many stations as you desire. The estimate will usually be the most reliable if done for all stations, phases and channels.

1. Double click on a pick on the right hand side to load its data.
2. On the top left side, specify the window in one channel you want the spectrum to be calculated for. Simply click once to pick the start and once more to pick the end. The chosen window will then be highlighted.
3. The spectrum will appear in the lower left corner. The grey lines denote 95% jackknife confidence intervals.
4. An automatic fit of the theoretical source spectrum will be calculated. You can manually adjust it.
5. If you are satisfied, press **Accept** and the fitted parameters will show up on the right hand side.

** Rinse and repeat 1 to 5 until the parameters have been estimated at enough stations. **

6. Adapt the density and wave velocities on the right hand side to the given problem if necessary.
7. Click the **Write QuakeML** button to save the event as a QuakeML file to the filesystem.
