#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 06-06-2010
# Purpose - The main script that is to be run.

import sys
sys.dont_write_bytecode = True
import os, tasks, xmlgenerator, xmlcompiler, snippets

def main() :
    print '''Enter a snippet number to begin.
    To end, enter a negative snippet number.
    Please use absolute paths everywhere.'''

    s = filter( lambda x: x[0] != '_' and x != 'os' and x != 'sys' and x != 'module', dir( snippets ) )
    print '-'*50

    oSnip=zip( range( len( s ) ), s )
    soSnip=map( str,oSnip )
    
    print '\n'.join( soSnip )
    choice=int( raw_input( '... ' ) )
    snipID=1
    inputID=1
    xml=[ '<workflow>' ]

    if not os.access( 'tmp', os.W_OK ) :
        os.mkdir( 'tmp' )

    while choice>=0 :

        currentSnippet=getattr( getattr( snippets, oSnip[ choice ][1] ), oSnip[ choice ][1] )
        inputsToBeGot=currentSnippet.tags
        currentInputs=[]

        for i in range( len( inputsToBeGot ) ) :
            ioro = 'i'
            if i == len( inputsToBeGot ) -1 :
                ioro = 'o'
            currentInputs.append( raw_input( '%s%d - %s ... '%( ioro, inputID, currentSnippet.details[i] ) ) )
            inputID+=1

        #print currentInputs

        if True :#s[ currentSnippet ]().validateInputs( currentInputs ) :
            xml=xmlgenerator.getxml( xml, currentSnippet, currentInputs, snipID, inputID-len( inputsToBeGot ) )
            # THIS IS WHAT YOU SHOULD BE UNCOMMENTING DURING DEBUG SESSIONSprint xml

            if xml[:5]==list('ERROR') :
                print ''.join(xml) #'Error while generating XML ... Will Quit'
                sys.exit(1)

        else :
            inputID -= len( inputsToBeGot )
            print 'WRONG'*10
        print '-'*50            
        choice=int( raw_input( '... ' ) )
        snipID+=1

    xml.append( '</workflow>' )
    
    xmlFile=open( 'tmp/workflow.xml', 'w' )
    xmlFile.write( ''.join( xml ) )
    xmlFile.close()

    xmlcompiler.compile( 'tmp/workflow.xml', 'tmp/workflow.py' )

    
if __name__=='__main__' :
    main()
