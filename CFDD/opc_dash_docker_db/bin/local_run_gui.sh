#! /bin/bash

green=`tput setaf 2`
reset=`tput sgr0`

name_image="server-image-gui"
name_container="server-container-gui"
filename="gui.py"
IP=172.19.0.2
PORT=8050
NETWORKID="ntwofleads"

echo -e "${green}\n\nBuilding docker-image...${reset}"
docker build -t $name_image .

echo -e "${green}\n\nShow all images:${reset}"
docker image ls
echo -e "\n\n"

echo -e "${green}\n\nRun docker-image:${reset}"

# The -it runs Docker interactively (so you get a pseudo-TTY with STDIN).
# The --rm causes Docker to automatically remove the container when it exits.
(curl --silent --retry 30 --retry-delay 1 --retry-connrefused \
    http://localhost:$PORT ; \
    (sleep 2 && python -m webbrowser http://localhost:$PORT)) &
docker run -it --rm -p $PORT:$PORT --network $NETWORKID --ip $IP --name $name_container -i $name_image "src/${filename}"

echo -e "${green}\n\nRemove image...${reset}"
docker rmi $name_image
