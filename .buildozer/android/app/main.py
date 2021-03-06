from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from pydub.playback import play
from pydub import AudioSegment
#https://docs.python.org/2/library/threading.html info about threading
from threading import Thread
import sys
from kivy.lang import Builder
import sr
from random import randint
# Load kv file
Builder.load_file('simon.kv')

class MainMenu(Screen):
    pass
class LevelMenu(Screen):
    pass
class DifficultyMenu(Screen):
    pass
class CreditsMenu(Screen):
    pass
class GameMenu(Screen):
    pass
class TutorialMenu(Screen):
    pass
# Create a screen manager - docs reference https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html
# Need to add voice commands for each red_button - we can do this by returning value from sr script and have conditional statements
sm = ScreenManager()
sm.add_widget(MainMenu(name='mainmenu'))
sm.add_widget(GameMenu(name='game'))
sm.add_widget(DifficultyMenu(name='difficulty'))
sm.add_widget(CreditsMenu(name='credits'))
sm.add_widget(TutorialMenu(name='tutorial'))
def animate(widget,color):
    #ref for tutorial: https://youtu.be/qMKPNqbuR5Y
    anim = Animation(background_color = (255,255,255,1),duration = 1)
    anim += Animation(background_color=color,duration=1)
    anim += Animation(background_color=widget.color,duration=0.3)
    anim.start(widget)
def Board(pattern):
     i = 0
     # make buttons flash using animate function - note to self get rid of prints
     for i in range(0,len(pattern)):
        if(pattern[i] == 1):
            widget = GameMenu()
            button_red = widget.ids.red
            animate(button_red,button_red.background_color)
            sound = AudioSegment.from_mp3('red.mp3')
            play(sound)
        elif(pattern[i] == 2):
            sound = AudioSegment.from_mp3('blue.mp3')
            play(sound)
        elif(pattern[i] == 3):
            sound = AudioSegment.from_mp3('yellow.mp3')
            play(sound)
        elif(pattern[i] == 4):
            sound = AudioSegment.from_mp3('green.mp3')
            play(sound)
        else:
            print("HOW JUST HOW YOU BROKE THE GAME HOPE YOU'RE PROUD HAHAHAA ")

def GameLogic(lives):
    #generate pattern here use array
    #only break if the pattern is wrong
    #this variable will be used to compare array index to guess
    arrIndex = 0;
    # need to append to pattern in loop if user guesses correct
    pattern = [1,2,3,4]
    global guess
    #flash user ;)
    board = Thread(target=Board,args=[pattern])
    board.setDaemon(True)
    board.start()
    while(1):
        voiceCommand = sr.voice_input()
        while(not voiceCommand):
                voiceCommand = sr.voice_input()
        if("red" in voiceCommand.lower()):

            sound = AudioSegment.from_mp3('red.mp3')
            play(sound)
            guess = 1
        elif("blue" in voiceCommand.lower()):
            sound = AudioSegment.from_mp3('blue.mp3')
            play(sound)
            guess = 2
        elif("yellow" in voiceCommand.lower()):
            sound = AudioSegment.from_mp3('yellow.mp3')
            play(sound)
            guess = 3
        elif("green" in voiceCommand.lower()):
            sound = AudioSegment.from_mp3('green.mp3')
            play(sound)
            guess = 4
        elif("quit" in voiceCommand.lower() or "exit" in voiceCommand.lower() or "close" in voiceCommand.lower()):
            sm.current="mainmenu"
            #restart thread
            main = Thread(target=Main)
            main.setDaemon(True)
            main.start()
            break
        else:
            print("Could not understand command - valid commands are red,green,blue & yellow")
            continue
        if(guess == pattern[arrIndex] and guess != "" and arrIndex != len(pattern)):
            arrIndex += 1
        elif(guess != pattern[arrIndex] and guess != ""):
            lives = lives - 1
            sound = AudioSegment.from_mp3('fail.mp3')
            play(sound)
            print("lives",lives)
            arrIndex = 0
            if(lives <= 0):
                print("BREAKING ", pattern[arrIndex], "  GUESS " , guess)
                print("HAHA FAILURE, YOU FAILED HAHAHAHHAHAHHAHHAHAHHAHAHAH NOOB")
                sm.current = "mainmenu"
                main = Thread(target=Main)
                main.setDaemon(True)
                main.start()
                break
            continue
        if(arrIndex == len(pattern)):
            #will generate random number and add to pattern
            random = randint(1,4)
            pattern.append(random)
            arrIndex = 0
            board = Thread(target=Board,args=[pattern])
            board.setDaemon(True)
            board.start()
    print("Ending game logic")
# may add screen to ask user if they want to use voice commands
def Main():
    # can perform game events in here such as switching windows and game commands
    # infinite loop for voice commands may be issue
    while(1):
        voiceCommand = sr.voice_input()
        while(not voiceCommand):
            voiceCommand = sr.voice_input()
        #include options for switching game menus in here may separate into functions
        if("quit" in voiceCommand.lower() or "exit" in voiceCommand.lower() or "close" in voiceCommand.lower()):
            print("IN HERE")
            break
        elif("play" in voiceCommand.lower() or "start" in voiceCommand.lower() or "game" in voiceCommand.lower()):
            sm.current = 'game'
            #make medium default difficulty
            game = Thread(target = GameLogic,args=[2])
            game.setDaemon(True)
            game.start()
            break
        elif("developers" in voiceCommand.lower() or "credits" in voiceCommand.lower()):
            sm.current = 'credits'
        elif('back' in voiceCommand.lower() or 'main menu' in voiceCommand.lower()):
            sm.current =  'mainmenu'
        elif('level' in voiceCommand.lower() or 'change' in voiceCommand.lower() or 'difficulty' in voiceCommand):
            sm.current =  'difficulty'
        if("easy" in voiceCommand.lower() and sm.current == 'difficulty'):
            sm.current = 'game'
            #need to find way to stop threads
            game = Thread(target = GameLogic,args=[3])
            game.setDaemon(True)
            game.start()
            break
        elif("medium" in voiceCommand.lower() and sm.current ==  'difficulty'):
            sm.current = 'game'
            game = Thread(target = GameLogic,args=[2])
            game.setDaemon(True)
            game.start()
            break
        elif("hard" in voiceCommand.lower() and sm.current=='difficulty'):
            sm.current = 'game'
            #need to find way to stop threads
            game = Thread(target = GameLogic,args=[1])
            game.setDaemon(True)
            game.start()
            break
        elif("tutorial" in voiceCommand.lower() or "help" in voiceCommand.lower()):
            sm.current = 'tutorial'
        else:
            #if user tries saying something that is not in commands
            print("Not a command, use button labels on screen for valid commands or try saying\'Play a game\' ", voiceCommand)
    print("Exiting main")
    sys.exit()

main = Thread(target=Main)
main.setDaemon(True)
main.start()

class MainApplication(App):
    def build(self):
        return sm
if __name__ == '__main__':
    MainApplication().run()
    #will need sr to run in paralell with gui
