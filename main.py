#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 06-06-2010
# Purpose - The main script that is to be run.

import sys
sys.dont_write_bytecode = True
import os, tasks, xmlgenerator, xmlcompiler, snippets, subprocess, random

def main() :
    print '''Enter a snippet number to begin.
To end, enter a negative snippet number.
Please try and use absolute paths whereever possible.
Relative paths are relative to the main Shellom directory, from where main.py has been run.'''

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

        
        
        for i in currentSnippet.packages :
            if( os.system( "dpkg -l | awk '{ print $2 }' | tail -n +6 | grep %s > /dev/null"%i ) != 0 ) :
                print i + ' missing. Install the package before using this snippet.'
                sys.exit( -1 )



        lists = []
        more = 0
        for i in range( len( inputsToBeGot ) ) :
            ioro = 'i'
            if i == len( inputsToBeGot ) -1 :
                ioro = 'o'
            #currentInputs.append( 
            newInput = raw_input( '%s%d - %s ... '%( ioro, inputID + i + more, currentSnippet.details[i] ) )

            if len( newInput ) > 4 and newInput[:4] == 'list' :
                lists.append( i )
                newInput = newInput[4:].strip().split( ', ' )
                newInput[0] = newInput[0][1:].strip()
                newInput[-1] = newInput[-1][:-2].strip()
                more += len( newInput ) - 1

            currentInputs.append( newInput )

        
        if len( lists ) > 0 :
            lenLists = len( currentInputs[ lists[0] ] )
        else :
            lenLists = 0

        for i in lists :
            if lenLists != len( currentInputs[i] ) :
                print 'Lists incompatible. Exiting ...'
                sys.exit( -1 )

        if len( lists ) > 0 and lists[-1] != len( inputsToBeGot ) -1 :
            print 'The last input must be a list. Exiting.'
            sys.exit( -1 )
        if lenLists != 0 :
            notLists = list( set( range( len( inputsToBeGot ) ) ).difference( set( lists ) ) )
            notLists.sort()
    
            thisInput = [0] * len( inputsToBeGot )
            for i in notLists :
                thisInput[i] = currentInputs[i]
    
            for i in range( lenLists ) :
                for j in lists :
                    thisInput[j] = currentInputs[j][i]
                xml = xmlgenerator.getxml( xml, currentSnippet, thisInput, snipID, inputID )
                inputID += len( inputsToBeGot )
                snipID += 1
        else :
            xml = xmlgenerator.getxml( xml, currentSnippet, currentInputs, snipID, inputID )
        

        inputID += len( inputsToBeGot ) + more
        print ( xml )

        if xml[:5]==list('ERROR') :
            print ''.join(xml)
            sys.exit(1)

        print '-'*50            
        choice=int( raw_input( '... ' ) )
#        snipID+=1

    xml.append( '</workflow>' )
    
    xmlFile=open( 'tmp/workflow.xml', 'w' )
    xmlFile.write( ''.join( xml ) )
    xmlFile.close()

    xmlcompiler.compile( 'tmp/workflow.xml', 'tmp/workflow.py' )

    
if __name__=='__main__' :
    main()
