import requests
import random
import time
from shutil import copy
import os
import datetime

from constants import DEBUG, HOST_DATABASE, PORT_DATABASE, IMAGES_YOLO_PATH, UPDATE_FREQUENCY_YOLO
from helpers import datetime_to_url_string, create_folder

class Yolo:
    def __init__(self) -> None:
        create_folder(IMAGES_YOLO_PATH)

    @staticmethod
    def yolo_output() -> str:
        # TODO

        # select dummy image with timestamp
        imagename = str(random.randint(1,5)) # choose random image (temp until db acces works)
        filename = imagename + '.jpg'
        path_src = "./data/images_dummy/" + filename

        # store image in IMAGES_YOLO_PATH (directory)
        datetime_now = datetime.datetime.now()
        filename = datetime_to_url_string(datetime_now) + ".jpg"
        path_dest = IMAGES_YOLO_PATH + filename
        copy(path_src, path_dest)

        return filename

    @staticmethod
    def upload_file(filename:str):
        print(filename)
        database_host_adress = 'http://' + HOST_DATABASE + ':' + str(PORT_DATABASE) + "/set_timestamp/"
        image_yolo_path = os.path.join(IMAGES_YOLO_PATH, filename)
        file = open(image_yolo_path, 'rb')
        payload = {
            'file1': (filename, file, 'image/jpeg')
            }
        request = requests.post(database_host_adress, files = payload)
        print(request)
        file.close()
        os.remove(image_yolo_path)

    @classmethod
    def run(cls):
        #TODO: Check if this is actually how yolo is running
        while True:
            filename = cls.yolo_output()
            cls.upload_file(filename)
            time.sleep(UPDATE_FREQUENCY_YOLO)

if __name__ == '__main__':
    # start  flask network server
    print("Starting Yolo...")
    try:
        yolo = Yolo()
        yolo.run()
    finally:
        print("\nClosing Yolo...")
