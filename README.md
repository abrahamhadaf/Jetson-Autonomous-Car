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


`export PYTHONPATH=/usr/local/lib/python3.6/pyrealsense2
`
