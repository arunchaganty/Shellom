#import os, random, re
#import Image 
try :
    import os, random, re
    import Image
except ImportError :
    print "Check if you have the Image Python module.\nInstall it using sudo apt-get install python-imaging"

class resizeImage() :
    name = 'Resize an image to a given percentage or size'
    sname = 'resizeImage'
    ID = 3
    details = [ 'Input Image', 'Resize yyy% or yyyxyyy', 'Output file' ]
    tags = [ 'infile', 'factor', 'outfile' ]
    defaults = [ 'shot.jpg', '100%', 'resize'+str( random.randint( 1,10000 ) ) ]
    errors = [ 'Input image not found', 'Wrong resize factor format. Type, for example as 64% or 640x480.', '' ]
    types = [ 'path:r', 'pattern:(^\d+%$)|(^\d+x\d+$)', 'path:w' ]
    packages = [ 'imagemagick' ]

    def __init__( self ) :
        try :
        	import os, random, re
        	import Image
        except ImportError :
            print "Couldn't import one or more of os, random, re and Image."

    def validateInputs( self, inputs ) :
        if not os.access( inputs[0], os.R_OK ) :
            return False
        if os.access( inputs[2], os.F_OK ) and not os.access( inputs[2], os.W_OK ) :
            return False
        return True

    def doJob( self, inputs ) :
        if re.match( '^\d+%$',inputs[1] ) :
            factor=int( inputs[1][:-1] )
            temp=int(inputs[1][:-1])
            temp=Image.open( inputs[0] ).size
            cmd='%dx%d'%( factor*temp[0]/100.0, factor*temp[1]/100.0 )
        elif re.match('^\d+x\d+$', inputs[1] ) :
            cmd = inputs[1]
        
        #it=self.validateInputs( inputs )
        #if it :
        #    print it
        #else :
        os.system( 'convert "%s" -resize %s "%s"'%( inputs[0], cmd, inputs[2] ) )

#allSnippets[ resize_image.sname ] = resize_image
