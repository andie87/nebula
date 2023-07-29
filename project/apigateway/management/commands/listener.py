import datetime
import json
import time
import logging

from django.core.management.base import BaseCommand

from vendor.confluent_kafka.helper import Producer as Producer
from confluent_kafka import Consumer, KafkaError
from apigateway.src.modules.document_processing.upload import UploadDoc

from django.conf import settings

logger = logging.getLogger("GriffinLog")


def send_email(message):
    """ Default format for pepipost """
    print("write_to_log")
    body = f"{message}"
    body += "this message failed to wrote to elastic, please chek elastic service"
    logger.error(body)




def get_meta_data(start_time, json_data):
    if "retry_time" in json_data:
        if json_data["retry_time"]:
            inserted_time = int(json_data["retry_time"])
        else:
            inserted_time = int(json_data["inserted_time"]) if "inserted_time" in json_data else int(time.time())
    else:
        inserted_time = int(json_data["inserted_time"]) if "inserted_time" in json_data else int(time.time())

    idle_time = start_time - inserted_time
    retry_count = int(json_data["retry_counter"]) if "retry_counter" in json_data else 0

    return idle_time, retry_count


def re_compose_meta(message, topic):
    date_now = time.time()
    service_name = message["service_name"]

    if message.get('retry_counter', 0) >= message.get('max_retry', 15):
        # if reach max retry just send email
        try:
            send_email(message, service_name)
            # write to file, to be retried by scheduler
            # reset retry count
            message["retry_counter"] = 0
            message['retry_time'] = None

            # define kafka message life time in the end of retry
            life_time = int(date_now) - int(message["inserted_time"])
            print(f"topic lifetime {life_time}")

        except Exception as err:
            logger.error("error recompose meta".format(str(err), message))
            pass
        return False, message

    print("   message retry : {} ".format(message.get('retry_counter', 1)))
    message['retry_counter'] = int(message.get('retry_counter', 0)) + 1
    message['retry_time'] = date_now
    message['max_retry'] = 15 if 'max_retry' not in message else message.get('max_retry')

    return True, message


def re_compose_message(msg, topic):
    status = False
    meta = {}
    try:
        status, msg = re_compose_meta(msg, topic)
    except Exception as e:
        logger.error("error recompose message {} {}".format(str(e), msg))
        print("error recompose message {} {}".format(str(e), msg))

    return status, msg


def publish_back_to_kafka(msg, topic):
    try:
        kafka_producer = Producer(settings.CONFLUENT_KAFKA_PRODUCER)
    except Exception as err:
        print("error while publish back to kafka: {}".format(str(err)))
        return False
    try:
        status, data = re_compose_message(msg, topic)
        if status:
            data = json.dumps(data).encode('utf-8')
            result = kafka_producer.produce(topic, data)
            kafka_producer.producer_poll(0)


    except Exception as ex:
        kafka_producer.producer_poll(1)
        print("error while publish back to kafka: {}".format(str(ex)))
        time.sleep(5)
        publish_back_to_kafka(msg, topic)
        return False

    kafka_producer.flush()
    return True


class Command(BaseCommand):
    help = 'Initial command to start the listener'

    def add_arguments(self, parser):
        super().add_arguments(parser)

    def handle(self, *args, **options):

        consumer_settings = settings.CONFLUENT_KAFKA_CONSUMER

        try:
            kafka_consumer = Consumer(consumer_settings)
            kafka_consumer.subscribe(settings.TOPIC_KAFKA)
            upload_doc = UploadDoc()
        except Exception as err:
            logger.error("error when initiate kafka topic".format(str(err)))
            err_message = "Failed to connect to kafka. Detail : {}".format(str(err))
            print(err_message)

        try:
            while True:
                msg = kafka_consumer.poll(timeout=1)
                if msg is None:
                    continue
                elif not msg.error():

                    jsonf = json.loads(msg.value().decode('utf-8'))
                    print(msg.value())
                    start_time = time.time()
                    datenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print("Script run at {} ".format(datenow))

                    idle_time, retry_count = get_meta_data(start_time, jsonf)
                    print(f"topic idle_time {idle_time}")

                    try:
                        msg, error, status = upload_doc.processing(jsonf)
                        if not status:
                            print(error)
                            logger.error("upload document failed {}".format(error))
                            publish_back_to_kafka(msg, settings.TOPIC_KAFKA[0])

                        else:
                            # track message lifetime
                            if "meta" in msg:
                                life_time = int(start_time) - int(msg["inserted_time"])
                                print(f"topic lifetime {life_time}")

                    except Exception as err:
                        print("[ ERROR ] {}".format(err))
                        logger.error("General error ".format(str(err)))
                        if "execution_flag" in jsonf:
                            jsonf["execution_flag"]["result"] = str(err)
                            publish_back_to_kafka(jsonf, settings.TOPIC_KAFKA[0])

                elif msg.error().code() == KafkaError._PARTITION_EOF:
                    print('End of partition reached {0}/{1}'.format(msg.topic(), msg.partition()))
                else:
                    print('Error occured: {0}'.format(msg.error().str()))

        except KeyboardInterrupt:
            pass

        except Exception as err:
            logger.error("error when read kafka message {}".format(str(err)))
            print(err)

        finally:
            kafka_consumer.close()
