 # Requirements
    Linux
    Python 3+
    Pip3
    Virtualenvwrapper (Optional but highly recommended)
    Elasticsearch 6.8
    
    Linux
    Docker 
       
 # Installing
 
     $ git clone git@github.com:LimaGuilherme/what-is-your-band-favorite-word-api.git
     $ mkvirtualenv -p python3 band-favorite-word-api
     $ workon band-favorite-word-api
     $ pip install -r requirements.txt
     
     Dealing with environments variables

    $ cd
    $ vim .bashrc
    
    Add this in the end of file and reopen the terminal
    alias load-env='export $(cat .env | xargs)'
    alias load-env-test='export $(cat .env.test | xargs)'
    
    $ load-env
    
    Create a .env file based on .env.sample, with your custom configuration (if necessary) and then:

    $ load-env
    

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
* ElasticSearch


# Authors
Guilherme Lima - Initial work

# License
This project is licensed under the MIT License - see the LICENSE.md file for details
    