import numpy as np
import cv2
# vision variables

img = 0
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('a'): ## and doesn't work here !!
        # -- it's a pointer not a logic operation
        img = frame
        corner_spacing =27

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = np.float32(gray)
        corners = cv2.goodFeaturesToTrack(gray, 81, 0.001, corner_spacing)
        corners = np.int0(corners)
        xLoc = []
        yLoc = []
        for corner in corners:
            x, y = corner.ravel()
            xLoc.append(x)
            yLoc.append(y)
            cv2.circle(img, (x, y), 3, 255, -1)
        print(len(corners))
    cv2.imshow('frame', frame)
    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == ord('q'): ## and doesn't work here !!
        break

cap.release()
cv2.destroyAllWindows()