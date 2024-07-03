from app.main.libs.elasticsearch import (
    DOSTOR_INDEX,
    get_document,
    update_document,
)
from typing import Any
from app.main.utils.exceptions import BadRequestException


class ConstitutionService:
    def get_article_by_id(self, article_id: str) -> dict[str, Any]:
        res = get_document(DOSTOR_INDEX, article_id)
        if not res:
            raise BadRequestException("no article found with this id")
        return res

    def update_article(self, article_id: str, article_data: dict[str, Any]) -> None:
        article_data.pop("_id", None)
        update_document(DOSTOR_INDEX, article_id, article_data)
