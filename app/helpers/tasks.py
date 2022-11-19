from app import celery
from app.helpers.emails import Emails

@celery.task
def exception_occurred(error):
    Emails().exception_occurred(error)