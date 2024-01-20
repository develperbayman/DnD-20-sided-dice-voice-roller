import threading
import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import random
import time  # Import the time module

# Initialize pygame for sound playback
pygame.init()

recognizer = sr.Recognizer()

chatbot_busy = False

def play_activation_sound():
    try:
        # Replace 'path_to_activation_sound.mp3' with the actual path to your sound file
        sound = pygame.mixer.Sound('./computer.wav')
        sound.play()
    except pygame.error as e:
        print(f"Error playing activation sound: {e}")

def roll_dice():
    return random.randint(1, 20)

def announce_result(result):
    response = f"The roll is {result}."
    
    if result == 20:
        response += " Critical hit!"
    elif result == 1:
        response += " miss!"
    
    print("Chatbot:", response)
    text_to_speech(response, lang='en', gender='female')

def text_to_speech(text, lang='en', gender='female'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save('output.mp3')
        pygame.mixer.music.load('output.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        # Wait for the sound to finish playing before deleting the temporary file
        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(30)

        # Delete the temporary file after playback
        os.remove('output.mp3')
    except Exception as e:
        print(f"Error during text-to-speech: {e}")

def listen_for_input():
    global chatbot_busy
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)

        while True:
            try:
                print("Listening...")
                audio_data = recognizer.listen(source)
                user_input = recognizer.recognize_google(audio_data).lower()
                print("User:", user_input)

                if 'computer roll dice' in user_input and not chatbot_busy:
                    print("Dice roller activated. Rolling the dice.")
                    play_activation_sound()

                    # Introduce a delay of 1.5 seconds
                    time.sleep(1.5)

                    result = roll_dice()
                    announce_result(result)

            except sr.UnknownValueError:
                print("Could not understand audio. Please try again.")
            except Exception as e:
                print(f"An error occurred: {e}")

def main():
    try:
        input_thread = threading.Thread(target=listen_for_input)
        input_thread.start()
    except Exception as e:
        print(f"Error starting input thread: {e}")

if __name__ == "__main__":
    main()

