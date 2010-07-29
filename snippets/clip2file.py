#import random, os
try :
    import random, os	
except ImportError :
    print "Check if you have the following Python modules : os and random"

class clip2file() :
    name = 'Paste the contents of the clipboard into a file'
    sname = 'clip2file'
    ID = 1
    details = [ 'Output file' ]
    tags = [ 'outfile' ]
    defaults = [ 'clip2file'+str( random.randint( 1,10000 ) ) ]
    errors = [ '' ]
    types = [ 'path:w' ]
    packages = [ 'xclip' ]

    def __init__( self ) :
        try :
        	import random, os	
        except ImportError :
            print "Couldn't import either or both of os and random"

    def validateInputs( self,inputs ) :
        return True
        #return os.access( inputs[ 0 ] , os.F_OK ) and not os.access( inputs[ 0 ], os.W_OK )

    def doJob( self, inputs ) :
        os.system( 'xclip -o -selection clipboard >> "%s"'%( inputs[ 0 ] ) )

#allSnippets[ clip2file.sname ] = clip2file
