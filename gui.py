#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
import os, re, subprocess, sys
sys.dont_write_bytecode = True
import snippets, xmlgenerator, xmlcompiler

if not os.access( 'tmp', os.W_OK ) :
    os.mkdir( 'tmp' )

helpText = '''1. To start, select a snippet and click 'Add snippet'.
2. Enter all the inputs and click either Add snippet ( after selecting the next snippet ) or Finish depending on whether or not you are done.
3. If there are any errors in the inputs, you will be allowed to correct them.
4. Click Finish when you are done. You can select where to store the workflow.

NOTES :
1. To make it easy for you to enter paths, select the cell where a path is required and click 'Insert Folder'. You have to fill in the file name manually though.
2. For batch operations, use the 'Insert List' button to insert a list of files into the cell currently selected.
3. If you have entered a list of inputs for a snippet, you might want to insert a list of files to store the snippet's outputs. Use 'Insert List' for that purpose as well.'''

class ListWidget( QtGui.QListWidget ) :
    def mousePressEvent( self, e ) :
        if e.button() == QtCore.Qt.LeftButton :
            self.t = e.pos()
        QtGui.QListWidget.mousePressEvent( self, e )

        


class TreeWidget( QtGui.QTreeWidget ) :
    def mousePressEvent( self, e ) :
        if e.button() == QtCore.Qt.LeftButton :
            self.t = e.pos()
            self.emit( QtCore.SIGNAL( 'dropFolder' ) )
        QtGui.QTreeWidget.mousePressEvent( self, e )

    def dropEvent( self, e ) :

        try :
            target = self.itemAt( e.pos() )
    
            if 1 :#type( e.source() ) == TreeWidget :
                if target.parent() == target.treeWidget().topLevelItem( target.treeWidget().topLevelItemCount() -1 ) and target.parent() and not target.childCount() :
                    target.setText( 2, QtCore.QString( self.itemAt( e.source().t ).text( 2 ) ) )
        except BaseException :
            pass
        



class Ui_MainWindow(  QtGui.QMainWindow ):

    snipID = 1 # The ID that is assigned to a snippet in the XML file
    inputID = 1 # The ID assisgned to inputs
    xml = [ '<workflow>' ] # This list holds lines that will make up the XML file. It's a list because of faster appends than on strings

    oldSnipID = 1 # The ID, one more than the last snippet that worked. To be used when snippets fail and snipID needs to be reset
    oldInputID = 1 # Analogous to above

    firstTime = True # Used to make sure the a submit action is not triggered the first time a snippet is added


    def displaySnippet( self ) :
        '''Displays the snippet selected'''
        if self.firstTime == False :
            x = self.submitInputs()
            if x == -2 :
                return -1
        else :
            self.firstTime = False

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
                    curSnip = ''
                    return -1
        
        #--------------------------------------------------------------------------------

        node = QtGui.QTreeWidgetItem( self.inputsList )
        node.setFlags( QtCore.Qt.ItemIsEnabled )
        node.setText( 0, snippet.sname )

        for i in snippet.details :
            item = QtGui.QTreeWidgetItem( node )
            item.setFlags( QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled )
            item.setText( 1, i )

        self.curSnip = snippet.sname
        self.inputsList.expandItem( node )




    
    
    def clearInputs( self ) :
        '''Clears the present snippet's inputs'''
        node = self.inputsList.topLevelItem( self.inputsList.topLevelItemCount() - 1 )
        
        if not node :
            return

        for i in range( node.childCount() ) :
            node.child( i ).setText( 2, '' )
    
    
    
    def setTreeProperties( self, toBeShown ) :
        '''Sets the previous snippet's inputs to be draggable but not editable when a new snippet is added'''
        root = self.inputsList.topLevelItem( self.inputsList.topLevelItemCount() - 1 )
        root.setFlags( QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled ) 

        for i in range( len( toBeShown[0] ) ) :
            root.child( i ).setFlags( QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled ) 

        toBeShown = toBeShown[1:]

        for i in range( root.childCount() ) :
            root.child( i ).setFlags( QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled ) 

        for input in toBeShown :
            item = QtGui.QTreeWidgetItem( root )
            item.setFlags( QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled )
            item.setText( 0, root.text( 0 ) )
            
            for j in range( len( input ) ) :
                field = input[j]
                f = QtGui.QTreeWidgetItem( item )
                f.setFlags( QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled )
                f.setText( 1, item.child( j ).text( 1 ) )
                f.setText( 2, field )

    
    def getInputs( self ) :
        '''Returns a list of inputs suitably formatted for other functions to take care of.'''
        currentInputs = []
        lists = [] # A list of input-indices that are lists
        
        toBeShown = [[]]

        i = 0
        node = self.inputsList.topLevelItem( self.inputsList.topLevelItemCount() - 1 )
        while i < node.childCount() :
            newInput =  str( node.child( i ).text( 2 ) )

            toBeShown[0].append( newInput )

            # Convert Shellom lists 'list( -, - )' to Python lists '[ -, - ]'
            if len( newInput ) > 4 and newInput[:4] == 'list' :
                lists.append( i )
                newInput = newInput[4:].strip().split( ', ' )
                newInput[0] = newInput[0][1:].strip()
                newInput[-1] = newInput[-1][:-1].strip()

            currentInputs.append( newInput )
            i += 1 

        return ( currentInputs, lists, toBeShown )


    
    
    
    
    
    def submitInputs( self ) :
        '''This function adds the current snippet to the XML.'''

        #if self.snippetSelected == 0  or self.curSnip == '' :
        #    return -2

        # Make sure that a snippet is selected
        selection = str( self.inputsList.topLevelItem( self.inputsList.topLevelItemCount() - 1 ).text( 0 ) )
        snippet = getattr( getattr( snippets, selection ), selection )

        currentInputs, lists, toBeShown = self.getInputs()


        if len( lists ) > 0 :
            lenLists = len( currentInputs[ lists[0] ] )
        else :
            lenLists = 0
        
        # Make sure that if there are lists, they are all of the same length
        for i in lists :
            if lenLists != len( currentInputs[i] ) :
                QtGui.QMessageBox.warning( self,
                        'Error', 'Lists entered are of different lengths. Try correcting them.' )
                return -2
        
        #If there are lists in the inputs :
        if lenLists != 0 :
            notLists = list( set( range( len( toBeShown[0] ) ) ).difference( set( lists ) ) )
            notLists.sort()
        
            thisInput = [0] * len( toBeShown[0] )
            for i in notLists :
                thisInput[i] = currentInputs[i]

            # Make a copy of the XML so that if an input from a list is wrong,
            # we can reject all previous inputs from the list.
            copy = []
            copy.extend( self.xml )
        
            for i in range( lenLists ) :
                for j in lists :
                    thisInput[j] = currentInputs[j][i]
                tmp = xmlgenerator.getxml( copy, snippet, thisInput, self.snipID, self.inputID )

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
                    return -2
                # _This_ set of inputs from the lists is valid
                else :
                    copy = tmp
                    self.snipID += 1
                    self.inputID += len( toBeShown[0] )

            self.setTreeProperties( toBeShown )
            self.xml = copy

            # Make necessary changes to old IDs
            self.oldSnipID = self.snipID + 1
            self.oldInputID = self.inputID + 1

        # There is a single input :
        else :
            copy = []
            copy.extend( self.xml )
            tmp = xmlgenerator.getxml( copy, snippet, currentInputs, self.snipID, self.inputID )
            if tmp[:5] == list( 'ERROR' ) :
                QtGui.QMessageBox.warning( self, 'Error !', ''.join( tmp ) + '. Try rechecking your inputs' )
                #self.clear()
                return -2
            else :
                self.xml = tmp
                self.snipID += 1
                self.inputID += len( currentInputs )
                self.setTreeProperties( [currentInputs] )

            self.oldSnipID = self.snipID + 1
            self.oldInputID = self.inputID + 1



        print ''.join( self.xml ), '\n\n\n\n\n\n'




    def finishWorkflow(self) :
        '''Writes and compiles the XML file to form an executable workflow.'''

        try :
            returnCode = self.submitInputs()
        except BaseException :
            return
        if returnCode :
            return
        self.xml.append( '</workflow>')

        outputFile = QtGui.QFileDialog.getSaveFileName( parent = self, caption = "Select where to store workflow ... " )
        outputFile = outputFile.split( '.' )

        xmlFile=open( 'tmp/workflow.xml', 'w' )
        xmlFile.write( ''.join( self.xml ) )
        xmlFile.close()
    
        xmlcompiler.compile( 'tmp/workflow.xml', 'tmp/workflow.py' )

        sys.exit( 0 )


    
  
    def insertFolder( self ) :
        '''Used to insert a folder at the cell currently selected in the tree of inputs.'''
        if len( self.inputsList.selectedItems() ) == 0  or self.inputsList.selectedItems()[0].isDisabled() == True :
            QtGui.QMessageBox.warning( self, 'Error !', 'First select an input cell from the current snippet.' )
            return
            
        outputFolder = QtGui.QFileDialog.getExistingDirectory( parent = self, caption = "Select the folder ... " )

        target = self.inputsList.selectedItems()[0]
        target.setText( 2, outputFolder )


  
    def insertLists( self ) :
        '''Used to insert a list of input or output files'''
        if len( self.inputsList.selectedItems() ) == 0  or self.inputsList.selectedItems()[0].isDisabled() == True :
            QtGui.QMessageBox.warning( self, 'Error !', 'First select an input cell from the current snippet.' )
            return

        inputOrOutput = QtGui.QMessageBox.question( self, 'Input or output ?', 'Do you want to input a list?\nDo you want to fill in a list of random output files ?\nPress OK for the former', 2, button1 = 0, button2 = 1 ) - 1

        if inputOrOutput == 0 :
            folder = str( QtGui.QFileDialog.getExistingDirectory( parent = self, caption = "Select the folder ... " ) )
            recursive = QtGui.QMessageBox.question( self, 'Recursive ?', 'Search recursively ?', 2, button1 = 0, button2 = 1 ) - 1
            filterString = QtGui.QInputDialog.getText( self, 'Filter String', 'Enter a part of the file name or extension' )
            
            if filterString[1] == False :
                return
            filterString = filterString[0]

            if recursive == 1:
                ourList = filter( lambda x : re.match( '.*%s.*'%filterString, x ), os.listdir( folder ) )

            else :
                ourList = []
                gen = os.walk( folder )
                while 1 :
                    try :
                        fileListTuple = gen.next()[1:]

                        fileList = []
                        for i in fileListTuple :
                            fileList.extend( i )
                        
                        ourList.extend( filter( lambda x : re.match( '.*%s.*'%filterString, x ), fileList ) )
                    except BaseException :
                        break
            self.inputsList.selectedItems()[0].setText( 2, ( 'list( %s )'%', '.join( ourList ) ) )
        else :
            folder = str( QtGui.QFileDialog.getExistingDirectory( parent = self, caption = "Select the folder ... " ) )
            if folder != '' :
                folder += '/'

            self.inputsList.selectedItems()[0].setText( 2, '' )

            fileName = QtGui.QInputDialog.getText( self, 'How should the file name be ?', 'Enter a filename with extension.\nThe selected cell will be filled with a list of names like (filename)(random number).(extension).' )
            
            if fileName[1] == False :
                return
            fileName = str( fileName[0] )
            
            i = 0
            node = self.inputsList.topLevelItem( self.inputsList.topLevelItemCount() - 1 )
            while i < node.childCount()  :
                cur = str( node.child( i ).text( 2 ) )
                if len( cur ) <= 6 or cur[:5] != 'list(' or cur[-1] != ')' :
                    i += 1
                    continue
                length = len( cur[5:][:-1].strip().split(',') )
                
                template = fileName.split( '.' )
            
                out = []
                import random
                for i in range( length ) :
                    if len( template ) == 1 :
                        out.append( '%s%s%d'%( folder, template[0], random.randint( 0, 100*length ) ) )
                    else :
                        out.append( '%s%s%d.%s'%( folder, template[0], random.randint( 0, 100*length ), '.'.join( template[1:] ) ) )

                self.inputsList.selectedItems()[0].setText( 2, ( 'list( %s )'%', '.join( out ) ) )
                break

            if i == node.childCount()  and str( self.inputsList.selectedItems()[0].text( 2 ) ) == '' :
                QtGui.QMessageBox.warning( self, 'Error !', 'None of your inputs have a properly formatted list.' )



    def helpMe( self ) :
        h = QtGui.QTextEdit(self)
        h.setGeometry( QtCore.QRect( 280, 50, 460, 401 ) )
        h.setWindowFlags( QtCore.Qt.Dialog )
        h.setReadOnly( True )
        h.append( helpText )
        h.show()




  
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
        
        self.snippetsList = ListWidget( self.centralwidget )
        self.snippetsList.setGeometry(QtCore.QRect(0, 20, 180, 360))
        self.snippetsList.setDragDropMode( QtGui.QAbstractItemView.DragOnly )
        self.snippetsList.setObjectName( "snippetsList" )
        
        self.inputsList = TreeWidget( self.centralwidget )
        self.inputsList.setGeometry( QtCore.QRect( 180, 0, 460, 401 ) )
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
        
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(450, 410, 3, 70))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        
        self.finishButton = QtGui.QPushButton(self.centralwidget)
        self.finishButton.setGeometry(QtCore.QRect(460, 420, 87, 27))
        self.finishButton.setObjectName("finishButton")
        
        self.helpButton = QtGui.QPushButton(self.centralwidget)
        self.helpButton.setGeometry(QtCore.QRect(550, 450, 87, 27))
        self.helpButton.setObjectName("helpButton")
        
        self.insertListsButton = QtGui.QPushButton(self.centralwidget)
        self.insertListsButton.setGeometry(QtCore.QRect(460, 450, 87, 27))
        self.insertListsButton.setObjectName("insertListsButton")
        
        self.clearInputsButton = QtGui.QPushButton(self.centralwidget)
        self.clearInputsButton.setGeometry(QtCore.QRect(550, 420, 87, 27))
        self.clearInputsButton.setObjectName("clearInputsButton")

        self.addSnippetButton = QtGui.QPushButton(self.centralwidget)
        self.addSnippetButton.setGeometry(QtCore.QRect(0, 380, 87, 27))
        self.addSnippetButton.setObjectName("addSnippetButton")

        self.insertFileOrFolderButton = QtGui.QPushButton(self.centralwidget)
        self.insertFileOrFolderButton.setGeometry(QtCore.QRect(90, 380, 80, 27))
        self.insertFileOrFolderButton.setObjectName("insertFileOrFolderButton")

        self.snippetsLabel = QtGui.QLabel(self.centralwidget)
        self.snippetsLabel.setGeometry(QtCore.QRect(0, 0, 210, 17))
        self.snippetsLabel.setObjectName("snippetsLabel")

        MainWindow.setCentralWidget( self.centralwidget )

        self.retranslateUi( MainWindow )
        QtCore.QObject.connect( self.clearInputsButton, QtCore.SIGNAL( "clicked()" ), self.clearInputs )
        QtCore.QObject.connect(self.addSnippetButton, QtCore.SIGNAL("clicked()"), self.displaySnippet )
        QtCore.QObject.connect(self.finishButton, QtCore.SIGNAL("clicked()"), self.finishWorkflow )
        QtCore.QObject.connect(self.insertFileOrFolderButton, QtCore.SIGNAL("clicked()"), self.insertFolder )
        QtCore.QObject.connect(self.insertListsButton, QtCore.SIGNAL("clicked()"), self.insertLists )
        QtCore.QObject.connect(self.helpButton, QtCore.SIGNAL("clicked()"), self.helpMe )
        QtCore.QMetaObject.connectSlotsByName( MainWindow )
        
        # Populate the list with snippets
        s = filter( lambda x: x[0] != '_' and x != 'os' and x != 'sys' and x != 'module', dir( snippets ) )
        for i in s :
            item = QtGui.QListWidgetItem( i )
            self.snippetsList.addItem( item )
            item.setFlags( QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled )
            self.snippetsList.addItem( item )



    def retranslateUi( self, MainWindow ):
        MainWindow.setWindowTitle( QtGui.QApplication.translate( "MainWindow", "Shellom", None, QtGui.QApplication.UnicodeUTF8 ) )
        __sortingEnabled = self.snippetsList.isSortingEnabled()
        self.snippetsList.setSortingEnabled( False )
        self.snippetsList.setSortingEnabled( __sortingEnabled )
        self.inputsList.headerItem().setFlags( QtCore.Qt.NoItemFlags )
        self.inputsList.headerItem().setText( 0, QtGui.QApplication.translate( "MainWindow", "Snippet", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.inputsList.headerItem().setText( 1, QtGui.QApplication.translate( "MainWindow", "Tag", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.inputsList.headerItem().setText( 2, QtGui.QApplication.translate( "MainWindow", "Input", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.finishButton.setText( QtGui.QApplication.translate( "MainWindow", "Finish", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.helpButton.setText( QtGui.QApplication.translate( "MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.insertListsButton.setText( QtGui.QApplication.translate( "MainWindow", "Insert List", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.clearInputsButton.setText( QtGui.QApplication.translate( "MainWindow", "Clear inputs", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.addSnippetButton.setText(QtGui.QApplication.translate("MainWindow", "Add snippet", None, QtGui.QApplication.UnicodeUTF8))
        self.insertFileOrFolderButton.setText(QtGui.QApplication.translate("MainWindow", "Insert folder", None, QtGui.QApplication.UnicodeUTF8))
        self.snippetsLabel.setText(QtGui.QApplication.translate("MainWindow", " Snippets :", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication( sys.argv )
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi( MainWindow )
    MainWindow.show()
    sys.exit( app.exec_() )
