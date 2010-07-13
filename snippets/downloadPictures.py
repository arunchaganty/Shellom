#import urllib2, random, os
#from BeautifulSoup import BeautifulSoup
try :
    import urllib2, random, os
except ImportError :
    print "Couldn't import one or more of urllib2, random and os."

class downloadPictures() :
    name = 'Download all pictures from a webpage'
    sname = 'downloadPictures'
    ID = 5
    details = [ 'URL of webpage', 'Folder to store images in' ]
    tags = [ 'url', 'folder' ]
    defaults = [ 'http://www.google.com/', 'download_pictures'+str( random.randint( 1,10000 ) ) ]
    errors = [ '', '' ]
    types = [ '', '' ]
    packages = [ 'python-beautifulsoup' ]

    def __init__( self ) :
        try :
        	import urllib2, random, os
        except ImportError :
            print "Couldn't import one or more of urllib2, random and os."
	from BeautifulSoup import BeautifulSoup

    def validateInputs( self, inputs ) :
        return True

    def doJob( self, inputs ) :
        # os.system('if [ ! -d %s ] then; mkdir %s; fi'%( inputs[1], inputs[1] ) )
        if not os.access( inputs[1], os.W_OK ) :
            os.mkdir( inputs[1] )
        page = urllib2.urlopen( inputs[0] )
        soup = BeautifulSoup( page.read() )
        images = filter( lambda x: x[ 'src' ][0]=='/', soup.findAll( 'img' ) )
        ctr = 0
        for i in images :
            temp=urllib2.urlopen( inputs[0]+i[ 'src' ] )
            x=open( inputs[1]+'/pic%d'%( ctr ), 'w' )
            x.write( temp.read() )
            x.close()
            ctr+=1

#allSnippets[ download_pictures.sname ] = download_pictures
