# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 15:44:10 2017

@author: Victor Rogalev
"""

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Dropbox\Python scripts\HDF5 converter\Converter_v2.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtWidgets, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(346, 149)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        
        self.btnBrowse = QtWidgets.QPushButton(Dialog)
        self.btnBrowse.setObjectName("btnBrowse")
        self.gridLayout.addWidget(self.btnBrowse, 0, 1, 1, 1)
        
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 2)
        
        self.Convert = QtWidgets.QPushButton(Dialog)
        self.Convert.setEnabled(False)
        self.Convert.setToolTipDuration(0)
        self.Convert.setObjectName("Convert")
        self.gridLayout.addWidget(self.Convert, 1, 1, 1, 1)
        
        self.Filename = QtWidgets.QLineEdit(Dialog)
        self.Filename.setObjectName("Filename")
        self.gridLayout.addWidget(self.Filename, 0, 0, 1, 1)
        
        self.Rename = QtWidgets.QRadioButton(Dialog)
        self.Rename.setChecked(True)
        self.Rename.setObjectName ("Rename")
        self.gridLayout.addWidget(self.Rename, 1, 0, 1, 1)
        
        self.History = QtWidgets.QTextEdit(Dialog)
        self.History.setFrameShape(QtWidgets.QFrame.Panel)
        self.History.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.History.setLineWidth(1)
        self.History.setObjectName("History")
        self.gridLayout.addWidget(self.History, 3, 0, 1, 3)
        self.History.setReadOnly(True)
        self.History.moveCursor(QtGui.QTextCursor.End)
        self.History.ensureCursorVisible

        Dialog.setWindowTitle("Convert SPESCLAb2 ---> HDF5")
        self.btnBrowse.setText("Browse")
        self.Convert.setText("Convert")
        self.Rename.setText("Must be checked if file(s) have repeating region names")
        self.Filename.setText("Choose file(s) to convert")
        self.History.setText("<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">Warning!!! </span></p><p><span style=\" font-weight:600;\">Make sure you use xml file in a </span><span style=\" font-weight:600; text-decoration: underline;\">COMPACT</span><span style=\" font-weight:600;\"> mode. </span><span style=\" font-weight:600; text-decoration: underline;\">Non-compact</span><span style=\" font-weight:600;\"> files works only for 1D data so far...</span></p></body></html>")

