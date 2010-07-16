#!/usr/bin/env python

# Form implementation generated from reading ui file 'shellom.ui'
#
# Created: Fri Jul 16 10:24:57 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!
import os, re, subprocess
import snippets
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def showSnippet(self) :
        print 'showSnippet'

    def submitInputs(self) :
        print 'submitInputs'

    def getList(self) :
        print 'getList'

        #l = os.listdir( str( self.directoryLineEdit.text() ) )
        #l = filter( lambda x: re.match( '.*%s.*'%str( self.filterLineEdit.text() ), x ), l )
        #toBePut = 'list( %s )'%' ,'.join( l )

        x = subprocess.Popen( 'ls -a%s %s | grep %s'%( self.recursive.isChecked() and 'R' or ' ', str( self.directoryLineEdit.text() ) , str( self.filterLineEdit.text() ) ), shell=True, stdout=subprocess.PIPE )
        toBePut = 'list( %s )'%', '.join( x.communicate()[0].split('\n')[:-1] )
        self.listPlainTextEdit.clear()
        self.listPlainTextEdit.setPlainText( toBePut )
        return toBePut

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(701, 595)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 10, 231, 31))
        self.comboBox.setObjectName("comboBox")

        self.sSnippet = QtGui.QPushButton(self.centralwidget)
        self.sSnippet.setGeometry(QtCore.QRect(260, 10, 121, 31))
        self.sSnippet.setObjectName("sSnippet")

        self.sInputs = QtGui.QPushButton(self.centralwidget)
        self.sInputs.setGeometry(QtCore.QRect(110, 370, 85, 27))
        self.sInputs.setObjectName("sInputs")

        self.treeView = QtGui.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(400, 10, 281, 381))
        self.treeView.setObjectName("treeView")

        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 60, 371, 301))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        #self.tableWidget.setRowCount(1)

        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        #item = QtGui.QTableWidgetItem()
        #self.tableWidget.setItem(0, 0, item)

        self.getListLabel = QtGui.QLabel(self.centralwidget)
        self.getListLabel.setGeometry(QtCore.QRect(10, 420, 161, 21))
        self.getListLabel.setObjectName("getListLabel")

        self.recursive = QtGui.QCheckBox(self.centralwidget)
        self.recursive.setGeometry(QtCore.QRect(10, 450, 90, 22))
        self.recursive.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.recursive.setChecked(True)
        self.recursive.setObjectName("recursive")

        self.directoryLineEdit = QtGui.QLineEdit(self.centralwidget)
        self.directoryLineEdit.setGeometry(QtCore.QRect(90, 480, 151, 31))
        self.directoryLineEdit.setObjectName("directoryLineEdit")
        self.directoryLabel = QtGui.QLabel(self.centralwidget)
        self.directoryLabel.setGeometry(QtCore.QRect(20, 490, 57, 17))
        self.directoryLabel.setObjectName("directoryLabel")

        self.filterLabel = QtGui.QLabel(self.centralwidget)
        self.filterLabel.setGeometry(QtCore.QRect(20, 530, 181, 16))
        self.filterLabel.setObjectName("filterLabel")

        self.filterLineEdit = QtGui.QLineEdit(self.centralwidget)
        self.filterLineEdit.setGeometry(QtCore.QRect(210, 520, 113, 27))
        self.filterLineEdit.setObjectName("filterLineEdit")

        self.getListButton = QtGui.QPushButton(self.centralwidget)
        self.getListButton.setGeometry(QtCore.QRect(120, 560, 85, 27))
        self.getListButton.setObjectName("getListButton")

        self.listPlainTextEdit = QtGui.QPlainTextEdit(self.centralwidget)
        self.listPlainTextEdit.setGeometry(QtCore.QRect(390, 450, 271, 101))
        self.listPlainTextEdit.setReadOnly(True)
        self.listPlainTextEdit.setObjectName("listPlainTextEdit")

        self.listLabel = QtGui.QLabel(self.centralwidget)
        self.listLabel.setGeometry(QtCore.QRect(390, 420, 57, 17))
        self.listLabel.setObjectName("listLabel")

        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 400, 701, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")

        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(380, 0, 20, 411))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.sSnippet, QtCore.SIGNAL("clicked()"), self.showSnippet)
        QtCore.QObject.connect(self.getListButton, QtCore.SIGNAL("clicked()"), self.listPlainTextEdit.clear)
        QtCore.QObject.connect(self.sInputs, QtCore.SIGNAL("clicked()"), self.submitInputs)
        QtCore.QObject.connect(self.getListButton, QtCore.SIGNAL("clicked()"), self.getList)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #------------------------------------------------------------------------------------------------------

        s = filter( lambda x: x[0] != '_' and x != 'os' and x != 'sys' and x != 'module', dir( snippets ) )
        for i in s :
            self.comboBox.addItem( i )




    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.sSnippet.setText(QtGui.QApplication.translate("MainWindow", "Select Snippet", None, QtGui.QApplication.UnicodeUTF8))
        self.sInputs.setText(QtGui.QApplication.translate("MainWindow", "Submit Inputs", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MainWindow", "Input ID", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MainWindow", "Input details", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("MainWindow", "Input", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.getListLabel.setText(QtGui.QApplication.translate("MainWindow", "Form a list from a directory", None, QtGui.QApplication.UnicodeUTF8))
        self.recursive.setText(QtGui.QApplication.translate("MainWindow", "Recursive", None, QtGui.QApplication.UnicodeUTF8))
        self.directoryLabel.setText(QtGui.QApplication.translate("MainWindow", "Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.filterLabel.setText(QtGui.QApplication.translate("MainWindow", "Part of file name or extension", None, QtGui.QApplication.UnicodeUTF8))
        self.getListButton.setText(QtGui.QApplication.translate("MainWindow", "Get List", None, QtGui.QApplication.UnicodeUTF8))
        self.listLabel.setText(QtGui.QApplication.translate("MainWindow", "List", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

