# Image Inpainting - TELEA

* <a href='doc/README.md'>Deeplab documentation</a><br>

## Prerequisites

The following should be installed on your machine before starting with the installation process:

*   Docker

## Installation

1. start Docker 
2. run the `src/run_video_inpainting.sh` bash file 

### Alternative 1

1. start Docker
2. run `docker build -t inpainting_image .` in command line
3. run `docker run -it --rm --name inpainting_container -i inpainting_image "/src/video_inpainting.py"` in command line 

### Alternative 2

If pre-built Docker image is available as .tar file

1. start Docker
2. run `docker load -i <absolute path to image file>`


## Settings

For configuration see the `src/config.toml` file.
