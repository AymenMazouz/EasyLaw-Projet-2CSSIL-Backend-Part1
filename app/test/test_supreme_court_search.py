import pytest
from unittest.mock import patch
from app.main.service.search_service import SearchService


class ElasticResponse:
    def __init__(self, body: dict) -> None:
        self.body = body


@pytest.fixture
def search_service():
    return SearchService()


def test_supreme_court_decisions_no_filters(search_service: SearchService):
    with patch.object(search_service, "es") as mock_es:
        es_return = {"hits": {"hits": [], "total": {"value": 0}}}
        mock_es.search.return_value = ElasticResponse(es_return)
        page = 1
        per_page = 10
        search_service.supreme_court_decisions(
            "", page, per_page, None, None, None, None, None
        )
        query = {
            "query": {"bool": {"must": {"match_all": {}}, "filter": []}},
            "from": 0,
            "size": 10,
        }
        mock_es.search.assert_called_with(index="supreme-court", body=query)


def test_supreme_court_decisions_with_date(search_service: SearchService):
    with patch.object(search_service, "es") as mock_es:
        es_return = {"hits": {"hits": [], "total": {"value": 0}}}
        mock_es.search.return_value = ElasticResponse(es_return)
        page = 1
        per_page = 10
        search_service.supreme_court_decisions(
            "", page, per_page, "2019/01/01", "2022/01/01", None, None, None
        )

        query = {
            "query": {
                "bool": {
                    "must": {"match_all": {}},
                    "filter": [
                        {"range": {"date": {"gte": "2019/01/01"}}},
                        {"range": {"date": {"lte": "2022/01/01"}}},
                    ],
                }
            },
            "from": 0,
            "size": 10,
        }

        mock_es.search.assert_called_with(index="supreme-court", body=query)


"""
def test_supreme_court_decisions_with_end_date(search_service):
    with patch.object(search_service, "es") as mock_es:
        mock_es.search.return_value = {}
        result = search_service.supreme_court_decisions(
            "", 1, 10, None, "2022-12-31", None, None, None
        )
        assert result == search_service._format_search_res({}, 1, 10)


def test_supreme_court_decisions_with_subject(search_service):
    with patch.object(search_service, "es") as mock_es:
        mock_es.search.return_value = {}
        result = search_service.supreme_court_decisions(
            "", 1, 10, None, None, None, "subject", None
        )
        assert result == search_service._format_search_res({}, 1, 10)


def test_supreme_court_decisions_with_number(search_service):
    with patch.object(search_service, "es") as mock_es:
        mock_es.search.return_value = {}
        result = search_service.supreme_court_decisions(
            "", 1, 10, None, None, None, None, 123
        )
        assert result == search_service._format_search_res({}, 1, 10)
"""
