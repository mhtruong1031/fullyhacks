from openai import OpenAI
from elevenlabs.client import ElevenLabs

import speech_recognition as sr
from playsound import playsound

# Custom modules
import add_ons

DEFAULT_MODEL = "gpt-4o"
WAKE_WORD = "nova"
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
        self.elevenlabs_client = ElevenLabs(api_key=el_api_key)

        # Initialize session memory
        self.messages = []

    def __listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            langs = ["en-US", "vi-VN"]
            for lang in langs:
                try:
                    command = recognizer.recognize_google(audio, language=lang)
                    print(f"Detected language ({lang}): {command}")
                    break
                except sr.UnknownValueError:
                    continue
            return command
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""
        
    def speak(self, text):
        audio = self.elevenlabs_client.text_to_speech.convert(
                text          = text,
                voice_id      = add_ons.voice_ids['ChaewonLeSserafim'],
                model_id      = "eleven_multilingual_v2",
                output_format = "mp3_44100_128",
        )
        file_path = add_ons.save_as_audio_file(audio, f"temp.mp3")
        playsound(file_path)
    
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
    def run_novanote(self):
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

            if command.startswith(WAKE_WORD):
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
            