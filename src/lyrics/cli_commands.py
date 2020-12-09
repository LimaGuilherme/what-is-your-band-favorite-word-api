import click

from src import configurations as config_module
from src.lyrics import exceptions
from src.lyrics.application_service import RunTimeWordsService
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
    click.secho('Starting operation, this may take a while. Get some coffee.', fg='green')

    config_module.create_simple_config(spotify_client_id=spotify_client_id,
                                       spotify_client_secret=spotify_client_secret,
                                       genius_access_token=genius_access_token)


@main.command()
@click.option('--artist', prompt='Search lyrics for this band', help='Artist or Band Name', required=True)
@click.option('--terms-quantity', prompt='The number of words you desire', required=True,
              help='The number of words you desire', type=int)
def get_lyrics(artist, terms_quantity):

    configurations = config_module.get_config(config_type='simple')

    albums_searcher = AlbumsSearcher(configurations)
    track_searcher = TrackSearcher(configurations)
    lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher, configurations)
    artist_searcher = ArtistSearcher(configurations)
    statistic = create_statistic()

    runtime_word_service = RunTimeWordsService(lyrics_searcher, statistic, artist_searcher)
    click.secho('Starting operation, this may take a while. Get some coffee.', fg='green')

    try:
        words_frequency = runtime_word_service.count_frequency(artist, int(terms_quantity))
        click.secho(words_frequency, fg='blue')
    except exceptions.ArtistNotFound:
        click.secho(f'No artist were found with this name: {artist}', fg='red')
    except exceptions.LyricsNotFound:
        click.secho(f'No lyrics were found with this artist: {artist}', fg='red')

