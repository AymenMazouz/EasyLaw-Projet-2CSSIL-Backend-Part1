from app.main.libs.elasticsearch import (
    SUPREME_COURT_INDEX,
    get_document,
    update_document,
)
from typing import Any
from app.main.utils.exceptions import BadRequestException


class SupremeCourtService:

    def get_decision_by_id(self, decision_id: str) -> dict[str, Any]:
        res = get_document(SUPREME_COURT_INDEX, decision_id)
        if not res:
            raise BadRequestException("no decision found with this id")
        return res

    def update_decision(self, decision_id: str, decision_data: dict[str, Any]) -> None:
        decision_data.pop("_id", None)
        update_document(SUPREME_COURT_INDEX, decision_id, decision_data)
