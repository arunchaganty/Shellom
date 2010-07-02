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

    toMain=['import sys\nsys.dont_write_bytecode = False\nsys.path.append("..")\nimport snippets']

    s=soup.findAll( 'snippet' )
    if not s :
        print 'No snippets selected !'
        sys.exit( 1 )

    for c in s :
        io=c.findAll( 'field' )
        io = map( lambda x: x.string, io )
        #io=[ i.string for i in io]
        print io
        name = c[ 'task' ]
        toMain.append( 'if not snippets.%s.%s().validateInputs(%s) :\n\tprint "Error in %s !"\n\tsys.exit( -1 )'%( name, name, io, name ) )
        toMain.append( 'snippets.%s.%s().doJob(%s)'%( name, name, io ) )
        
    wf=open( workflow,'w' )
    wf.write( '\n'.join( toMain ) )
    wf.close()
