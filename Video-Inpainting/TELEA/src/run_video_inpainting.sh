#! /bin/bash

green=`tput setaf 2`
reset=`tput sgr0`

image_name="inpainting_image"
container_name="inpainting_container"
filename= "video_inpainting.py"

echo -e "${green} Building Docker-image... ${reset}"
docker build -t $image_name .

echo -e "${green} Run Docker-image: ${reset}"
docker run -it --rm --name $container_name -i $image_name "/src/${filename}"

echo -e "${green} Remove Docker-image... ${reset}"
docker rmi $image_name