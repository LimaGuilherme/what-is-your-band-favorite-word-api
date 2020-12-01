import click
from src import configurations as config_module

from src.lyrics.application_service import CLIArtistLyricsService
from src.lyrics.searchers import AlbumsSearcher, TrackSearcher, LyricsSearcher, ArtistSearcher
from src.lyrics.statitics import create_statistic


@click.group()
def main():
    pass


@main.command()
@click.option('--artist', help='Artist or Band Name')
def config_credentials(status):
    pass


@main.command()
@click.option('--artist', help='Artist or Band Name')
def get_lyrics(artist):

    config = config_module.get_config()
    albums_searcher = AlbumsSearcher(config)
    track_searcher = TrackSearcher(config)
    lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher, config)
    artist_searcher = ArtistSearcher(config)
    statistic = create_statistic()

    artist_service = CLIArtistLyricsService(lyrics_searcher, statistic, artist_searcher)
    words_frequency = artist_service.count_frequency(artist)
    click.echo(words_frequency)
