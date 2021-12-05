# How to run different docker applications

1. Run Docker Daemon / Docker Desktop Application
2. Open for each docker container / application in the following a new terminal window in this directory (.CFDD/opc_dash_docker_db/). Then start the application by typing the following command:

## MacOs / Ubuntu
```
bash bin/local_run_[application Name].sh
```
## Microsoft Windows
```
bin/local_run_[application Name].sh
```

For ```[application Name]``` you want to insert one of the following names:

    - dataBase
    - gui
    - yolo
    - opc

Make sure to start by running the dataBase application first (see example below), because this is also where the Yolo Application stores its data (timestamps and images). The server for the Dash webinterface and OPC-Server load their data from the dataBase application.
## MacOs / Ubuntu
```
bash bin/local_run_dataBase.sh
```
## Microsoft Windows
```
bin/local_run_dataBase.sh
```