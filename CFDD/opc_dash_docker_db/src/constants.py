# general constants
# ---------------------------------------------

# set the debug mode to True or false
DEBUG=True


# GUI
# ---------------------------------------------

# Port the dash GUI Server is reachable
PORT_GUI = 8050

# network host address
HOST_GUI = "172.19.0.2"

# updatefrequency of UI in seconds
UPDATE_FREQUENCY_GUI = 2.0

# setting how long it takes until gui shows, that no error is found after the last error detection
GUI_ERROR_THRESHOLD = 2

# standard image
IMAGE_STANDARD = "standard_image"

# the address the web-app from the dash-Server accesses the images from the DataBase directly
HOST_DATABASE_BROWSER = "localhost"


# OPC
# ---------------------------------------------

# sets the interval how often new data are fetched from the database
UPDATE_FREQUENCY_OPC = 2.0

#specifies the name of the database file
DATABASE_NAME = "./data/MARCE.db"

# specifies the name of the table in the database
TABLE_NAME = "MARCELLING"

# limits the number of timestamps fetched by opc server
MAX_NUM_TIMESTAMPS_OPC = 10

# YOLO
# ---------------------------------------------

IMAGES_YOLO_PATH = "./data/images_yolo/"

UPDATE_FREQUENCY_YOLO = 1.5

# DataBase
# ---------------------------------------------

# Port the dash DataBase Server is reachable
PORT_DATABASE = 8052

# network host address
HOST_DATABASE = "172.19.0.3"

# flask puts pushed images here
IMAGES_DATABASE_PATH = './data/images_database/'

# limits the number of timestamps and images stored in the database and the directory
MAX_NUM_TIMESTAMPS = 10
