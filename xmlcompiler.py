#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 09-06-2010
# Purpose - To parse a workflow's XML file and convert it to executable python
# code.

from BeautifulSoup import BeautifulStoneSoup
import sys

def compile( xmlFileName,workflow ) :
    """Compiles an XML file into python code for the workflow."""

    xmlFile=open( xmlFileName,'r' )
    if not xmlFile :
        print 'NONEXISTENT XML FILE or WRONG PATH'
        sys.exit( 1 )

    xml=xmlFile.read()
    xmlFile.close()
    soup=BeautifulStoneSoup(xml)

    toMain=['import sys, os\nsys.dont_write_bytecode = False\nsys.path.append("..")\nimport snippets']

    s=soup.findAll( 'snippet' )
    if not s :
        print 'No snippets selected !'
        sys.exit( 1 )

    for c in s :
        io=c.findAll( 'field' )
        io = map( lambda x: x.string, io )

        print io
        name = c[ 'task' ]
        toMain.append( 'curSnip = snippets.%s.%s()'%( name, name ) )
        toMain.append( "inList = %s\nfor i in range( len( inList ) ) :\n\tif curSnip.types[i] == 'path:r' :\n\t\tif not os.access( inList[i], os.R_OK ) :\n\t\t\tprint 'Error reading some input files due to malfunction of a previous snippet. Exiting ...'\n\t\t\tsys.exit( -1 )"%( io ) )
        toMain.append( 'if not curSnip.validateInputs(%s) :\n\tprint "Error in %s !"\n\tsys.exit( -1 )'%( io, name ) )
        toMain.append( 'curSnip.doJob(inList)' )
        
    wf=open( workflow,'w' )
    wf.write( '\n'.join( toMain ) )
    wf.close()
