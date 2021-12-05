#! /bin/bash

green=`tput setaf 2`
reset=`tput sgr0`

name_image="server-image-yolo"
name_container="server-container-yolo"
filename="yolo.py"
IP=172.19.0.5
PORT=8051
NETWORKID="ntwofleads"

echo -e "${green}\n\nBuilding docker-image...${reset}"
docker build -t $name_image .

echo -e "${green}\n\nShow all images:${reset}"
docker image ls
echo -e "\n\n"

echo -e "${green}\n\nRun docker-image:${reset}"

# The --rm causes Docker to automatically remove the container when it exits.
docker run -it --rm -p $PORT:$PORT --network $NETWORKID --ip $IP --name $name_container -i $name_image "src/${filename}"

echo -e "${green}\n\nRemove image...${reset}"
docker rmi $name_image