from django.conf import settings
from django.utils import simplejson

import redis

def send_message_to_client(userid, message_dictionary):
    """
    Sends a message to the web client through websockets
    """
    r = redis.StrictRedis(host=settings.CELERY_REDIS_HOST, port=settings.CELERY_REDIS_PORT, db=settings.CELERY_REDIS_DB)
    channel = 'channel_{0}'.format(userid)
    json_message = simplejson.dumps(message_dictionary)
    r.publish(channel, json_message)


