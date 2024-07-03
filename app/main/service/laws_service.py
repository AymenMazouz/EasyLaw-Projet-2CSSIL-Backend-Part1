from app.main.libs.elasticsearch import LAWS_INDEX, get_document, update_document
from typing import Any
from app.main.utils.exceptions import BadRequestException


class LawsService:

    def get_law_by_id(self, law_id: str) -> dict[str, Any]:
        res = get_document(LAWS_INDEX, law_id)
        if not res:
            raise BadRequestException("no law found with this id")
        return res

    def update_law(self, law_id: str, law_data: dict[str, Any]) -> None:
        law_data.pop("_id", None)
        update_document(LAWS_INDEX, law_id, law_data)
