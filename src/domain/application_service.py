from typing import List


class ArtistLyricsService:

    def __init__(self, lyrics_searcher, statistic, repository):
        self.lyrics_searcher = lyrics_searcher
        self.statistic = statistic
        self.lyrics_repository = repository

    def count_frequency(self, artist: str) -> List:
        lyrics_list = self.lyrics_repository.get_by_artist(artist)
        return self.statistic.count_words_frequency(lyrics_list)

    def index(self, artist: str) -> None:
        lyrics_list = self.lyrics_searcher.get_lyrics(artist)
        for lyrics in lyrics_list:
            self.lyrics_repository.save(lyrics)
