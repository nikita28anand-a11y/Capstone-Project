import cv2
import numpy as np
import pygame
import serial
import time
import csv
from datetime import datetime

from tracker.tracker import CentroidTracker


pygame.mixer.init()
pygame.mixer.music.load("sounds/alert.mp3")


arduino = None

try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)
    print("Arduino connected")
except:
    print("Arduino not connected. Running in simulation mode")


net = cv2.dnn.readNet("models/yolov3.weights", "models/yolov3.cfg")

with open("models/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]


cap = cv2.VideoCapture(0)


ct = CentroidTracker()

csv_file = open("traffic_report.csv", "a", newline="")

csv_writer = csv.writer(csv_file)

csv_writer.writerow([
    "Date",
    "Time",
    "Objects",
    "Vehicles",
    "Density"
])

def send_stop():
    if arduino:
        arduino.write(b'S')

def send_go():
    if arduino:
        arduino.write(b'G')

while True:

    ret, frame = cap.read()

    if not ret:
        break

    height, width, channels = frame.shape

    blob = cv2.dnn.blobFromImage(
        frame,
        0.00392,
        (416, 416),
        (0, 0, 0),
        True,
        crop=False
    )

    net.setInput(blob)
    outs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []
    rects = []

    danger = False
    distance_status = "SAFE"

    for out in outs:
        for detection in out:

            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.7:

                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)

                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

                label_name = classes[class_id]

                if label_name in ["person", "car",
                 "truck", "bus", "motorbike"]:
                    rects.append((x, y, x + w, y + h))

    indexes = cv2.dnn.NMSBoxes(
        boxes,
        confidences,
        0.5,
        0.4
    )

    font = cv2.FONT_HERSHEY_SIMPLEX

    objects = ct.update(rects)

    total_objects = 0
    vehicle_count = 0
    traffic_density = "LOW"

    if len(indexes) > 0:

        total_objects = len(indexes.flatten())

        for i in indexes.flatten():

            label = str(classes[class_ids[i]])
            x, y, w, h = boxes[i]

            color = (0, 255, 0)

            if label in [
                "car",
                "truck",
                "bus",
                "motorbike",
                "bicycle"
            ]:
                vehicle_count += 1

                if vehicle_count >= 5:
                    traffic_density = "MEDIUM"

                if vehicle_count >= 10:
                    traffic_density = "HIGH"

            if label in [
                "person",
                "car",
                "truck",
                "bus",
                "bicycle",
                "motorbike"
            ]:

                if w > 250:
                    danger = True
                    distance_status = "VERY NEAR"
                    color = (0, 0, 255)

                elif w > 150:
                    distance_status = "NEAR"
                    color = (0, 165, 255)

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                color,
                2
            )

            text = f"{label} {round(confidences[i] * 100, 1)}%"

            cv2.putText(
                frame,
                text,
                (x, y - 10),
                font,
                0.8,
                color,
                2
            )

    
    for (objectID, centroid) in objects.items():

        cv2.putText(
            frame,
            f"ID {objectID}",
            (centroid[0] - 10, centroid[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 255),
            2
        )

        cv2.circle(
            frame,
            (centroid[0], centroid[1]),
            4,
            (0, 255, 255),
            -1
        )

    
    cv2.putText(
        frame,
        f"Distance Status: {distance_status}",
        (40, 90),
        font,
        0.8,
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Total Objects: {total_objects}",
        (40, 130),
        font,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Vehicles: {vehicle_count}",
        (40, 170),
        font,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Traffic Density: {traffic_density}",
        (40, 210),
        font,
        0.8,
        (255, 0, 255),
        2
    )

    
    if danger:

        cv2.putText(
            frame,
            "WARNING! AUTO STOP ACTIVATED",
            (40, 50),
            font,
            1,
            (0, 0, 255),
            3
        )

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()

        send_stop()

    else:

        pygame.mixer.music.stop()
        send_go()

    current_time = datetime.now()

    csv_writer.writerow([
      current_time.strftime("%d-%m-%Y"),
      current_time.strftime("%H:%M:%S"),
      total_objects,
      vehicle_count,
      traffic_density
    ]) 

    current_time_display = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    cv2.putText(
      frame,
      current_time_display,
      (40, 250),
      font,
      0.6,
      (255, 255, 255),
      2
    )   

    cv2.imshow(
        "AI Automotive Safety System",
        frame
    )

    key = cv2.waitKey(1)

    if key == ord('s'):

        filename = datetime.now().strftime(
        "output_images/capture_%Y%m%d_%H%M%S.jpg"
        )

        print("Saving to:", filename)

        success = cv2.imwrite(filename, frame)

        print("Saved:", success)
    if key == 27:
        break

pygame.mixer.music.stop()

csv_file.close()

cap.release()
cv2.destroyAllWindows()