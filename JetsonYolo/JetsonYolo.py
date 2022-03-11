import cv2
import numpy as np
from elements.yolo import OBJ_DETECTION
from adafruit_servokit import ServoKit
import board
import busio
import time
from approxeng.input.selectbinder import ControllerResource
from realsense_depth import *
# Import Pyrealsense2 by running this in terminal "export PYTHONPATH=/usr/local/lib/python3.6/pyrealsense2"
import pyrealsense2

# Execution time
start_time = time.time()

# FOR THESE SPEEDS, THE CAR MUST BE IN TRAINING MODE OR ELSE THE CAR WILL GO FULL SPEED AND FLY TO KEMPER HALL
STOP = 110
LOWSPEED = 115 
#MEDIUMSPEED = 124 
#HIGHSPEED = 125

print("Initializing Servos")
i2c_bus1=(busio.I2C(board.SCL, board.SDA))
print("Initializing ServoKit")
kit = ServoKit(channels=16, i2c=i2c_bus1)
print("Done initializing")

point = (400, 300)

def show_distance(event, x, y, args, params):
    global point
    point = (x, y)


Object_classes = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
                'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
                'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
                'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
                'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
                'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
                'hair drier', 'toothbrush' ]

Object_colors = list(np.random.rand(80,3)*255)
Object_detector = OBJ_DETECTION('weights/yolov5m.pt', Object_classes)

def gstreamer_pipeline(
    capture_width=320,
    capture_height=180,
    display_width=640,
    display_height=360,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

# Initialize Camera Intel Realsense
dc = DepthCamera()

# To flip the image, modify the flip_method parameter (0 and 2 are the most common)
print(gstreamer_pipeline(flip_method=0))
##jetson camera commented out. Using (1) for the fish eye camera
dcstart=0
fps=0

print("Execution Time: --- %s seconds ---" % (time.time() - start_time))
if dc is not None:

    while dc is not None:
        ret, depth_frame, color_frame = dc.get_frame()
        depthlabel = depth_frame[point[1], point[0]]

        end=time.time()
        diff=end-dcstart
        fps=1/diff
        dcstart=end
        label = ''
        if ret:
            # detection process
            objs = Object_detector.detect(color_frame)
            
            # plotting
            for obj in objs:
                label = obj['label']
                score = obj['score']
                [(xmin,ymin),(xmax,ymax)] = obj['bbox']
                color = Object_colors[Object_classes.index(label)]
                color_frame = cv2.rectangle(color_frame, (xmin,ymin), (xmax,ymax), color, 2)
                # if(label == "stop sign"):
                #     print (depth_frame[point[1], point[0]]) #addition
                #     print("xmin ",xmin)
                #     print("ymin",ymin)
                #     print("xmax",xmax)
                #     print("ymax", ymax) 
                color_frame = cv2.putText(color_frame, f'{label} ({str(score)}) ({str(depthlabel)}) ', (xmin,ymin), cv2.FONT_HERSHEY_SIMPLEX , 0.75, color, 1, cv2.LINE_AA)


        if(label == "stop sign"):
            depths = depth_frame[point[1], point[0]]
            depthstop = int(depths)
            if(depthstop < 400 and depthstop > 1):
                print("Stopping")
                kit.servo[1].angle = STOP
            else:
                print("Driving")
                kit.servo[1].angle = LOWSPEED
        if(label == "person"):
            if(xmin > 200):
                print("Turning Left")
                kit.servo[0].angle = 60
            if(xmin < 200):
                print("Turning right")
                kit.servo[0].angle = 120
        


        
        # if(label == "stop sign"):
        #     kit.servo[0].angle = STOP

        # elif(label == "person"):
        #     if(xmin > 200):
        #         kit.servo[1].angle = 60
        #     elif(xmin < 200):
        #         kit.servo[1].angle = 120
        
        # else:
        #     # If no object, go at low speed
        #     kit.servo[0].angle = LOWSPEED

        fps_text="fps:{:.2f}".format(fps)
        cv2.putText(color_frame, fps_text, (5,30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255,255),1)

        cv2.imshow("Depth Frame", depth_frame)
        cv2.imshow("Color Frame", color_frame)
        keyCode = cv2.waitKey(30)
        if keyCode == ord('q'):
            break
    cv2.destroyAllWindows()
else:
    print("Unable to open camera")
