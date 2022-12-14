from flask import Flask, Blueprint, request
from ...helpers.api import ApiHelper
from ...decorators import rapidapi_only
import app.models.all as Models
from app import cache

api_bp = Blueprint("clubs", __name__)

@api_bp.get("/clubs")
@rapidapi_only
@cache.cached(query_string=True)
def clubs():
    query_params = ApiHelper().convert_query_params()
    result = Models.Clubs().find_clubs_with_page_and_limit(query_params[0], query_params[1])
    
    if not result[1]:
        return {
            "status" : result[2],
            "title" : "An error occurred",
            "detail": result[0]
        }, result[2]

    return {
        "pagination" : ApiHelper().pagination_model(query_params[0], len(result[0]), result[2]),
        "clubs" : result[0]
    }

@api_bp.get("/clubs/<club_id>")
@rapidapi_only
@cache.cached()
def specific_club(club_id):
    result = Models.Clubs().get_club(club_id)
    
    if not result[1]:
        return {
            "title" : "An error occurred",
            "status" : 404,
            "detail": "Invalid Club ID"
        }, 404

    return {
        "club" : result[0]
    }

@api_bp.get("/clubs/<club_id>/image")
@rapidapi_only
@cache.cached()
def club_badge(club_id):
    result = Models.Clubs().get_club_image(club_id)
    
    if not result[1]:
        return {
            "title" : "An error occurred",
            "status" : 404,
            "detail": "Invalid Club ID"
        }, 404

    return {
        "image" : result[0]
    }