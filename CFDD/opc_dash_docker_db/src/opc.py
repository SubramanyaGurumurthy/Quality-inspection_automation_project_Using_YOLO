import datetime
import sys
sys.path.insert(0, "..")
import time
import pandas as pd

from constants import UPDATE_FREQUENCY_OPC, MAX_NUM_TIMESTAMPS_OPC
from helpers import get_new_Data, datetime_for_table

from opcua import ua, Server

if __name__ == "__main__":

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/")

    # setup our own namespace, not really necessary but should as spec
    uri = "timestamps"
    id = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # fetch latest timestamps from dataBase
    latest_timestamps = [datetime.datetime.now() for i in range(MAX_NUM_TIMESTAMPS_OPC)]
    latest_timestamps_opc = objects.add_object(id, "latest_timestamp")
    latest_timestamp_opc_list = []
    for i in range(MAX_NUM_TIMESTAMPS_OPC):
        timestamp_string = datetime_for_table(latest_timestamps[i])
        latest_timestamp_opc_list.append(latest_timestamps_opc.add_variable(id, "timestamp no." + str(i), timestamp_string))

    # starting!
    server.start()
    
    try:
        count = 0
        while True:
            time.sleep(int(UPDATE_FREQUENCY_OPC))
            
            new_data = get_new_Data(latest_timestamps[0])
            latest_timestamps = new_data + latest_timestamps
            latest_timestamps = latest_timestamps[:MAX_NUM_TIMESTAMPS_OPC]
        
            for i in range(MAX_NUM_TIMESTAMPS_OPC):
                timestamp_string = datetime_for_table(latest_timestamps[i])
                latest_timestamp_opc_list[i].set_value(timestamp_string)
            
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()