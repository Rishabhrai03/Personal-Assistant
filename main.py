import speech_recognition as sr
import pyttsx3

listner = sr.Recognizer()
try:
    with sr.Microphone() as source:
        voice = listner.listen(source)
        command = listner.recognize_google(voice)
        print(command)
        pass
except Exception as e:
    print(f'Error {e}')


def speak(audio):
    print(f'audio {audio}')


if __name__ == '__main__':
    speak('')
