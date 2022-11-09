from flask import Flask, Blueprint, request
from ...helpers.api import ApiHelper
from ...helpers.decorators import rapidapi_only
from app.models import Player, PlayerImage
from app import cache

api_bp = Blueprint("players", __name__)

@api_bp.get("/players")
@rapidapi_only
@cache.cached(query_string=True)
def players():
    query_params = ApiHelper().convert_query_params()
    result = Player().find_players_with_page_and_limit(query_params[0], query_params[1])
    
    if not result[1]:
        return {
            "status" : result[2],
            "title" : "An error occurred",
            "detail": result[0]
        }, result[2]

    return {
        "pagination" : ApiHelper().pagination_model(query_params[0], len(result[0]), result[2]),
        "players" : result[0]
    }

@api_bp.get("/players/nation/<nation_id>")
@rapidapi_only
@cache.cached(query_string=True)
def players_by_nation(nation_id):
    query_params = ApiHelper().convert_query_params()
    result = Player().find_players_by_nation_with_page_and_limit(query_params[0], query_params[1], nation_id)
    
    if not result[1]:
        return {
            "status" : result[2],
            "title" : "An error occurred",
            "detail": result[0]
        }, result[2]

    return {
        "pagination" : ApiHelper().pagination_model(query_params[0], len(result[0]), result[2]),
        "players" : result[0]
    }

@api_bp.get("/players/league/<league_id>")
@rapidapi_only
@cache.cached(query_string=True)
def players_by_league(league_id):
    query_params = ApiHelper().convert_query_params()
    result = Player().find_players_by_league_with_page_and_limit(query_params[0], query_params[1], league_id)
    
    if not result[1]:
        return {
            "status" : result[2],
            "title" : "An error occurred",
            "detail": result[0]
        }, result[2]

    return {
        "pagination" : ApiHelper().pagination_model(query_params[0], len(result[0]), result[2]),
        "players" : result[0]
    }

@api_bp.get("/players/club/<club_id>")
@rapidapi_only
@cache.cached(query_string=True)
def players_by_club(club_id):
    query_params = ApiHelper().convert_query_params()
    result = Player().find_players_by_club_with_page_and_limit(query_params[0], query_params[1], club_id)
    
    if not result[1]:
        return {
            "status" : result[2],
            "title" : "An error occurred",
            "detail": result[0]
        }, result[2]

    return {
        "pagination" : ApiHelper().pagination_model(query_params[0], len(result[0]), result[2]),
        "players" : result[0]
    }

@api_bp.get("/players/<player_id>")
@rapidapi_only
@cache.cached()
def player_by_id(player_id):
    result = Player().find_player_by_id(player_id)
    
    if not result[1]:
        return {
            "status" : result[2],
            "title" : "An error occurred",
            "detail": result[0]
        }, result[2]

    return {
        "player" : result[0]
    }

@api_bp.get("/players/<player_id>/image")
@rapidapi_only
@cache.cached()
def player_image(player_id):
    result = PlayerImage().get_image_by_id(player_id)
    
    if not result[1]:
        return {
            "title" : "An error occurred",
            "status" : 404,
            "detail": "Invalid Player ID"
        }, 404

    return {
        "image" : result[0]
    }

@api_bp.get("/players/<player_id>/price")
@rapidapi_only
def player_price(player_id, force_update = False):
    if "price_update" in request.args and int(request.args["price_update"]) == 1:
        Player().update_player_prices(player_id)
    
    result = Player().get_player_price(player_id)
    
    if not result[1]:
        return {
            "title" : "An error occurred",
            "status" : 404,
            "detail": "Invalid Player ID"
        }, 404

    return {
        "prices" : result[0]
    }

@api_bp.get("/players/latest/<player_id>")
@rapidapi_only
@cache.cached(query_string=True)
def latest_players(player_id):
    query_params = ApiHelper().convert_query_params()
    result = Player().latest_players(query_params[0], query_params[1], player_id)
    
    if not result[1]:
        return {
            "title" : "An error occurred",
            "status" : 404,
            "detail": "Invalid Player ID"
        }, 404

    return {
        "pagination" : ApiHelper().pagination_model(query_params[0], len(result[0]), result[2]),
        "players" : result[0]
    }

@api_bp.post("/players/search")
@rapidapi_only
def search_players():
    request_json = request.get_json()
    result = Player().search_players(request_json)
    
    if not result[1]:
        return {
            "title" : "An error occurred",
            "status" : 404,
            "detail": "No Matching Players"
        }, 404

    return {
        "players" : result[0]
    }