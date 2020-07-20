import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2
import numpy as np
import time


def red_detect(frame):  # オレンジ色を検出し、画像加工を施す。
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = (0, 230, 150)
    upper = (30, 255, 255)
    red = cv2.inRange(hsv, lower, upper)
    kernal = np.ones((5, 5), "uint8")
    red = cv2.dilate(red, kernal)
    res = cv2.bitwise_and(frame, frame, mask=red)
    (ret, contours, hierarchy) = cv2.findContours(
        red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x = 0
    y = 0
    w = 0
    h = 0
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 100):
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(
                frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "RED color", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
            cv2.drawMarker(frame, (480, 350), (255, 255, 0),
                           markerType=cv2.MARKER_SQUARE, markerSize=5, thickness=10)
            cv2.drawMarker(frame, ((x + w//2), (y + h//2)), (255, 255, 0),
                           markerType=cv2.MARKER_SQUARE, markerSize=5, thickness=10)
            cv2.arrowedLine(frame, (480, 350),
                            ((x + w//2), (y + h//2)), (255, 0, 0), 5)
            cv2.rectangle(frame, (330, 200), (630, 500), (0, 255, 0), 1)
    return frame, x, y, w, h  # 動画データとピクセル（x,y,z,h）を返す


def tracker(drone, x, y, w, h):  # ドローンの動作を指定している

   if 1 <= (y + h // 2) < 100:
        drone.up(10)
        # time.sleep(0.5)
        print("up")
    if (y + h // 2) > 550:
        drone.down(10)
        # time.sleep(0.5)
        print("down")
    if 1 <= (x + w // 2) < 100:
        drone.left(7)
        # time.sleep(0.5)
        print("left")
    if (x + w // 2) > 860:
        drone.right(7)
        # time.sleep(0.5)
        print("right")


def main():
    drone = tellopy.Tello()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)

        container = av.open(drone.get_video_stream())
        # skip first 300 frames
        frame_skip = 300
        while True:
            for frame in container.decode(video=0):
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                start_time = time.time()
                image = cv2.cvtColor(
                    np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                image, x, y, w, h = red_detect(image)
                cv2.imshow('Red_vctor', image)
                key = cv2.waitKey(1) & 0xff
                if key == ord('t'):
                    drone.takeoff()
                if key == ord('l'):
                    drone.land()
                if key == ord('q'):
                    break
                tracker(drone, x, y, w, h)
                if frame.time_base < 1.0/60:
                    time_base = 1.0/60
                else:
                    time_base = frame.time_base
                frame_skip = int((time.time() - start_time)/time_base)
            break

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
