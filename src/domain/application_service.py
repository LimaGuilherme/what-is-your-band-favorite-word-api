from src import exceptions
from src.domain.statitics import StatisticCount


class ArtistLyricsService:

    def __init__(self, lyrics_searcher,
                 statistic: StatisticCount,
                 repository,
                 artist_searcher):
        self.lyrics_searcher = lyrics_searcher
        self.statistic = statistic
        self.lyrics_repository = repository
        self.artist_searcher = artist_searcher

    def count_frequency(self, artist: str) -> dict:
        if not self.artist_searcher.is_this_artist_valid(artist):
            raise exceptions.ArtistNotFound

        lyrics_list = self.lyrics_repository.get_by_artist(artist)

        if not lyrics_list:
            raise exceptions.LyricsNotFound

        return self.statistic.count_words_frequency(lyrics_list)

    def index(self, artist: str) -> None:
        if not self.artist_searcher.is_this_artist_valid(artist):
            raise exceptions.ArtistNotFound

        lyrics_list = self.lyrics_searcher.get_lyrics(artist)

        if not lyrics_list:
            raise exceptions.LyricsNotFound

        for lyrics in lyrics_list:
            self.lyrics_repository.save(lyrics)
