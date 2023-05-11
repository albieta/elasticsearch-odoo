from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch(["http://localhost:9200"])

index_name = "odoo_keywords"
mapping = {
    "properties": {
        "id": {"type": "text"},
        "description": {"type": "text"},
        "keywords": {"type": "text"},
    }
}

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body={"mappings": mapping})

docs = [
    {
        "id": "1",
        "description": "Aalto Ice Tank is a multipurpose basin ideally suited for testing ships and other maritime structures in ice",
        "keywords": "Environment, IT, Renewable energy",
    },
    {
        "id": "2",
        "description": "Aalto NeuroImaging Infrastructure (ANI) is a research-dedicated infrastructure ",
        "keywords": "Electrical, Plasma, Environment",    
    },
    {
        "id": "3",
        "description": "Aalto Acoustics Lab is a multidisciplinary research centre of the Aalto University",
        "keywords": "Observation, Nanomaterials",
    }
]

for i, doc in enumerate(docs):
    if not es.exists(index=index_name, id=doc['id']):
        es.index(index=index_name, id=doc['id'], body=doc)

query = {
    "query": {
        "query_string": {
            "query": "*env*",
            "fields": ["keywords"]
        }
    }
}

# Search for documents
response = es.search(index=index_name, body=query)

print("Search results:")
for hit in response["hits"]["hits"]:
    print(f"Description: {hit['_source']['description']}")
    print(f"Keywords: {hit['_source']['keywords']}")


#es.delete_by_query(index=index_name, body={"query": {"match_all": {}}})