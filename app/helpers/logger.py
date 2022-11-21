import logging
from os import environ

if environ.get("development") == "0":
    filename = "logs/app.log"
else:
    filename = "/var/www/app/logs/log.log"

logging.basicConfig(
    filename=filename,
    level=logging.DEBUG, 
    format='%(asctime)s %(levelname)s %(name)s : %(message)s'
)