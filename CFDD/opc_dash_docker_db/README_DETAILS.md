
# Objective: 
Transfer object detection values reseived from Jetson Nano to a database and communicate the payload consisting of timestamp, images of marcelling detected to the OPC server and webserver. All four parts are supposed to be virtualized and runnable on different devices.

# Docker
Every Application is containerized in a dedicated docker application. With the right docker settings is possible to run all four applications on different devices. For simplicity no docker-compose or Kubernetes software is used yet. A virtual network is setup instead, everytime the dataBase application is started. The containers are communicating via flask over network protocol on different ports.

# Applications
## OPC UA Server
OPC UA (short for Open Platform Communications United Architecture) is a data exchange standard for industrial communication (machine-to-machine or PC-to-machine communication). 
The implementation of the OPC UA server is based on the demo implementation(https://github.com/FreeOpcUa/python-opcua). 
Currently, the OPC UA server is assigned a separate namespace and is started along with YOLO module. The timestamp at which marcelling is detected is inserted into the database and adiitionally displayed on the GUI along with an image of the faulty carbon sheet.

## Database Functionality (SQLite3 with Python)
The database provides the following 4 capabilities:
- *Create database*: If a table does not exist, create one with the name specified in CONSTANTS.py
- *Insert database*: Insert the timestamps received from the YOLO module into the database. When the number of rows exceeds MAX_NUM_TIMESTAMPS defined in CONSTANTS.py the older entries are deleted.
- *Query database*: Function retreives 10 latest timestamps that have been documented since the timestamp specified by the user.
- *Delete database*: It is a database maintenance function that can be used to clean up/delete older timestamps in the database. Currently retains only the latest 10 ids 

- *Flask Server*: The Flask Server makes the database accessible via the network. This API is accessed by the other three applications provided.

## YOLO
The Yolo Application is just a dummy application for the actual implementation of yolo in docker. (see readme in the CFDD folder)

## Dash Server
The dash server is fetching the latest timestamps as well as images from the database. It hosts a website where these information can be accessed and the current marcelling status can be observed easily. This Webpage is opened automatically by the batch or bash script provided.

# Further Improvements
- Implement security (cryptography)
- Additional queries to take advantage of values in database
- using docker-compose or Kubernetes to manage the applications on different devices
- performance improvements regarding speed and update frequency

# Standard Documentation
- https://open62541.org/doc/current/

# Useful Links
- https://www.youtube.com/watch?v=uu5p_3lHqcU
- https://github.com/mailrocketsystems/OPCUA/blob/main/opcua_server.py