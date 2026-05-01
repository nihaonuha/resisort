import cv2
import numpy as np

color_ranges = {
    "Red": ([175, 87, 0], [180, 255, 255]),
    "Yellow": ([21, 95, 42], [28, 255, 241]),
    "Green": ([36, 25, 25], [86, 255, 255]),
    "Orange": ([4, 31, 198], [10, 255, 255]),
    "Brown": ([0, 55, 107], [26, 255, 169]),
    "Violet": ([130, 0, 0], [175, 255, 255]),
    "Gold": ([13, 104, 91], [17, 179, 255]),
    "White": ([7, 0, 200], [31, 24, 255]),
    "Black": ([0, 14, 0], [46, 191, 96])
}

resistor_values = {
    "Black": 0, "Brown": 1, "Red": 2, "Orange": 3, 
    "Yellow": 4, "Green": 5, "Blue": 6, "Violet": 7, 
    "Gray": 8, "White": 9
}

def resistor_value(filepath):
    frame = cv2.imread(filepath)
    if frame is None:
        return {"error": "Could not read image"}

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    combined_mask = np.zeros(hsv_frame.shape[:2], dtype=np.uint8)
    masks = {}
    for color_name, (low, high) in color_ranges.items():
        mask = cv2.inRange(hsv_frame, np.array(low), np.array(high))
        combined_mask = cv2.bitwise_or(combined_mask, mask)
        masks[color_name] = mask

    kernel = np.ones((5, 5), np.uint8)
    cleaned_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
    cleaned_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [
        cnt for cnt in contours if 100 < cv2.contourArea(cnt) < 2000
    ]

    band_colors = []
    if len(filtered_contours) > 0:
        sorted_contours = sorted(filtered_contours, key=lambda c: cv2.boundingRect(c)[0])
        for contour in sorted_contours:
            for color_name, mask in masks.items():
                temp_mask = np.zeros_like(mask)
                cv2.drawContours(temp_mask, [contour], -1, 255, thickness=cv2.FILLED)
                masked = cv2.bitwise_and(mask, mask, mask=temp_mask)
                if cv2.countNonZero(masked) > 0:
                    band_colors.append(color_name)
                    break

    if len(band_colors) >= 3:
        first_digit = resistor_values.get(band_colors[0], -1)
        second_digit = resistor_values.get(band_colors[1], -1)
        multiplier = 10 ** resistor_values.get(band_colors[2], -1)
        tolerance = band_colors[3] if len(band_colors) > 3 else "5%"

        if first_digit == -1 or second_digit == -1 or multiplier == -1:
            return {"error": "Invalid color bands"}

        resistance = (first_digit * 10 + second_digit) * multiplier
        return {"value": f"{resistance} Ω ± {tolerance}"}
    
    return {"error": "Not enough bands detected"}