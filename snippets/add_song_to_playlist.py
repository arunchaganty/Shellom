import os

class add_song_to_playlist() :
    name = 'Add a song to a playlist'
    sname = 'add_song_to_playlist'
    ID = 7
    details = [ 'Path to song', 'Path to playlist' ]
    tags = [ 'song', 'playlist' ]
    defaults = [ '/dev/null', '/dev/null' ]
    errors = [ '', '' ]

    def __init__( self ) :
        import os

    def validateInputs( self, inputs ) :
        return True
        #return os.access( os.path.abspath( inputs[0] ), os.F_OK ) #and os.access( '/'.join( inputs[1].split('/')[:-1] ), os.W_OK )

    def doJob( self, inputs ) :
        print 'echo %s >> %s'%( inputs[0], inputs[1] ) 
        os.system( 'pwd' )
        os.system( 'echo %s >> %s'%( inputs[0], inputs[1] ) )

#allSnippets[ add_song_to_playlist.sname ] = add_song_to_playlist
