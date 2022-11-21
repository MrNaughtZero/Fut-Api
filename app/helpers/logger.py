import logging
from os import environ

if environ.get("development") == "0":
    location = "/var/www/app/logs/log.log"
else:
    location = "logs/log.log"

logging.basicConfig(filename=location,level=logging.DEBUG)