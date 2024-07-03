from elasticsearch import Elasticsearch
from app.main.config import Config

es_client = Elasticsearch(
    Config.ELASTIC_HOST,
    basic_auth=("elastic", Config.ELASTIC_PASSWORD),
    verify_certs=False,
)
# indexes
LAWS_INDEX = "laws"
SUPREME_COURT_INDEX = "supreme-court"
DOSTOR_INDEX = "dostor"
CONSEIL_ETAT_INDEX = "conseil"


def get_document(index: str, doc_id: str) -> dict | None:
    doc = es_client.get(index=index, id=doc_id)
    if not doc["found"]:
        return None
    res = doc["_source"]
    res["_id"] = doc["_id"]
    return res


def update_document(index: str, doc_id: str, doc_data: dict):
    es_client.update(index=index, id=doc_id, body={"doc": doc_data})
