import pyautogui
import time

print("Click the top-left corner of the button...")
time.sleep(3)  # Wait for first click
x1, y1 = pyautogui.position()
print(f"First position: {(x1, y1)}")

print("\nNow click the bottom-right corner of the button...")
time.sleep(3)  # Wait for second click
x2, y2 = pyautogui.position()
print(f"Second position: {(x2, y2)}")

# Calculate the coordinates
x = min(x1, x2)  # leftmost x
y = min(y1, y2)  # topmost y
width = abs(x2 - x1)  # width
height = abs(y2 - y1)  # height

print(f"\nButton coordinates: ({x}, {y}, {width}, {height})")