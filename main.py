#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 06-06-2010
# Purpose - The main script that is to be run.

import sys, tasks, xmlgenerator, xmlcompiler, repository

def main() :
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

        if True : #s[ currentSnippet ].validateInputs( currentInputs ) :
            xml=xmlgenerator.getxml( xml, s[ currentSnippet ], currentInputs, snipID, inputID-len( inputsToBeGot ) )
            print xml

            if xml==list('ERROR') :
                print 'Error while generating XML ... Will Quit'
                sys.exit(1)

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


# NOT IN USE. THIS WAS A RUDIMENTARY VERSION'S MAIN.PY.
# THIS IS USELESS UNTIL CHANGED


#from xmlgen.py import *
#from xmlparse.py import *
### from tasks import *
### from BeautifulSoup import BeautifulStoneSoup
### 
### def ironout(n,soup):
###     if not n[0]=='~':
###         return n
###     x=soup.find(attrs={'id':int(n[1:])})
###     #print soup
###     #print '\n'+x+'\n'
###     return ironout(x.string.strip(),soup)
### 
### def main():
###     print 'Enter -1 as an option to finish your workflow'
###     gid=1
###     print '\n'.join(options)
###     opstring='<workflow>\n'
###     nextoption=int(raw_input("... "))
###     while not nextoption==-1 :
###     	opstring+='  <%s>\n'%(options[nextoption])
###     	nextinput=getInput(nextoption)
###     	while not nextinput=='0' :
###     		opstring+='    <%s id="%d">'%(nextinput,gid)
###     		print 'Present ID : %d'%(gid)
###     		n=raw_input(nextinput+' ... ')
###     		opstring+=ironout(n,BeautifulStoneSoup(opstring))
###     		opstring+='</%s>\n'%(nextinput)
###     		print 40*'-'
###     		nextinput=getInput(nextoption)
###     		gid+=1
###     	opstring+='  </%s>\n'%(options[nextoption])
###     	print '\n'.join(options)
###     	nextoption=int(raw_input("... "))
###     op=open('tmp/workflow.xml','w')
###     opstring+='</workflow>'
###     op.write(opstring)
###     op.close()
### 
### if __name__=='__main__' :
###	main()
