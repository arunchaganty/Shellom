class forDebugging :
    name = 'This is for debugging purposes'
    sname = 'forDebugging'
    ID = 100
    details = [ 'blah', 'file' ]
    tags = [ 'delay', 'inininin' ]
    defaults = [ '0', '' ]
    errors = [ '', '' ]
    types = [ '', '' ]
    packages = [ 'abracadabra-so-to-say' ]
    
    def validateInputs ( self, inputs ) :
        return True

    def doJob( self, inputs ) :
        pass
