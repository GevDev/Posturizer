import sys
import time
import cv2
import numpy as np
import pyautogui


def main():
    # Load DNN face detector
    net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'res10_300x300_ssd_iter_140000.caffemodel')

    # Load Haar cascade for eyes
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    # Set initial height threshold
    height_threshold = 333

    move_threshold_up_key = ord('/')
    move_threshold_down_key = ord('.')
    quit_key = ord('q')
    threshold_up_down_pixel_adjustment = 5
    loop_delay = 0.04  # Slow down loop so we're not constantly checking the camera and loading up the CPU

    # Start capturing video
    cap = cv2.VideoCapture(0)

    count = 0 # Used as a super janky way to create a countdown until window is minimized
    count_start_time = 0
    last_hidden_time = 0
    slouched = False
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Convert frame to blob to feed into DNN
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

        # Set the input and forward pass the blob through the network
        net.setInput(blob)
        detections = net.forward()

        # Loop over the detections
        for i in range(0, detections.shape[2]):
            # Extract the confidence (i.e., probability) associated with the prediction
            confidence = detections[0, 0, i, 2]

            # Filter out weak detections by ensuring the `confidence` is greater than the minimum confidence
            if confidence > 0.5:
                # Compute the (x, y)-coordinates of the bounding box for the face
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (x, y, w, h) = box.astype("int")

                # Draw bounding box for the face
                cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)

                # Get the region of interest in the grayscale image
                roi_gray = cv2.cvtColor(frame[y:h, x:w], cv2.COLOR_BGR2GRAY)

                # Detect eyes using Haar cascade
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0, 0, 255), 2)

                    # Check if eyes are below the height threshold
                    if y+ey+eh > height_threshold:
                        print(count)
                        count += 1
                        current_time = time.time()
                        count_start_time = current_time
                        if count >= 169 and not slouched and (current_time - last_hidden_time > 5):
                            slouched = True
                            last_hidden_time = current_time
                            print("Sloucher! Minimizing!!!")
                            if sys.platform.startswith('win'):
                                print("UsingWindows")
                                pyautogui.hotkey('win', 'd')
                            elif sys.platform.startswith('darwin'):
                                print("UsingMac")
                                pyautogui.press('f11')
                            # time.sleep(5)  # just chill while we minimize windows\//
                    else:
                        if slouched:
                            print("Back straightened!")
                            time.sleep(0.8)  # chill just in case things are still minimized
                            if sys.platform.startswith('win'):
                                print("UsingWindows")
                                pyautogui.hotkey('win', 'd')
                            elif sys.platform.startswith('darwin'):
                                print("UsingMac")
                                pyautogui.press('f11')
                            slouched = False
                            count = 0
                        elif time.time() - count_start_time > 2:
                            count = 0

        # Draw the threshold line
        cv2.line(frame, (0, height_threshold), (frame.shape[1], height_threshold), (255, 0, 0), 2)

        # Show the frame
        cv2.imshow('Frame', frame)

        # Check for user input to adjust threshold
        key = cv2.waitKey(1)
        if key == move_threshold_up_key:
            height_threshold -= threshold_up_down_pixel_adjustment
            print(height_threshold)
        elif key == move_threshold_down_key:
            height_threshold += threshold_up_down_pixel_adjustment
            print(height_threshold)
        elif key & 0xFF == quit_key:  # Quit if the user presses 'q'
            break

        # Use this as a way to slow down the loop so we're not constantly checking the camera and loading up the CPU
        # TODO: There might be a better way to do this natively with opencv, but their docs are a bit ugly
        time.sleep(loop_delay)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
