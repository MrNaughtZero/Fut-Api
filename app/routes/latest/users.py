from flask import Flask, Blueprint, request
import app.models.all as Models
import datetime

api_bp = Blueprint("users", __name__)

@api_bp.post("/test/user/free")
def free_test_user():
    json = request.get_json()
    data = {
        "subscription": "free",
        "end_date" : None
    }
    new_user = Models.User().add_user(data)
    return {"status" : "user added"}, 200

@api_bp.post("/test/user/premium")
def premium_test_user():
    json = request.get_json()
    data = {
        "subscription": "premium",
        "end_date" : datetime.datetime.now() + datetime.timedelta(28)
    }
    new_user = Models.User().add_user(data)
    return {"status" : "user added"}, 200