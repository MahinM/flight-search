import random
import time
import sys
from datetime import datetime
from kafka.client import SimpleClient
from kafka.producer import KeyedProducer

class Producer(object):

    def __init__(self, addr):
        self.client = SimpleClient(addr)
        self.producer = KeyedProducer(self.client)

    def produce_msgs(self, source_symbol):
	   flight_list = [355773,355803,355828,355858,355888,647685,647705,647735,859483,859513]
        while True:
            session_id = random.randint(1000,10000)
            flight_id = flight_list[random.randrange(0,len(flight_list))]
            time_field = datetime.now().strftime("%Y%m%d %H%M%S")
            str_fmt = "{};{};{};{}"
            message_info = str_fmt.format(source_symbol,
                                          session_id,
                                          flight_id,
                                          1, #1 seat
                                          time_field)
            print message_info
            self.producer.send_messages('flight_purchased', source_symbol, message_info)
            time.sleep(1)

if __name__ == "__main__":
    args = sys.argv
    ip_addr = str(args[1])
    partition_key = str(args[2])
    prod = Producer(ip_addr)
    prod.produce_msgs(partition_key)

