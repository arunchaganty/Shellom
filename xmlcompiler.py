#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 09-06-2010
# Purpose - To parse a workflow's XML file and convert it to executable python
# code.

from BeautifulSoup import BeautifulStoneSoup
import sys
import repository

def compile( xmlFileName,workflow ) :
    """Compiles an XML file into python code for the workflow."""

    xmlFile=open( xmlFileName,'r' )
    if not xmlFile :
        print 'NONEXISTENT XML FILE or WRONG PATH'
        sys.exit( 1 )

    xml=xmlFile.read()
    xmlFile.close()
    soup=BeautifulStoneSoup(xml)

    toMain=['import sys\nsys.dont_write_bytecode = False\nsys.path.append("..")\nfrom repository import *']

    s=soup.workflow.findChild()
    if not s :
        print 'No snippets selected !'
        sys.exit( 1 )
    temp=[s]
    temp.extend( s.findNextSiblings() )
    for c in temp :
        io=c.findAll()
        io=[str( i.string ) for i in io]
        toMain.append( 'if not %s().validateInputs(%s) :\n\tprint "Error in %s !"\n\tsys.exit( -1 )'%( str( repository.allSnippets[ str( c.name ).upper() ] )[11:], io, str( repository.allSnippets[ str( c.name ).upper() ] )[11:] ) )
        toMain.append( '%s().doJob(%s)'%( str( repository.allSnippets[ str( c.name ).upper() ] )[11:], io ) )
        
    wf=open( workflow,'w' )
    wf.write( '\n'.join( toMain ) )
    wf.write( '\nimport os\nos.system( "rm repository.py" )\n' )
    wf.close()
