from flask_restx import Resource, Namespace
from app.main.config import Config
from http import HTTPStatus
from flask import Response
import requests


api = Namespace("Scraping", description="Scraping related operations")


@api.route("/")
class ScrapingController(Resource):
    def get(self):
        requests.get(Config.SCRAPING_SERVICE_URL + "/run-scraping")
        return Response(status=HTTPStatus.OK)
