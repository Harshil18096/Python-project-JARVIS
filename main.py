import speech_recognition as sr     #speechrecognition                            
import os
import win32com.client              #pywin32
import datetime
import pywhatkit
import openai
from config import apikey

chatStr = ""
def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"Harshil: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print("\nJARVIS :",response["choices"][0]["text"])
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

    print(text)
    print("\n=========================================\n\n")

def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        audio = r.listen(source)
        try:
            print("Recognizing...")
            #query = r.recognize_google(audio, language="en-in")
            query = r.recognize_google(audio, language="hindi-in")
            print(f"\nYOU : {query}")
            return query
        except Exception as e:
            say("Some Error Occurred,Sorry from Jarvis")
            #return "Some Error Occurred. Sorry from Jarvis"
        
def writemode():
    query = input("\nyou :")
    return query

def keyboardInput():
    print("Enter a prompt (type 'exit' to quit):")
    while True:
        query = input("You: ")
        if query.lower() == 'exit':
            break
        ai(query)

if __name__ == '__main__':
    print("Hello I am JARVIS A. I.")
    say("hello i am jarvis A. I...")
    while True:
        print("\nListening...")
        query = takeCommand()

        # if "Switch to writing mode".lower() in query.lower():
        #     say("Switched to writing Mode!")

        #     while 1:
        #         query = writemode()

        #         if "stop".lower() in query.lower():
        #             say("GOODBYE...")
        #             exit()
        #         else:
        #             continue

        if "play" in query:
            song = query.replace('play', '')
            say("Playing " + song)
            x = pywhatkit.playonyt(song)
            exit()

        elif "open" in query:
            web = query.replace('open', '')
            say("Opening " + web + "in browser")
            pywhatkit.search(web)
            exit()

        elif "the time" in query:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"The time is {time}")
            say(f"The time is {time}")

        elif 'the date' in query:
            date = datetime.datetime.now().strftime('%d/%m/%Y')
            print(f"The time is {date}")
            say(f"The date is {date}")

        # elif "open vs".lower() in query.lower():
        #     os.system(f"open \kathr\AppData\Local\Programs\Microsoft VS Code\Code.exe")

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "stop".lower() in query.lower():
            say("GOODBYE...")
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""
            say("NOW CHAT IS CLEAR...")

        elif "write mode" in query.lower():
            keyboardInput()

        else:
            print("Chatting...")
            chat(query)

