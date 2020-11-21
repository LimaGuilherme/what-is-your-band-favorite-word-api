#!/bin/bash

echo "create new index"
curl -X PUT "localhost:9200/lyrics/" -d'
{
      "mappings": {
          "properties": {
            "lyrics": {
              "type": "text",
              "term_vector": "with_positions_offsets_payloads",
              "store": true,
              "analyzer": "custom_analyzer"
            },
            "artist": {
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
                "type_as_payload"
              ]
            }
          }
        }
      }
    }';