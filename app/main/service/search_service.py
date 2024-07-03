from app.main.config import Config
import requests


class SearchService:
    def __init__(self):
        self.url = Config.SEARCH_SERVICE_URL

    def supreme_court_decisions(
        self,
        search_query: str,
        page: int,
        per_page: int,
        start_date: str | None,
        end_date: str | None,
        search_field: str | None,
        subject: str | None,
        number: int | None,
        sort_by: str | None,
    ):
        params: dict[str, str | None] = {
            "search_query": search_query,
            "page": str(page),
            "per_page": str(per_page),
            "start_date": start_date,
            "end_date": end_date,
            "search_field": search_field,
            "subject": subject,
            "number": str(number),
            "sort_by": sort_by,
        }

        response = requests.get(self.url + "/supreme-court", params=params)
        return response.json()

    def laws(
        self,
        search_query: str,
        page: int,
        per_page: int,
        signature_start_date: str | None,
        signature_end_date: str | None,
        journal_start_date: str | None,
        journal_end_date: str | None,
        text_type: str | None,
        text_number: str | None,
        ministry: str | None,
        field: str | None,
        sort_by: str | None,
    ):

        params: dict[str, str | int | None] = {
            "search_query": search_query,
            "page": page,
            "per_page": per_page,
            "signature_start_date": signature_start_date,
            "signature_end_date": signature_end_date,
            "journal_start_date": journal_start_date,
            "journal_end_date": journal_end_date,
            "text_type": text_type,
            "text_number": text_number,
            "ministry": ministry,
            "field": field,
            "sort_by": sort_by,
        }

        response = requests.get(self.url + "/laws", params=params)
        return response.json()

    def constitution(
        self,
        search_query: str,
        page: int,
        per_page: int,
        section_name: str | None,
        chapter_name: str | None,
        section_number: int | None,
        chapter_number: int | None,
        article_number: int | None,
    ):

        params: dict[str, str | int | None] = {
            "search_query": search_query,
            "page": page,
            "per_page": per_page,
            "section_name": section_name,
            "chapter_name": chapter_name,
            "section_number": section_number,
            "chapter_number": chapter_number,
            "article_number": article_number,
        }
        response = requests.get(self.url + "/constitution", params=params)
        return response.json()

    def conseil(
        self,
        search_query: str,
        page: int,
        per_page: int,
        number: int | None,
        chamber: str | None,
        section: str | None,
        procedure: str | None,
        start_date: str | None,
        end_date: str | None,
        sort_by: str | None,
    ):
        params: dict[str, str | int | None] = {
            "search_query": search_query,
            "page": page,
            "per_page": per_page,
            "number": number,
            "chamber": chamber,
            "section": section,
            "procedure": procedure,
            "start_date": start_date,
            "end_date": end_date,
            "sort_by": sort_by,
        }
        response = requests.get(self.url + "/conseil", params=params)
        return response.json()
