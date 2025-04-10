import cv2

capture = cv2.videoCapture(0)

while True:
    success, image = capture.read()

    if(success):
        cv2.imshow('CAM TEST', image)

    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyWindow()