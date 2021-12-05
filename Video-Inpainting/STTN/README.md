# Video Inpainting - STTN
#### (Note - Unfortunately STTN could not be implemented in docker. Following instructions are for running on local machine)

1. Clone STTN from git in your local machine

     `git clone https://github.com/researchmm/STTN.git`

2. Download the pretrained models from the link below, save it in `checkpoints/` folder.
  
     https://drive.google.com/file/d/1ZAMV8547wmZylKRt5qR_tC5VlosXD4Wv/view?usp=sharing

3. Keep your sample video file in `/examples` and create a folder inside `/examples` for storing mask video frames as images
4. In a seperate folder download deeplab from git into your local machine 

     https://github.com/tensorflow/models/tree/master/research/deeplab
     
5. Save the provided <a href='deeplab_modified.ipynb'>deeplab_modified.ipynb</a> in `../deeplab/` folder (in local machine)

6. Run your video file in `deeplab_modified.ipynb` to obtain mask video file

7. Run the obtained mask video in <a href='frames.py'>frames.py</a> to extract its frames and save it in created mask folder

8. Run `python3 test.py --video examples/video_file_name --mask examples/mask_folder_name  --ckpt checkpoints/sttn.pth`
  
9. The outputs videos are saved at `examples/`
  
10. For live video implementation an object needs to be created which temporarily stores the mask frames and this object is can be used for Inpainting
