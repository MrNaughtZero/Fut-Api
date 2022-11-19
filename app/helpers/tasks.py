from app import celery
from app.helpers.emails import Emails

@celery.task
def exception_occurred(error):
    try:
        Emails().exception_occurred(error)
    except Exception as e:
        raise Exception(e)

@celery.task
def players_updated(amount_of_players):
    try:
        Emails().players_update(amount_of_players)
    except Exception as e:
        raise Exception(e)

@celery.task
def check_unknown_cards():
    try:
        Emails().unknown_cards()
    except Exception as e:
        raise Exception(e)