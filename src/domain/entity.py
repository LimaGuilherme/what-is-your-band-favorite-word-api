class Lyrics:

    def __init__(self, artist: str, album: str, track: str, lyrics: str, lyric_id=None):
        self.id = lyric_id
        self.artist = artist
        self.album = album
        self.track = track
        self.lyrics = lyrics
