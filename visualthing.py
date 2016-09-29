import cv2
import numpy as np
video = cv2.VideoCapture(0)
video.set(3, 640)             # Set capture width to 640px
video.set(4, 480)            # Set capture height to 480px
 
YELLOW_LOWER = 20, 140, 140
YELLOW_UPPER = 50, 255, 255
 

BLUE_LOWER = 100, 140, 140
BLUE_UPPER = 150, 255, 255
 
 
BALL_LOWER = (0, 140, 140)   # HSV
BALL_UPPER = (20, 255, 255)   # HSV
while True:
    success, frame = video.read() # Grab another frame from the camera
    blurred = cv2.blur(frame, (10,10))
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV) # Convert red, green and blue to hue, saturation and brightness
 
    # This recognizes blue goal
    blue_mask = cv2.inRange(hsv, BLUE_LOWER, BLUE_UPPER)
    blue_mask = cv2.dilate(blue_mask, None, iterations=2)
    blue_cutout = cv2.bitwise_and(frame,frame, mask=blue_mask)
    blue_cnts, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print "Blue countours:", blue_cnts
 
    for cnt in blue_cnts:
      x,y,w,h = cv2.boundingRect(cnt)
      print("Blue goal at:", x,y,w,h)
      cv2.rectangle(blue_cutout, (x,y),(x+w,y+h), (255,255,255))
 
#    print "Blue goal at:", blue_rects
 
    # This recognizes balls
    mask = cv2.inRange(hsv, BALL_LOWER, BALL_UPPER)
    mask = cv2.dilate(mask, None, iterations=2)
    cutout = cv2.bitwise_and(frame,frame, mask=mask)
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
 
    if cnts:
        c = max(cnts, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
            cv2.circle(frame, center, int(radius), (0, 0, 255), 5)
            distance = round((1/radius)*100*11.35, 2)
            cv2.putText(frame, str(radius), (int(x),int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255,255,255),1)
 
    stacked = np.hstack([frame, cutout, blue_cutout])
    cv2.imshow('justaname', stacked)
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
