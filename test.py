# # Python 3.8.0
# import imaplib
# import email
# import traceback
#
# import pyttsx3
#
# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)
#
# ORG_EMAIL = "@gmail.com"
# FROM_EMAIL = "heenashaikh11111111" + ORG_EMAIL
# FROM_PWD = "HeenaShaikh001"
# SMTP_SERVER = "imap.gmail.com"
# SMTP_PORT = 993
#
#
# def speak(audio):
#     engine.say(audio)
#     engine.runAndWait()
#     print(f'audio {audio}')
#
#
# def read_email_from_gmail():
#     try:
#         mail = imaplib.IMAP4_SSL(SMTP_SERVER)
#         mail.login(FROM_EMAIL, FROM_PWD)
#         mail.select('inbox')
#
#         data = mail.search(None, 'ALL')
#         mail_ids = data[1]
#         id_list = mail_ids[0].split()
#         first_email_id = int(id_list[0])
#         latest_email_id = int(id_list[3])
#
#         for i in range(latest_email_id, first_email_id, -1):
#             data = mail.fetch(str(i), '(RFC822)')
#             for response_part in data:
#                 arr = response_part[0]
#                 if isinstance(arr, tuple):
#                     msg = email.message_from_string(str(arr[1], 'utf-8'))
#                     email_subject = msg['subject']
#                     email_from = msg['from']
#                     speak('From : ' + email_from + '\n')
#                     speak('Subject : ' + email_subject + '\n')
#
#     except Exception as e:
#         traceback.print_exc()
#         print(str(e))
#
#
# read_email_from_gmail()


# import time
#
# import win32con
# import win32gui
# #
# time.sleep(2)
# Minimize = win32gui.GetForegroundWindow()
# win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)

# from pynput import keyboard
#
#
# def on_press(key):
#     try:
#         print(f'alphanumeric key {key.char} pressed')
#     except AttributeError:
#         print(f'special key {key} pressed')
#
# #
# # def on_release(key):
# #     print(f'{key} released')
# #     if key == keyboard.Key.esc:
# #         # Stop listener
# #         return False
#
#
# # Collect events until released
# with keyboard.Listener(
#         on_press=on_press) as listener:
#     listener.join()

# time.sleep(2)
# Minimize = win32gui.GetForegroundWindow()
# win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)

# os.system()
import tkinter as tk
from PIL import Image

root = tk.Tk()
file = 'My Assistant/assets/sound.gif'

info = Image.open(file)
frames = info.n_frames
print(frames)
im = [tk.PhotoImage(file=file, format=f'gif -index {i}') for i in range(frames)]
print(im)

# tk.PhotoImage(file=file, format=f'gif -index{i}')


root.mainloop()
