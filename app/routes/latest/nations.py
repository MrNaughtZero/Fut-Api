from flask import Flask, Blueprint, request
from ...helpers.api import ApiHelper
from ...decorators import rapidapi_only
from app.models import Nations
from app import cache

api_bp = Blueprint("nations", __name__)

@api_bp.get("/nations")
@rapidapi_only
@cache.cached(query_string=True)
def nations():
    query_params = ApiHelper().convert_query_params()
    result = Nations().find_nations_with_page_and_limit(query_params[0], query_params[1])
    
    if not result[1]:
        return {
            "status" : result[2],
            "title" : "An error occurred",
            "detail": result[0]
        }, result[2]

    return {
        "pagination" : ApiHelper().pagination_model(query_params[0], len(result[0]), result[2]),
        "nations" : result[0]
    }

@api_bp.get("/nations/<nation_id>")
@rapidapi_only
@cache.cached()
def specific_nation(nation_id):
    result = Nations().get_nation(nation_id)
    
    if not result[1]:
        return {
            "title" : "An error occurred",
            "status" : 404,
            "detail": "Invalid Nation ID"
        }, 404

    return {
        "nation" : result[0]
    }

@api_bp.get("/nations/<nation_id>/image")
@rapidapi_only
@cache.cached()
def nation_image(nation_id):
    result = Nations().get_nation_image(nation_id)
    
    if not result[1]:
        return {
            "title" : "An error occurred",
            "status" : 404,
            "detail": "Invalid Nation ID"
        }, 404

    return {
        "image" : result[0]
    }