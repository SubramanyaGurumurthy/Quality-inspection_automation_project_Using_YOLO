#!/usr/bin/env python
# coding: utf-8

# # Overview
# 
# This program demonstrates the DeepLab model performing semantic segmentation on a sample input video.
# Also, masking is applied to the semantic labels. Afterwards, an inpainting algorithm is used in order to
# reconstruct the background, blocked by the masked foreground object.
# Expected output is a video displaying the semantic segmentation and masking as well as a separate video where inpainting was applied.
# 
# ### About DeepLab
# The models used in this program perform semantic segmentation. Semantic segmentation models focus on assigning semantic labels, such as sky, person, or car, to multiple objects and stuff in a single image.


# ## Import Libraries

import os
from io import BytesIO
import tarfile
import tempfile
from six.moves import urllib

from matplotlib import gridspec
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import cv2
from utils import get_dataset_colormap
import tensorflow as tf
import toml


# ## Import configurations from the config.toml file
config = toml.load("config.toml")


# ## Import helper methods
# These methods help us perform the following tasks:
# * Load the latest version of the pretrained DeepLab model
# * Load the colormap from the PASCAL VOC dataset
# * Adds colors to various labels, such as "pink" for people, "green" for bicycle and more
# * Visualize an image, and add an overlay of colors on various regions

class DeepLabModel(object):
  """Class to load deeplab model and run inference."""

  INPUT_TENSOR_NAME = 'ImageTensor:0'
  OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
  INPUT_SIZE = 513
  FROZEN_GRAPH_NAME = 'frozen_inference_graph'

  def __init__(self, tarball_path):
    """Creates and loads pretrained deeplab model."""
    self.graph = tf.Graph()

    graph_def = None
    # Extract frozen graph from tar archive.
    tar_file = tarfile.open(tarball_path)
    for tar_info in tar_file.getmembers():
      if self.FROZEN_GRAPH_NAME in os.path.basename(tar_info.name):
        file_handle = tar_file.extractfile(tar_info)
        graph_def = tf.GraphDef.FromString(file_handle.read())
        break

    tar_file.close()

    if graph_def is None:
      raise RuntimeError('Cannot find inference graph in tar archive.')

    with self.graph.as_default():
      tf.import_graph_def(graph_def, name='')

    self.sess = tf.Session(graph=self.graph)

  def run(self, image):
    """Runs inference on a single image.

    Args:
      image: A PIL.Image object, raw input image.

    Returns:
      resized_image: RGB image resized from original input image.
      seg_map: Segmentation map of `resized_image`.
    """
    width, height = image.size
    resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)
    target_size = (int(resize_ratio * width), int(resize_ratio * height))
    resized_image = image.convert('RGB').resize(target_size, Image.ANTIALIAS)
    batch_seg_map = self.sess.run(
        self.OUTPUT_TENSOR_NAME,
        feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
    seg_map = batch_seg_map[0]
    return resized_image, seg_map


def create_pascal_label_colormap():
  """Creates a label colormap used in PASCAL VOC segmentation benchmark.

  Returns:
    A colormap for visualizing segmentation results.
  
  colormap = np.zeros((_DATASET_MAX_ENTRIES[_PASCAL], 3), dtype=int)
  ind = np.arange(_DATASET_MAX_ENTRIES[_PASCAL], dtype=int)

  for shift in reversed(list(range(8))):
    for channel in range(3):
      colormap[:, channel] |= bit_get(ind, channel) << shift
    ind >>= 3"""
  colormap = np.ones((2, 3), dtype=int)
  colormap[0]=colormap[0]*0
  colormap[1]=colormap[1]*255
    

  return colormap


def label_to_color_image(label):
  """Adds color defined by the dataset colormap to the label.

  Args:
    label: A 2D array with integer type, storing the segmentation label.

  Returns:
    result: A 2D array with floating type. The element of the array
      is the color indexed by the corresponding element in the input label
      to the PASCAL color map.

  Raises:
    ValueError: If label is not of rank 2 or its value is larger than color
      map maximum entry."""
  print(label)
  if label.ndim != 2:
    raise ValueError('Expect 2-D input label')

  colormap = create_pascal_label_colormap()

  if np.max(label) >= len(colormap):
    raise ValueError('label value too large.')
  return colormap[label]


def vis_segmentation(image, seg_map):
  """Visualizes input image, segmentation map and overlay view."""
  plt.figure(figsize=(15, 5))
  grid_spec = gridspec.GridSpec(1, 4, width_ratios=[6, 6, 6, 1])

  plt.subplot(grid_spec[0])
  plt.imshow(image)
  plt.axis('off')
  plt.title('input image')

  plt.subplot(grid_spec[1])
  seg_image = label_to_color_image(seg_map).astype(np.uint8)
  plt.imshow(seg_image)
  plt.axis('off')
  plt.title('segmentation map')

  plt.subplot(grid_spec[2])
  plt.imshow(image)
  plt.imshow(seg_image, alpha=0.7)
  plt.axis('off')
  plt.title('segmentation overlay')

  unique_labels = np.unique(seg_map)
  ax = plt.subplot(grid_spec[3])
  plt.imshow(
      FULL_COLOR_MAP[unique_labels].astype(np.uint8), interpolation='nearest')
  ax.yaxis.tick_right()
  plt.yticks(range(len(unique_labels)), LABEL_NAMES[unique_labels])
  plt.xticks([], [])
  ax.tick_params(width=0.0)
  plt.grid('off')
  plt.show()


LABEL_NAMES = np.asarray(['background','person'])

FULL_LABEL_MAP = np.arange(len(LABEL_NAMES)).reshape(len(LABEL_NAMES), 1)
FULL_COLOR_MAP = label_to_color_image(FULL_LABEL_MAP)


# ## Select a pretrained model
# We have trained the DeepLab model using various backbone networks. Select one from the MODEL_NAME list.

MODEL_NAME = 'mobilenetv2_coco_voctrainaug'  # @param ['mobilenetv2_coco_voctrainaug', 'mobilenetv2_coco_voctrainval', 'xception_coco_voctrainaug', 'xception_coco_voctrainval']

_DOWNLOAD_URL_PREFIX = 'http://download.tensorflow.org/models/'
_MODEL_URLS = {
    'mobilenetv2_coco_voctrainaug':
        'deeplabv3_mnv2_pascal_train_aug_2018_01_29.tar.gz',
    'mobilenetv2_coco_voctrainval':
        'deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz',
    'xception_coco_voctrainaug':
        'deeplabv3_pascal_train_aug_2018_01_04.tar.gz',
    'xception_coco_voctrainval':
        'deeplabv3_pascal_trainval_2018_01_04.tar.gz',
}
_TARBALL_NAME = 'deeplab_model.tar.gz'

model_dir = tempfile.mkdtemp()
tf.io.gfile.makedirs(model_dir)

download_path = os.path.join(model_dir, _TARBALL_NAME)
print('downloading model, this might take a while...')
urllib.request.urlretrieve(_DOWNLOAD_URL_PREFIX + _MODEL_URLS[MODEL_NAME],
                   download_path)
print('download completed! loading DeepLab model...')
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

MODEL = DeepLabModel(download_path)
print('model loaded successfully!')

# if video was selected as source in the config file, it is captured here
if config["camera-or-video"]["video"]:
  path_to_video = config["video"]["path-to-video"]
  cap = cv2.VideoCapture(path_to_video)

# if camera was selected as source in the config file, it is captured here
if config["camera-or-video"]["camera"]:
  camera_index = config["camera"]["camera-index"]
  cap = cv2.VideoCapture(camera_index)

def seg_thresh(a):
    a[a<15]=0
    a[a>15]=0
    a[a==15]=1
    return a

# for saving result videos, if specified in config file
fourcc = cv2.VideoWriter_fourcc(*'MP4V')

if config["save-video"]["save-segmentation-masking-result"]:
  path_to_segmentation_masking_video = config["save-video"]["path-to-segmentation-masking-result-video"]
  out_segmentation_masking = cv2.VideoWriter(path_to_segmentation_masking_video, fourcc, 20.0, (513,288))

if config["save-video"]["save-inpainting-result"]:
  path_to_inpainting_video = config["save-video"]["path-to-inpainting-result-video"]
  out_inpainting = cv2.VideoWriter(path_to_inpainting_video, fourcc, 20.0, (513,288))


while True:
    ret, frame = cap.read()
    
    if ret == True:
    
        # From cv2 to PIL
        cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)

        # Run model
        resized_im, seg_map = MODEL.run(pil_im)
        seg_map=seg_thresh(seg_map)

        # Adjust color of mask
        seg_image = get_dataset_colormap.label_to_color_image(
            seg_map, get_dataset_colormap.get_pascal_name()).astype(np.uint8)

        # Convert PIL image back to cv2 and resize
        frame = np.array(pil_im)
        r = seg_image.shape[1] / frame.shape[1]
        dim = (int(frame.shape[0] * r), seg_image.shape[1])[::-1]
        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        resized = cv2.cvtColor(resized, cv2.COLOR_RGB2BGR)

        # Stack horizontally color frame and mask
        color_and_mask = np.hstack((resized, seg_image))
        cv2.imshow('mask', color_and_mask)
        
        # Inpainting using TELEA
        one_channel_image = cv2.cvtColor(seg_image, cv2.COLOR_BGR2GRAY)
        inpainted = cv2.inpaint(resized, one_channel_image, 10, cv2.INPAINT_TELEA)
        cv2.imshow('inpainting', inpainted)

        # save videos, if specified in config file
        if config["save-video"]["save-segmentation-masking-result"]:
          out_segmentation_masking.write(seg_image)

        if config["save-video"]["save-inpainting-result"]:
          out_inpainting.write(inpainted)


        if cv2.waitKey(25) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            if config["save-video"]["save-segmentation-masking-result"]:
              out_segmentation_masking.release()
            if config["save-video"]["save-inpainting-result"]:
              out_inpainting.release()            
            break
    else:
        print('end of input')
        cap.release()
        cv2.destroyAllWindows()
        if config["save-video"]["save-segmentation-masking-result"]:
          out_segmentation_masking.release()
        if config["save-video"]["save-inpainting-result"]:
          out_inpainting.release() 
        break


