from flask import Flask, Blueprint
from ...helpers.api import ApiHelper
from ...helpers.decorators import any_key_required, limiter
from app.models import Leagues
from app import cache

api_bp = Blueprint("leagues", __name__)

@api_bp.get("/leagues")
@any_key_required
@limiter
@cache.cached(query_string=True)
def leagues():
    query_params = ApiHelper().convert_query_params()
    result = Leagues().find_leagues_with_page_and_limit(query_params[0], query_params[1])
    
    if not result[1]:
        return {
            "status" : result[2],
            "title" : "An error occurred",
            "detail": result[0]
        }, result[2]

    return {
        "pagination" : ApiHelper().pagination_model(query_params[0], len(result[0]), result[2]),
        "leagues" : result[0]
    }

@api_bp.get("/leagues/<league_id>")
@any_key_required
@limiter
@cache.cached()
def specific_league(league_id):
    result = Leagues().get_league(league_id)
    
    if not result[1]:
        return {
            "title" : "An error occurred",
            "status" : 404,
            "detail": "Invalid League ID"
        }, 404

    return {
        "league" : result[0]
    }

@api_bp.get("/leagues/<league_id>/image")
@any_key_required
@limiter
@cache.cached()
def league_image(league_id):
    result = Leagues().get_league_image(league_id)
    
    if not result[1]:
        return {
            "title" : "An error occurred",
            "status" : 404,
            "detail": "Invalid League ID"
        }, 404

    return {
        "image" : result[0]
    }