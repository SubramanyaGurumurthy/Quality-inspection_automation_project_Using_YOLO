import cv2
vidcap = cv2.VideoCapture(r'path\to\your\mask-video\x.mp4')
success,image = vidcap.read()
count = 0
success = True
while success:
  success,image = vidcap.read()
  image = cv2.resize(image,(512,288),fx=0, fy=0)
  cv2.imwrite(r"C:\Users\Asus\Desktop\auds\x\frame%d.png" % count, image)     # save frame as JPEG file
  if cv2.waitKey(10) == 27:                     # exit if Escape is hit
      break
  count += 1
