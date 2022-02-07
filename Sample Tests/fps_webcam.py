import cv2
import time

cap=cv2.VideoCapture(0)

start=0
fps=0


while True:
    rec,frame = cap.read()

    end=time.time()
    diff=end-start
    fps=1/diff
    start=end

    fps_text="pfs:{:.2f}".format(fps)
    cv2.putText(frame, fps_text, (5,30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255,255),1)

    cv2.imshow("webcam",frame)
    key=cv2.waitKey(1)

    if key == 81 or key == 113:   #q to quit
        break
cap.release()

print('complete')
