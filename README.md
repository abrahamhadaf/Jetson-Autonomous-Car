# EEC 174BY Jetson Autonomous Car

## YOLOv5

Yolov5 model is implemented in the Pytorch framework. PyTorch is an open-source machine learning library based on the Torch library, used for computer vision and natural language processing applications. Here is a complete guide for installing PyTorch & torchvision on [Jetson Development Kits](https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-10-now-available/72048/2).

We'll be using a Intel Realsense D435 depth camera to detect the distance of objects.

Use the following command to check if a camera is recognized

`ls /dev/video*`

## Download Yolov5 Model
Select the desired model based on model size, required speed, and accuracy. You can find available models here in the Assets section. Download the model using the command below and move it to the weights folder. 

```
mkdir weights
cd weights
wget https://github.com/ultralytics/yolov5/releases/download/v5.0/yolov5s.pt
```

## Depth Camera

The pyrealsense2 wrapper cannot be installed with the pip install pyrealsense2 method on devices with Arm processors such as Jetson, because the PyPi pip packages are not compatible with Arm processors. That typically means that the best option is to use CMake to build librealsense and the Python bindings at the same time.

To fix this issue we followed this [article](https://cognitivexr.at/blog/2021/07/29/installing-pyrealsense2-nvidia-jetson-xavier-nx.html) to fix the python module compatability.

Intel Realsense d435i can be used for various needs, such as detecting 3D objects. We used this [tutorial](https://pysource.com/2021/03/11/distance-detection-with-depth-camera-intel-realsense-d435i/) to find the distance of objects using OpenCV and the depth camera.


```
export PYTHONPATH=/usr/local/lib/python3.6/pyrealsense2
python3 JetsonYolo.py
```
