import json
from django.conf import settings
import logging
import time


logger = logging.getLogger("GriffinLog")

class AccessLogMiddleware(object):

    def logging(self, user="", path="", service_name="",time_stamp="", response_time=0,request_body="", response="", status_code=200 ):
        #time_stamp_format "%Y-%m-%dT%H:%M:%S"
        log_data ={
            "path": path,
            "user": user,
            "service_name": service_name,
            "response_time" : response_time,
            "time_stamp": time_stamp,
            "MM": time_stamp.split("-")[1],
            "HH": (time_stamp.split("T")[1]).split(":")[0],
            "DD": (time_stamp.split("T")[0]).split("-")[2],
            "request": request_body,
            "response": response,
            "status_code": status_code,
            "retry_counter" : 0,
            "max_retry" : 15,
            "inserted_time" : int(time.time())
        }

        kafka_producer = settings.KAFKA_PRODUCER
        try:
            data = json.dumps(log_data).encode('utf-8')
            result = kafka_producer.produce(settings.TOPIC_KAFKA, data)
            kafka_producer.producer_poll(0)
        except Exception as ex:
            kafka_producer.producer_poll(1)
            msg = "[AccessLogMiddleware][__call__] KafkaException, err : {}".format(str(ex))
            print(msg)
            logger.error(msg)
