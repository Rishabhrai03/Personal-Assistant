import email
import imaplib
import operator
import os
import smtplib
import sys
import time
import traceback
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import speech_recognition as sr
import pyttsx3
from datetime import datetime
import cv2
import json
from pyjokes import pyjokes
from wikipedia import summary
import webbrowser
import subprocess
import pyautogui
from requests import get

# from test import SMTP_SERVER, FROM_EMAIL, FROM_PWD

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# set your social credentials in Credentials.txt file
account = open('D:\\Virtual Assistant\\My Assistant\\Credentials1.txt', 'r').read()
Account = json.loads(account)


# print(Account)


def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        listener.pause_threshold = 1
        voice = listener.listen(source, timeout=1, phrase_time_limit=5)
    try:
        print('recognizing...')
        command = listener.recognize_google(voice, language='en-in')
        print(f'User said {command}')

    except Exception as e:
        # print(f'Error {e}')
        # speak("sorry i didn't get you...say that again please")
        return 'None'
    return command


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    print(f'audio {audio}')


def first_wish():
    hour = int(datetime.now().hour)
    if 0 <= hour < 12:
        speak('good morning...!')
    elif 12 <= hour < 18:
        speak('good afternoon...!')
    else:
        speak('good evening...!')

    speak('how may i help you?')


def get_news():
    speak('please wait... fetching the latest news...')
    url = 'https://newsapi.org/v2/everything?q=tesla&from=2021-03-02&sortBy=publishedAt&apiKey=93258ebfd0fb4331a679a30d6f4c8737'
    news_data = get(url).json()
    news = news_data['articles']
    headlines = []
    count = ['first', 'second', 'third', 'fourth', 'fifth']
    for i in news:
        headlines.append(i['title'])
    for j in range(len(count)):
        speak(f"today's {count[j]} news is {headlines[j]}")
    # print(news)


def send_email():
    speak('can you help me with text? what to say in email?')
    query = str(take_command()).lower()
    from_email = 'heenashaikh11111111@gmail.com'
    password = 'HeenaShaikh001'
    to_email = 'rrai3nov1997@gmail.com'  # niteshkumar@vivamca.org
    speak('please tell me the subject of email...')
    query_subject = str(take_command())
    subject_email = query_subject
    speak('what will be the message to be send...')
    query_message = str(take_command())
    message_email = query_message
    speak('do you want to attach any file in your email???')
    if 'attach file' in query or 'send file' in query or 'yes' in query:
        speak('please enter the file path for attachments..')
        file_location = input('please enter the file path here: ')

        speak('please wait i am sending your email')
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject_email

        msg.attach(MIMEText(message_email, 'plain'))
        file_name = os.path.basename(file_location)
        attachment = open(file_location, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {file_name}')
        msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, message_email)
        server.quit()
        speak(f'your email has been send to {to_email}')

    else:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        # text = msg.as_string()
        server.sendmail(from_email, to_email, message_email)
        server.quit()
        speak(f'your email has been send to {to_email}')


def read_email_from_gmail():
    smtp_server = "imap.gmail.com"
    try:
        mail = imaplib.IMAP4_SSL(smtp_server)
        mail.login(Account['Gmail']['UserId'], Account['Gmail']['password'])
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[3])

        for i in range(latest_email_id, first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)')
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1], 'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    speak('From : ' + email_from + '\n')
                    speak('Subject : ' + email_subject + '\n')

    except Exception as e:
        traceback.print_exc()
        print(str(e))


# To set reminder
def save_reminder(content):
    if "remind me to" in content or 'remind me' in content:
        content = content.replace("remind me", "")
    reminder = open(r"Reminders.txt", "a+")
    reminder.write(content)
    reminder.close()


# To get reminders
def get_reminders():
    reminder = open(r"Reminders.txt", "r+")
    # print(reminder.readlines())
    speak(reminder.readlines())
    reminder.close()


def get_operator_fn(op):
    return {
        '+': operator.add,
        '-': operator.sub,
        'x': operator.mul,
        'divided': operator.__truediv__,
        'Mod': operator.mod,
        'mod': operator.mod,
        '^': operator.xor,
    }[op]


def eval_binary_expr(op1, oper, op2):
    try:
        op1, op2 = int(op1), int(op2)
        return speak(get_operator_fn(oper)(op1, op2))
    except Exception as error:
        speak("sorry sir cant hear you properly...")


def get_location():
    speak('wait... let me check...!')
    try:
        get_ip = get('https://api.ipify.org').text
        print("your ip: -", get_ip)
        url = f'https://get.geojs.io/v1/ip/geo/{get_ip}.json'
        location = get(url).json()
        speak(
            f'i am not sure... but i think we are in {location["region"]} state, {location["city"]} city, {location["country"]}.')
        # print(location)
    except Exception as error:
        speak('sorry... due to network issue am not able to find our location...')


def task_execution():
    first_wish()
    while True:
        query = take_command().lower()
        time.sleep(2)
        if 'open camera' in query:
            camera = cv2.VideoCapture(0)
            while True:
                ret, img = camera.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(1)
                if k == 27:
                    break
            camera.release()
            cv2.destroyAllWindows()

        if 'about' in query:  # need to edit this
            query = query.replace('about', '')
            data = summary(query, sentences=2)
            speak(data)

        if 'google' in query or 'chrome' in query:
            speak('what should  i search on google?')
            search = take_command().lower()
            # TwitterBot.google_search(search)
            webbrowser.open("https://www.google.com/search?q=" + search)

        if 'youtube' in query:
            # webbrowser.open('youtube.com')
            speak('What should i search on youtube ?')
            search = take_command().lower()
            webbrowser.open('https://www.youtube.com/results?search_query=' + search)

        if "open calculator" in query:
            subprocess.Popen('C:\\Windows\\System32\\calc.exe')

        if "close calculator" in query:
            os.system("taskkill /f /im  C:\\Windows\\System32\\calc.exe")

        if "open paint" in query or 'paint' in query:
            subprocess.Popen('C:\\WINDOWS\\system32\\mspaint.exe')

        if 'calculate' in query:
            speak('what should i calculate?')
            calculation_string = take_command().lower()
            eval_binary_expr(*(calculation_string.split()))

        if 'switch window' in query or 'switch applicaticon' in query or 'switch' in query:
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.keyUp('alt')

        if 'news' in query:
            get_news()
        if 'send email' in query or 'send reports' in query:
            send_email()

        if 'shutdown' in query:
            speak("Hold On a Sec ! Your system is on its way to shut down")
            os.system('shutdown /r /t 5')
            # subprocess.call('shutdown / p /f')

        # if 'notepad' in query:
        #
        if 'exit' in query or 'sleep' in query or 'bye' in query:
            speak('Okay bye, thanks for using me... see you soon...!')
            break
        if "who are you" in query or "define yourself" in query:
            intro = '''Hello, I am Person. Your personal Assistant.
                I am here to make your life easier. You can command me to perform
                various tasks such as calculating sums or opening applications etcetra'''
            speak(intro)

        if "who made you" in query or "created you" in query:
            speak('I have been created by Rishabh Rai and Uday Futak.')

        if "write a note" in query or 'make a note' in query:
            speak("What should i write, sir")
            note = take_command()
            file = open('jarvis.txt', 'w')
            speak("Sir, Should i include date and time")
            date_time = take_command()
            if 'yes' in date_time or 'sure' in date_time:
                str_Time = datetime.now().strftime("% H:% M:% S")
                file.write(str_Time)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)

        if "show note" in query:
            speak("Showing Notes")
            file = open("jarvis.txt", "r").read()
            print(file)
            speak(file)

        if 'remind me' in query:
            save_reminder(query)
            speak('your reminders are saved successfully...')

        if "my reminder" in query:
            try:
                get_reminders()
                speak("I guess that's all I had to remind you")
            except Exception as e:
                speak("Sorry could not fetch reminders")

        if 'joke' in query:
            speak(pyjokes.get_joke())

        if 'minimise all' in query or 'minimize all' in query:
            pyautogui.hotkey('winleft', 'd')
            speak('task completed minimized all the open windows...!')

        if 'screenshot' in query:
            im1 = pyautogui.screenshot()
            path = os.path.join(os.environ['USERPROFILE'], 'Desktop', "Screenshot")
            try:
                os.mkdir(path)
                im1.save(r"{}\screenshot.png".format(path))
                speak('your screenshot has been saved on desktop folder')
            except FileExistsError as e:
                im1.save(r"{}\screenshot.png".format(path))

        if 'current location' in query or 'where are we' in query:
            get_location()


if __name__ == '__main__':
# def main_task():
    while True:
        command = take_command().lower()
        if 'wake up' in command or 'hey' in command:
            task_execution()
        if 'goodbye' in command:
            sys.exit()
