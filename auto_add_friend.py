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
import json


MESSAGES = {
    'en': {
        'select_language': 'Select language (en/zh): ',
        'email_settings_incomplete': "Email settings incomplete. Please check your .env file contains:",
        'email_verified': "Email settings verified successfully!",
        'email_verify_error': "Error verifying email settings: {}",
        'email_sent': "Email notification sent successfully!",
        'email_error': "Error sending email: {}",
        'button_clicked': "Button clicked!",
        'button_dark': "Button is dark. Skipping click.",
        'click_top_left': "Click the top-left corner of the button...",
        'click_bottom_right': "\nNow click the bottom-right corner of the button...",
        'first_position': "First position: {}",
        'second_position': "Second position: {}",
        'verify_area': "\nVerifying monitoring area...",
        'confirm_area': "Is this the correct area? Press 'y' to continue or 'n' to reset position",
        'set_button_position': "Do you want to set button position? (y/n): ",
        'starting_finder': "\nStarting button finder...",
        'button_coords': "\nButton coordinates: {}",
        'using_default': "Using default button coordinates...",
        'active_coords': "Active button coordinates: {}",
        'showing_area': "Showing monitoring area...",
        'position_confirmed': "Position confirmed! Starting monitoring...",
        'position_rejected': "Position rejected. Let's try again.\n",
        'want_email': "Do you want email notifications? (y/n): ",
        'email_enabled': "Email notifications enabled.",
        'email_disabled': "Email notifications will be disabled due to configuration issues.",
        'monitoring': "Monitoring button... Press 'Delete' to exit. (Long press)",
        'exit_detected': "Exit command detected. Exiting program.",
        'button_dark_long': "Button has been dark for 1 minute!",
        'sending_email': "Sending email notification...",
        'email_notifications_disabled': "Email notifications are disabled.",
        'program_interrupted': "Program interrupted.",
        'program_exited': "Program exited.",
        'current_settings': 'Current settings:',
        'setting_language': '1. Language: {}',
        'setting_threshold': '2. Brightness threshold: {}',
        'setting_position': '3. Button position: {}',
        'setting_email': '4. Email notifications',
        'setting_continue': '5. Continue with current settings',
        'skip_settings': '3. Skip settings',
        'change_settings': 'What would you like to change? (1-3): ',
        'change_more': 'Would you like to change anything else? (y/n): ',
        'invalid_choice': 'Invalid choice. Please select 1-3.',
        'verify_position': 'Would you like to verify the button position for this session?',
        'save_position_default': 'Would you like to save this position as the default? (y/n): ',
        'want_change_settings': 'Would you like to modify any system settings? (y/n): '
    },
    'zh': {
        'select_language': '請選擇語言 (預設中文，按Enter繼續，或輸入en切換至英文): ',
        'email_settings_incomplete': "電郵設定不完整。請檢查.env檔案包含以下內容：",
        'email_verified': "電郵設定驗證成功！",
        'email_verify_error': "驗證電郵設定時出錯：{}",
        'email_sent': "郵件通知發送成功！",
        'email_error': "發送郵件時出錯：{}",
        'button_clicked': "已點擊按鈕！",
        'button_dark': "按鈕變暗。跳過點擊。",
        'click_top_left': "請點擊按鈕的左上角...",
        'click_bottom_right': "\n現在點擊按鈕的右下角...",
        'first_position': "第一個位置：{}",
        'second_position': "第二個位置：{}",
        'verify_area': "\n驗證監控區域...",
        'confirm_area': "這是正確的區域嗎？按'y'繼續或按'n'重新設定位置",
        'set_button_position': "是否要設定按鈕位置？(y/n): ",
        'starting_finder': "\n開始尋找按鈕...",
        'button_coords': "\n按鈕座標：{}",
        'using_default': "使用預設按鈕座標...",
        'active_coords': "目前使用的按鈕座標：{}",
        'showing_area': "顯示監控區域...",
        'position_confirmed': "位置已確認！開始監控...",
        'position_rejected': "位置已拒絕。讓我們重試。\n",
        'want_email': "是否要啟用電郵通知？(y/n): ",
        'email_enabled': "已啟用電郵通知。",
        'email_disabled': "由於設定問題，電郵通知將被停用。",
        'monitoring': "監控按鈕中... 按住'Delete'鍵退出。(長按)",
        'exit_detected': "檢測到退出指令。正在結束程式。",
        'button_dark_long': "按鈕已持續變暗一分鐘！",
        'sending_email': "正在發送電郵通知...",
        'email_notifications_disabled': "電郵通知已停用。",
        'program_interrupted': "程式已中斷。",
        'program_exited': "程式已結束。",
        'current_settings': '目前設定：',
        'setting_language': '1. 語言：{}',
        'setting_threshold': '2. 亮度閾值：{}',
        'setting_position': '3. 按鈕位置：{}',
        'setting_email': '4. 電郵通知',
        'setting_check_interval': '5. 檢查間隔：{}',
        'setting_dark_time_threshold': '6. 黑暗時間閾值：{}',
        'setting_continue': '5. 使用目前設定繼續',
        'skip_settings': '3. 跳過設定',
        'change_settings': '想要更改哪個設定？(1-3)：',
        'change_more': '是否要更改其他設定？(y/n)：',
        'invalid_choice': '無效的選擇。請選擇 1-3。',
        'verify_position': '是否要驗證本次執行的按鈕位置？',
        'save_position_default': '是否要將此位置儲存為預設值？(y/n)：',
        'want_change_settings': '是否要修改系統設定？(y/n)：'
    }
}

# At the top of the file, after imports
LANG = 'zh'  # Default language

def get_language(settings):
    """Get user's preferred language"""
    global LANG  # Declare global
    while True:
        if settings['language'] == 'none' or (settings['language'] != 'zh' and settings['language'] != 'en'):
            lang = input(MESSAGES['zh']['select_language']).lower()
            
            if lang == 'en':
                settings['language'] = 'en'
            else:
                settings['language'] = 'zh'
            save_settings(settings)
            return settings['language']
        else:
            return settings['language']

def verify_email_settings():
    """Verify email settings are properly configured"""
    load_dotenv()
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    
    if not all([sender_email, receiver_email, password]):
        print(MESSAGES[LANG]['email_settings_incomplete'])
        print("- SENDER_EMAIL")
        print("- RECEIVER_EMAIL")
        print("- EMAIL_PASSWORD")
        return False
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.quit()
        print(MESSAGES[LANG]['email_verified'])
        return True
    except Exception as e:
        print(MESSAGES[LANG]['email_verify_error'].format(e))
        return False

def send_email_notification():
    """Send email notification without credentials verification"""
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    
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
        print(MESSAGES[LANG]['email_sent'])
    except Exception as e:
        print(MESSAGES[LANG]['email_error'].format(e))

# Screen capture and check functions
def capture_screen(x, y, width, height):
    return ImageGrab.grab(bbox=(x, y, x + width, y + height))

def is_button_dark(image, threshold=100):
    np_image = np.array(image)
    gray_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
    avg_brightness = np.mean(gray_image)
    # print(f"Average brightness: {avg_brightness:.2f} (Threshold: {threshold})")  # Added logging
    return avg_brightness < threshold

def check_and_click(x, y, width, height, threshold):
    """Check the button area, and click if the button is not dark."""
    screen_capture = capture_screen(x, y, width, height)
    if not is_button_dark(screen_capture, threshold):
        pyautogui.click(x + width // 2, y + height // 2)
        print(MESSAGES[LANG]['button_clicked'])
    else:
        print(MESSAGES[LANG]['button_dark'])
    return is_button_dark(screen_capture, threshold)

def find_button_coords():
    print(MESSAGES[LANG]['click_top_left'])
    time.sleep(3)
    x1, y1 = pyautogui.position()
    print(MESSAGES[LANG]['first_position'].format((x1, y1)))

    print(MESSAGES[LANG]['click_bottom_right'])
    time.sleep(3)
    x2, y2 = pyautogui.position()
    print(MESSAGES[LANG]['second_position'].format((x2, y2)))

    x = min(x1, x2)
    y = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    return (x, y, width, height)

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
    
    new_width = int(np_image.shape[1] * 0.25)
    new_height = int(np_image.shape[0] * 0.25)
    np_image = cv2.resize(np_image, (new_width, new_height))
    
    cv2.namedWindow('Monitoring Area', cv2.WINDOW_NORMAL)
    cv2.imshow('Monitoring Area', np_image)
    cv2.waitKey(1)
    
    print(MESSAGES[LANG]['verify_area'])
    print(MESSAGES[LANG]['confirm_area'])
    
    while True:
        if keyboard.is_pressed('y'):
            cv2.destroyAllWindows()
            return True
        elif keyboard.is_pressed('n'):
            cv2.destroyAllWindows()
            return False
        cv2.waitKey(1)
    
    ############### for MacOS ###############
    # while True:
    #     key = keyboard.read_key()
    #     if key == 16: # y = 16
    #         cv2.destroyAllWindows()
    #         return True
    #     elif key == 45: # n = 45
    #         cv2.destroyAllWindows()
    #         return False
    #########################################

def get_button_coordinates():
    """Function to handle button coordinate initialization"""
    while True:
        print(MESSAGES[LANG]['starting_finder'])
        coords = find_button_coords()
        print(MESSAGES[LANG]['button_coords'].format(coords))
        print(MESSAGES[LANG]['active_coords'].format(coords))
        print(MESSAGES[LANG]['showing_area'])
        
        if show_monitoring_area(coords):
            print(MESSAGES[LANG]['position_confirmed'])
            return coords
        else:
            print(MESSAGES[LANG]['position_rejected'])
            continue

def load_settings():
    """Load settings from JSON file, create default if not exists"""
    default_settings = {
        "language": "none", # for the first time, it will be set to zh by default
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
        # If file doesn't exist or is invalid, create new with defaults
        save_settings(default_settings)
        return default_settings

def initialize_preferences(settings):
    """Initialize session preferences with default values"""
    return {
        'button_coords': tuple(settings['button_coords']),
        'enable_email': False,
        'monitor_active': True,
        'current_session': {
            'dark_duration': 0,
            'alerts_sent': 0,
            'start_time': time.time()
        }
    }

def get_user_preferences(settings):
    """Get user preferences with improved flow"""
    global LANG
    preferences = initialize_preferences(settings)
    
    # First, confirm critical session preferences
    if input(MESSAGES[LANG]['set_button_position']).lower() in ['y']:
        new_coords = get_button_coordinates()
        preferences['button_coords'] = new_coords
        settings['button_coords'] = list(new_coords)
        save_settings(settings)
    
    # Ask about email notifications for this session
    if input(MESSAGES[LANG]['want_email']).lower() in ['y', '']:
        if verify_email_settings():
            preferences['enable_email'] = True
            print(MESSAGES[LANG]['email_enabled'])
        else:
            print(MESSAGES[LANG]['email_disabled'])
    
    # Show current settings but don't prompt for changes by default
    print(f"\n{MESSAGES[LANG]['current_settings']}")
    print(MESSAGES[LANG]['setting_language'].format(settings['language']))
    print(MESSAGES[LANG]['setting_threshold'].format(settings['brightness_threshold']))
    print(MESSAGES[LANG]['setting_position'].format(preferences['button_coords']))
    print(MESSAGES[LANG]['setting_email'].format(preferences['enable_email']))
    print(MESSAGES[LANG]['setting_check_interval'].format(settings['check_interval']))
    print(MESSAGES[LANG]['setting_dark_time_threshold'].format(settings['dark_time_threshold']))
    print('--------------------------------')

    return preferences

def save_settings(settings):
    """Save current settings to JSON file"""
    with open('settings.json', 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)

# Main script
settings = load_settings()
LANG = get_language(settings)
preferences = get_user_preferences(settings)

# Use preferences for session-specific values
button_coords = preferences['button_coords']
enable_email = preferences['enable_email']
current_session = preferences['current_session']

# Use settings for persistent values
brightness_threshold = settings['brightness_threshold']
dark_time_threshold = settings['dark_time_threshold']
check_interval = settings['check_interval']

print(MESSAGES[LANG]['monitoring'])
try:
    while True:
        if keyboard.is_pressed('delete'):
            print(MESSAGES[LANG]['exit_detected'])
            break

        if check_and_click(*button_coords, brightness_threshold):
            print(MESSAGES[LANG]['button_dark'])
            current_session['dark_duration'] += check_interval
            if current_session['dark_duration'] >= dark_time_threshold:
                print(MESSAGES[LANG]['button_dark_long'])
                if enable_email and current_session['alerts_sent'] == 0:
                    print(MESSAGES[LANG]['sending_email'])
                    send_email_notification()
                    current_session['alerts_sent'] += 1
                else:
                    print(MESSAGES[LANG]['email_notifications_disabled'])
        else:
            current_session['dark_duration'] = 0

        time.sleep(check_interval)
except KeyboardInterrupt:
    print(MESSAGES[LANG]['program_interrupted'])
finally:
    print(MESSAGES[LANG]['program_exited'])

