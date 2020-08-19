import elasticsearch
import elasticsearch_dsl

from elasticsearch_dsl.connections import connections


class ElasticSearchConnection(object):

    def __init__(self):
        self.__connection = connections.create_connection(
            hosts=[{'host': 'localhost', 'port': 9200}],
            use_ssl=False,
            verify_certs=False,
            connection_class=elasticsearch.RequestsHttpConnection
        )


class Lyrics(elasticsearch_dsl.DocType):

    artist = elasticsearch_dsl.Text()
    lyrics = elasticsearch_dsl.Text()
    track = elasticsearch_dsl.Text()
    album = elasticsearch_dsl.Text()

    class Index:
        name = 'lyrics'
        doc_type = '_doc'

    class Meta:
        doc_type = '_doc'

    @classmethod
    def index(cls, **kwargs):
        lyrics = cls(**kwargs)
        try:
            lyrics.save()
        except elasticsearch.TransportError as ex:
            return str(ex)
        except Exception as ex:
            return str(ex)

        return lyrics

    @classmethod
    def get_item(cls, artist):
        searcher = cls.search().query("match", artist="Safadao").params(size=1000, timeout='150s')
        return searcher.execute()
