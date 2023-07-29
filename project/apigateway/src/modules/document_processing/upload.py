
import logging
import datetime
import time

from django.conf import settings
#from vendor.elasticsearch.helper import Elastic


logger = logging.getLogger("GriffinLog")

class UploadDoc:
    def __init__(self):
        self.messages = None
        pass

    def processing(self, message):
        self.messages = message

        try:
            if "result" in self.messages:
                if self.messages["result"]:
                    print("this message already ingest to elastic")
                    return self.messages, "", True

            # insert to elastic
            index_log = "{}".format(settings.INDEX_NAME)
            document_id = "{}-{}-{}".format(self.messages["service_name"] if "service_name" in self.messages else "",
                                         self.messages["user"], int(time.time()))
            print("{}".format(document_id))
            print("{}".format(self.messages))
            #elastic = Elastic()
            #response, status, err = elastic.insert_document( index_log, document_id, self.messages)

            # if not status:
            #     raise ValueError(err)

            print('[{}] INGESTED REGULER DATA %s ROWS at {}'.format( self.messages, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        except Exception as err:
            error_string = ('[{}] [{}] failed ingest, {}'.format(self.messages, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), err))
            logger.error(error_string)
            self.messages["result"] = False
            return self.messages, "", False

        self.messages["result"] = True
        return self.messages , "", True
