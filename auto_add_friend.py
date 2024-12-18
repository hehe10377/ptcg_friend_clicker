from PIL import ImageGrab, Image, ImageDraw
from dotenv import load_dotenv
import os
import cv2
import numpy as np
import pyautogui
import time
import keyboard
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def verify_email_settings():
    """Verify email settings are properly configured"""
    # Load environment variables from .env file
    load_dotenv()
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    
    if not all([sender_email, receiver_email, password]):
        print("Email settings incomplete. Please check your .env file contains:")
        print("- SENDER_EMAIL")
        print("- RECEIVER_EMAIL")
        print("- EMAIL_PASSWORD")
        return False
    
    try:
        # Test connection to SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.quit()
        print("Email settings verified successfully!")
        return True
    except Exception as e:
        print(f"Error verifying email settings: {e}")
        return False
    
def send_email_notification():
    """Send email notification without credentials verification"""
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    
    # Create the email
    subject = "Button Alert: Dark for 1 Minute"
    body = "The monitored button has remained dark for 1 minute. Please check the application."
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email notification sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Screen capture and check functions
def capture_screen(x, y, width, height):
    return ImageGrab.grab(bbox=(x, y, x + width, y + height))

def is_button_dark(image, threshold=100):
    np_image = np.array(image)
    gray_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
    avg_brightness = np.mean(gray_image)
    return avg_brightness < threshold

def check_and_click(x, y, width, height, threshold):
    """Check the button area, and click if the button is not dark."""
    screen_capture = capture_screen(x, y, width, height)
    if not is_button_dark(screen_capture, threshold):
        pyautogui.click(x + width // 2, y + height // 2)
        print("Button clicked!")
    else:
        print("Button is dark. Skipping click.")
    return is_button_dark(screen_capture, threshold)

def find_button_coords():
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

    return (x, y, width, height)

def show_monitoring_area(coords):
    """Display a rectangle showing the monitoring area."""
    # Take a screenshot
    screenshot = ImageGrab.grab()
    # Convert to PIL Image if it isn't already
    draw = ImageDraw.Draw(screenshot)
    
    # Draw rectangle with red outline
    x, y, width, height = coords
    draw.rectangle(
        [x, y, x + width, y + height],
        outline='red',
        width=2
    )
    
    # Convert to numpy array for cv2
    np_image = np.array(screenshot)
    # Convert RGB to BGR (cv2 uses BGR)
    np_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
    
    # Scale down the image to 25% of original size
    new_width = int(np_image.shape[1] * 0.25)
    new_height = int(np_image.shape[0] * 0.25)
    np_image = cv2.resize(np_image, (new_width, new_height))
    
    # Show the image
    cv2.namedWindow('Monitoring Area', cv2.WINDOW_NORMAL)
    cv2.imshow('Monitoring Area', np_image)
    cv2.waitKey(1)  # Add a small delay to ensure window updates
    
    print("\nVerifying monitoring area...")
    print("Is this the correct area? Press 'y' to continue or 'n' to reset position")
    
    while True:
        if keyboard.is_pressed('y'):
            cv2.destroyAllWindows()
            return True
        elif keyboard.is_pressed('n'):
            cv2.destroyAllWindows()
            return False
        cv2.waitKey(1)  # Keep window responsive

def get_button_coordinates():
    """Function to handle button coordinate initialization"""
    DEFAULT_COORDS = (2570, 1010, 260, 50)  # Define default coordinates as a constant
    
    user_input = input("Do you want to set button position? (y/n): ").lower()
    
    while True:
        if user_input == 'y':
            print("\nStarting button finder...")
            coords = find_button_coords()
            print(f"\nButton coordinates: {coords}")
        else:
            print("Using default button coordinates...")
            coords = DEFAULT_COORDS

        print(f"Active button coordinates: {coords}")
        print("Showing monitoring area...")
        
        if show_monitoring_area(coords):
            print("Position confirmed! Starting monitoring...")
            return coords
        else:
            print("Position rejected. Let's try again.\n")
            continue

def get_user_preferences():
    """Get user preferences for button position and email notifications"""
    preferences = {
        'button_coords': None,
        'enable_email': False
    }
    
    # Ask about email notifications
    email_input = input("Do you want email notifications? (y/n): ").lower()
    if email_input == 'y':
        if verify_email_settings():
            preferences['enable_email'] = True
            print("Email notifications enabled.")
        else:
            print("Email notifications will be disabled due to configuration issues.")
            preferences['enable_email'] = False
    
    # Get button coordinates
    preferences['button_coords'] = get_button_coordinates()
    
    return preferences

# Main script
preferences = get_user_preferences()
button_coords = preferences['button_coords']
enable_email = preferences['enable_email']
brightness_threshold = 140
dark_duration = 0
dark_time_threshold = 60

print("Monitoring button... Press 'Delete' to exit.")
try:
    while True:
        if keyboard.is_pressed('delete'):
            print("Exit command detected. Exiting program.")
            break

        if check_and_click(*button_coords, brightness_threshold):
            print("Button is dark.")
            dark_duration += 0.5
            if dark_duration >= dark_time_threshold:  # Check for 1 minute
                print("Button has been dark for 1 minute!")
                if enable_email:
                    print("Sending email notification...")
                    send_email_notification()
                else:
                    print("Email notifications are disabled.")

        else:
            dark_duration = 0  # Reset duration if button is no longer dark

        time.sleep(0.5)
except KeyboardInterrupt:
    print("Program interrupted.")
finally:
    print("Program exited.")

