from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


from django.contrib.auth.models import User
from rest_admin.src.modules.auth.models import UserSecretKey
import redis

from django.conf import settings
from datetime import datetime

def connect_to_redis():
    ## no need to close redis connection
    ## https://stackoverflow.com/questions/24875806/redis-in-python-how-do-you-close-the-connection/24876863#24876863

    if settings.REDIS_PASSWORD:
        redis_ins = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, password=settings.REDIS_PASSWORD )
    else:
        redis_ins = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0 )
    return redis_ins


@receiver(post_save, sender=User)
def remove_user_cache(sender, instance, **kwargs):
    print("redis deleted")
    redis_ins = connect_to_redis()
    key_prefix = 'apigateway:user:basic-auth:%s' % instance.username
    keys = redis_ins.keys(f"{key_prefix}*")
    print(keys)
    for key in keys:
        redis_ins.delete(key)





