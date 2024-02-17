import speech_recognition as sr
import pyttsx3 as py
from googletrans import Translator
import datetime
import requests  
import openai
import os  
import webbrowser  
import pywhatkit 
import pyautogui 
import time  
import psutil
import cv2
from PIL import Image

# Code Written by Shivam Attri

# Initialize the Speech Recognition
r = sr.Recognizer()

Username = input("Name : ")
Botname = "Shivam"

engine = py.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def say(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10)

    try:
        print('Recognizing...')
        say("Recognizing...")

        command = r.recognize_google(audio).lower()
        print(f"{Username}: {command}")
        
        # Translate the recognized command from Hindi to English
        command_english = Translate(command)
        
    except sr.UnknownValueError:
        return ""

    return command_english                              # Code Written by Shivam Attri

# Translation Function
def Translate(command):
    print("Translating from Hindi to English")
    line = str(command)
    translate = Translator()
    result = translate.translate(line)
    Translation = result.text
    print(f"{Username}: {Translation}")
    return Translation

# Connect (To connect Translator and speak function)
def Connector():
    query = listen()
    My_Command_In_English = Translate(query)
    return My_Command_In_English

# Define intent recognition
def recognize_intent(command):
    intent = None

    intents = {
        "weather_intent": ["weather", "forecast", "temperature"],
        "time_intent": ["time", "current time", "clock"],
        "news_intent": ["news", "headlines"],
        "music_intent": ["music", "play music"],
        "search_intent": ["search", "find", "look up"],
        "calculator_intent": ["calculate", "math", "mathematics"],
        "open_app_intent": ["open", "launch", "start"],
        "close_app_intent": ["close", "quit", "exit"],
        "volume_intent": ["volume", "sound", "loudness"],
        "system_control_intent": ["shutdown", "restart", "mute"],
        "reminder_intent": ["remind", "reminder", "note"],
        "translate_intent": ["translate", "language"],
        "help_intent": ["help", "assist", "guide"],
        "camera_intent": ["take a pic", "take a photo", "click a photo", "click a photo", "take my pic", "take my photo"]
        # Add more intents and keywords as needed
        # Code Written by Shivam Attri
    }

    for intent_name, keywords in intents.items():
        for keyword in keywords:
            if keyword in command:
                intent = intent_name
                break

    return intent

# Function to greet the user
def greet_user():
    current_time = datetime.datetime.now()
    if current_time.hour < 12:
        return "Good morning! "+ {Username}
    elif 12 <= current_time.hour < 17:
        return "Good afternoon! Sir" + {Username}
    elif 17 <= current_time.hour < 20:
        return "Good evening! Sir" + {Username}
    else:
        return " "

# Function To Calculate Mathematical Expression
def Calculate(expression):
    try:
        result = eval(expression)
        print(result)

    except Exception as e:
        print("Please write the expression again")

OPENWEATHER_API_ID = ""                     # Code Written by Shivam Attri

# Function to get weather report
def get_weather_report(city):
    try:
        # Make sure to handle potential errors in the API request
        res = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_ID}&units=metric"
        )
        res.raise_for_status()  # Raise an HTTPError for bad responses
        data = res.json()

        weather = data["weather"][0]["main"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]

        return weather, f"{temperature}℃", f"{feels_like}℃"
    except requests.RequestException as e:
        # Handle any request exceptions (e.g., network issues, API errors)
        print(f"Error during API request: {e}")
        return None

openai.api_key = ""      # Code Written by Shivam Attri

# Function to answer question using Openai
def QuestionsAnswer(question):
    prompt = f'{Username} : {question}\n{Botname} : '
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    if completion.choices[0].message != None:
        # Extract the response content from the completion result
        response_content = completion.choices[0].message.get('content', None)
        if response_content is not None:
            return response_content
    return 'Failed to generate response!'

# To Close Application
def close_specific_app(app_name):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if app_name.lower() in proc.info['name'].lower():
            try:
                process = psutil.Process(proc.info['pid'])
                process.terminate()
                say(f"Closing {app_name}.")
                return True
            except Exception as e:
                say(f"Failed to close {app_name}.")
                return False
    say(f"{app_name} is not currently running.")
    return False                                                            # Code Written by Shivam Attri

# Take Picture
def capture_photo_and_open():
    # Define the directory where you want to save the captured photo
    save_directory = "Pictures"  # Replace with the actual directory path

    # Check if the directory exists; if not, create it
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Initialize the camera
    camera = cv2.VideoCapture(0)  # 0 represents the default camera (usually the webcam)

    # Check if the camera is opened successfully
    if not camera.isOpened():
        print("Error: Could not open camera.")
        return

    try:
        # Capture a frame from the camera
        ret, frame = camera.read()

        if not ret:
            print("Error: Could not capture a frame.")
            return

        # Generate a unique filename for the captured photo (e.g., using a timestamp)
        timestamp = time.strftime("%Y%m%d%H%M%S")
        photo_filename = os.path.join(save_directory, f"captured_photo_{timestamp}.jpg")

        # Save the captured frame as an image file
        cv2.imwrite(photo_filename, frame)
        print(f"Photo captured and saved as '{photo_filename}'.")

        # Open the captured photo using Pillow
        image = Image.open(photo_filename)
        image.show()

    finally:
        # Release the camera
        camera.release()

if __name__ == "__main__":

    while True:
        say(greet_user())
        say("I am Shivam. Your personal AI voice assistant")
        say("How can I assist you today")

        # Your main code loop
        while True:
            
            command = listen()
            intent = recognize_intent(command)

        # To tell Weather Report
            if intent == "weather_intent":
                try:
                    # Handle weather-related commands
                    print("You want to know the weather. I'll find that for you.")
                    city = input("Enter the city name: ")  # Use input() instead of listen() for simplicity
                    print(f"Getting weather report for your city {city}")
                    
                    weather_info = get_weather_report(city)

                    if weather_info:
                        weather, temperature, feels_like = weather_info
                        print(f"The current temperature is {temperature}, but it feels like {feels_like}")
                        print(f"Also, the weather report talks about {weather}")
                        print("For your convenience, I am printing it on the screen, sir.")
                        print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")
                    else:
                        print("Failed to retrieve weather information.")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

        # To tell Time
            elif intent == "time_intent":
                # Handle time-related commands
                say("You're interested in the current time. Let me check.")
                strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                say(f"Sir, the time is {strfTime}")

        # To tell News
            elif intent == "news_intent":
                say("You want to know the latest news. Let me fetch that for you.")
                search_url = f"https://www.google.com/search?rlz=1C1YTUH_en-GBIN1081IN1081&oq=google+conv&gs_lcrp=EgZjaHJvbWUqBwgEEAAYgAQyBggAEEUYOTINCAEQABiDARixAxiABDIMCAIQABgUGIcCGIAEMgcIAxAAGIAEMgcIBBAAGIAEMgcIBRAAGIAEMgcIBhAAGIAEMgcIBxAAGIAEMgcICBAAGIAEMgcICRAAGIAE0gEIOTk0OWowajeoAgCwAgA&sourceid=chrome&ie=UTF-8&cs=0&csui=1&gsas=1&csuio=6&csuip=15&q=India%27s+top+10+news+in+English&mstk=AUzJOivMg2Vop2zlYweepzttTiRoK5djU-QPvjds8M9Jaf3wQ1efvQqtoV4POmaZjOCAfmwa3l7o9FrAcEauY4vvbbecOre33BJwFFpMS60l1zBwfpUUEqs6hUZfltrpTpDXKTrmJg4-kHcmbMwx7kpXfC8Be_yiQXd85D1g0VEtzbdq-NDLh1kuyLAeh8-oWJGpQUUVzUmL6drIwGszxTju1bkCi5OFSDcn8QQutrV2F29btKtwGDOlAQKAY5bzL9KU&csuir=1"
                webbrowser.open(search_url)

        # To play Music
            elif intent == "music_intent":
                search_music = command.replace("music_intent", "").strip()
                os.startfile("E:\My Files\Applications\Google Chrome")
                music_query = search_music
                pywhatkit.playonyt(music_query)

        # To take Picture
            elif intent == "camera_intent":
                say("Capturing a photo...")
                capture_photo_and_open()
                say("Photo captured and saved.")

        # To Search on Google
            elif intent == "search_intent":
                search_query = command.replace("search_intent", "").strip()
                search_url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(search_url)
                response = "I've opened a Google search for you."

        # To Calculate Something
            elif intent == "calculator_intent":
                # Handle calculator-related commands
                say("What math expression would you like me to calculate?")
                math_expression = listen()
                Calculate(math_expression)

        # To Open Any Application
            elif intent == "open_app_intent":
                # Handle app opening commands
                if "whatsapp" in command:
                    say("Opening WhatsApp.")
                    os.start("E:\\Applications\\WhatsApp")  # Update the file location
                elif "chrome".lower() in command.lower():
                    say("opening chrome")
                    os.startfile("E:\\Applications\\Google Chrome") # Update the file location
                elif "setting".lower() in command.lower():
                    say("opening setting")
                    os.startfile("E:\\Applications\\Settings") # Update the file location
                elif "control Panel".lower() in command.lower():
                    say("opening Control Panel")
                    os.startfile("E:\\Applications\\Control Panel") # Update the file location
                elif "command prompt".lower() in command.lower():
                    say("opening Command Prompt")
                    os.startfile("E:\\Applications\\Command Prompt") # Update the file location
                elif "file explorer".lower() in command.lower():
                    say("opening File Explorer")
                    os.startfile("E:\\Applications\\File Explorer") # Update the file location
                elif "file manager".lower() in command.lower():
                    say("opening file manager")
                    os.startfile("E:\\Applications\\computer") # Update the file location

        # To Close Any Application
            elif intent == "close_app_intent":
                # Handle app closing commands
                if "chrome" in command:
                    if close_specific_app("Chrome.exe"):
                        say("Closing Google Chrome.")
                        pyautogui.hotkey('alt', 'f4')
                elif "setting" in command:
                    if close_specific_app("ImmersiveControlPanel.exe"):
                        say("Closing Setting.")
                        pyautogui.hotkey('alt', 'f4')
                elif "control panel" in command:
                    if close_specific_app("control.exe"):
                        say("Closing Control Panel")
                        pyautogui.hotkey('alt', 'f4')

        # To Increase or Decrease Volume 
            elif intent == "volume_intent":
                # Handle volume control commands
                if "volume up" in command:
                    for _ in range(15):
                        pyautogui.press("volumeup")
                elif "volume down" in command:
                    for _ in range(15):
                        pyautogui.press("volumedown")
                elif "mute" in command:
                    pyautogui.press("volumemute")

        # To Shut Down Or Restart System
            elif intent == "system_control_intent":
                # Handle system control commands
                if "shutdown" in command:
                    os.system("shutdown /s /t 5")
                elif "restart" in command:
                    os.system("shutdown /r /t 5")
                elif "refresh" in command:
                    pyautogui.hotkey('f5')

        # To Stop Shivam for some time
            elif "pause" in command.lower() or "sleep" in command.lower() or "rest" in command.lower():
                # Handle pausing Jarvis
                say("For how much time would you like me to pause? (Specify the number of minutes)")
                try:
                    minutes = int(input("Enter time in minutes (Only Number): "))  # Corrected the missing closing parenthesis
                    seconds = minutes * 60
                    say(f"Jarvis will be paused for {minutes} minutes.")
                    time.sleep(seconds)
                    say("I'm back! How can I assist you?")
                    
                except ValueError:
                    say("Invalid input. Please enter a valid number of minutes.")

        # To Stop Shivam Permanantly
            elif any(keyword in command.lower() for keyword in ["goodbye", "good bye", "exit"]):
                # Handle exit commands
                say("Goodbye Sir")
                print(f"{Botname}: Goodbye, Sir")
                break

        # To Maximize this Window
            elif 'maximize this window' in command.lower():
                pyautogui.hotkey('win', 'up')

        # To Minimize the window
            elif 'minimize this window' in command.lower():
                pyautogui.hotkey('win', 'down')

        # To Open New Window
            elif 'open new window' in command.lower():
                pyautogui.hotkey('ctrl', 'n')

        # To Open Incognito Window
            elif 'open incognito window' in command.lower():
                pyautogui.hotkey('ctrl', 'shift', 'n')

        # To Open History Of Chrome
            elif 'open history' in command.lower():
                pyautogui.hotkey('ctrl', 'h')

        # To Open Download History
            elif 'open downloads' in command.lower():
                pyautogui.hotkey('ctrl', 'j')

        # To Clear Browsing History
            elif 'clear browsing history' in command.lower():
                pyautogui.hotkey('ctrl', 'shift', 'delete')

        # To Open Previous tab
            elif 'previous tab' in command.lower():
                pyautogui.hotkey('ctrl', 'shift', 'tab')

        # To Open Next Tab
            elif 'next tab' in command.lower():
                pyautogui.hotkey('ctrl', 'tab')
                
        # To reload the site
            elif "reload" in command.lower():
                pyautogui.hotkey('ctrl', 'r')
                
        # To pause youtube video
            elif "pause" in command.lower() :
                pyautogui.hotkey('k')
                if "resume" in command.lower():
                    pyautogui.hotkey('k')

        # To Thank Shivam
            elif "thank you" in command.lower() or "thanks" in command.lower():
                say("Welcome Sir")

        # To check the Battery Status
            elif "system status" in command:
                battery = psutil.sensors_battery()
                percent = battery.percent
                if percent > 70 :
                    say("Battery is sufficeint. Ready to perform any task")
                elif 50 < percent < 70 :
                    say("Needs Charging But not right now")
                else :
                    say("Urgently need Charging")

        # To answer general question
            else:
                # Handle general queries using OpenAI
                reply = QuestionsAnswer(command)
                print(f"{Botname}: {reply}")
                say(reply)

    # End of your code
    # Code Written by Shivam Attri
