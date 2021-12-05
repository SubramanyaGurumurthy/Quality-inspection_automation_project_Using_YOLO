# Table of Contents
- [Helpful Infos for a Better Workflow](#helpful-information-for-a-better-workflow)
- [Carbon Fiber Discrepancy Detection](#carbon-fiber-discrepancy-detection)
    - [Structure](#cfdd-structure)
    - [README files](#cfdd-readme-files)
- [Video Inpainting](#video-inpainting)
    - [Structure](#structure)
    - [Seperate README files](#there-are-seperate-readme-files-for-all-three-approaches)

# Helpful Infos for a Better Workflow
* <a href='README_DOCKER.md'>Docker Explanation</a><br>
* <a href='README_GIT.md'>Git Explanation</a><br>

# Carbon Fiber Discrepancy Detection
## CFDD Structure
    .
    ├── ...
    ├── CFDD
    │   ├── README.md
    │   ├── opc_docker_dash_db
    │   │   ├── bin
    │   │   ├── data
    │   │   ├── src
    │   │   ├── Dockerfile
    │   │   ├── README_run.md
    │   │   ├── README_details.md
    │   │   ├── requirements.txt
    │   │   └── Papers
    │   └── yolo
    │       ├── darknet
    │       ├── README_run.md
    │       ├── README_details.md
    │       ├── camera_capture.py
    │       ├── chart_final 6000.png
    │       ├── yolo_tiny_config.cfg
    │       ├── YOLO-V4.py
    │       ├── yolov4-tiny.conv.29
    │       └── Papers
    └── ...

## CFDD README files

* <a href='CFDD/README.md'>What is CFDD?</a><br>
* <a href='CFDD/opc_dash_docker_db/README_RUN.md'>How to run docker with opc, dash and dataBase</a><br>
* <a href='CFDD/opc_dash_docker_db/README_DETAILS.md'>Docker with opc, dash and dataBase implementation details</a><br>
* <a href='CFDD/yolo/README_RUN.md'>YOLO: How to run it</a><br>
* <a href='CFDD/yolo/README_DETAILS.md'>YOLO implementation details</a><br>

# Video Inpainting
## Structure:
    .
    ├── ...
    ├── Video Impainting
    │   ├── TELEA                   # Inpainting using the classical Telea approach
    │   ├── GAN                     # Inpainting using flow guided video completion with GAN
    │   ├── STTN                    # Inpainting using STTN
    │   ├── Videos                  # some results using a test video (original test video also included)
    │   └── Papers                  # the papers we used (pdf)
    └── ...

## There are seperate README files for all three approaches.
* <a href='Video-Inpainting/TELEA/README.md'>Video Inpainting with TELEA README</a><br>
* <a href='Video-Inpainting/GAN/README.md'>Video Inpainting with GAN README</a><br>
* <a href='Video-Inpainting/STTN/README.md'>Video Inpainting with STTN README</a><br>

