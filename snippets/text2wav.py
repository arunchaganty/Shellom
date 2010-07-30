#import random, os
try :
    import random, os
except ImportError :
    print "Check if you have the following Python modules : random and os."

class text2wav() :
    name = 'Convert the text in a file to a wav sound file'
    sname = 'text2wav'
    ID = 2
    details = [ 'Input file', 'Output file' ]
    tags = [ 'infile', 'outfile' ]
    defaults = [ '/dev/null', 'text2wave'+str( random.randint( 1,10000 ) ) ]
    errors = [ '', '' ]
    types = [ 'path:r', 'path:w' ]
    packages = [ 'festival' ]

    def __init__( self ) :
        try :
        	import random, os
        except ImportError :
            print "Couldn't import one or more of random and os."

    def validateInputs( self,inputs ) :
        #return True
        return  ( not os.access( inputs[ 1 ] , os.F_OK ) ) or os.access( inputs[ 1 ], os.W_OK )

    def doJob( self, inputs ) :
        os.system( 'text2wave < "%s" > "%s"'%( inputs[ 0 ], inputs[ 1 ] ) )

#allSnippets[ text2wave.sname ] = text2wave
