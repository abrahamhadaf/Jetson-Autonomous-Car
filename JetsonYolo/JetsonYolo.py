import cv2
import numpy as np
from elements.yolo import OBJ_DETECTION
from adafruit_servokit import ServoKit
import board
import busio
import time
from approxeng.input.selectbinder import ControllerResource
# Execution time
start_time = time.time()

# FOR THESE SPEEDS, THE CAR MUST BE IN TRAINING MODE OR ELSE THE CAR WILL GO FULL SPEED AND FLY TO KEMPER HALL
STOP = 110
LOWSPEED = 115 
MEDIUMSPEED = 116 
HIGHSPEED = 117

print("Initializing Servos")
i2c_bus1=(busio.I2C(board.SCL, board.SDA))
print("Initializing ServoKit")
kit = ServoKit(channels=16, i2c=i2c_bus1)
print("Done initializing")

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
Object_detector = OBJ_DETECTION('weights/yolov5s.pt', Object_classes)

def gstreamer_pipeline(
    capture_width=640,
    capture_height=360,
    display_width=640,
    display_height=360,
    framerate=40,
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


# To flip the image, modify the flip_method parameter (0 and 2 are the most common)
print(gstreamer_pipeline(flip_method=0))
##jetson camera commented out. Using (1) for the fish eye camera
cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
#cap = cv2.VideoCapture(1)
start=0
fps=0
print("Execution Time: --- %s seconds ---" % (time.time() - start_time))
if cap.isOpened():
    window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
    # Window
    while cv2.getWindowProperty("CSI Camera", 0) >= 0:
        ret, frame = cap.read()
        #frame = cv2.resize(frame,(640,360))
        end=time.time()
        diff=end-start
        fps=1/diff
        start=end
        label = ''
        if ret:
            # detection process
            objs = Object_detector.detect(frame)
            

            # plotting
            for obj in objs:
                # print(obj)
                label = obj['label']
                score = obj['score']
                [(xmin,ymin),(xmax,ymax)] = obj['bbox']
                color = Object_colors[Object_classes.index(label)]
                frame = cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), color, 2)
                # if(label == 'stop sign'):
                #     print("xmin ",xmin)
                #     print("ymin",ymin)
                #print(xmax,ymax) 
                frame = cv2.putText(frame, f'{label} ({str(score)})', (xmin,ymin), cv2.FONT_HERSHEY_SIMPLEX , 0.75, color, 1, cv2.LINE_AA)

        if(label == "stop sign"):
            kit.servo[0].angle = STOP
            # 3 second delay for stop sign
            time.sleep(0.45)
            # Then go
            kit.servo[0].angle = LOWSPEED
        elif(label == "person"):
            kit.servo[0].angle = STOP
        
        else:
            # If no object, go at low speed
            kit.servo[0].angle = LOWSPEED
            # Go straight (90 degrees)
            kit.servo[1].angle = 90

        fps_text="fps:{:.2f}".format(fps)
        cv2.putText(frame, fps_text, (5,30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255,255),1)
        cv2.imshow("CSI Camera", frame)
        keyCode = cv2.waitKey(30)
        if keyCode == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
else:
    print("Unable to open camera")
