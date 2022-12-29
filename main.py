import sys
from neuralintents import GenericAssistant
import speech_recognition as sr
import threading
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import google_search
import tkinter as tk


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)



def talk(text):
    engine.say(text)
    engine.runAndWait()


def play_youtube(command):
    cmnd = ""
    if 'play' in command:
        cmnd = command.replace("play ", "")
    if 'on youtube' in cmnd:
        cmnd = cmnd.replace("on youtube", '')
    if 'can you' in cmnd:
        cmnd = cmnd.replace('can you', '')
    talk('playing ' + cmnd)
    trd = threading.Thread(target=pywhatkit.playonyt, args=[cmnd])
    trd.start()


def web_browser(command):
    cmnd = command
    if 'show me' in cmnd:
        cmnd = command.replace("show me ", "")
    if 'on web browser' in cmnd:
        cmnd = cmnd.replace("on web browser", '')
    if 'open web browser and search ' in cmnd:
        cmnd = cmnd.replace('open web browser and search ', '')
    if 'open browser and search ' in cmnd:
        cmnd = cmnd.replace('open web browser and search ', '')
    if 'open my browser and search ' in cmnd:
        cmnd = cmnd.replace('open web browser and search ', '')
    trd = threading.Thread(target=pywhatkit.search, args=[cmnd])
    trd.start()


def wiki_p(command):
    cmnd = command
    try:
        if 'tell me about ' in cmnd:
            cmnd = cmnd.replace("tell me about ", "")
        if 'enlight me about ' in cmnd:
            cmnd = cmnd.replace("enlight me about ", '')
        if 'what is ' in cmnd:
            cmnd = cmnd.replace('what is ', '')
        if "give me some some info about " in cmnd:
            cmnd = cmnd.replace("give me some some info about ", "")
        if "when did " in cmnd:
            cmnd = cmnd.replace("when did ", "")
        if "when was " in cmnd:
            cmnd = cmnd.replace("when was ", "")
        if "how many " in cmnd:
            cmnd = cmnd.replace("how many ", "")
        if "who is " in cmnd:
            cmnd = cmnd.replace("who is ", "")
        if "who was " in cmnd:
            cmnd = cmnd.replace("who was ", "")
        print(cmnd)
        talk('searching for' + cmnd)
        info = wikipedia.summary(cmnd, lines=2)
        print(info)
        talk(info)
    except Exception:
        talk("unable to find any suitable answer on my own")
        web_browser(cmnd)


def stop_vs():
    sys.exit()


def command_trim(command):
    cmnd = ''
    if "hey alexa " in command:
        cmnd = command.replace('hey alexa ', '')
    elif 'alexa ' in command:
        cmnd = command.replace('alexa ', '')
    return cmnd


def take_command():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=0.5)
            print('listening...')
            voice = listener.listen(source, timeout=8, phrase_time_limit=8)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command_trim(command)
                print(command)
                return command
            else:
                return ""

    except Exception:
        return take_command()


def run_alexa():
    assistant = GenericAssistant('intents.json')
    assistant.train_model()
    assistant.save_model()
    assistant.load_model()
    while True:
        command = take_command()
        if command != "":
            response = assistant.request(command)
            if 'youtube' in response:
                play_youtube(command)
            elif 'time' in response:
                time = datetime.datetime.now().strftime('%I:%M %p')
                talk('Current time is ' + time)
            elif 'webbrowser' in response:
                web_browser(command)
            elif 'search' in response:
                try:
                    res = google_search.query(command)
                    talk(res)
                except Exception:
                    talk("unable to find short and straight answer in internet")
                    wiki_p(command)
            elif 'joke' in response:
                talk(pyjokes.get_joke())
            elif 'send message' in response:
                talk("if you logged in to the whatsApp only then message will be sent within 30 seconds")
                pywhatkit.sendwhatmsg_instantly("+8801760886380", "this is test msg by python", 30, True, 5)
            elif "Sad to see you go" or "Talk to you later" or "Goodbye!" in response:
                talk(response)
                stop_vs()
        else:
            talk("hello this is alexa. You have to mention my name before giving me any command.")
            continue


if __name__ == '__main__':
    run_alexa()

