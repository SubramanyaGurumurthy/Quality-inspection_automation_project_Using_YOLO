'''
Capturing images from Logitec C270 camera by clicking "SPACE" key has been implemented. 
The captured images are saved to the folder with a given path.   
'''
# Import the opencv libraries
import cv2
import os

# define a video capture object: '0' PC Webcam, '1' external webcam
cam = cv2.VideoCapture(1)

cv2.namedWindow("Output")

img_counter = 0

while True:
    # Capture the video frame
    # by frame
    ret, frame = cam.read()

    if not ret:
        print("failed to grab frame")
        break
    # Display the resulting frame
    cv2.imshow("Output", frame)

    k = cv2.waitKey(1)
    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        # SPACE pressed to capture images
        img_name = "img_{}.png".format(img_counter)
        # Define the path where to save the captured images
        path = '/Users/ozge/Desktop/defect_img'
        #cv2.imwrite(img_name, frame)
        # Save the captured images
        cv2.imwrite(os.path.join(path, img_name), frame)
        # Print a note once the image is captured
        print("{} written!".format(img_name))
        img_counter += 1

# After the loop release the cap object
cam.release()
# Destroy all the windows
cv2.destroyAllWindows()
