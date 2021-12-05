## Details about YOLOv4

#### 1)	Dataset preparation

It is mandatory that our dataset follows the YOLO format. Each image from the dataset would associate with a .txt file having the same name, which contains the object classes and their coordinate following this syntax: 
````
<object-class> <x_center> <y_center> <width> <height>
````
There are many open-source GUI tools (e.g. ["LabelImg" (Download)](https://tzutalin.github.io/labelImg/)) which can help you easily generate label file from image, and we chose to use LabelImg software. To make the label, just simply drag and drop your mouse to create a bounding box around your objects, then the tool would generate the label file automatically.
For each image, a corresponding text file is created, and it has the exactly the same name as the image, but only a .txt extension. 
After the labeling process is complete, your dataset should contain all the images with their bounding box labels (in .txt format). We will store these files into a folder ‘obj’, which will be zipped and then uploaded to Drive.

#### 2) Training with Colab

We decided to train with Google’s Colab GPU, as the training on GPUs is proven to be much faster than on CPUs. To start training the model with Colab, one must have a Google account, and from there it is quite simple to access Colab and start a new session.
In summary, the steps for this part are:
   - Setting up Colab Notebook and Enabling GPU.
   - Cloning and Building Darknet for Running YOLOv3-v4.
   - Downloading YOLOv4 pre-trained model file, the best object detector there is.
   - Training the model
   - Running object detections on webcam images and video in real-time. 



#### 3) YOLOv4 Tiny

We decided to use YOLO (You Only Look Once) algorithm in detecting marcelling. YOLO is a state-of-the-art computer vision algorithm, which can perform object detection and localization in real-time. More details on the algorithm can be found in the paper at: https://arxiv.org/abs/2004.10934. 

For training YOLO algorithm, it is necessary to provide *weights*, which are optimized coefficients of a function of our model, which describes the object we are looking for, in a general form. We haven't started the training from scratch, as it would take a very long time, but rather employed transfer learning.

In transfer learning, we are esentially re-using already available models as a starting point for the purpose of our task. In such a way we created our own weights. The model which we used was pre=trained on COCO dataset - a dataset containing 80 objects.

We chose YOLOv4 tiny structure, as we found out that *tiny* structure allows for faster inferencing, and as such, it was more suitable for our application. Generally speaking, the notation *tiny* simply refers to the structure of YOLO algorithm being simplified to having less layers (such as convolutional layers) in processing the data. 

The training was done with Google Colab, utilizing the free GPU which they provide. This was however limited to a maximum of 12 hours a day of free GPU. 

#### Jetson Nano

Jetson Nano is esentially a small, low power and portable computer, optimized for AI applications, such as in our case, object recognition. Our model was deployed on Jetson Nano, and in addition, it should be also deployed in Docker. 

Docker is esentially making our application run in a container, which contains the application source code, OS libraries and dependancies, so that the code can be ran in any environment. Esentially, Docker would prevent any compatibility issues and enable easy deployment on any platform.

