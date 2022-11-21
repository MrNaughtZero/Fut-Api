from flask import Flask, Blueprint
from app.database import setup_db
from flask_caching import Cache
from os import environ
from .helpers import logger
from app.celery import create_celery
from datetime import timedelta
from celery.schedules import crontab

app = Flask(__name__)
app.secret_key = environ.get('APP_SECRET')

config = {
    "DEBUG": True,
    "CACHE_TYPE": environ.get("CACHE_TYPE"),
    "CACHE_DEFAULT_TIMEOUT": environ.get("CACHE_DEFAULT_TIMEOUT"),
    "CACHE_REDIS_HOST" : environ.get("CACHE_REDIS_HOST"),
    "CACHE_REDIS_PORT" : environ.get("CACHE_REDIS_PORT"),
    "CACHE_REDIS_DB" : environ.get("CACHE_REDIS_DB"),
    "CACHE_REDIS_URL" : environ.get("CACHE_REDIS_URL"),
    "JSON_SORT_KEYS" : False,
}

app.config.from_mapping(config)
celery = create_celery(app)
cache = Cache(app)

## add beat schedule to celery
celery.conf.CELERYBEAT_SCHEDULE = {
    "update-players" : {
        "task" : "app.helpers.tasks.update_players",
        "schedule" : crontab(hour=13, minute=44)
    }
}

from .routes.latest import cards, clubs, leagues, nations, players, users
app.register_blueprint(cards.api_bp, url_prefix="/v1")
app.register_blueprint(clubs.api_bp, url_prefix="/v1")
app.register_blueprint(leagues.api_bp, url_prefix="/v1")
app.register_blueprint(nations.api_bp, url_prefix="/v1")
app.register_blueprint(players.api_bp, url_prefix="/v1")
app.register_blueprint(users.api_bp, url_prefix="/v1")

setup_db(app)

from app.helpers.tasks import exception_occurred

@app.errorhandler(Exception)
def all_exception_handler(error):
    app.logger.error(error)
    return {
        "title" : "An error occurred",
        "status" : 500,
        "detail": "Something has went wrong. Please try your request again."
    }, 500

if __name__ == "__main__":
    app.run()