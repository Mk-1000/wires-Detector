import cv2
import numpy as np


def exe(wire_colors):
    # Define color ranges for each wire
    color_ranges = {}
    for wire, color in wire_colors.items():
        if color == "black":
            color_ranges[wire] = (np.array([0, 0, 0]), np.array([180, 255, 50]))
        elif color == "brown":
            color_ranges[wire] = (np.array([0, 100, 100]), np.array([20, 255, 255]))
        elif color == "red":
            color_ranges[wire] = (np.array([170, 100, 100]), np.array([180, 255, 255]))
        elif color == "orange":
            color_ranges[wire] = (np.array([5, 100, 100]), np.array([15, 255, 255]))
        elif color == "yellow":
            color_ranges[wire] = (np.array([20, 100, 100]), np.array([30, 255, 255]))
        elif color == "green":
            color_ranges[wire] = (np.array([40, 100, 100]), np.array([80, 255, 255]))
        elif color == "blue":
            color_ranges[wire] = (np.array([100, 100, 100]), np.array([130, 255, 255]))
        elif color == "purple":
            color_ranges[wire] = (np.array([125, 100, 100]), np.array([150, 255, 255]))
        elif color == "white":
            color_ranges[wire] = (np.array([0, 0, 180]), np.array([180, 25, 255]))
        else:
            raise ValueError(f"Invalid color '{color}' for wire '{wire}'")

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the region of interest (ROI) for the connector
        x, y, w, h = 100, 100, 400, 300  # Adjust the values to fit your specific case
        roi = frame[y:y + h, x:x + w]

        wire_contours = {}
        # For each thread and predefined color range, find the corresponding contours in the image
        for wire, (lower, upper) in color_ranges.items():
            wire_mask = cv2.inRange(hsv, lower, upper)
            wire_contours[wire], _ = cv2.findContours(wire_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Check if all wires are present
        if all(len(contours) > 0 for contours in wire_contours.values()):
            # If all wires are present, check if they are organized
            wire_centers = {}
            for wire, contours in wire_contours.items():
                wire_centers[wire] = tuple(np.round(np.mean(contours[0], axis=0))[0])

            sorted_wires = sorted(wire_centers.keys(), key=lambda wire: wire_centers[wire][1])
            if sorted_wires == list(wire_colors.keys()):
                print("All wires are organized and have the correct colors")
                # Draw a green lamp on the screen
                lamp_color = (0, 255, 0)
            else:
                print("Wires are present but not organized")
                # Draw a red lamp on the screen
                lamp_color = (0, 0, 255)

            # Draw a green rectangle around the ROI
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            # No wires detected, do not show a lamp
            lamp_color = None

        if lamp_color is not None:
            # Draw a lamp with the appropriate color on the screen
            lamp_size = 10
            lamp_thickness = 10
            lamp_margin = 50
            lamp_position = (frame.shape[1] - lamp_size - lamp_margin, lamp_margin)
            cv2.circle(frame, lamp_position, lamp_size // 2, lamp_color, lamp_thickness)

        cv2.imshow('Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2
