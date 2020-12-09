MAPPING = {
    "properties": {
        "lyrics": {
            "type": "text",
            "term_vector": "with_positions_offsets_payloads",
            "store": True,
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

SETTINGS = {
    "index": {
        "refresh_interval": -1
    },
    "analysis": {
        "analyzer": {
            "custom_analyzer": {
                "type": "custom",
                "tokenizer": "whitespace",
                "filter": [
                    "lowercase",
                    "type_as_payload",
                ]
            }
        }
    }
}
