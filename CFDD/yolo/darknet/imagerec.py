from datetime import datetime
from darknet import *

# load in our YOLOv4 architecture network

network, class_names, class_colors = load_network("cfg/yolov4-csp.cfg", "cfg/coco.data", "yolov4-csp.weights")
width = network_width(network)
height = network_height(network)

# darknet helper function to run detection on image
def darknet_helper(img, width, height):
  darknet_image = make_image(width, height, 3)
  img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  img_resized = cv2.resize(img_rgb, (width, height),
                              interpolation=cv2.INTER_LINEAR)

  # get image ratios to convert bounding boxes to proper size
  img_height, img_width, _ = img.shape
  width_ratio = img_width/width
  height_ratio = img_height/height

  # run model on darknet style image to get detections
  copy_image_from_bytes(darknet_image, img_resized.tobytes())
  detections = detect_image(network, class_names, darknet_image)
  free_image(darknet_image)
  return detections, width_ratio, height_ratio

  from time import localtime, asctime, gmtime
from datetime import datetime

# run test on person.jpg image that comes with repository
image = cv2.imread("data/person.jpg")





#image = cv2.imread("data/blk.png")
detections, width_ratio, height_ratio  = darknet_helper(image, width, height)
print(detections)

out = pd.DataFrame({'time':[], 'label':[], 'confidence_pct':[]}) # Initialize empty dataframe

for label, confidence, bbox in detections:
  
  left, top, right, bottom = bbox2points(bbox)
  left, top, right, bottom = int(left * width_ratio), int(top * height_ratio), int(right * width_ratio), int(bottom * height_ratio)
  cv2.rectangle(image, (left, top), (right, bottom), class_colors[label], 2)
  cv2.putText(image, "{} {} [{:.2f}]".format(ts, label, float(confidence)),
                    (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    class_colors[label], 2)
  now = datetime.now()
  ts = now.strftime("%H:%M:%S")

  
  dict_to_append = {'time':ts, 'label':label, 'confidence_pct':confidence}
  out = out.append(dict_to_append, True)
  
out = out.drop_duplicates(subset=['label']) 
data = out.to_json(orient='columns')

cv2_imshow(image)
print(out)

import json
with open('/content/data.json', 'w') as f:
    json.dump(data, f)


