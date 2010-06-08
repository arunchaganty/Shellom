#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 06-06-2010

# NOT IN USE. THIS WAS A RUDIMENTARY VERSION'S MAIN.PY.
# THIS IS USELESS UNTIL CHANGED


#from xmlgen.py import *
#from xmlparse.py import *
from tasks import *
from BeautifulSoup import BeautifulStoneSoup

def ironout(n,soup):
    if not n[0]=='~':
        return n
    x=soup.find(attrs={'id':int(n[1:])})
    #print soup
    #print '\n'+x+'\n'
    return ironout(x.string.strip(),soup)

def main():
    print 'Enter -1 as an option to finish your workflow'
    gid=1
    print '\n'.join(options)
    opstring='<workflow>\n'
    nextoption=int(raw_input("... "))
    while not nextoption==-1 :
    	opstring+='  <%s>\n'%(options[nextoption])
    	nextinput=getInput(nextoption)
    	while not nextinput=='0' :
    		opstring+='    <%s id="%d">'%(nextinput,gid)
    		print 'Present ID : %d'%(gid)
    		n=raw_input(nextinput+' ... ')
    		opstring+=ironout(n,BeautifulStoneSoup(opstring))
    		opstring+='</%s>\n'%(nextinput)
    		print 40*'-'
    		nextinput=getInput(nextoption)
    		gid+=1
    	opstring+='  </%s>\n'%(options[nextoption])
    	print '\n'.join(options)
    	nextoption=int(raw_input("... "))
    op=open('tmp/workflow.xml','w')
    opstring+='</workflow>'
    op.write(opstring)
    op.close()

if __name__=='__main__' :
	main()
