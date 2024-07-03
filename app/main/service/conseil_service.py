from app.main.libs.elasticsearch import (
    CONSEIL_ETAT_INDEX,
    get_document,
    update_document,
)
from typing import Any
from app.main.utils.exceptions import BadRequestException


class ConseilService:
    def get_decision_by_id(self, decision_id: str) -> dict[str, Any]:
        res = get_document(CONSEIL_ETAT_INDEX, decision_id)
        if not res:
            raise BadRequestException("no decision found with this id")
        return res

    def update_decision(self, decision_id: str, decision_data: dict[str, Any]) -> None:
        decision_data.pop("_id", None)
        update_document(CONSEIL_ETAT_INDEX, decision_id, decision_data)
