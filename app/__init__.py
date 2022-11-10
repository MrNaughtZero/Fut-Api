from flask import Flask, Blueprint
from app.database import setup_db
from flask_caching import Cache
from os import environ

app = Flask(__name__)
app.debug = True
app.secret_key = environ.get("APP_SECRET")

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "JSON_SORT_KEYS" : False
}

app.config.from_mapping(config)
cache = Cache(app)

from .routes.latest import cards, clubs, leagues, nations, players, users
app.register_blueprint(cards.api_bp, url_prefix="/v1")
app.register_blueprint(clubs.api_bp, url_prefix="/v1")
app.register_blueprint(leagues.api_bp, url_prefix="/v1")
app.register_blueprint(nations.api_bp, url_prefix="/v1")
app.register_blueprint(players.api_bp, url_prefix="/v1")
app.register_blueprint(users.api_bp, url_prefix="/v1")

setup_db(app)

if __name__ == "__main__":
    app.run()