from google.colab import drive
drive.mount('/content/drive')

!git clone https://github.com/AlexeyAB/darknet


%cd /content/darknet/
!sed -i 's/OPENCV=0/OPENCV=1/' Makefile
!sed -i 's/GPU=0/GPU=1/' Makefile
!sed -i 's/CUDNN=0/CUDNN=1/' Makefile
!sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile
!sed -i 's/LIBSO=0/LIBSO=1/' Makefile

!make

# get the scaled yolov4 weights file that is pre-trained to detect 80 classes (objects) from shared google drive

!wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.conv.29

!pip install split-folders




from google.colab import drive

# Before running anymore code, upload the dataset to an empty directory in Drive. 
# In my case, the directory is called CTC. To do it, just uncomment the line below

%mkdir /content/drive/MyDrive/CTC

%cd /content/drive/MyDrive/CTC/
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


import os
%cd /content/darknet/


# #Set up training file directories for custom dataset

%cp /content/drive/MyDrive/CTC/classes.txt data/obj.names
%mkdir data/obj
#copy image and labels .jpg format
%cp /content/drive/MyDrive/CTC/train/marcelling/*.jpg data/obj/
%cp /content/drive/MyDrive/CTC/val/marcelling/*.jpg data/obj/

# copy image and labels in .png format

%cp /content/drive/MyDrive/CTC/train/marcelling/*.png data/obj/
%cp /content/drive/MyDrive/CTC/val/marcelling/*.png data/obj/

%cp /content/drive/MyDrive/CTC/train/marcelling/*.txt data/obj/
%cp /content/drive/MyDrive/CTC/val/marcelling/*.txt data/obj/

# referenced https://blog.roboflow.com/train-yolov4-tiny-on-custom-data-lighting-fast-detection/ for below:
with open('data/obj.data', 'w') as out:
  out.write('classes = 1\n')
  out.write('train = data/train.txt\n')
  out.write('valid = data/valid.txt\n')
  out.write('names = data/obj.names\n')
  out.write('backup = backup/')

  # #write train file (just the image list)


with open('data/train.txt', 'w') as out:
  for img in [f for f in os.listdir('/content/drive/MyDrive/CTC/train/marcelling') if (f.endswith('jpg') or f.endswith('png'))]:
    out.write('data/obj/' + img + '\n')


    

#write the valid file (just the image list)
import os

with open('data/valid.txt', 'w') as out:
  for img in [f for f in os.listdir('/content/drive/MyDrive/CTC/train/marcelling') if (f.endswith('jpg') or f.endswith('png'))]:
    out.write('data/obj/' + img + '\n')

#we build iteratively from base config files. This is the same file shape as cfg/yolo-obj.cfg
def file_len(fname):
  with open(fname) as f:
    for i, l in enumerate(f):
      pass
  return i + 1

num_classes = file_len('/content/drive/MyDrive/CTC/classes.txt')
max_batches = num_classes*2000
steps1 = .8 * max_batches
steps2 = .9 * max_batches
steps_str = str(steps1)+','+str(steps2)
num_filters = (num_classes + 5) * 3


print("writing config for a custom YOLOv4 detector detecting number of classes: " + str(num_classes))

#Instructions from the darknet repo
#change line max_batches to (classes*2000 but not less than number of training images, and not less than 6000), f.e. max_batches=6000 if you train for 3 classes
#change line steps to 80% and 90% of max_batches, f.e. steps=4800,5400
if os.path.exists('./cfg/custom-yolov4-tiny-detector.cfg'): os.remove('./cfg/custom-yolov4-tiny-detector.cfg')


#customize iPython writefile so we can write variables
from IPython.core.magic import register_line_cell_magic

@register_line_cell_magic
def writetemplate(line, cell):
    with open(line, 'w') as f:
        f.write(cell.format(**globals()))

# Commented out IPython magic to ensure Python compatibility.
# %%writetemplate ./cfg/custom-yolov4-tiny-detector.cfg
# [net]
# # Testing
# #batch=1
# #subdivisions=1
# # Training
# batch=64
# subdivisions=24
# width=416
# height=416
# channels=3
# momentum=0.9
# decay=0.0005
# angle=0
# saturation = 1.5
# exposure = 1.5
# hue=.1
# 
# learning_rate=0.00261
# burn_in=1000
# max_batches = 6000
# policy=steps
# steps= .8*max_batches
# scales=.1,.1
# 
# [convolutional]
# batch_normalize=1
# filters=32
# size=3
# stride=2
# pad=1
# activation=leaky
# 
# [convolutional]
# batch_normalize=1
# filters=64
# size=3
# stride=2
# pad=1
# activation=leaky
# 
# [convolutional]
# batch_normalize=1
# filters=64
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers=-1
# groups=2
# group_id=1
# 
# [convolutional]
# batch_normalize=1
# filters=32
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [convolutional]
# batch_normalize=1
# filters=32
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers = -1,-2
# 
# [convolutional]
# batch_normalize=1
# filters=64
# size=1
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers = -6,-1
# 
# [maxpool]
# size=2
# stride=2
# 
# [convolutional]
# batch_normalize=1
# filters=128
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers=-1
# groups=2
# group_id=1
# 
# [convolutional]
# batch_normalize=1
# filters=64
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [convolutional]
# batch_normalize=1
# filters=64
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers = -1,-2
# 
# [convolutional]
# batch_normalize=1
# filters=128
# size=1
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers = -6,-1
# 
# [maxpool]
# size=2
# stride=2
# 
# [convolutional]
# batch_normalize=1
# filters=256
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers=-1
# groups=2
# group_id=1
# 
# [convolutional]
# batch_normalize=1
# filters=128
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [convolutional]
# batch_normalize=1
# filters=128
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers = -1,-2
# 
# [convolutional]
# batch_normalize=1
# filters=256
# size=1
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers = -6,-1
# 
# [maxpool]
# size=2
# stride=2
# 
# [convolutional]
# batch_normalize=1
# filters=512
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# ##################################
# 
# [convolutional]
# batch_normalize=1
# filters=256
# size=1
# stride=1
# pad=1
# activation=leaky
# 
# [convolutional]
# batch_normalize=1
# filters=512
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [convolutional]
# size=1
# stride=1
# pad=1
# filters=18
# activation=linear
# 
# 
# 
# [yolo]
# mask = 3,4,5
# anchors = 10,14,  23,27,  37,58,  81,82,  135,169,  344,319
# classes=1
# num=6
# jitter=.3
# scale_x_y = 1.05
# cls_normalizer=1.0
# iou_normalizer=0.07
# iou_loss=ciou
# ignore_thresh = .7
# truth_thresh = 1
# random=0
# nms_kind=greedynms
# beta_nms=0.6
# 
# [route]
# layers = -4
# 
# [convolutional]
# batch_normalize=1
# filters=128
# size=1
# stride=1
# pad=1
# activation=leaky
# 
# [upsample]
# stride=2
# 
# [route]
# layers = -1, 23
# 
# [convolutional]
# batch_normalize=1
# filters=256
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [convolutional]
# size=1
# stride=1
# pad=1
# filters=18
# activation=linear
# 
# [yolo]
# mask = 1,2,3
# anchors = 10,14,  23,27,  37,58,  81,82,  135,169,  344,319
# classes=1
# num=6
# jitter=.3
# scale_x_y = 1.05
# cls_normalizer=1.0
# iou_normalizer=0.07
# iou_loss=ciou
# ignore_thresh = .7
# truth_thresh = 1
# random=0
# nms_kind=greedynms
# beta_nms=0.6

# Commented out IPython magic to ensure Python compatibility.
#here is the file that was just written. 
#you may consider adjusting certain things

#like the number of subdivisions 64 runs faster but Colab GPU may not be big enough
#if Colab GPU memory is too small, you will need to adjust subdivisions to 16

%cat cfg/custom-yolov4-tiny-detector.cfg

!./darknet detector train data/obj.data cfg/custom-yolov4-tiny-detector.cfg yolov4-tiny.conv.29 -dont_show -map

#If you get CUDA out of memory adjust subdivisions above!
#adjust max batches down for shorter training above



