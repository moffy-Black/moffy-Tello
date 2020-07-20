import cv2
import numpy as np


def main():

    red_lower = (0, 230, 150)
    red_upper = (30, 255, 255)

    cap = cv2.VideoCapture(0)
    W = cap.get(cv2.CAP_PROP_FRAME_WIDTH)/2
    H = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/2
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame, hierarchy = red_detect(frame, red_lower, red_upper, W, H)
            cv2.imshow('window', frame)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


def red_detect(frame, lower, upper, W, H):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red = cv2.inRange(hsv, lower, upper)
    kernal = np.ones((5, 5), "uint8")
    red = cv2.dilate(red, kernal)
    res = cv2.bitwise_and(frame, frame, mask=red)
    (ret, contours, hierarchy) = cv2.findContours(
        red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 100):
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(
                frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "RED color", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
            cv2.drawMarker(frame, (320, 240), (255, 255, 0),
                           markerType=cv2.MARKER_SQUARE, markerSize=5, thickness=10)
            cv2.drawMarker(frame, ((x + w//2), (y + h//2)), (255, 255, 0),
                           markerType=cv2.MARKER_SQUARE, markerSize=5, thickness=10)
            cv2.arrowedLine(frame, (320, 240),
                            ((x + w//2), (y + h//2)), (255, 0, 0), 5)
    return frame, hierarchy


if __name__ == '__main__':
    main()
