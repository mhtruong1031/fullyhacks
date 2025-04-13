from openai import OpenAI
from elevenlabs.client import ElevenLabs

import speech_recognition as sr
import json

# Custom modules
import add_ons, threading

DEFAULT_MODEL = "gpt-3.5-turbo"
WAKE_WORD = "jarvis"
EXIT_WORD = "thank you"

class NovaNotes:
    def __init__(self, gpt_api_key: str, el_api_key: str, text_mode: bool = False, max_tokens: int = 40, default_model:str = DEFAULT_MODEL) -> None:
        # NovaNotes variables
        self.text_mode = text_mode
        self.activated = False # GPT-mode

        # GPT Configurables
        self.api_key       = gpt_api_key
        self.default_model = default_model
        self.max_tokens    = max_tokens

        self.client = OpenAI(api_key=self.api_key)

        # Voice engine

        

        # Initialize session memory
        self.messages = []
        self.messages.append({"role": "system", "content": self.memory})

    def __listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"YOU: {command}")
            return command
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""
        
    def speak(self, text):
        print(f"NovaNotes: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def ask_gpt(self, prompt):
        self.messages.append({"role": "user", "content": prompt})

        try:
            chat = self.client.chat.completions.create(
                model      = self.default_model,
                messages   = self.messages,
                max_tokens = self.max_tokens
            )
            return chat.choices[0].message.content.strip()
        except Exception as e:
            print(f"API Error: {e}")
            return "Sorry, something went wrong when talking to OpenAI."
        
    def ask_gpt_with_image(self, prompt: str, image_path: str):
        messages = [{"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{add_ons.encode_image(image_path)}"}
                    }
        ]}]


        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            max_tokens=50
        )
        return response.choices[0].message.content.strip()
    
    # Activates GPT responses
    def __activate_gpt(self):
        self.activated = True

    def __deactivate_gpt(self):
        self.activated = False
    
    # Main runtime function of NovaNotes
    def run_jarvis(self):
        self.speak("NovaNotes is online and listening.")
        
        while True:
            # Grab user command
            if self.text_mode:
                command = input("You: ").lower()
            else:
                command = self.__listen().lower()

            # Check to power off NovaNotes
            if "power off" in command:
                self.speak("Shutting down. Until next time.")
                break

            if command.startswith("jarvis"):
                j_command = command[7:]
            else:
                j_command = command
            
            # || SPECIAL FUNCTIONS ||

            


            # || ------------------------------ ||

            # GPT Activation and Deactivation
            if self.activated and EXIT_WORD in command:
                self.speak("You're welcome, sir. Sleeping now.")
                self.__deactivate_gpt()
                continue
            
            if command.startswith(f"hey {WAKE_WORD}"): 
                self.__activate_gpt()
            
            # GPT Response if activated
            if self.activated and command.strip() != "":
                response = self.ask_gpt(command)
                self.speak(response)
                continue
            