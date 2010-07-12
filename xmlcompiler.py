#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 09-06-2010
# Purpose - To parse a workflow's XML file and convert it to executable python
# code.

from BeautifulSoup import BeautifulStoneSoup
import sys, os

def compile( xmlFileName,workflow ) :
    """Compiles an XML file into python code for the workflow."""

    xmlFile=open( xmlFileName,'r' )
    if not xmlFile :
        print 'NONEXISTENT XML FILE or WRONG PATH'
        sys.exit( 1 )

    xml=xmlFile.read()
    xmlFile.close()
    soup=BeautifulStoneSoup(xml)

    toMain=['#! /usr/bin/env python\nimport sys, os\nsys.dont_write_bytecode = False\nsys.path.append("..")\nimport snippets']
    toMain.append( '''def doIt( curSnip, inList ) :
    for i in range( len( inList ) ) :
        if curSnip.types[i] == 'path:r' and not os.access( inList[i], os.R_OK ) :
            print 'Error reading some input files probably due to malfunctioning of previous snippets. Exiting ...'
            sys.exit( -1 )
    if not curSnip.validateInputs( inList ) :
        print "Error in %s !"%curSnip.sname
        sys.exit( -1 )
    curSnip.doJob( inList )\n#-------------------------------------------\n''' )

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
        toMain.append( "inList = %s"%io )
        toMain.append( "doIt( curSnip, inList )" )
        #toMain.append( "inList = %s\nfor i in range( len( inList ) ) :\n\tif curSnip.types[i] == 'path:r' :\n\t\tif not os.access( inList[i], os.R_OK ) :\n\t\t\tprint 'Error reading some input files due to malfunction of a previous snippet. Exiting ...'\n\t\t\tsys.exit( -1 )"%( io ) )
        #toMain.append( 'if not curSnip.validateInputs(%s) :\n\tprint "Error in %s !"\n\tsys.exit( -1 )'%( io, name ) )
        #toMain.append( 'curSnip.doJob(inList)\n#-------------------------------------------\n' )
        
    wf=open( workflow,'w' )
    wf.write( '\n'.join( toMain ) )
    wf.close()
    os.system( 'chmod +x '+ workflow )
