#import random, re, os
try :
    import random, re, os
except ImportError :
    print "Check if you have the following Python modules : random, re and os."

class screenshot() :
    name = 'Take a screenshot of the entire screen'
    sname = 'screenshot'
    ID = 4
    details = [ 'Delay in seconds', 'Output image file' ]
    tags = [ 'delay', 'outfile' ]
    defaults = [ '0', 'screenshot'+str( random.randint( 1,10000 ) )+'.jpg' ]
    errors = [ '', '' ]
    types = [ 'integer', 'path:w' ]
    packages = [ 'imagemagick' ]

    def __init__( self ) :
        try :
        	import random, re, os
        except ImportError :
            print "Couldn't import one or more of random, re and os."

    def validateInputs ( self, inputs ) :
        return re.match('^\d+$',inputs[0] )

    def doJob( self, inputs ) :
        os.system( 'sleep %s; import -window root "%s"'%( inputs[0], inputs[1] ) )

#allSnippets[ screenshot.sname ] = screenshot
