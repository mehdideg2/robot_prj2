import pygame
from gtts import gTTS
import speech_recognition as sr
import datetime
import time
import nltk
import threading
import random

LANG = 'fr'
DIR = "./assets/sounds/"
nltk.download('words')
nltk.download('maxent_ne_chunker')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')


GREETING_KEYWORDS = ("hello", "salut", "vas-tu", "ça va", "ça se passe",)
GREETING_RESPONSES = ["'super mec", "mouai", "ça va, merci!", "Parfait"]

def check_for_greeting(sentence):
    for word in sentence.words:
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETING_RESPONSES)

def listen():
    while 1:
        r = sr.Recognizer()
        try:
            sr.Microphone()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("say something")
                audio = r.listen(source)
            if audio != None:
                recog = r.recognize_google(audio, language=LANG)
                print(recog)
                person_name = get_name(recog)
                play_sounds_with_gtts("Salut, " + str(person_name))

        except Exception as err:
            time.sleep(1)
            print(err)

def play_sounds_with_gtts(m_text):
    current_time = datetime.datetime.now().time()
    tts = gTTS(text=m_text, lang=LANG)
    sound_file_name = (DIR + str(current_time).replace(':', '').replace('.', ''))
    tts.save(sound_file_name)
    pygame.mixer.music.load(sound_file_name)
    pygame.mixer.music.play()

def get_name(sentence):
    for sent in nltk.sent_tokenize(sentence):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                if chunk.label() == "PERSON":
                    name = ' '.join(c[0] for c in chunk)
                    return name

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((750, 750))
    pygame.display.set_caption('Basic Pygame program')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # set image
    robot_face = pygame.image.load("./assets/images/{}".format("v-10-512.png"))
    robot_face = pygame.transform.scale(robot_face, (750, 750))
    screen.blit(robot_face, (0, 0))

    # say hello
    hello_text = "Bonjour, je m'appelle Mehdi, et vous ?"
    play_sounds_with_gtts(hello_text)

    # Listen thread
    listen_thread = threading.Thread(target=listen)
    listen_thread.start()

    # Event loop
    while 1:
        time.sleep(0.1)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


if __name__ == '__main__':
    main()
