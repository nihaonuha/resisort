# ver 1. one frame capture and display % of colour

import cv2
import numpy as np

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to capture image.")
        break

    # display the live video feed
    cv2.imshow("Live Video (Press Space to Capture)", frame)

    # capture frame on spacebar (ASCII value 32)
    if cv2.waitKey(1) & 0xFF == 32:  # spacebar pressed
        captured_frame = frame.copy()
        hsv_frame = cv2.cvtColor(captured_frame, cv2.COLOR_BGR2HSV)
        print("Frame Captured.")
        break
    

# release camera, close live feed window
cam.release()
cv2.destroyAllWindows()

# black
low_black = np.array([0,0,0])
high_black = np.array([14,255,111])
black_mask =  cv2.inRange(hsv_frame, low_black, high_black)
# black  = cv2.bitwise_and(frame, frame, mask = black_mask)
black = cv2.bitwise_not(black_mask)

# brown
low_brown = np.array([5,220,24])
high_brown = np.array([10,255,101])
brown_mask = cv2.inRange(hsv_frame, low_brown, high_brown)
brown = cv2.bitwise_and(frame, frame, mask = brown_mask)

# red
low_red = np.array([161, 155, 84])
high_red = np.array([179, 255, 255])
red_mask =  cv2.inRange(hsv_frame, low_red, high_red)
red  = cv2.bitwise_and(frame, frame, mask = red_mask)

# orange
low_orange = np.array([4,31,198])
high_orange = np.array([10,255,255])
orange_mask =  cv2.inRange(hsv_frame, low_orange, high_orange)
orange  = cv2.bitwise_and(frame, frame, mask = orange_mask)

# yellow
low_yellow = np.array([21, 95, 42])
high_yellow = np.array([28,255,241])
yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
yellow = cv2.bitwise_and(frame, frame, mask = yellow_mask)

# green
low_green = np.array([54, 41, 0])
high_green = np.array([77, 255, 157])
green_mask = cv2.inRange(hsv_frame, low_green, high_green)
green = cv2.bitwise_and(frame, frame, mask = green_mask)

# blue
low_blue = np.array([94, 80, 2])
high_blue = np.array([126, 255, 255])
blue_mask =  cv2.inRange(hsv_frame, low_blue, high_blue)
blue  = cv2.bitwise_and(frame, frame, mask = blue_mask)

# violet
low_violet = np.array([121, 64, 65])
high_violet = np.array([169, 202, 255])
violet_mask =  cv2.inRange(hsv_frame, low_violet, high_violet)
violet  = cv2.bitwise_and(frame, frame, mask = violet_mask)

# gray

# white
low_white = np.array([8, 71, 139])
high_white = np.array([22, 108, 242])
white_mask =  cv2.inRange(hsv_frame, low_white, high_white)
white  = cv2.bitwise_and(frame, frame, mask = white_mask)

cv2.imshow("frame", frame)
cv2.imshow("red mask", red)
# cv2.imshow("blue mask", blue)
cv2.imshow("orange mask", orange)
cv2.imshow("brown mask", brown)
cv2.imshow("green mask", green)
# cv2.imshow("black mask", black)
cv2.imshow("yellow mask", yellow)

masks = [red_mask, orange_mask, blue_mask, brown_mask, black_mask, green_mask]
color_names = ["Red", "Orange", "Blue", "Brown", "Black", "Green"]

# calculate total pixels in the image
total_pixels = frame.shape[0] * frame.shape[1]

# calculate percentage of each color
color_percentages = {}

for mask, name in zip(masks, color_names):
    detected_pixels = cv2.countNonZero(mask)
    percentage = (detected_pixels / total_pixels) * 100
    color_percentages[name] = round(percentage, 2)

print("Color Percentages:", color_percentages)

combined_mask = cv2.bitwise_or(black_mask, brown_mask, red_mask, orange_mask)

kernel = np.ones((3,3), np.uint8)
cleaned_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
cleaned_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_CLOSE, kernel)

# Detecting contours on cleaned mask
contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter out very small or very large contours (likely noise or the entire resistor)
min_contour_area = 100  # Minimum area for a band (adjust as needed)
max_contour_area = 500  # Maximum area to avoid selecting the whole resistor

filtered_contours = [
    cnt for cnt in contours if min_contour_area < cv2.contourArea(cnt) < max_contour_area
]

# Check if any contours are detected (bands in frame)
if len(filtered_contours) == 0:
    print("No bands detected.")
else:
    print(f"Bands detected: {len(filtered_contours)}")

    # Sort contours by x position (left to right)
    sorted_contours = sorted(filtered_contours, key=lambda c: cv2.boundingRect(c)[0])

    for i, contour in enumerate(sorted_contours):
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle around each band
        cv2.putText(frame, f"Band {i + 1}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# Display the result
cv2.imshow("Detected Bands", frame)
cv2.imshow("Combined Mask", combined_mask)
cv2.imshow("Cleaned Mask", cleaned_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()