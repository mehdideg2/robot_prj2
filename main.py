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
liste_de_mots_clefs_pos = ["bien", "bon", "parfait", "impeccable", "super", "suffisant", "rapide"]
liste_de_mots_clefs_neg = ["mal", "terrible", "dégueulasse", "infecte", "lent", "long"]
negation = "pas"
assurance = "très"
Jauge = compteur = last_val = connotation_finale = connotation_totale = 0


def listen():
    while 1:

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

def welcome_message():
    hello_text = "Bonjour ! Appuyez sur une touche pour commencer"
    play_sounds_with_gtts(hello_text)

def goodbye_message():
    bye_text = "Merci d'avoir répondu. Au revoir!"
    play_sounds_with_gtts(bye_text)

def find_connotation():
    enreg = listen()
    # enreg = "C'était très bon" #pour simuler des tests rapidement
    compteur = val = val_inter = 0
    while compteur < len(liste_de_mots_clefs_pos): #Parcourir tous les mots-clé
        if enreg.find(liste_de_mots_clefs_pos[compteur]) > 0: #Si le mot-clé est trouvé dans la phrase
            debut_mot_cle_pos = enreg.find(liste_de_mots_clefs_pos[compteur])
            val = val + 1
            if enreg.find(negation, debut_mot_cle_pos-5, debut_mot_cle_pos) > 0: #Si le mot "pas" est trouvé juste avant le mot-clé
                val = -1 * val #On inverse le résultat obtenu (si positif --> négatif, et vice versa)
            if enreg.find(assurance, debut_mot_cle_pos-5, debut_mot_cle_pos) > 0:  # Si le mot "très", "trop" est trouvé
                val = 2 * val #On accentue le score dans le cas où l'utilisateur utilise "très" ou "trop"
            val_inter = val_inter + val
        compteur = compteur + 1 #On passe au mot-clé suivant
    compteur = 0
    while compteur < len(liste_de_mots_clefs_neg):
        if enreg.find(liste_de_mots_clefs_neg[compteur]) > 0:
            val = val - 1
        compteur = compteur + 1
        last_val = val
    print("Connotation = ", last_val)
    return last_val

def init_interface():
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

def poser_les_questions():
    global connotation_totale
    for question in liste_questions:
        play_sounds_with_gtts(question)
        time.sleep(1)
        connotation_finale = find_connotation()
        connotation_totale = connotation_totale + connotation_finale
    return connotation_totale

def main():
    # global connotation_finale
    init_interface()
    welcome_message()
    while 1:
        time.sleep(0.1)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                print("Question...")
                poser_les_questions()
                print("Connotation totale = ", connotation_totale)
                goodbye_message()

if __name__ == '__main__':
    main()

"""
Le programme de détection de voix ne capte généralement pas le premier mot prononcé -- Le programme ne reconnait pas bien les mots (problème micro?)
La jauge de connotation ne calcule pas correctement -- Calcul faux (quelques mots clés oubliés?)
"""