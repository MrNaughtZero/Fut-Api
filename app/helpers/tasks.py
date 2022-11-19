from app import celery
from app.helpers.emails import Emails

@celery.task
def exception_occurred(error):
    try:
        Emails().exception_occurred(error)
    except Exception as e:
        raise Exception(e)