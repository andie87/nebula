import asyncio
import confluent_kafka
from confluent_kafka import KafkaException


class AIOProducer:
    def __init__(self, configs, loop=None):
        print("[CK][AIOProducer][__init__] 1")
        self._loop = loop or asyncio.get_event_loop()
        self._producer = confluent_kafka.Producer(configs)
        self._cancelled = False
        ''' Remark This line if using Gunicorn '''
        # self._poll_thread = Thread(target=self._poll_loop)
        # self._poll_thread.start()

    def _poll_loop(self):
        print("[CK][AIOProducer][_poll_loop] 1")
        while not self._cancelled:
            print("[AIOProducer][_poll_loop] 2")
            self._producer.poll(0.1)

    def close(self):
        print("[AIOProducer][close] 1")
        self._cancelled = True
        # self._poll_thread.join()

    def produce(self, topic, value):
        """
        An awaitable produce method.
        """
        result = self._loop.create_future()

        def ack(err, msg):
            if err:
                self._loop.call_soon_threadsafe(result.set_exception, KafkaException(err))
            else:
                self._loop.call_soon_threadsafe(result.set_result, msg)

        self._producer.produce(topic, value, on_delivery=ack)
        return result

    def produce2(self, topic, value, on_delivery):
        """
        A produce method in which delivery notifications are made available
        via both the returned future and on_delivery callback (if specified).
        """
        result = self._loop.create_future()

        def ack(err, msg):
            if err:
                self._loop.call_soon_threadsafe(
                    result.set_exception, KafkaException(err))
            else:
                self._loop.call_soon_threadsafe(
                    result.set_result, msg)
            if on_delivery:
                self._loop.call_soon_threadsafe(
                    on_delivery, err, msg)

        self._producer.produce(topic, value, on_delivery=ack)
        return result

    def producer_poll(self, timeout=0):
        self._producer.poll(timeout)


class Producer:
    def __init__(self, configs):
        print("[CK][Producer][produce] 1")
        self._producer = confluent_kafka.Producer(configs)
        self._cancelled = False
        ''' Remark This line if using Gunicorn '''
        # self._poll_thread = Thread(target=self._poll_loop)
        # self._poll_thread.start()

    def _poll_loop(self):
        print("[CK][Producer][_poll_loop] 1")
        while not self._cancelled:
            print("[CK][Producer][_poll_loop] 2")
            self._producer.poll(0.1)

    def close(self):
        print("[CK][Producer][_poll_loop] 2")
        self._cancelled = True
        # self._poll_thread.join()

    def produce(self, topic, value, on_delivery=None):
        self._producer.produce(topic, value, on_delivery=on_delivery)

    def producer_poll(self, timeout=0):
        self._producer.poll(timeout)

    def flush(self):
        self._producer.flush()
