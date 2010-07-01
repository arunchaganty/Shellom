#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 06-06-2010
# Purpose - The main script that is to be run.

import sys
sys.dont_write_bytecode = True
import os, tasks, xmlgenerator, xmlcompiler, repository

def main() :
    print '''Enter a snippet number to begin.
    To end, enter a negative snippet number.
    Please use absolute paths everywhere.'''

    s=repository.allSnippets
    print '-'*50

    oSnip=zip( range( len( s ) ), s.keys() )
    soSnip=map( str,oSnip )
    
    print '\n'.join( soSnip )
    choice=int( raw_input( '... ' ) )
    snipID=1
    inputID=1
    xml=[ '<workflow>' ]

    while choice>=0 :

        currentSnippet=oSnip[ choice ][ 1 ]
        inputsToBeGot=s[ currentSnippet  ].tags
        currentInputs=[]

        for i in range( len( inputsToBeGot ) ) :
            currentInputs.append( raw_input( '%d - %s ... '%( inputID, s[ currentSnippet ].details[i] ) ) )
            inputID+=1

        print currentInputs

        # Input validation also has to be done !!
        if True :#s[ currentSnippet ]().validateInputs( currentInputs ) :
            xml=xmlgenerator.getxml( xml, s[ currentSnippet ], currentInputs, snipID, inputID-len( inputsToBeGot ) )
            print xml

            if xml==list('ERROR') :
                print 'Error while generating XML ... Will Quit'
                sys.exit(1)

        else :
            inputID -= len( inputsToBeGot )
            print 'WRONG'*10
        print '-'*50            
        choice=int( raw_input( '... ' ) )
        snipID+=1

    xml.append( '</workflow>' )
    
    if not os.access( 'tmp', os.W_OK ) :
        os.mkdir( 'tmp' )
    xmlFile=open( 'tmp/workflow.xml', 'w' )
    xmlFile.write( ''.join( xml ) )
    xmlFile.close()

    xmlcompiler.compile( 'tmp/workflow.xml', 'tmp/workflow.py' )

    
if __name__=='__main__' :
    main()
