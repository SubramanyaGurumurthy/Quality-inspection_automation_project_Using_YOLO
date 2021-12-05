# CFDD - Carbon Fiber Discrepancy Detection
#### This is a software for automatic detection of irregularities in carbon fiber, in the production line at CTC-GmbH.

# Real Time Object Detection using YOLO with OpenCV and Training Custom Dataset on Google Colab 
This project implements a real-time detection of marcelling in carbon fibres using YOLOv4 algorithm, that was trained on a custom dataset, and by using a pre-trained weights on a COCO dataset. As an inherent part of object detection stage, a OPC server, Dash server and a database were implemented in three different and dedicated Docker containers. These Docker containers were communicating over the network using a Flask server which was simply integrated into the dataBase application, and storing the timestamps as well as timestamped images of the detected carbon fibre defects.

We attempted to implement YOLOv4 in Docker as well, however as we ran into some errors with this, the algorithm is yet to be containerized. That is the reason why CFDD is subdivided into two folders *yolo* and *opc_dash_docker_db*. To demonstrate how the OPC-server, Dash-server and database work, there is an application in the *opc_dash_docker_db* folder too. This application is a dummy for the actual yolo container. It uploads a continuous flow of timestamps and images to the database.











