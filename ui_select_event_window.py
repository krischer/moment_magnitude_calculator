# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui_files/ui_select_event_window.ui'
#
# Created: Mon Jul 16 01:49:22 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SelectEventWindow(object):
    def setupUi(self, SelectEventWindow):
        SelectEventWindow.setObjectName(_fromUtf8("SelectEventWindow"))
        SelectEventWindow.setEnabled(True)
        SelectEventWindow.resize(1100, 700)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SelectEventWindow.sizePolicy().hasHeightForWidth())
        SelectEventWindow.setSizePolicy(sizePolicy)
        SelectEventWindow.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtGui.QWidget(SelectEventWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.webView = QtWebKit.QWebView(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webView.sizePolicy().hasHeightForWidth())
        self.webView.setSizePolicy(sizePolicy)
        self.webView.setObjectName(_fromUtf8("webView"))
        self.gridLayout_2.addWidget(self.webView, 0, 0, 3, 2)
        self.choose_event_button = QtGui.QPushButton(self.centralwidget)
        self.choose_event_button.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choose_event_button.sizePolicy().hasHeightForWidth())
        self.choose_event_button.setSizePolicy(sizePolicy)
        self.choose_event_button.setObjectName(_fromUtf8("choose_event_button"))
        self.gridLayout_2.addWidget(self.choose_event_button, 3, 3, 1, 1)
        self.cancel_button = QtGui.QPushButton(self.centralwidget)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.gridLayout_2.addWidget(self.cancel_button, 3, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(242, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 3, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(599, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 3, 1, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(148, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 3)
        self.starttime = QtGui.QDateTimeEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.starttime.sizePolicy().hasHeightForWidth())
        self.starttime.setSizePolicy(sizePolicy)
        self.starttime.setDateTime(QtCore.QDateTime(QtCore.QDate(2012, 1, 1), QtCore.QTime(0, 0, 0)))
        self.starttime.setCalendarPopup(True)
        self.starttime.setObjectName(_fromUtf8("starttime"))
        self.gridLayout.addWidget(self.starttime, 0, 4, 1, 2)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(138, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 1, 1, 3)
        self.endtime = QtGui.QDateTimeEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.endtime.sizePolicy().hasHeightForWidth())
        self.endtime.setSizePolicy(sizePolicy)
        self.endtime.setDateTime(QtCore.QDateTime(QtCore.QDate(2012, 12, 1), QtCore.QTime(0, 0, 0)))
        self.endtime.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(7999, 12, 31), QtCore.QTime(23, 59, 59)))
        self.endtime.setCalendarPopup(True)
        self.endtime.setObjectName(_fromUtf8("endtime"))
        self.gridLayout.addWidget(self.endtime, 1, 4, 1, 2)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 2)
        spacerItem4 = QtGui.QSpacerItem(178, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 2, 2, 1, 3)
        self.min_magnitude = QtGui.QDoubleSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.min_magnitude.sizePolicy().hasHeightForWidth())
        self.min_magnitude.setSizePolicy(sizePolicy)
        self.min_magnitude.setDecimals(1)
        self.min_magnitude.setMinimum(-5.0)
        self.min_magnitude.setMaximum(10.0)
        self.min_magnitude.setProperty("value", -3.0)
        self.min_magnitude.setObjectName(_fromUtf8("min_magnitude"))
        self.gridLayout.addWidget(self.min_magnitude, 2, 5, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 2)
        spacerItem5 = QtGui.QSpacerItem(188, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 3, 2, 1, 3)
        self.max_magnitude = QtGui.QDoubleSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.max_magnitude.sizePolicy().hasHeightForWidth())
        self.max_magnitude.setSizePolicy(sizePolicy)
        self.max_magnitude.setDecimals(1)
        self.max_magnitude.setMinimum(-5.0)
        self.max_magnitude.setMaximum(10.0)
        self.max_magnitude.setProperty("value", 5.0)
        self.max_magnitude.setObjectName(_fromUtf8("max_magnitude"))
        self.gridLayout.addWidget(self.max_magnitude, 3, 5, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setStyleSheet(_fromUtf8("font: 11pt \"Lucida Grande\";"))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 3)
        spacerItem6 = QtGui.QSpacerItem(148, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 4, 3, 1, 2)
        self.northeast_label = QtGui.QLabel(self.groupBox)
        self.northeast_label.setStyleSheet(_fromUtf8("font: 11pt \"Lucida Grande\";"))
        self.northeast_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.northeast_label.setObjectName(_fromUtf8("northeast_label"))
        self.gridLayout.addWidget(self.northeast_label, 4, 5, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setStyleSheet(_fromUtf8("font: 11pt \"Lucida Grande\";"))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 3)
        spacerItem7 = QtGui.QSpacerItem(148, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem7, 5, 3, 1, 2)
        self.southwest_label = QtGui.QLabel(self.groupBox)
        self.southwest_label.setStyleSheet(_fromUtf8("font: 11pt \"Lucida Grande\";"))
        self.southwest_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.southwest_label.setObjectName(_fromUtf8("southwest_label"))
        self.gridLayout.addWidget(self.southwest_label, 5, 5, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem8)
        self.search_events_button = QtGui.QPushButton(self.groupBox)
        self.search_events_button.setObjectName(_fromUtf8("search_events_button"))
        self.horizontalLayout_2.addWidget(self.search_events_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addWidget(self.groupBox, 0, 2, 1, 2)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_4.addWidget(self.label_7, 0, 0, 1, 1)
        spacerItem9 = QtGui.QSpacerItem(258, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem9, 0, 1, 1, 2)
        self.selected_event_id_label = QtGui.QLabel(self.groupBox_2)
        self.selected_event_id_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.selected_event_id_label.setObjectName(_fromUtf8("selected_event_id_label"))
        self.gridLayout_4.addWidget(self.selected_event_id_label, 0, 3, 1, 3)
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)
        spacerItem10 = QtGui.QSpacerItem(258, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem10, 1, 1, 1, 2)
        self.selected_latitude_label = QtGui.QLabel(self.groupBox_2)
        self.selected_latitude_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.selected_latitude_label.setObjectName(_fromUtf8("selected_latitude_label"))
        self.gridLayout_4.addWidget(self.selected_latitude_label, 1, 3, 1, 3)
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_4.addWidget(self.label_9, 2, 0, 1, 1)
        spacerItem11 = QtGui.QSpacerItem(258, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem11, 2, 1, 1, 4)
        self.selected_longitude_label = QtGui.QLabel(self.groupBox_2)
        self.selected_longitude_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.selected_longitude_label.setObjectName(_fromUtf8("selected_longitude_label"))
        self.gridLayout_4.addWidget(self.selected_longitude_label, 2, 5, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox_2)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_4.addWidget(self.label_12, 3, 0, 1, 1)
        spacerItem12 = QtGui.QSpacerItem(258, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem12, 3, 1, 1, 3)
        self.selected_depth_label = QtGui.QLabel(self.groupBox_2)
        self.selected_depth_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.selected_depth_label.setObjectName(_fromUtf8("selected_depth_label"))
        self.gridLayout_4.addWidget(self.selected_depth_label, 3, 4, 1, 2)
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_4.addWidget(self.label_10, 4, 0, 1, 1)
        spacerItem13 = QtGui.QSpacerItem(238, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem13, 4, 2, 1, 3)
        self.selected_origin_time_label = QtGui.QLabel(self.groupBox_2)
        self.selected_origin_time_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.selected_origin_time_label.setObjectName(_fromUtf8("selected_origin_time_label"))
        self.gridLayout_4.addWidget(self.selected_origin_time_label, 4, 5, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox_2)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_4.addWidget(self.label_11, 5, 0, 1, 1)
        spacerItem14 = QtGui.QSpacerItem(238, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem14, 5, 2, 1, 3)
        self.selected_magnitude_label = QtGui.QLabel(self.groupBox_2)
        self.selected_magnitude_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.selected_magnitude_label.setObjectName(_fromUtf8("selected_magnitude_label"))
        self.gridLayout_4.addWidget(self.selected_magnitude_label, 5, 5, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem15 = QtGui.QSpacerItem(178, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem15)
        self.selected_event_load_details = QtGui.QPushButton(self.groupBox_2)
        self.selected_event_load_details.setEnabled(False)
        self.selected_event_load_details.setObjectName(_fromUtf8("selected_event_load_details"))
        self.horizontalLayout.addWidget(self.selected_event_load_details)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_13 = QtGui.QLabel(self.groupBox_2)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_3.addWidget(self.label_13, 0, 0, 1, 1)
        spacerItem16 = QtGui.QSpacerItem(138, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem16, 0, 1, 1, 1)
        self.selected_event_p_phase_picks = QtGui.QLabel(self.groupBox_2)
        self.selected_event_p_phase_picks.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.selected_event_p_phase_picks.setObjectName(_fromUtf8("selected_event_p_phase_picks"))
        self.gridLayout_3.addWidget(self.selected_event_p_phase_picks, 0, 2, 1, 1)
        self.label_14 = QtGui.QLabel(self.groupBox_2)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_3.addWidget(self.label_14, 1, 0, 1, 1)
        spacerItem17 = QtGui.QSpacerItem(138, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem17, 1, 1, 1, 1)
        self.selected_event_s_phase_picks = QtGui.QLabel(self.groupBox_2)
        self.selected_event_s_phase_picks.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.selected_event_s_phase_picks.setObjectName(_fromUtf8("selected_event_s_phase_picks"))
        self.gridLayout_3.addWidget(self.selected_event_s_phase_picks, 1, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        spacerItem18 = QtGui.QSpacerItem(20, 2, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem18)
        self.selected_event_warning = QtGui.QLabel(self.groupBox_2)
        self.selected_event_warning.setStyleSheet(_fromUtf8("color: red"))
        self.selected_event_warning.setText(_fromUtf8(""))
        self.selected_event_warning.setObjectName(_fromUtf8("selected_event_warning"))
        self.verticalLayout_2.addWidget(self.selected_event_warning)
        self.gridLayout_2.addWidget(self.groupBox_2, 2, 2, 1, 2)
        spacerItem19 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem19, 1, 2, 1, 1)
        SelectEventWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SelectEventWindow)
        QtCore.QMetaObject.connectSlotsByName(SelectEventWindow)

    def retranslateUi(self, SelectEventWindow):
        SelectEventWindow.setWindowTitle(QtGui.QApplication.translate("SelectEventWindow", "Select Event", None, QtGui.QApplication.UnicodeUTF8))
        self.choose_event_button.setText(QtGui.QApplication.translate("SelectEventWindow", "Choose event", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_button.setText(QtGui.QApplication.translate("SelectEventWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("SelectEventWindow", "Event search", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SelectEventWindow", "Min. date:", None, QtGui.QApplication.UnicodeUTF8))
        self.starttime.setDisplayFormat(QtGui.QApplication.translate("SelectEventWindow", "MMM dd yyyy HH:mm ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SelectEventWindow", "Max. date:", None, QtGui.QApplication.UnicodeUTF8))
        self.endtime.setDisplayFormat(QtGui.QApplication.translate("SelectEventWindow", "MMM dd yyyy HH:mm ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("SelectEventWindow", "Min. magnitude:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("SelectEventWindow", "Max. magnitude", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("SelectEventWindow", "Northeast Corner (lat, long):", None, QtGui.QApplication.UnicodeUTF8))
        self.northeast_label.setText(QtGui.QApplication.translate("SelectEventWindow", "0.00, 0.00", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("SelectEventWindow", "Southwest Corner (lat, long):", None, QtGui.QApplication.UnicodeUTF8))
        self.southwest_label.setText(QtGui.QApplication.translate("SelectEventWindow", "0.00, 0.00", None, QtGui.QApplication.UnicodeUTF8))
        self.search_events_button.setText(QtGui.QApplication.translate("SelectEventWindow", "Search for Events", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("SelectEventWindow", "Selected Event", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("SelectEventWindow", "Event id:", None, QtGui.QApplication.UnicodeUTF8))
        self.selected_event_id_label.setText(QtGui.QApplication.translate("SelectEventWindow", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("SelectEventWindow", "Lat:", None, QtGui.QApplication.UnicodeUTF8))
        self.selected_latitude_label.setText(QtGui.QApplication.translate("SelectEventWindow", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("SelectEventWindow", "Lng:", None, QtGui.QApplication.UnicodeUTF8))
        self.selected_longitude_label.setText(QtGui.QApplication.translate("SelectEventWindow", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("SelectEventWindow", "Depth:", None, QtGui.QApplication.UnicodeUTF8))
        self.selected_depth_label.setText(QtGui.QApplication.translate("SelectEventWindow", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("SelectEventWindow", "Origin Time:", None, QtGui.QApplication.UnicodeUTF8))
        self.selected_origin_time_label.setText(QtGui.QApplication.translate("SelectEventWindow", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("SelectEventWindow", "Magnitude:", None, QtGui.QApplication.UnicodeUTF8))
        self.selected_magnitude_label.setText(QtGui.QApplication.translate("SelectEventWindow", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.selected_event_load_details.setText(QtGui.QApplication.translate("SelectEventWindow", "Load Details", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("SelectEventWindow", "Number of P-phase picks:", None, QtGui.QApplication.UnicodeUTF8))
        self.selected_event_p_phase_picks.setText(QtGui.QApplication.translate("SelectEventWindow", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("SelectEventWindow", "Number of S-phase picks:", None, QtGui.QApplication.UnicodeUTF8))
        self.selected_event_s_phase_picks.setText(QtGui.QApplication.translate("SelectEventWindow", "-", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
