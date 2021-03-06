# EEC 174BY Jetson Autonomous Car
![IMG_0989](https://user-images.githubusercontent.com/45084728/158081913-04ebb779-8b2b-41a3-9770-9982ced32215.jpeg)

### Received 2022 EEC 174BY Outstanding Senior Design Project Award



## Requirements
[Pytorch](https://qengineering.eu/install-pytorch-on-jetson-nano.html)

## YOLOv5

Yolov5 model is implemented in the Pytorch framework. PyTorch is an open-source machine learning library based on the Torch library, used for computer vision and natural language processing applications. Here is a complete guide for installing PyTorch & torchvision on [Jetson Development Kits](https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-10-now-available/72048/2).

We'll be using a Intel Realsense D435 depth camera to detect the distance of objects.

Use the following command to check if a camera is recognized

`ls /dev/video*`

## Download Yolov5 Model
Select the desired model based on model size, required speed, and accuracy. You can find available models here in the [Assets](https://github.com/ultralytics/yolov5/releases) section. Download the model using the command below and move it to the weights folder. 

```
mkdir weights
cd weights
wget https://github.com/ultralytics/yolov5/releases/download/v5.0/yolov5s.pt
```

Here is a comparison of all the recent YOLO models.
![YOLO comparison](https://user-images.githubusercontent.com/26833433/155040763-93c22a27-347c-4e3c-847a-8094621d3f4e.png)

## Depth Camera

The pyrealsense2 wrapper cannot be installed with the pip install pyrealsense2 method on devices with Arm processors such as Jetson, because the PyPi pip packages are not compatible with Arm processors. That typically means that the best option is to use CMake to build librealsense and the Python bindings at the same time.

To fix this issue we followed this [article](https://cognitivexr.at/blog/2021/07/29/installing-pyrealsense2-nvidia-jetson-xavier-nx.html) to fix the python module compatability.

Intel Realsense d435i can be used for various needs, such as detecting 3D objects. We used this [tutorial](https://pysource.com/2021/03/11/distance-detection-with-depth-camera-intel-realsense-d435i/) and this one [by intel](https://dev.intelrealsense.com/docs/nvidia-jetson-tx2-installation) to find the distance of objects using OpenCV and the depth camera.


```
export PYTHONPATH=/usr/local/lib/python3.6/pyrealsense2
python3 JetsonYolo.py
```

![trim FD0B2F82-268C-476C-B4A8-301CEF662D75](https://user-images.githubusercontent.com/45084728/156067969-0fe2ecd1-2fe2-4cbd-b051-d1dfe281d63a.gif)


## PCA9685 and ESC

It's easy to use the PCA9685 sensor with Python or CircuitPython and the Adafruit CircuitPython PCA9685 module.  This module allows you to easily write Python code that control servos and PWM with this breakout. JetsonHacks provides his [ServoKit](https://www.jetsonhacks.com/2019/07/22/jetson-nano-using-i2c/) resource and [lab tutorial](https://eec193.github.io/) using the same method and module. 
```
sudo pip3 install adafruit-circuitpython-pca9685
sudo pip3 install adafruit-circuitpython-servokit
```
We can test the servo and throttle on I2C Bus 1
```
from adafruit_servokit import ServoKit
import board
import busio
import time
from approxeng.input.selectbinder import ControllerResource
    
print("Initializing Servos")
i2c_bus1=(busio.I2C(board.SCL, board.SDA))
print("Initializing ServoKit")
kit = ServoKit(channels=16, i2c=i2c_bus1)
print("Done initializing")

## Turn 80 degrees
kit.servo[0].angle = 80
time.sleep(1)
## Turn 120 degrees
kit.servo[0].angle = 120
time.sleep(1)
## Throttle
kit.servo[1].angle = 120
```
![trim 43EDAA41-258F-4B9F-BB5A-DB42CBF3124A](https://user-images.githubusercontent.com/45084728/156069635-38dddec5-0083-4e1f-a0eb-c1b026f38e30.gif)


![trim 3D35DD19-279A-4C4F-B70A-8C7F27E4E071](https://user-images.githubusercontent.com/45084728/156446457-172b59ed-e3a5-4f0d-a895-c1d44114b07d.gif)



