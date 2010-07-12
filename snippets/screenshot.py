import random, re, os

class screenshot() :
    name = 'Take a screenshot of the entire screen'
    sname = 'screenshot'
    ID = 4
    details = [ 'Delay in seconds', 'Output image file' ]
    tags = [ 'delay', 'outfile' ]
    defaults = [ '0', 'screenshot'+str( random.randint( 1,10000 ) ) ]
    errors = [ '', '' ]
    types = [ '', 'path:w' ]
    packages = [ 'imagemagick' ]

    def __init__( self ) :
	import random, re, os

    def validateInputs ( self, inputs ) :
        return re.match('^\d+$',inputs[0] )

    def doJob( self, inputs ) :
        os.system( 'sleep %s; import -window root "%s"'%( inputs[0], inputs[1] ) )

#allSnippets[ screenshot.sname ] = screenshot
