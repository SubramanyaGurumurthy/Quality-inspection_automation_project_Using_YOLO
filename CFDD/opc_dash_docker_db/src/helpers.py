import urllib.parse
import datetime
import requests
import json
import os
from constants import DEBUG, PORT_GUI, HOST_GUI, HOST_DATABASE, PORT_DATABASE

# creates file directory if not created yet
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return

def datetime_to_url_string(timestamp:datetime) -> str:
    timestamp_string = timestamp.isoformat()
    timestamp_url_string = urllib.parse.quote_plus(timestamp_string)
    return timestamp_url_string

def datetime_from_url_string(timestamp_url_string:str) -> datetime:
    timestamp_string = urllib.parse.unquote(timestamp_url_string)
    timestamp = datetime.datetime.fromisoformat(timestamp_string)
    return timestamp

def datetime_for_table(datetime):
    return datetime.strftime("%Y-%m-%d %H:%M:%S")

def get_new_Data(timestamp_latest_received:datetime) -> list:
    """This function returns new timestamps that are newer than the timestamp given by the parameter.
    """
    timestamp_latest_received = datetime_to_url_string(timestamp_latest_received)
    uri_dataBase = 'http://' + HOST_DATABASE + ':' + str(PORT_DATABASE) + '/get_new_timestamps/' + timestamp_latest_received
    
    try:
        u_response = requests.get(uri_dataBase)
        json_response = u_response.text

        new_data_strings = json.loads(json_response)
        new_data_datetimes = list(map(datetime.datetime.fromisoformat, new_data_strings))

        print("connection success")

    except requests.ConnectionError:
        print("Connection Error")
        new_data_datetimes = []

    return new_data_datetimes
