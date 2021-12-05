# Table of Contents
- [How to train a custom YOLO object detector](#how-to-train-a-custom-yolo-object-detector-using-google-colab)
  - [1. Create a 'yolo' folder in Google Drive, mount drive, ...](#1-create-a-yolo-folder-in-google-drive-mount-drive-link-your-folder-and-navigate-to-the-yolo-folder)
  - [2. Git clone the Darknet repository](2-git-clone-the-darknet-repository-with-git-to-your-local-computer)
  - [3. Create & upload the files for training](3-create--upload-the-files-for-training-ie-labeled-custom-dataset-yolov4-customcfg-name-of-the-classes-objnames-objdata-)
  - [4. Prepare the custom .cfg file.](#4-prepare-the-custom-cfg-file-you-need-to-make-the-following-changes-in-your-config-file-eg-yolov4-customcfg)
  - [5. Make changes in the Makefile to enable OPENCV and GPU](#5-make-changes-in-the-makefile-to-enable-opencv-and-gpu)
  - [6. Download pre-trained weights - fine-tuning](#6-download-pre-trained-weights---fine-tuning)
  - [7. Perform training](#7-perform-training)
  - [8. Test your custom training](#8-test-your-custom-training)
- [Setting up YOLOv4 on Jetson Nano](#setting-up-yolov4-on-jetson-nano)
  - [Getting started with Jetson Nano](#getting-started-with-jetson-nano)
  - [Setting up the hardware with ubuntu OS](#setting-up-the-hardware-with-ubuntu-os-burning-the-iso-image-onto-sd-card)
  - [Install and Run YOLO on Nvidia Jetson Nano (with GPU)](#setting-up-the-hardware-with-ubuntu-os-burning-the-iso-image-onto-sd-card)
  - [How to run YOLO on both COCO dataset and a custom dataset](#how-to-run-yolo-on-both-coco-dataset-and-a-custom-dataset)

# How to train a custom YOLO object detector (Using Google Colab)
## 1. Create a 'yolo' folder in Google Drive, mount drive, link your folder and navigate to the 'yolo' folder.
```
from google.colab import drive
drive.mount('/content/drive')
```
## 2. Git clone the [Darknet repository](https://github.com/AlexeyAB/darknet) with git to your local computer. 

## 3. Create & upload the files for training (i.e. labeled custom dataset 'yolov4-custom.cfg', name of the classes 'obj.names', 'obj.data' )

- ‘obj.zip’ contains input image files (‘.jpg’ and / or ‘.png’), and their corresponding labels. 

- ‘yolov4-custom.cfg’ is a configuration file, which essentially specifies how is our network structured (the number of convolutional layers the image is passed through, all the filtering, up sampling and other corresponding operations which extract features from the input). Here, we can copy the yolov4-tiny.cfg from the ‘darknet/cfg’ directory, and save it with the different name (such as ‘yolov4-custom.cfg’)

*We opted for using yolov4-tiny network, which is simpler than the full yolov4, and as 8x faster at the inference time.*
    
- ‘obj.names’ is a file which contains the names of the objects which we detect. In our case it was only one object – ‘marcelling’. In the case of [COCO dataset](https://cocodataset.org/#home), one can see 80 objects, which the model can detect.

- ‘obj.data’ is a file that contains the paths to the training dataset. 

We can create these files manually. To do so, we upload *zipped* dataset to drive, extract it and use following code to make *obj.data* and *obj.names* files.

Preparing the training and testing dataset by using [splitfolder](https://pypi.org/project/split-folders/) library. We wanted to validate our model during training with examples that have not been seen yet, therefore we needed a validation set. Note that the structure of the uploaded *zip* file is the following:

    .
    ├── Marcelling_dataset
    └── marcelling              
        ├── img0.jpg                     
        ├── img0.txt                    
        ├── img1.png                  
        ├── img1.txt  
        └── ...

Where the marcelling folder contains images of the defects and the corresponding labels in YOLOv4 format. Note that the images which we used were in both .jpg and .png format, which was accounted for in the code below.

```
!unzip Marcelling_dataset.zip

%cd /content/drive/MyDrive/CTC/Marcelling_dataset/marcelling/
!cp classes.txt /content/drive/MyDrive/CTC/
!rm classes.txt

input_folder = '/content/drive/MyDrive/CTC/Marcelling_dataset'
output_folder = '/content/drive/MyDrive/CTC/'

import splitfolders
splitfolders.ratio(input_folder, output=output_folder,seed=1337, ratio=(.8,.1,.1), group_prefix=2)

%cp /content/drive/MyDrive/CTC/classes.txt /content/darknet/data/train.txt
%cp /content/drive/MyDrive/CTC/classes.txt /content/darknet/data/valid.txt
```
### Setting up the files
```
import os
%cd /content/darknet/

%cp /content/drive/MyDrive/CTC/classes.txt data/obj.names
%mkdir data/obj
```
Copy image and labels .jpg format
```
%cp /content/drive/MyDrive/CTC/train/marcelling/*.jpg data/obj/
%cp /content/drive/MyDrive/CTC/val/marcelling/*.jpg data/obj/
```
Copy image and labels in .png format
```
%cp /content/drive/MyDrive/CTC/train/marcelling/*.png data/obj/
%cp /content/drive/MyDrive/CTC/val/marcelling/*.png data/obj/

%cp /content/drive/MyDrive/CTC/train/marcelling/*.txt data/obj/
%cp /content/drive/MyDrive/CTC/val/marcelling/*.txt data/obj/
```
referenced [Roboflow](https://blog.roboflow.com/train-yolov4-tiny-on-custom-data-lighting-fast-detection/) for below:
```
with open('data/obj.data', 'w') as out:
  out.write('classes = 1\n')
  out.write('train = data/train.txt\n')
  out.write('valid = data/valid.txt\n')
  out.write('names = data/obj.names\n')
  out.write('backup = backup/')
```
Write train file (just the image list)
```
with open('data/train.txt', 'w') as out:
  for img in [f for f in os.listdir('/content/drive/MyDrive/CTC/train/marcelling') if (f.endswith('jpg') or f.endswith('png'))]:
    out.write('data/obj/' + img + '\n')
```
Write the valid file (just the image list)
```
with open('data/valid.txt', 'w') as out:
  for img in [f for f in os.listdir('/content/drive/MyDrive/CTC/train/marcelling') if (f.endswith('jpg') or f.endswith('png'))]:
    out.write('data/obj/' + img + '\n')
```
## 4. Prepare the custom .cfg file. You need to make the following changes in your config file (e.g. yolov4-custom.cfg)
    - change line batch to batch=64
    - change line submissions to submissions=16 
    - set network size width=416, height=416 or any value multiple of 32

    - change line max_batches to (classes*2000) but not less than the number of training images and not less than 6000), exp. max_batches=6000 if you train for 3 classes
    - change the line steps to 80% and 90% of max_batches, exp. steps=4800,5400

    - change filters=255 to filters=(classes+5)*3 in the last "3" [convolutional] layers BEFORE each [yolo] layer. 
    - change line classes=80 to your number of objects in each of "3" [yolo] layers.  

So, if classes=1 then, filters=18. If classes=2 then, filters=21.

## 5. Make changes in the Makefile to enable OPENCV and GPU
```
%cd darknet
!sed -i 's/OPENCV=0/OPENCV=1/' Makefile
!sed -i 's/GPU=0/GPU=1/' Makefile
!sed -i 's/CUDNN=0/CUDNN=1/' Makefile
!make
```
## 6. Download pre-trained weights - fine-tuning
```
!wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.conv.29
```
## 7. Perform training 
```
!./darknet detector train data/obj.data cfg/yolov4-custom.cfg yolov4-tiny.conv.29 -dont_show
```
## 8. Test your custom training 
Make changes to your custom .cfg file (i.e. yolov4-custom.cfg) to set it to test mode:
- change line batch to batch=1
- change line subdivisions to subdivisions=1 
# Setting up YOLOv4 on Jetson Nano
## [Getting started](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit) with Jetson Nano
## Setting up the hardware with ubuntu OS (burning the iso image onto SD card):
### 1. Download Jetson [Nano developer kit SD card Image](https://developer.nvidia.com/jetson-nano-sd-card-image)
### 2. Writing the image on to SD card using Windows / Ubuntu
-	Format the SD Memory card  
-	Download the [etcher software](https://www.balena.io/etcher)
-	only Windows: Insert the SD memory card if not inserted to computer, and select the memory card as drive
- only Ubuntu: Click on select image and choose the zipped image file downloaded earlier
-	Flash the downloaded ISO onto memory card

## Install and Run YOLO on Nvidia Jetson Nano (with GPU)
### 1. Update the libraries 
```
sudo apt-get update
```
### 2. Export Cuda path (check the CUDA version in your Jetson and change the below command accordingly)
```
export PATH=/usr/local/cuda-10.2/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-10.2/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```
### 3. Download Darknet and YOLOv4 (pre-trained weights)
```
git clone https://github.com/AlexeyAB/darknet
cd darknet
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights
```
### 4. Enable the GPU. We need to Edit the Makefile to enable the GPU, Cuda and Opencv. 
```
gedit Makefile

Set the values:
GPU=1
CUDNN=1
OPENCV=1
and the rest leave it as it is
```
### 5. Compile Darknet
```
make
```
## How to run YOLO on both COCO dataset and a custom dataset 
Make sure that you have already uploaded the customized configuration file and the model weights after training on Google Colab into /darknet/ folder.  

### 1. Go into the Darknet folder
```
cd darknet
```
### 2. Choose one of the following command lines depending on which which type of detection you want to perform. 
#### 2a. Running inference on an image
Edit “test.jpg” with the path of your image.
```
./darknet detector test cfg/coco.data cfg/yolov4_tiny.cfg yolov4-tiny.weights -ext_output text.jpg
```
#### 2b. Running a real-time inference from the webcam
The 0 at the end of the line is the index of the Webcam. So, if you have more webcams, you can change the index (with 1, 2, and so on) to use a different webcam.
```
./darknet detector demo cfg/coco.data cfg/yolov4_tiny.cfg yolov4-tiny.weights -c 0
```
#### 2c. Running inference on a video file
Edit “test.mp4” with the path of your video file.
```
./darknet detector demo cfg/coco.data cfg/yolov4_tiny.cfgyolov4-tiny.weights -ext_output test.mp4
```
#### 2d. Running a real-time inference using our weights, our training data and a Raspberry-Pi camera
```
$ ./darknet detector demo cfg/obj.data cfg/yolov4-tiny-custom.cfg yolov4-6000.weights 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)416, height=(int)416,format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv flip-method=2 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink'
```
