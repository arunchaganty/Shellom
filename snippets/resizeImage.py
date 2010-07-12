import tasks, os, random, re
import Image

class resizeImage() :
    name = 'Resize an image to a given percentage or size'
    sname = 'resizeImage'
    ID = 3
    details = [ 'Input Image', 'Resize yyy% or yyyxyyy', 'Output file' ]
    tags = [ 'infile', 'factor', 'outfile' ]
    defaults = [ '/dev/null', '100%', 'resize'+str( random.randint( 1,10000 ) ) ]
    errors = [ 'Input image not found', 'Wrong resize factor format. Type, for example as 64% or 640x480.', '' ]
    types = [ 'path:r', '', 'path:w' ]
    packages = [ 'imagemagick' ]

    def __init__( self ) :
	import tasks, os, random, re
	import Image

    def validateInputs( self, inputs ) :
        return True
        err=[]
        if not os.access( inputs[0], os.R_OK ) :
            err.append( 0 )
        if os.access( inputs[2], os.F_OK ) and not os.access( inputs[2], os.W_OK ) :
            err.append( 2 )
        if type( inputs[1] ) != str or not ( re.match( '^\d+%$',inputs[1] ) or re.match('^\d+x\d+$', inputs[1] ) ) :
            err.append( 1 )
        return err

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
        os.system( 'convert %s -resize %s %s'%( inputs[0], cmd, inputs[2] ) )

#allSnippets[ resize_image.sname ] = resize_image
