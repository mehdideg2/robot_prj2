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
# nltk.download('words')
# nltk.download('maxent_ne_chunker')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')


# GREETING_KEYWORDS = ("hello", "salut", "vas-tu", "ça va", "ça se passe",)
# GREETING_RESPONSES = ["'super mec", "mouai", "ça va, merci!", "Parfait"]

liste_questions = ["Avez-vous aimé votre déjeuner?", "Le service était-il rapide?", "La quantité était-elle suffisante?"]
liste_de_mots_clefs_pos = ["bien", "bon", "parfait", "impeccable", "super"]
liste_de_mots_clefs_neg = ["mal", "terrible", "dégueulasse", "infecte"]
negation = "pas"

Jauge = compteur = 0
last_val = 0

# def check_for_greeting(sentence):
#     for word in sentence.words:
#         if word.lower() in GREETING_KEYWORDS:
#             return random.choice(GREETING_RESPONSES)


def listen():
    while 1:
        #timeout = time.time() + 10

        #if time.time() > timeout: #si pas de réponse de l'utilisateur en 10 secondes, le robot se reset
        #break
        r = sr.Recognizer()
        try:
            sr.Microphone()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Parlez maintenant")
                audio = r.listen(source)
            if audio != None:
                recog = r.recognize_google(audio, language=LANG)
                print(recog)
                return recog

                #person_name = get_name(recog)
                #play_sounds_with_gtts("Salut, " + str(person_name))

        except Exception as err:
            time.sleep(1)
            print(err)

def play_sounds_with_gtts(m_text):
    current_time = datetime.datetime.now().time()
    tts = gTTS(text=m_text, lang=LANG)
    sound_file_name = (DIR + str(current_time).replace(':', '').replace('.', '')) #générer le nom du fichier son par rapport à la date&heure
    tts.save(sound_file_name)
    pygame.mixer.music.load(sound_file_name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def get_name(sentence):
    for sent in nltk.sent_tokenize(sentence):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                if chunk.label() == "PERSON":
                    name = ' '.join(c[0] for c in chunk)
                    return name

def welcome_message():
    hello_text = "Bonjour, appuyez sur une touche pour commencer"
    play_sounds_with_gtts(hello_text)

def goodbye_message():
    bye_text = "Merci d'avoir répondu. Au revoir"
    play_sounds_with_gtts(bye_text)

def find_connotation():  #utiliser variable globale pour last_val. vérif si globlale
    enreg = listen()
    compteur = val = val_inter = 0
    while compteur < len(liste_de_mots_clefs_pos):
        if enreg.find(liste_de_mots_clefs_pos[compteur]) > 0:
            val = val + 1
            if enreg.find(negation) > 0:
                val = -1 * val
            val_inter = val_inter + val
        compteur = compteur + 1
    compteur = 0
    while compteur < len(liste_de_mots_clefs_neg):
        if enreg.find(liste_de_mots_clefs_neg[compteur]) > 0:
            val = val - 1
        compteur = compteur + 1
        last_val = val
    # print("Connotation = ", last_val)
    return last_val

def main():
    global last_val

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

    welcome_message()

    # Listen thread
    # listen_thread = threading.Thread(target=listen)
    # listen_thread.start()

    #find_connotation_thread = threading.Thread(target=find_connotation) #Créer un thread pour la fonction find_conno
    #find_connotation_thread.start()

    # Event loop

    while 1:
        time.sleep(0.1)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                print("Question...")
                poser_les_questions()
                print("Connotation = ", last_val)
                goodbye_message()

def poser_les_questions():

    for question in liste_questions:
        play_sounds_with_gtts(question)
        time.sleep(1)
        find_connotation()



if __name__ == '__main__':
    main()

"""
Le programme de détection de voix ne capte généralement pas le premier mot prononcé
La jauge de connotation ne calcule pas correctement
"""