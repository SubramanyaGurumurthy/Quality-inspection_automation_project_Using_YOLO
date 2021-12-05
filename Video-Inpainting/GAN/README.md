# Video Inpainting - Flow guided video completion (FGVC) using GAN

#### (Note - Unfortunately FGVC/GAN could not be implemented in docker. Following instructions are for running on local machine)

## Prerequisites
- Anaconda
- Python 3.8 (tested on 3.8.5)
- PyTorch 1.6.0

and the Python dependencies listed in requirements.txt

1. Clone FGVC from git in your local machine

     `git clone https://github.com/vt-vl-lab/FGVC.git`


2. To get started, please run the following commands:
  ```
  conda create -n FGVC
  conda activate FGVC
  conda install pytorch=1.6.0 torchvision=0.7.0 cudatoolkit=10.1 -c pytorch
  conda install matplotlib scipy
  pip install -r requirements.txt
  ```

3. Next, download the model weight and demo data using the following command:
  ```
  chmod +x download_data_weights.sh
  ./download_data_weights.sh
  ```
## Obtain mask video

4. In a seperate folder download deeplab from git into your local machine 

     https://github.com/tensorflow/models/tree/master/research/deeplab
     
5. Save the provided <a href='deeplab_modified.ipynb'>deeplab_modified.ipynb</a> in `../deeplab/` folder (in local machine)

6. Run your video file in `deeplab_modified.ipynb` to obtain mask video file

## Quick start

- Object removal:
```bash
cd tool
python video_completion.py \
       --mode object_removal \
       --path ../data/your_video_file \
       --path_mask ../data/your_mask_file \
       --outroot ../result/result_file \
       --seamless
```

- FOV extrapolation:
```bash
cd tool
python video_completion.py \
       --mode video_extrapolation \
       --path ../data/your_video_file \
       --outroot ../result/tennis_extrapolation \
       --H_scale 2 \
       --W_scale 2 \
       --seamless
```

You can remove the `--seamless` flag for a faster processing time.

