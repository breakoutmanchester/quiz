import win32con
import win32file
import win32event
import win32api
import sys
import time
from pynput.mouse import Button, Controller
import pygame
import datetime
from winerror import ERROR_ALREADY_EXISTS
import mysql.connector 
from mysql.connector import Error

mutex_name = "my_script_mutex"
mutex_handle = win32event.CreateMutex(None, False, mutex_name)
last_error = win32api.GetLastError()

mode = ""

if last_error == ERROR_ALREADY_EXISTS:
    mutex_handle = None
    print("Another instance of the script is already running.")
    sys.exit(1)

# SQL Configuration 
config = { 
  "host":"192.168.1.208",
  "port": "3333",
  "user":"root",
  "password":"pass",
  "database": "scores",
}

pygame.init()

# Set up the screen
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Scan Card")

background_image = pygame.image.load("cp_logo.jpeg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Font for rendering text
font_big = pygame.font.Font("C:/Users/QUIZ/Desktop/quiz final/Super_Creamy.ttf", 150)
font_small = pygame.font.Font("C:/Users/QUIZ/Desktop/quiz final/Super_Creamy.ttf", 100)

# Function to display text at the center of the screen
def draw_text_center(text, font, color, y_offset=0):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + y_offset))
    screen.blit(text_surface, text_rect)

# Main loop
scanned_card_data = None
running = True
input_text = ''
count = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if scanned_card_data is None:
                if event.key == pygame.K_RETURN:
                    scanned_card_data = input_text
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    # Clear the screen
    screen.blit(background_image, (0, 0))

    # Display message
    if scanned_card_data is None:
        draw_text_center("Please scan your card", font_small, (255, 255, 255))
        
            
    else:
        try:
            with mysql.connector.connect(**config) as db:
                cursor = db.cursor()

                cursor.execute(f"SELECT * FROM scores.teams where CardID = '{scanned_card_data}';")
                result = cursor.fetchone()

                if result is not None:
                    draw_text_center(f"Welcome", font_small, (255, 255, 255), y_offset=-75)
                    teamName = result[2]
                    mode = result[14]
                    print("mode", mode)
                    draw_text_center(f"{teamName}", font_big, (255, 255, 173), y_offset=50)
                    pygame.display.flip()
                    time.sleep(4)
                    running = False
                else:
                    draw_text_center(f"Invalid card!", font_small, (255, 51, 51))
                    scanned_card_data = None
                    pygame.display.flip()
                    time.sleep(2)
        except Exception as ex:
            print(ex)
    pygame.display.flip()

pygame.quit()

# Rest of your script below this line
print("Script is now running...")

from moviepy.editor import VideoFileClip

# Play the video before game starts
clip = VideoFileClip("quiznew.mp4")
clip_resized = clip.resize(height=1080)
clip_resized.preview()

import serial
import pygame
import os
import random

ser1 = serial.Serial('COM3', 9600)
ser1.timeout = 1

ser3 = serial.Serial('COM8', 9600)
ser3.timeout = 1

ser5 = serial.Serial('COM9', 9600)
ser5.timeout = 1

ser4 = serial.Serial('COM6', 9600)
ser4.timeout = 1

pygame.init()

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Quiz')

correctsound = pygame.mixer.Sound("correct.mp3")
incorrectsound = pygame.mixer.Sound("incorrect.mp3")
finalsound = pygame.mixer.Sound("airhorn.mp3")
finalsound.play()

if mode.lower() == 'y' or mode.lower() == 'yes':
    question_images = [
        'Africa.png', 'audiojack.png', 'Batmansdog.png', 'Beatles.png', 'berlinwall.png', 'bestsellers.png', 'bones_humanbody.png', 'Carjack.png', 'Chess king.png', 'Cleopatra.png', 'comedy_adventure.png', 
        'drag_icon_catchphrase.png', 'experience_school.png', 'family_trips.png', 'fashion_campaigns.png', 'Goldholeinone.png', 'GOT.png', 'inter_miami.png', 'Jack & Jill.png', 'Lightning.png', 'michael_jackson.png',
        'mountain_range.png', 'native_speakers.png', 'pharoh.png', 'pyramids.png', 'queenbee.png', 'queenchess.png', 'red_planet.png', 'released_albums.png', 'rising_sun.png', 'simon_fuller.png', 'statue_of_liberty.png',
        'super_mushroom.png', 'surpirse_releasing.png', 'this_is_us.png', 'titanic.png', 'Twilight.png', 'volleyball.png', 'Water.png'
    ]
    quiz_answers = [
        '2', '5', '3', '1', '1', 'oprah', '9', '5', '4', '1', 'spice', 'rupaul', 'einstein', 'peppa', 'beckham', '3', '9', 'beckham', '5', '2', 'oprah', '8', '8', '4', '8', '6', '6', '9', 'oned', '10',
        'spice', '8', 'mario', 'beyon', 'oned', '7', '2', '3', '1'
    ]

else:
##Halloween
    question_images = [
        #WHEEL
        'beckham1.png', 'beyon.png', 'einstein.png', 'homer1.png', 'homer2.png', 'mario1.png', 'oned1.png', 'oprah1.png', 'peppa.png', 'rupaul.png', 'spice1.png', 'spice2.png',
        #BOXES
        'box1 1.png', 'box1 2.png', 'box1 4.png', 'box2 1.png', 'box2 2.png', 'box2 3.png', 'box2 4.png', 'box3 1.png', 'box3 2.png', 'box3 3.png', 'box4 1.png', 'box4 2.png',
        #TRUE OR FALSE
        'false1.png', 'false2.png', 'false3.png', 'true1.png', 'true2.png', 'true3.png', 'true4.png', 'true5.png',
        #CARDS
        'king1.png', 'king2.png', 'king4.png', 'jack1.png', 'jack2.png', 'queen1.png', 'queen2.png',
    ]
    quiz_answers = [
        'beckham', 'beyon', 'einstein', 'homer', 'homer', 'mario', 'oned','oprah', 'peppa', 'rupaul', 'spice', 'spice',
        '7', '7', '7', '9', '9', '9', '9', '8', '8', '8', '10','10',
        '2', '2', '2', '1', '1', '1', '1', '1',
        '4', '4', '4', '5', '5', '6', '6',
    ]



# for final
#question_images = [
#    'unicorn.png', 'berriesQ.png', 'pringles.png', 'sharks.png', 'monarch.png', 'blackjack.png', 'christmas_pie.png',
#    'nightmarechristmas.png', 'fireice.png', 'mongolia.png', 'mediterranean_sea.png', 'olive_oil.png', 'mountain_range.png',
#    'atomic_number.png', 'planets.png', 'largestland.png', 'harry_potter.png', 'broadway_show.png', 'american_idol.png',
#    'inception.png', 'poem_lliad.png', 'touch_group.png', 'lived_in.png', 'steven_speilberg.png', 'homer.png', 'autobiography.png',
#    'peppa_piggy.png', 'peppa_piggy2.png', 'spicegirls.png', 'playstation_game.png', 'mario_kart.png', 'tongue_sticking.png',
 #   'comic_relief.png', 'lion_king_trakc.png', 'beckham.png', 'photons.png'
#]
#quiz_answers = [
#    '1', '1', '1', '2', '5', '4', '6',
#    '6', '9', '8', '9', '10', '8',
 #   '7', '10', '9', '10', '7', '9',
  #  '9', 'homer', 'spice', 'beckham', 'oprah', 'homer', 'rupaul',
   # 'peppa', 'peppa', 'spice', 'spice', 'mario', 'einstein',
 #   'oned', 'beyon', 'beckham', 'einstein', 'oprah'
#]

quiz = list(zip(question_images, quiz_answers))
random.shuffle(quiz)
question_images, quiz_answers = zip(*quiz)

def play_music(music_file):
    pygame.mixer.init()
    if mode.lower() == 'y' or mode.lower() == 'yes':
        pygame.mixer.music.load(music_file)
    else:
        pygame.mixer.music.load("christmasquiz.mp3")
    
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

def update_DB(score):
    retry = 0
    numofretry = 3
    while retry < numofretry:
        try:
            with mysql.connector.connect(**config) as db:
                cursor = db.cursor()
                query = "UPDATE scores.teams SET Quiz = %s WHERE TeamName = %s"
                values = (score, teamName)
                cursor.execute(query, values)
                db.commit()
                print(cursor.rowcount, "record(s) affected")
                time.sleep(0.5)
        except Error as e:
            print(f"Error: {e}")
            if db.is_connected():
                db.rollback()
        finally:
            retry += 1
            if db.is_connected():
                cursor.close()
                db.close()

question_surfaces = []
try:
    for question_image in question_images:
        question_path = os.path.join('images', question_image)
        question_surface = pygame.image.load(question_path).convert()
        question_surfaces.append(question_surface)

    correct_path = os.path.join('images', 'correct.png')
    correct_surface = pygame.image.load(correct_path).convert_alpha()
    correct_path2 = os.path.join('images', 'correct2.png')
    correct_surface2 = pygame.image.load(correct_path2).convert_alpha()
    incorrect_path = os.path.join('images', 'incorrect.png')
    incorrect_surface = pygame.image.load(incorrect_path).convert_alpha()
    incorrect_path2 = os.path.join('images', 'incorrect2.png')
    incorrect_surface2 = pygame.image.load(incorrect_path2).convert_alpha()
except Exception as e:
    print(e)
    time.sleep(60)

font = pygame.font.Font('WigglyCurvesRegular-qZdAx.ttf', 78)
font2 = pygame.font.Font('WigglyCurvesRegular-qZdAx.ttf', 150)
font3 = pygame.font.Font('WigglyCurvesRegular-qZdAx.ttf', 108)
score = 0
start_time = pygame.time.get_ticks()
timer_minutes = 5

class BreakIt(Exception): pass

extra_time = 0

try:
    play_music("gameshow.mp3")
    processed_images = 0
    for j in range(2):
        for i in range(len(question_surfaces)):
            current_question_surface = question_surfaces[i]
            window.blit(current_question_surface, (0, 0))
            score_text = font.render('Score: {}'.format(score), True, (255, 255, 255))
            window.blit(score_text, (WINDOW_WIDTH - score_text.get_width() - 20, 20))
            pygame.display.flip()

            answer_received = False
            attempts = 0
            while not answer_received and attempts < 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            extra_time += 60000
                        elif event.button == 3:
                            extra_time -= 60000
                            
                current_time = pygame.time.get_ticks()
                time_diff = (current_time - start_time - extra_time) // 1000
                remaining_time = (timer_minutes * 60) - time_diff
                
                if remaining_time > 0:
                    window.blit(current_question_surface, (0, 0))
                    window.blit(score_text, (WINDOW_WIDTH - score_text.get_width() - 20, 20))

                    remaining_minutes = remaining_time // 60
                    remaining_seconds = remaining_time % 60
                    timer_text = font2.render(f"{remaining_minutes}:{remaining_seconds:02}", True, (255, 255, 255))
                    timer_rect = timer_text.get_rect(topleft=(10, 10))

                    timer_background = pygame.Rect(timer_rect.left, timer_rect.top, timer_rect.width, timer_rect.height)
                    pygame.draw.rect(window, (192, 192, 192), timer_background)

                    window.blit(timer_text, timer_rect)
                elif remaining_time < 2:
                    answer_received = True
                    background_color = (0, 0, 0)
                    final_score_text = font2.render('Final Score: {}'.format(score), True, (255, 255, 255))
                    final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                    returnstudio = font.render(f"Please return to the studio!", True, (255, 0, 0))
                    return_rect = returnstudio.get_rect(center=(1920 // 2, 1080 // 1.5))
                    window.fill(background_color)
                    window.blit(final_score_text, final_score_rect)
                    window.blit(returnstudio, return_rect)
                    finalsound.play()
                    pygame.display.flip()
                    try:
                        update_DB(score)
                    except:
                        print("Could not update to Database :()")

                    try:
                        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        with open('scores.txt', 'a') as file:
                            file.write(f"{str(current_time)} - Score: {score}\n")
                            file.close()
                    except Exception as e:
                        print(e)
                        print("Score =", score)

                    pygame.time.wait(1000000)
                pygame.display.flip()
                for ser in [ser1, ser4, ser3, ser5]:
                    if ser.in_waiting > 0:
                        serial_data = ser.readline().decode().strip()
                        print(serial_data)

                        if serial_data == quiz_answers[i]:
                            feedback_surface = correct_surface
                            answer_received = True
                            score += 1
                            correctsound.play()
                            if serial_data == '20':
                                score += 4
                            window.blit(feedback_surface, (0, 0))
                            pygame.display.flip()
                        elif serial_data == 'SKIP':
                            answer_received = False
                        else:
                            feedback_surface = incorrect_surface
                            attempts += 1
                            incorrectsound.play()
                            processed_images += 1
                            if processed_images == len(question_surfaces):
                                ser4.write(str.encode('1'))
                                raise BreakIt
                            window.blit(feedback_surface, (0, 0))
                        score_text = font.render('Score: {}'.format(score), True, (255, 255, 255))
                        window.blit(score_text, (WINDOW_WIDTH - score_text.get_width() - 30, 30))
                        pygame.display.flip()

                    pygame.time.wait(10)

                pygame.time.wait(1000)

except BreakIt:
    pass

try:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ser1.close()
            ser3.close()
            ser4.close()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                ser1.close()
                ser3.close()
                ser4.close()
                pygame.quit()
                sys.exit()
except BreakIt:
    pass
