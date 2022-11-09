from flask import Flask, Blueprint
from ...helpers.api import ApiHelper
from ...decorators import rapidapi_only
from app.models import Cards
from app import cache

api_bp = Blueprint("cards", __name__)

@api_bp.get("/cards")
@rapidapi_only
@cache.cached(query_string=True)
def cards():
    query_params = ApiHelper().convert_query_params()
    result = Cards().find_cards_with_page_and_limit(query_params[0], query_params[1])
    
    if not result[1]:
        return {
            "status" : result[2],
            "title" : "An error occurred",
            "detail": result[0]
        }, result[2]

    return {
        "pagination" : ApiHelper().pagination_model(query_params[0], len(result[0]), result[2]),
        "cards" : result[0]
    }

@api_bp.get("/cards/<card_id>")
@rapidapi_only
@cache.cached()
def specific_card(card_id):
    result = Cards().get_card(card_id)
    
    if not result[1]:
        return {
            "title" : "An error occurred",
            "status" : 404,
            "detail": "Invalid Card ID"
        }, 404

    return {
        "card" : result[0]
    }

@api_bp.get("/cards/<card_id>/image")
@rapidapi_only
@cache.cached()
def card_image(card_id):
    result = Cards().get_image(card_id)
    
    if not result[1]:
        return {
            "title" : "An error occurred",
            "status" : 404,
            "detail": "Invalid Card ID"
        }, 404

    return {
        "image" : result[0]
    }