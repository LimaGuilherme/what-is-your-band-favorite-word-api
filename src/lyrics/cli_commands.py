import click

from src import configurations as config_module
from src.lyrics.application_service import CLIArtistLyricsService
from src.lyrics.searchers import AlbumsSearcher, TrackSearcher, LyricsSearcher, ArtistSearcher
from src.lyrics.statitics import create_statistic


@click.group()
def main():
    pass


@main.command()
@click.option('--spotify-client-id', prompt='Your SPOTIFY CLIENT ID',  help='Your Spotify Client ID')
@click.option('--spotify-client-secret', prompt='Your SPOTIFY CLIENT SECRET', help='Your Spotify Client SECRET')
@click.option('--genius-access-token', prompt='Your Genius ACCESS SECRET', help='Your Genius ACCESS SECRET')
def config_credentials(spotify_client_id, spotify_client_secret, genius_access_token):
    config_module.create_simple_config(spotify_client_id=spotify_client_id,
                                       spotify_client_secret=spotify_client_secret,
                                       genius_access_token=genius_access_token)


@main.command()
@click.option('--artist', prompt='Search lyrics for this band', help='Artist or Band Name')
@click.option('--terms-quantity', prompt='The number of words you desire', help='The number of words you desire')
def get_lyrics(artist, terms_quantity):

    configurations = config_module.get_config(config_type='simple')

    albums_searcher = AlbumsSearcher(configurations)
    track_searcher = TrackSearcher(configurations)
    lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher, configurations)
    artist_searcher = ArtistSearcher(configurations)
    statistic = create_statistic()

    artist_service = CLIArtistLyricsService(lyrics_searcher, statistic, artist_searcher)
    words_frequency = artist_service.count_frequency(artist, int(terms_quantity))
    click.echo(words_frequency)
