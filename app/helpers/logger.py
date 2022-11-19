import logging

logging.basicConfig(
    filename='logs/log.log',
    level=logging.DEBUG, 
    format='%(asctime)s %(levelname)s %(name)s : %(message)s'
)