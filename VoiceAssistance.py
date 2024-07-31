import subprocess
import pyttsx3 
import random
import speech_recognition as sr 
import wikipedia  
import webbrowser
import os
import winshell  
import pyjokes   
import feedparser   
import requests  
import datetime 
import shutil
import ctypes
import time
import cv2  # Import OpenCV
from tkinter import *
from ecapture import ecapture as ec  
from pytube import YouTube    

voiceEngine = pyttsx3.init('sapi5')
voices = voiceEngine.getProperty('voices')
voiceEngine.setProperty('voice', voices[1].id)

def speak(text):
    voiceEngine.say(text)
    voiceEngine.runAndWait()

def wish():
    print("Welcome back !!")
    speak("Welcome back !!")
    
    hour = datetime.datetime.now().hour
    if hour >= 4 and hour < 12:
        speak("Good Morning !!")
        print("Good Morning !!")
    elif hour >= 12 and hour < 16:
        speak("Good Afternoon !!")
        print("Good Afternoon !!")
    elif hour >= 16 and hour < 24:
        speak("Good Evening !!")
        print("Good Evening !!")
    else:
        speak("Good Night, See You Tomorrow")

    speak("Jarvis at your service")
    print("Jarvis at your service")

def getName():
    global uname
    speak("Can I please know your name?")
    print("Can I please know your name?")
    uname = takeCommand()
    print("Name:", uname)
    speak("I am glad to know you!")
    print("I am glad to know you!")
    speak("How can I help you, " + uname)
    print("How can I help you, " + uname)

def updateCommandLabel(command):
    showCommand.set(command)

def takeCommand():
    global showCommand
    showCommand.set("Listening....")

    recog = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening to the user")
        recog.pause_threshold = 0.5
        userInput = recog.listen(source)

    try:
        print("Recognizing the command")
        command = recog.recognize_google(userInput, language='en-in')
        print(f"Command is: {command}\n")
        updateCommandLabel(command)

    except Exception as e:
        print(e)
        print("Unable to Recognize the voice.")
        updateCommandLabel("Unable to Recognize the voice.")
        return "None"

    return command

def getWeather(city_name):
    baseUrl = "http://api.openweathermap.org/data/2.5/weather?"
    url = baseUrl + "appid=" + 'd850f7f52bf19300a9eb4b0aa6b80f0d' + "&q=" + city_name
    response = requests.get(url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        temp = y["temp"]
        temp -= 273 
        pressure = y["pressure"]
        humidity = y["humidity"]
        desc = x["weather"]
        description = desc[0]["description"]
        info = (f" Temperature= {temp}°C\n atmospheric pressure (hPa) ={pressure} \n humidity = {humidity}% \n description = {description}")
        print(info)
        speak("Here is the weather report at")
        speak(city_name)
        speak(info)
    else:
        speak("City Not Found")

def getNews():
    try:
        rss_url = 'http://feeds.bbci.co.uk/news/world/rss.xml'
        feed = feedparser.parse(rss_url)
        
        if 'entries' in feed:
            headlines_list = [entry.title for entry in feed.entries]
            
            if headlines_list:
                speak("Here are some latest news headlines from BBC:")
                for headline in headlines_list[:5]:  # Fetching top 5 headlines
                    print(headline)
                    speak(headline)
            else:
                speak("Sorry, I couldn't fetch the news headlines at the moment.")
        else:
            speak("Failed to connect to BBC News RSS feed. Please try again later.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        speak("Sorry, an error occurred while fetching the news headlines.")

def open_calculator():
    try:
        subprocess.Popen('calc.exe')
    except FileNotFoundError:
        print("Calculator app not found on this system.")

def playMusic():
    speak("Enjoy the music!")
    music_dir = r"F:\MP3\English Songs"
    songs = os.listdir(music_dir)
    if songs:
        random_song = random.choice(songs)
        os.startfile(os.path.join(music_dir, random_song))
    else:
        speak("No music files found in the directory.")


def capture_photo(filename='img.jpg'):
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return
    
    # Capture a single frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Unable to capture image.")
        return
    
    # Save the captured image
    cv2.imwrite(filename, frame)
    print(f"Photo saved as {filename}")
    
    # Release the camera
    cap.release()

def callVoiceAssistant():
    global uname
    uname = ''  # Initialize uname
    assname = ''  # Initialize assname

    os.system('cls')
    wish()
    getName()
    print(uname)

    while True:
        command = takeCommand().lower()
        print(command)

        if "jarvis" in command:
            wish()
            
        elif 'how are you' in command:
            speak("I am fine, Thank you")
            speak("How are you, ")
            speak(uname)

        elif "good morning" in command or "good afternoon" in command or "good evening" in command:
            speak("A very " + command)
            speak("Thank you for wishing me! Hope you are doing well!")

        elif 'fine' in command or "good" in command:
            speak("It's good to know that you're fine")
            print("It's good to know that you're fine")
       
        elif "who are you" in command:
            speak("I am your desktop virtual assistant.")
            print("I am your desktop virtual assistant.")

        elif "change my name to" in command:
            speak("What would you like me to call you?")
            uname = takeCommand()
            speak('Hello again,')
            speak(uname)

        elif "what's your name" in command:
            speak("People call me Jarvis.")
            print("People call me Jarvis.")
        
        elif "change name" in command:
            speak("What would you like to call me?")
            assname = takeCommand()
            speak("Thank you for naming me!")

        elif "what's your name" in command:
            speak("People call me Jarvis.")
            print("People call me Jarvis.")
            speak(assname)
        
        elif 'time' in command:
            strTime = datetime.datetime.now()
            curTime = str(strTime.hour) + " hours " + str(strTime.minute) + " minutes " + str(strTime.second) + " seconds"
            speak(uname)
            speak(f" the time is {curTime}")
            print(curTime)

        elif "wikipedia" in command:
            speak("What do you want to search on Wikipedia?")
            search_command = takeCommand()
            if search_command:
                try:
                    results = wikipedia.summary(search_command, sentences=2)
                    speak("According to Wikipedia...")
                    speak(results)
                    
                except wikipedia.exceptions.DisambiguationError as e:
                    speak("Can you please specify? I found multiple results.")
                except wikipedia.exceptions.PageError as e:
                    speak("Sorry, I could not find any matching results.")
                    
        elif 'open youtube' in command:
            speak("Here you go, YouTube is opening\n")
            webbrowser.open("youtube.com")

        elif 'open google' in command:
            speak("Opening Google\n")
            webbrowser.open("google.com")
            
        elif 'open instagram' in command:
            speak("Opening Instagram\n")
            webbrowser.open("instagram.com")
            
        elif 'open whatsapp' in command:
            speak("Opening WhatsApp\n")
            webbrowser.open("web.whatsapp.com")
            
        elif 'open twitter' in command:
            speak("Opening Twitter\n")
            webbrowser.open("twitter.com")

        elif 'play music' in command:
            playMusic()

        elif 'joke' in command or 'tell me a joke' in command or 'jarvis tell me a joke' in command:
            speak(pyjokes.get_joke())
            print("Enjoy the joke: " +pyjokes.get_joke())

        elif "will you be my gf" in command or "will you be my bf" in command:
            speak("I'm not sure about that, maybe you should give me some time")

        elif "i love you" in command:
            speak("Thank you! But, it's a pleasure to hear it from you.")

        elif "weather" in command:
            speak("Please tell your city name")
            print("City name: ")
            cityName = takeCommand()
            getWeather(cityName)

        elif "what is" in command or "who is" in command:
            speak("Searching the Internet...")
            query = command
            query = query.replace("what is", "")
            query = query.replace("who is", "")
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            time.sleep(10)
        
        elif "news" in command:
            speak("Please wait, I am fetching the latest news headlines")
            getNews()

        elif "lock window" in command or "lock the window" in command:
            speak("Locking the device")
            ctypes.windll.user32.LockWorkStation()

        elif "shutdown the system" in command or "shutdown" in command:
            speak("Hold on a sec! Your system is on its way to shut down")
            subprocess.call('shutdown /p /f')

        elif "empty recycle bin" in command:
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
            speak("Recycle Bin emptied")

        elif "don't listen" in command or "stop listening" in command:
            speak("For how much time do you want to stop Jarvis from listening to commands?")
            a = int(takeCommand())
            time.sleep(a)
            print(a)

        elif "camera" in command or "take a photo" in command:
            capture_photo('img.jpg')

        elif "restart" in command:
            subprocess.call(["shutdown", "/r"])

        elif "hibernate" in command or "sleep" in command:
            speak("Hibernating")
            subprocess.call("shutdown /h")

        elif "log off" in command or "sign out" in command:
            speak("Make sure all the applications are closed before sign-out")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])

        elif "write a note" in command:
            speak("What should I write, sir?")
            note = takeCommand()
            with open('jarvis.txt', 'w') as file:
                speak("Sir, should I include date and time?")
                ans = takeCommand()
                if 'yes' in ans or 'sure' in ans:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    file.write(strTime)
                    file.write(" :- ")
                    file.write(note)
                else:
                    file.write(note)

        elif "show note" in command:
            speak("Showing Notes")
            with open("jarvis.txt", "r") as file:
                content = file.read()
                print(content)
                speak(content)

        elif 'open calculator' in command:
            open_calculator()
            
        elif 'exit' in command:
            speak("Thanks for giving me your time!")
            break

if __name__ == '__main__':
    app = Tk()
    app.geometry('500x250')
    app.configure(bg='black')
    app.title('JARVIS')

    showCommand = StringVar()
    label = Label(app, textvariable=showCommand, bg='black', fg='white', font=('Arial', 14), wraplength=450)
    label.pack(pady=20)

    btn = Button(app, text="Run JARVIS", bg='red', fg='white', font=('Arial', 12, 'bold'), command=callVoiceAssistant)
    btn.pack(pady=20)

    app.mainloop()
