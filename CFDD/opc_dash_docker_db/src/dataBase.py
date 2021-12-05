import datetime
from flask import Flask, send_file, request
import json
from constants import DEBUG, HOST_DATABASE, PORT_DATABASE, IMAGES_DATABASE_PATH, MAX_NUM_TIMESTAMPS, IMAGE_STANDARD, DATABASE_NAME, TABLE_NAME
from datetime import datetime, time, timedelta
import random
from helpers import datetime_from_url_string, create_folder, datetime_to_url_string
import os
import sqlite3
import time

class DataBase:
        """This is the main class of the "DataBase" object.
        At Instantiation the DataBAse class registers all the callbacks for the webapp.
        """
        count = 0
         
        @staticmethod
        def create_table():
            '''This function creates a database in the source directory with the name specified in constants.py
            Arguments: The name of the database
            Output: None    
            '''
        
            #Connection to the SQL database
            conn = sqlite3.connect(DATABASE_NAME)
            c = conn.cursor()
            
            #SQL query to create table with columns ID, Timestamp
            c.execute('CREATE TABLE IF NOT EXISTS TABLE_NAME(id INTEGER,TimeStamp TEXT)')   
            
            #Close connection to the SQL database
            c.close()
            conn.close()
            return 
        
        @staticmethod
        def get_timestamps_later_than(datetime_latest_sent) -> list:
            '''
            This function retreives the (max. 10) latest timestamps that have been documented since the given timestamp
            Arguments: The given timestamp(Timestamps later tha this given timsetampwill be returned)
            Output: List of 10 latest timestamps
            
            '''
            #Connection to the SQL database
            conn = sqlite3.connect(DATABASE_NAME) 
            c = conn.cursor()
            
            #Convert the received timestamp into format "m-d-Y H:M:S" for further comparison
            datetime_latest_sent_converted = datetime_latest_sent.strftime("%m-%d-%Y %H:%M:%S")
            
            latest_timestamp = []
            
            #SQL query to retreive latest 10 timestamps (oredered in descending order)
            c.execute('SELECT TimeStamp from TABLE_NAME ORDER BY TimeStamp DESC LIMIT 10')
            results = c.fetchall()
            
            #Store the results into a list
            res = [''.join(i) for i in results]
            
            #select all timestamps that occur after the given timestamp
            for i in res:            
                if (i > datetime_latest_sent_converted):
                    latest_timestamp.append(i)
             
            #Close connection to the SQL database 
            c.close()
            conn.close() 
            
            return latest_timestamp     
        

        @classmethod
        def add_timestamp_to_database(cls, timestamp:datetime) -> None:
            '''
            This function stores the timestamp received from the yolo module into the database. Index values older than MAX_NUM_TIMESTAMPS is deleted
            Arguments: The timestamp to be inserted(received from YOLO)
            Output: None
            
            '''
            #Connection to the SQL database
            conn = sqlite3.connect(DATABASE_NAME) #Connection to the SQL database
            c = conn.cursor()
            
            #Update the ID of the row
            cls.count = cls.count+1
            idx = cls.count
            
            time.sleep(1)    
            
            #SQL query to insert timestamps into database
            sql_insert = "INSERT INTO TABLE_NAME('id' ,'TimeStamp' ) VALUES(?,?)"
            timestamp_input = timestamp.strftime("%m-%d-%Y %H:%M:%S")
            insert_tuple = (idx,timestamp)
            c.execute(sql_insert,insert_tuple)   
            conn.commit() 
            print("Record added successfully") 
            
            #Remove older entries to prevent database from overflowing
            DataBase.database_cleanup()    
            
            #Close connection to the SQL database 
            c.close()
            conn.close()
            return        
        
        
        @staticmethod
        def database_cleanup() -> None:
            '''
            This function is a database maintenance  function that can be used to clean up/delete older timestamps in the database. Currently retains only the latest 10 ids
            Arguments: The database name
            Output: None    
            '''
            #Connection to the SQL database
            conn = sqlite3.connect(DATABASE_NAME) #Connection to the SQL database
            c = conn.cursor()
            
            #SQL query to delete all entries except latest 10
            c.execute('DELETE from TABLE_NAME WHERE id NOT in (SELECT id from TABLE_NAME ORDER BY TimeStamp DESC LIMIT 10)')
            conn.commit() 
            
            #Close connection to the SQL database
            c.close()
            conn.close()          
            
            return      
            
        

        def __init__(self):
            
            create_folder(IMAGES_DATABASE_PATH)
            DataBase.create_table()
            self.app=Flask(__name__)
            self.app.config['UPLOAD_FOLDER'] = IMAGES_DATABASE_PATH

            @self.app.route('/')
            def hello():
                return 'Hello, World!'

            @self.app.route('/get_new_timestamps/<datetime_latest_sent>', methods=['GET'])
            def get_new_timestamps(datetime_latest_sent):
                datetime_latest_sent = datetime_from_url_string(datetime_latest_sent)
                
                timestamps_new = DataBase.get_timestamps_later_than(datetime_latest_sent)
                new_timestamps_to_send_json = json.dumps(timestamps_new, default=str)

                return new_timestamps_to_send_json

            @self.app.route('/get_image/<timestamp_imagename_str>', methods=['GET'])
            def get_image(timestamp_imagename_str):
                if timestamp_imagename_str == IMAGE_STANDARD:
                    filename = IMAGE_STANDARD + '.jpg'
                    path = os.path.join('../data/', filename)
                else:
                    timestamp = datetime_from_url_string(timestamp_imagename_str)
                    timestamp_str = datetime_to_url_string(timestamp)
                    filename = timestamp_str + ".jpg"
                    path = os.path.join('.' + IMAGES_DATABASE_PATH, filename)
                
                return send_file(path, mimetype='image/jpg')

            @self.app.route('/set_timestamp/', methods=['POST', 'GET'])
            def upload_file():
                if request.method == 'POST':
                    if 'file1' not in request.files:
                        return 'there is no file1 in form!'

                    # store uploaded file to folder
                    file1 = request.files['file1']
                    path = os.path.join(self.app.config['UPLOAD_FOLDER'], file1.filename)
                    file1.save(path)
                    
                    # get timestamp from filename
                    filename_without_ending = os.path.splitext(file1.filename)[0]
                    timestamp = datetime_from_url_string(filename_without_ending)

                    DataBase.add_timestamp_to_database(timestamp)
                    
                    # limit number of images in IMAGES_DATABASE_PATH to MAX_NUM_TIMESTAMPS
                    num_files = len([name for name in os.listdir(IMAGES_DATABASE_PATH) if os.path.isfile(os.path.join(IMAGES_DATABASE_PATH, name))])
                    num_files_to_delete = 0
                    if (MAX_NUM_TIMESTAMPS < num_files):
                        num_files_to_delete = num_files - MAX_NUM_TIMESTAMPS
                    images_in_folder = sorted(os.listdir(IMAGES_DATABASE_PATH))

                    for filename in images_in_folder[:num_files_to_delete]:
                        os.remove(IMAGES_DATABASE_PATH + filename)

                    return path

                return '''
                <h1>Upload new File</h1>
                <form method="post" enctype="multipart/form-data">
                <input type="file" name="file1">
                <input type="submit">
                </form>
                '''



if __name__ == '__main__':
    # start  flask network server
    print("Starting DataBase...")
    try:
        database = DataBase()
        
        database.app.run(threaded=True, host=HOST_DATABASE, port=PORT_DATABASE, debug=DEBUG)
    finally:
        print("\nClosing DataBase...")
