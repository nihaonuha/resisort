# filename: trigger_esp32.py
import requests

ESP32_IP = "http://192.168.1.17"  # Replace with your ESP32's IP address

while True:
    key = input("Press ENTER to trigger ESP32 camera (or type 'exit'): ")
    if key.lower() == 'exit':
        break
    try:
        res = requests.get(f"{ESP32_IP}/trigger")
        print("ESP32 Response:", res.text)
    except Exception as e:
        print("Error:", e)