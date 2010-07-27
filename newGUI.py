#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
import os, re, subprocess, sys
sys.dont_write_bytecode = True
import snippets, xmlgenerator, xmlcompiler

if not os.access( 'tmp', os.W_OK ) :
    os.mkdir( 'tmp' )

class TreeWidget( QtGui.QTreeWidget ) :
    def mousePressEvent( self, e ) :
        if e.button() == QtCore.Qt.LeftButton :
            self.t = e.pos()
        QtGui.QTreeWidget.mousePressEvent( self, e )

    def dropEvent( self, e ) :
        target = self.itemAt( e.pos() )
        if target.parent() and not target.childCount() :
            target.setText( 2, QtCore.QString( self.itemAt( self.t ).text( 2 ) ) )


class SnippetItem( QtGui.QTreeWidgetItem ) :
    def __init__( self, name, parent ) :
        self = QtGui.QTreeWidgetItem( parent )
        self.setText( 0, name )
        self.setFlags( QtCore.Qt.NoItemFlags )

    def submitted( self ) :
        for i in xrange( self.childCount() ) :
            self.child( i ).setFlags( QtGui.QAbstractItemView.DragOnly )
            self.child( i ).setEditTriggers( QtGui.QAbstractItemView.NoEditTriggers )


class DetailsItem( QtGui.QTreeWidgetItem ) :
    def __init__( self, name, parent ) :
        self = QtGui.QTreeWidgetItem( parent )
        self.setText( name )

class Ui_MainWindow(  QtGui.QMainWindow ):
    snippetSelected = 0

    snipID = 1 # The ID that is assigned to a snippet in the XML file
    inputID = 1 # The ID assisgned to inputs
    xml = [ '<workflow>' ] # This list holds lines that will make up the XML file. It's a list because of faster appends than on strings

    oldSnipID = 1 # The ID, one more than the last snippet that worked. To be used when snippets fail and snipID needs to be reset

    def displaySnippet( self ) :
        if self.snippetSelected == 1 :
            temp = QtGui.QMessageBox.information( None,
            'Attention !',
            'You haven\'t submitted the current snippet\'s inputs. Do you want to continue ?',
            2,
            button1 = 1,
            button2 = 0 )
            # Cancel = 2, OK = 1

            if temp == 2 :
                return

            self.inputsList.takeTopLevelItem( self.inputsList.topLevelItemCount() -1 )

        #--------------------------------------------------------------------------------

        selection = str( self.snippetsList.currentItem().text() )
        snippet = getattr( getattr( snippets, selection ), selection )
        
        #--------------------------------------------------------------------------------
        
        for i in snippet.packages :
            if( os.system( "dpkg -l | awk '{ print $2 }' | tail -n +6 | grep %s > /dev/null"%i ) != 0 ) :
                try :
                    from __builtin__ import __import__
                    __import__( i )
                except ImportError :
                    QtGui.QMessageBox.warning( self, "Error !", '%s missing. Install the package before using this snippet.'%i )
                    return
        
        #--------------------------------------------------------------------------------

        node = QtGui.QTreeWidgetItem( self.inputsList )
        #node.setFlags( QtCore.Qt.NoItemFlags )
        node.setText( 0, snippet.sname )

        for i in snippet.details :
            item = QtGui.QTreeWidgetItem( node )
            item.setFlags( QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled )
            item.setText( 1, i )

        self.snippetSelected = 1
        self.inputsList.expandItem( node )

    def clearInputs( self ) :
        if self.snippetSelected == 1 :
            self.snippetSelected = 0
            self.inputsList.takeTopLevelItem( self.inputsList.topLevelItemCount() -1 )
            self.displaySnippet()


    def submitInputs( self ) :
        '''This function adds the current snippet to the XML.'''

        if self.snippetSelected == 2 :
            return

        # Make sure that a snippet is selected
        if self.currentSnippet == '' :
            return
        sn = getattr( getattr( snippets, self.currentSnippet ), self.currentSnippet ) # The current snippet class
        currentInputs = []
        lists = [] # A list of input-indices that are lists
        
        toBeShown = [[]]

        i = 0
        while i < self.tableWidget.rowCount() :
            newInput =  str( self.tableWidget.item( i , 1 ).text() )

            toBeShown[0].append( newInput )

            # Convert Shellom lists 'list( -, - )' to Python lists '[ -, - ]'
            if len( newInput ) > 4 and newInput[:4] == 'list' :
                lists.append( i )
                newInput = newInput[4:].strip().split( ', ' )
                newInput[0] = newInput[0][1:].strip()
                newInput[-1] = newInput[-1][:-1].strip()

            currentInputs.append( newInput )
            i += 1 

        if len( lists ) > 0 :
            lenLists = len( currentInputs[ lists[0] ] )
        else :
            lenLists = 0
        
        # Make sure that if there are lists, they are all of the same length
        for i in lists :
            if lenLists != len( currentInputs[i] ) :
                QtGui.QMessageBox.warning( self,
                        'Error', 'Lists entered are of different lengths. Try correcting them.' )
                return
        
        #If there are lists in the inputs :
        if lenLists != 0 :
            notLists = list( set( range( self.tableWidget.rowCount() ) ).difference( set( lists ) ) )
            notLists.sort()
        
            thisInput = [0] * self.tableWidget.rowCount()
            for i in notLists :
                thisInput[i] = currentInputs[i]

            # Make a copy of the XML so that if an input from a list is wrong,
            # we can reject all previous inputs from the list.
            copy = []
            copy.extend( self.xml )
        
            for i in range( lenLists ) :
                for j in lists :
                    thisInput[j] = currentInputs[j][i]
                tmp = xmlgenerator.getxml( copy, sn, thisInput, self.snipID, self.inputID )

                # I still don't know the cause of this bug :
                # *  thisInput contained a list of lists of inputs formed from the
                #    lists. But when appended to toBeShown, they just contained
                #    duplicates of the last list.append
                # *  SOLUTION - I use a copy of thisInput called debug
                debug = []
                debug.extend( thisInput )
                toBeShown.append( debug )
                
                # The input was invalid
                if tmp[:5] == list( 'ERROR' ) :
                    QtGui.QMessageBox.warning( self,
                            'Error', ''.join( tmp ) + '. Try rechecking your input. Inputs that preceeded this one in the list have not been processed.' )

                    #Revert to proper IDs
                    self.snipID = self.oldSnipID
                    self.inputID = self.oldInputID
                    return
                # _This_ set of inputs from the lists is valid
                else :
                    copy = tmp
                    self.snipID += 1
                    self.inputID += self.tableWidget.rowCount()

            self.showInTree( toBeShown )
            self.xml = copy

            # Make necessary changes to old IDs
            self.oldSnipID = self.snipID + 1
            self.oldInputID = self.inputID + 1

        # There is a single input :
        else :
            copy = []
            copy.extend( self.xml )
            tmp = xmlgenerator.getxml( copy, sn, currentInputs, self.snipID, self.inputID )
            if tmp[:5] == list( 'ERROR' ) :
                QtGui.QMessageBox.warning( self, 'Error !', ''.join( tmp ) + '. Try rechecking your inputs' )
                self.clear()
                return
            else :
                self.xml = tmp
                self.snipID += 1
                self.inputID += self.tableWidget.rowCount()
                self.showInTree( [currentInputs] )

            self.oldSnipID = self.snipID + 1
            self.oldInputID = self.inputID + 1



        print ''.join( self.xml )





    def setupUi( self, MainWindow ):
        MainWindow.setObjectName( "MainWindow" )
        MainWindow.resize( 640, 480 )
        sizePolicy = QtGui.QSizePolicy( QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred )
        sizePolicy.setHorizontalStretch( 0 )
        sizePolicy.setVerticalStretch( 0 )
        sizePolicy.setHeightForWidth( MainWindow.sizePolicy().hasHeightForWidth() )
        MainWindow.setSizePolicy( sizePolicy )
        MainWindow.setMinimumSize( QtCore.QSize( 640, 480 ) )
        MainWindow.setMaximumSize( QtCore.QSize( 640, 480 ) )

        self.centralwidget = QtGui.QWidget( MainWindow )
        self.centralwidget.setObjectName( "centralwidget" )
        
        self.snippetsList = QtGui.QListWidget( self.centralwidget )
        self.snippetsList.setGeometry( QtCore.QRect( 0, 0, 210, 400 ) )
        self.snippetsList.setObjectName( "snippetsList" )
        
        self.inputsList = TreeWidget( self.centralwidget )
        self.inputsList.setGeometry( QtCore.QRect( 210, 0, 451, 401 ) )
        self.inputsList.setMouseTracking( True )
        self.inputsList.setAcceptDrops( True )
        self.inputsList.setEditTriggers( QtGui.QAbstractItemView.AllEditTriggers )
        self.inputsList.setDragDropOverwriteMode( True )
        self.inputsList.setDragDropMode( QtGui.QAbstractItemView.DragDrop )
        self.inputsList.setSelectionBehavior( QtGui.QAbstractItemView.SelectItems )
        self.inputsList.setObjectName( "inputsList" )

        self.line = QtGui.QFrame( self.centralwidget )
        self.line.setGeometry( QtCore.QRect( 0, 410, 640, 3 ) )
        self.line.setFrameShape( QtGui.QFrame.HLine )
        self.line.setFrameShadow( QtGui.QFrame.Sunken )
        self.line.setObjectName( "line" )
        
        self.line_2 = QtGui.QFrame( self.centralwidget )
        self.line_2.setGeometry( QtCore.QRect( 360, 410, 3, 70 ) )
        self.line_2.setFrameShape( QtGui.QFrame.VLine )
        self.line_2.setFrameShadow( QtGui.QFrame.Sunken )
        self.line_2.setObjectName( "line_2" )
        
        self.finishButton = QtGui.QPushButton(self.centralwidget)
        self.finishButton.setGeometry(QtCore.QRect(460, 420, 87, 27))
        self.finishButton.setObjectName("finishButton")
        
        self.helpButton = QtGui.QPushButton(self.centralwidget)
        self.helpButton.setGeometry(QtCore.QRect(550, 420, 87, 27))
        self.helpButton.setObjectName("helpButton")
        
        self.insertListsButton = QtGui.QPushButton(self.centralwidget)
        self.insertListsButton.setGeometry(QtCore.QRect(370, 450, 87, 27))
        self.insertListsButton.setObjectName("insertListsButton")
        
        self.clearInputsButton = QtGui.QPushButton(self.centralwidget)
        self.clearInputsButton.setGeometry(QtCore.QRect(460, 450, 87, 27))
        self.clearInputsButton.setObjectName("clearInputsButton")
        
        self.submitButton = QtGui.QPushButton(self.centralwidget)
        self.submitButton.setGeometry(QtCore.QRect(370, 420, 87, 27))
        self.submitButton.setObjectName("submitButton")

        self.aboutButton = QtGui.QPushButton(self.centralwidget)
        self.aboutButton.setGeometry(QtCore.QRect(550, 450, 87, 27))
        self.aboutButton.setObjectName("aboutButton")
        
        MainWindow.setCentralWidget( self.centralwidget )

        self.retranslateUi( MainWindow )
        QtCore.QObject.connect( self.clearInputsButton, QtCore.SIGNAL( "clicked()" ), self.clearInputs )
        QtCore.QObject.connect( self.submitButton, QtCore.SIGNAL( "clicked()" ), self.submitInputs )
        QtCore.QObject.connect( self.snippetsList, QtCore.SIGNAL( "currentItemChanged( QListWidgetItem*,QListWidgetItem* )" ), self.displaySnippet )
        QtCore.QMetaObject.connectSlotsByName( MainWindow )
        
        # Populate the list with snippets
        s = filter( lambda x: x[0] != '_' and x != 'os' and x != 'sys' and x != 'module', dir( snippets ) )
        for i in s :
            self.snippetsList.addItem( i )



    def retranslateUi( self, MainWindow ):
        MainWindow.setWindowTitle( QtGui.QApplication.translate( "MainWindow", "Shellom", None, QtGui.QApplication.UnicodeUTF8 ) )
        __sortingEnabled = self.snippetsList.isSortingEnabled()
        self.snippetsList.setSortingEnabled( False )
        self.snippetsList.setSortingEnabled( __sortingEnabled )
        self.inputsList.headerItem().setText( 0, QtGui.QApplication.translate( "MainWindow", "Snippet", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.inputsList.headerItem().setText( 1, QtGui.QApplication.translate( "MainWindow", "Tag", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.inputsList.headerItem().setText( 2, QtGui.QApplication.translate( "MainWindow", "Input", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.finishButton.setText( QtGui.QApplication.translate( "MainWindow", "Finish", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.helpButton.setText( QtGui.QApplication.translate( "MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.insertListsButton.setText( QtGui.QApplication.translate( "MainWindow", "Inset Lists", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.clearInputsButton.setText( QtGui.QApplication.translate( "MainWindow", "Clear inputs", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.submitButton.setText( QtGui.QApplication.translate( "MainWindow", "Submit inputs", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.aboutButton.setText( QtGui.QApplication.translate( "MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8 ) )


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication( sys.argv )
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi( MainWindow )
    MainWindow.show()
    sys.exit( app.exec_() )
