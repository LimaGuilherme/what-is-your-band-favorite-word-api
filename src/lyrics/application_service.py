from abc import ABC, abstractmethod

from src.lyrics import exceptions
from src.lyrics.statitics import StatisticCount


class TopWordsService(ABC):

    @abstractmethod
    def count_frequency(self, artist: str, number_of_terms: int) -> dict:
        pass


class StorageTopWordsService(TopWordsService):

    def __init__(self,
                 lyrics_searcher,
                 statistic: StatisticCount,
                 repository,
                 artist_searcher):

        self.__lyrics_searcher = lyrics_searcher
        self.__statistic = statistic
        self.__lyrics_repository = repository
        self.__artist_searcher = artist_searcher

    def count_frequency(self, artist: str, number_of_terms: int) -> dict:
        if not self.__artist_searcher.is_this_artist_valid(artist):
            raise exceptions.ArtistNotFound

        lyrics_list = self.__lyrics_repository.get_by_artist(artist)

        if not lyrics_list:
            raise exceptions.LyricsNotFound

        return self.__statistic.count_words_frequency(lyrics_list, number_of_terms)


class RunTimeTopWordsService(TopWordsService):

    def __init__(self, lyrics_searcher,
                 statistic: StatisticCount,
                 artist_searcher):
        self.__lyrics_searcher = lyrics_searcher
        self.__statistic = statistic
        self.__artist_searcher = artist_searcher

    def count_frequency(self, artist: str, number_of_terms: int) -> dict:
        if not self.__artist_searcher.is_this_artist_valid(artist):
            raise exceptions.ArtistNotFound

        lyrics_list = self.__lyrics_searcher.get_lyrics(artist)

        if not lyrics_list:
            raise exceptions.LyricsNotFound

        return self.__statistic.count_words_frequency(lyrics_list, number_of_terms)


class IndexService:

    def __init__(self, lyrics_searcher,
                 repository,
                 artist_searcher):

        self.__lyrics_searcher = lyrics_searcher
        self.__lyrics_repository = repository
        self.__artist_searcher = artist_searcher

    def index(self, artist: str) -> None:
        if not self.__artist_searcher.is_this_artist_valid(artist):
            raise exceptions.ArtistNotFound

        lyrics_list = self.__lyrics_searcher.get_lyrics(artist)

        if not lyrics_list:
            raise exceptions.LyricsNotFound

        for lyrics in lyrics_list:
            self.__lyrics_repository.save(lyrics)
