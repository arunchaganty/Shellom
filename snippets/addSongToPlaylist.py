import os

class addSongToPlaylist() :
    name = 'Add a song to a playlist'
    sname = 'addSongToPlaylist'
    ID = 7
    details = [ 'Path to song', 'Path to playlist' ]
    tags = [ 'song', 'playlist' ]
    defaults = [ '/dev/null', '/dev/null' ]
    errors = [ '', '' ]
    types = [ 'path:r', 'path:w' ]
    packages = []

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
