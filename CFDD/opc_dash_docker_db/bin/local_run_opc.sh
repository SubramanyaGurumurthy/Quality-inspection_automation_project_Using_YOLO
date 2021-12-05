#! /bin/bash

green=`tput setaf 2`
reset=`tput sgr0`

name_image="server-image-opc"
name_container="server-container-opc"
filename="opc.py"
IP=172.19.0.4
PORT=4840
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