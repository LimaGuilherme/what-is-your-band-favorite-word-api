 # Installing Local
 
    Requirements
    
     Linux
     Python 3.9
     Elasticsearch 7+
     MongoDB
     
    $ cp .env.sample .env
    $ python3.8 -m venv wiybfw-api
    $ source wiybfw-api/bin/activate
    $ pip install -r requirements.txt
    $ export $(cat .env | xargs)
    $ flask run
    

# Dependencies #1 - ElasticSearch Index

    Assuming you alredy have ElasticSearch and Kibana running. Create the Index below:

    PUT /lyrics
    {
      "mappings": {
        "_doc": {
          "properties": {
            "lyrics": {
              "type": "text",
              "term_vector": "with_positions_offsets_payloads",
              "store": true,
              "analyzer": "custom_analyzer"
            },
            "artits": {
              "type": "text",
              "term_vector": "with_positions_offsets_payloads",
              "analyzer": "custom_analyzer"
            },
            "album": {
              "type": "text",
              "term_vector": "with_positions_offsets_payloads",
              "analyzer": "custom_analyzer"
            },
            "track": {
              "type": "text",
              "term_vector": "with_positions_offsets_payloads",
              "analyzer": "custom_analyzer"
            }
          }
        }
      },
      "settings": {
        "index": {
          "number_of_shards": 1,
          "number_of_replicas": 0
        },
        "analysis": {
          "analyzer": {
            "custom_analyzer": {
              "type": "custom",
              "tokenizer": "whitespace",
              "filter": [
                "lowercase",
                "type_as_payload",
                "custom_stop_words"
              ]
            }
          }
        }
      }
    }
    
   
   # Built With
* Coveralls - Python interface to coveralls.io API
* coverage - Code coverage measurement for Python
* Flask - The web framework used
* ElasticSearch - 
* MongoDB - 


# Authors
Guilherme Lima - Initial work

# License
This project is licensed under the MIT License - see the LICENSE.md file for details

# Warning
This code uses an  part of the Genius API and Spotifity API. So there is no guarantee 
that it won't stop working tomorrow, if they change how things work. I will however do
my best to make things working again as soon as possible if that happens. So if it 
stops working, let me know!


    