from PIL import ImageGrab, Image, ImageDraw
import cv2
import numpy as np
import time
import json
import os
import keyboard
import pyautogui

def load_settings():
    """Load settings from JSON file, create default if not exists"""
    default_settings = {
        "language": "zh",
        "brightness_threshold": 170,
        "button_coords": [2570, 1010, 260, 50],
        "check_interval": 0.5,
        "dark_time_threshold": 60,
        "email_settings": {
            "sender_email": "",
            "receiver_email": "",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587
        }
    }
    
    try:
        with open('settings.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        save_settings(default_settings)
        return default_settings

def save_settings(settings):
    """Save current settings to JSON file"""
    with open('settings.json', 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)

def capture_screen(x, y, width, height):
    return ImageGrab.grab(bbox=(x, y, x + width, y + height))

def calibrate_threshold(button_coords):
    """Calibrate the brightness threshold for the current system"""
    print("開始校準亮度閾值... / Starting brightness threshold calibration...")
    print("請確保按鈕處於明亮狀態（可見/活躍）/ Please ensure the button is in its LIGHT state (visible/active)")
    
    for i in range(3, 0, -1):
        print(f"將在 {i} 秒後捕捉明亮狀態... / Capturing light state in: {i} seconds...")
        time.sleep(1)
    
    # Capture light state
    screen_capture = capture_screen(*button_coords)
    np_image = np.array(screen_capture)
    gray_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
    light_brightness = np.mean(gray_image)
    print(f"已捕捉明亮狀態。亮度值：{light_brightness:.2f} / Light state captured. Brightness: {light_brightness:.2f}")
    
    print("\n現在等待按鈕進入暗淡狀態 / Now wait for the button to enter its DARK state")
    for i in range(3, 0, -1):
        print(f"將在 {i} 秒後捕捉暗淡狀態... / Capturing dark state in: {i} seconds...")
        time.sleep(1)
    
    # Capture dark state
    screen_capture = capture_screen(*button_coords)
    np_image = np.array(screen_capture)
    gray_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
    dark_brightness = np.mean(gray_image)
    print(f"已捕捉暗淡狀態。亮度值：{dark_brightness:.2f} / Dark state captured. Brightness: {dark_brightness:.2f}")
    
    # Calculate and validate threshold
    if light_brightness <= dark_brightness:
        raise ValueError("錯誤：明亮狀態的亮度必須大於暗淡狀態 / Error: Light brightness must be greater than dark brightness")
    
    threshold = (light_brightness + dark_brightness) / 2
    print(f"\n校準完成！新的閾值：{threshold:.2f} / Calibration complete! New threshold: {threshold:.2f}")
    return threshold

def find_button_coords():
    print("Click the top-left corner of the button...")
    time.sleep(3)
    x1, y1 = pyautogui.position()
    print(f"First position: {(x1, y1)}")

    print("\nNow click the bottom-right corner of the button...")
    time.sleep(3)
    x2, y2 = pyautogui.position()
    print(f"Second position: {(x2, y2)}")

    x = min(x1, x2)
    y = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    return (x, y, width, height)

def get_button_coordinates():
    """Function to handle button coordinate initialization"""
    print("\nStarting button finder...")
    coords = find_button_coords()
    print(f"\nButton coordinates: {coords}")
    print(f"Active button coordinates: {coords}")
    return coords

def show_monitoring_area(coords):
    """Display a rectangle showing the monitoring area."""
    screenshot = ImageGrab.grab()
    draw = ImageDraw.Draw(screenshot)
    
    x, y, width, height = coords
    draw.rectangle(
        [x, y, x + width, y + height],
        outline='red',
        width=2
    )
    
    np_image = np.array(screenshot)
    np_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
    
    # Resize for better visibility
    new_width = int(np_image.shape[1] * 0.25)
    new_height = int(np_image.shape[0] * 0.25)
    np_image = cv2.resize(np_image, (new_width, new_height))
    
    cv2.namedWindow('Monitoring Area', cv2.WINDOW_NORMAL)
    cv2.imshow('Monitoring Area', np_image)
    cv2.waitKey(1)
    
    print("\nVerifying monitoring area...")
    print("Is this the correct area? Press 'y' to continue or 'n' to reset position")
    
    while True:
        if keyboard.is_pressed('y'):
            cv2.destroyAllWindows()
            return True
        elif keyboard.is_pressed('n'):
            cv2.destroyAllWindows()
            return False
        cv2.waitKey(1)

def main():
    setup_messages = {
        'en': {
            'welcome': "\n=== Brightness & Position Setup ===",
            'step1': "\nStep 1: Initial Setup",
            'find_friend': "1. Find a friend who can successfully send you a message",
            'open_chat': "2. Open their chat window",
            'position_note': "3. You'll need to set the position of the 'Add Friend' button",
            'one_time': "Note: This setup only needs to be done once, unless you delete the 'settings.json' file",
            'ready': "\nPress Enter when ready, or 'n' to skip: ",
            
            'step2': "\nStep 2: Button Position",
            'position_skip': "Skipping position setup, using existing coordinates...",
            
            'step3': "\nStep 3: Brightness Calibration",
            'current_threshold': "Current brightness threshold: {}",
            'calibration_skip': "\nPress Enter to start calibration, or 'n' to skip: ",
            'setup_complete': "\nSetup complete! You can now run the main program.",
        },
        'zh': {
            'welcome': "\n=== 亮度和位置設置 ===",
            'step1': "\n步驟 1：初始設置",
            'find_friend': "1. 找一個可以成功發送訊息給你的好友",
            'open_chat': "2. 打開與該好友的聊天視窗",
            'position_note': "3. 您需要設置「交友邀請」按鈕的位置",
            'one_time': "注意：除非您刪除特定檔案(settings.json)，否則此設置只需完成一次",
            'ready': "\n準備好請按Enter，跳過請按'n': ",
            
            'step2': "\n步驟 2：按鈕位置",
            'position_skip': "跳過位置設置，使用現有座標...",
            
            'step3': "\n步驟 3：亮度校準",
            'current_threshold': "目前亮度閾值：{}",
            'calibration_skip': "\n按Enter開始校準，或按'n'跳過: ",
            'setup_complete': "\n設置完成！您現在可以運行主程式。"
        }
    }

    settings = load_settings()
    lang = settings['language'] if settings['language'] in setup_messages else 'zh'
    msgs = setup_messages[lang]
    
    print(msgs['welcome'])
    
    # Step 1: Initial instructions
    print(msgs['step1'])
    print(msgs['find_friend'])
    print(msgs['open_chat'])
    print(msgs['position_note'])
    print(msgs['one_time'])
    
    if input(msgs['ready']).lower() != 'n':
        # Step 2: Button Position
        print(msgs['step2'])
        while True:
            new_coords = get_button_coordinates()
            print("Showing monitoring area...")
            
            if show_monitoring_area(new_coords):
                settings['button_coords'] = list(new_coords)
                save_settings(settings)
                print("Position confirmed and saved!")
                break
            else:
                print("Position rejected.")
                if input(msgs['ready']).lower() == 'n':
                    print(msgs['position_skip'])
                    break
    else:
        print(msgs['position_skip'])
    
    # Step 3: Brightness Calibration
    print(msgs['step3'])
    print(msgs['current_threshold'].format(settings['brightness_threshold']))
    
    if input(msgs['calibration_skip']).lower() != 'n':
        try:
            new_threshold = calibrate_threshold(settings['button_coords'])
            settings['brightness_threshold'] = new_threshold
            save_settings(settings)
            print("Brightness threshold saved successfully!")
        except Exception as e:
            print(f"Error during calibration: {str(e)}")
            print("Settings were not changed.")
    
    print(msgs['setup_complete'])

if __name__ == "__main__":
    main() 