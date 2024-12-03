import serial
import pygame
import os
import sys
#from moviepy.editor import VideoFileClip
# Set up serial port for communication with external device
ser1 = serial.Serial('COM15', 9600)  # Replace 'COM16' with your first serial port name
ser1.timeout = 1

ser2 = serial.Serial('COM17', 9600)  # Replace 'COM8' with your second serial port name
ser2.timeout = 1

ser3 = serial.Serial('COM19', 9600)  # Replace 'COM14' with your third serial port name
ser3.timeout = 1

ser4 = serial.Serial('COM21', 9600)  # Replace 'COM14' with your third serial port name
ser4.timeout = 1
# Initialize Pygame
pygame.init()

# Set up Pygame window
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Quiz')



# Define quiz questions as image files
question_images = ['q1.png', 'q2.png', 'q3.png', 'q4.png', 'q5.png', 'q6.png', 'q7.png', 'q8.png', 'q9.png', 'q10.png', 'q11.png', 'q12.png', 'q13.png', 'q14.png', 'q15.png', 'q16.png', 'q17.png', 'q18.png', 'q19.png', 'q20.png'] 

# Define quiz answers
quiz_answers = ['2', '6', '8', '1', '4', '9', '4', '2', '9', '5', '7', '2', '9', '3', '5', '2', '10', '2', '6', '10'] #2 = False 6 = Jack 8 = Three 1 = True 9 = Two 20 = Countdown 10 = Four 7 = One

time2 = 0
# Load images for questions

def play_music(music_file):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

question_surfaces = []
for question_image in question_images:
    question_path = os.path.join('images', question_image)
    question_surface = pygame.image.load(question_path).convert()
    question_surfaces.append(question_surface)

# Load images for feedback
correct_path = os.path.join('images', 'correct.png')
correct_surface = pygame.image.load(correct_path).convert_alpha()

correct_path2 = os.path.join('images', 'correct2.png')
correct_surface2 = pygame.image.load(correct_path2).convert_alpha()

incorrect_path = os.path.join('images', 'incorrect.png')
incorrect_surface = pygame.image.load(incorrect_path).convert_alpha()

incorrect_path2 = os.path.join('images', 'incorrect2.png')
incorrect_surface2 = pygame.image.load(incorrect_path2).convert_alpha()

# Set up font for score display
font = pygame.font.SysFont('Arial', 55)

# Initialize score
score = 0

class BreakIt(Exception): pass

# Display questions and wait for answers
try:
    play_music("gameshow.mp3")  # replace with your file path
    processed_images = 0
    for j in range(2):
        for i in range(len(question_surfaces)):
            # Display current question and score
            current_question_surface = question_surfaces[i]
            window.blit(current_question_surface, (0, 0))
            score_text = font.render('Score: {}'.format(score), True, (255, 255, 255))
            window.blit(score_text, (WINDOW_WIDTH - score_text.get_width() - 20, 20))
            pygame.display.flip()

            # Start the timer
            start_time = pygame.time.get_ticks()
            # Wait for answer to be received via serial port
            answer_received = False
            attempts = 0  # Initialize counter for attempts
            while not answer_received and attempts < 1:  # Allow up to 3 attempts per question
                for ser in [ser1, ser2, ser4]:
                    if ser.in_waiting > 0:
                        # Read serial data
                        serial_data = ser.readline().decode().strip()

                        # Check if answer is correct
                        if serial_data == quiz_answers[i]:
                            print('Correct!')
                            feedback_surface = correct_surface
                            answer_received = True
                            score += 1  # Add 1 to score for correct answer
                            if serial_data == '20':
                                score += 4
                        elif serial_data == 'SKIP':
                            answer_recieved = True
                            raise BreakIt
                        else:
                            print('Incorrect. Please try again.')
                            feedback_surface = incorrect_surface
                            attempts += 1  # Increment attempt counter
                        processed_images += 1
                        if processed_images == len(question_surfaces):
                            ser4.write(str.encode('1'))
                            raise BreakIt
                        # Display feedback image and score
                        window.blit(feedback_surface, (0, 0))
                        score_text = font.render('Score: {}'.format(score), True, (255, 255, 255))
                        window.blit(score_text, (WINDOW_WIDTH - score_text.get_width() - 10, 10))
                        pygame.display.flip()

                    # Pause briefly before checking again
                    pygame.time.wait(10)

                # Pause before displaying next question
                pygame.time.wait(1000)

except BreakIt:
    pass

try:
    # Define quiz questions as image files
    
    stop_music()

    play_music("countdown.mp3")  # replace with your file path
    answer_received = False
    question_images = ['countdown.png'] 

    # Define quiz answers
    quiz_answers = ['20']
    question_surfaces = [] # Clear the list
    for question_image in question_images:
        question_path = os.path.join('images', question_image)
        question_surface = pygame.image.load(question_path).convert()
        question_surfaces.append(question_surface)



    # Display questions and wait for answers
    for l in range(2):
        for i in range(len(question_surfaces)):
            # Display current question and score
            current_question_surface = question_surfaces[i]
            window.blit(current_question_surface, (0, 0))
            score_text = font.render('Score: {}'.format(score), True, (255, 255, 255))
            window.blit(score_text, (WINDOW_WIDTH - score_text.get_width() - 20, 20))
            pygame.display.flip()

            # Start the timer
            start_time = pygame.time.get_ticks()
            # Wait for answer to be received via serial port
            answer_received = False
            attempts = 0  # Initialize counter for attempts
            while not answer_received and attempts < 1:  # Allow up to 3 attempts per question
                for ser in [ser2, ser4]:
                    if ser.in_waiting > 0:
                        # Read serial data
                        serial_data = ser.readline().decode().strip()

                        # Check if answer is correct
                        if serial_data == quiz_answers[i]:
                            print('Correct!')
                            feedback_surface = correct_surface
                            answer_received = True
                            score += 1  # Add 1 to score for correct answer
                            if serial_data == '20':
                                score += 4
                                ser4.write(str.encode('2'))
                                pygame.time.wait(1000)
                                raise BreakIt
                        elif serial_data == '999':
                            answer_recieved = True
                            ser4.write(str.encode('2'))
                            raise BreakIt
                        else:
                            print('Incorrect. Please try again.')
                            feedback_surface = incorrect_surface
                            ser4.write(str.encode('2'))
                            pygame.time.wait(1000)
                            attempts += 1  # Increment attempt counter
                            raise BreakIt

                
                        # Display feedback image and score
                        window.blit(feedback_surface, (0, 0))
                        score_text = font.render('Score: {}'.format(score), True, (0, 0, 0))
                        window.blit(score_text, (WINDOW_WIDTH - score_text.get_width() - 20, 20))
                        pygame.display.flip()
        
                    # Pause briefly before checking again
                    pygame.time.wait(10)

                # Pause before displaying next question
                pygame.time.wait(1000)


    
except BreakIt:
    pass
        # Display questions and wait for answers


try:  

        play_music("gameshow2.mp3")  # replace with your file path
            # Define new quiz questions and answers
        answer_received = False
        question_images = ['q1p2.png', 'q2p2.png', 'q3p2.png', 'q4p2.png', 'q5p2.png', 'q6p2.png', 'q7p2.png', 'q8p2.png', 'q9p2.png','q10p2.png', 'q11p2.png', 'q12p2.png', 'q13p2.png', 'q14p2.png', 'q15p2.png', 'q16p2.png', 'q17p2.png', 'q18p2.png', 'q19p2.png', 'q20p2.png', 'q21p2.png', 'q22p2.png', 'q23p2.png', 'q24p2.png', 'q25p2.png', 'q26p2.png', 'q27p2.png', 'q28p2.png', 'q29p2.png', 'q30p2.png']
        quiz_answers = ['spice', 'peppa', 'oned', 'rupaul', 'beyon', 'einstein', 'beyon', 'homer', 'einstein', 'beckham', 'oprah', 'oprah', 'mario', 'beyon', 'peppa', 'homer', 'beckham', 'einstein', 'beyon', 'peppa', 'oned', 'spice', 'beckham', 'beyon', 'spice', 'mario', 'oprah', 'oned', 'homer', 'mario']

        # Load images for questions
        question_surfaces = []
        for question_image in question_images:
            question_path = os.path.join('images', question_image)
            question_surface = pygame.image.load(question_path).convert()
            question_surfaces.append(question_surface)
        pygame.time.wait(1000)
        for z in range(2):
            for i in range(len(question_surfaces)):
                # Display current question and score
                current_question_surface = question_surfaces[i]
                window.blit(current_question_surface, (0, 0))
                score_text = font.render('Score: {}'.format(score), True, (255, 255, 255))
                window.blit(score_text, (WINDOW_WIDTH - score_text.get_width() - 10, 10))
                pygame.display.flip()

                # Wait for answer to be received via serial port
                answer_received = False
                attempts = 0  # Initialize counter for attempts
                while not answer_received and attempts < 1:  # Allow up to 3 attempts per question
                    for ser in [ser3]:
                        if ser.in_waiting > 0:
                            # Read serial data
                            serial_data = ser.readline().decode().strip()

                            # Check if answer is correct
                            if serial_data == quiz_answers[i]:
                                print('Correct!')
                                feedback_surface = correct_surface2
                                answer_received = True
                                score += 1  # Add 1 to score for correct answer
                            elif serial_data == 'DONEDONE':
                                answer_recieved = True
                                raise BreakIt
                            else:
                                print('Incorrect. Please try again.')
                                feedback_surface = incorrect_surface2
                                attempts += 1  # Increment attempt counter



                            # Display feedback image and score
                            window.blit(feedback_surface, (0, 0))
                            score_text = font.render('Score: {}'.format(score), True, (255, 255, 255))
                            window.blit(score_text, (WINDOW_WIDTH - score_text.get_width() - 10, 10))
                            pygame.display.flip()

                            # Pause briefly before checking again
                            pygame.time.wait(10)

                    # Pause before displaying next question
                    pygame.time.wait(1000)
except BreakIt:
    pass


# Display the final score
background_color = (0, 0, 0)
final_score_text = font.render('Final Score: {}'.  format(score), True, (255, 255, 255))
final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
# Main loop to keep the window open
try:
    window.fill(background_color)
    window.blit(final_score_text, final_score_rect)
    pygame.display.flip()

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Close serial port
            ser1.close()
            ser2.close()
            ser3.close()
            ser4.close()
            # Quit Pygame
            pygame.quit()

            # Exit the script
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Close serial port
                ser1.close()
                ser2.close()
                ser3.close()
                ser4.close()
                # Quit Pygame
                pygame.quit()

                # Exit the script
                sys.exit()
except BreakIt:
    pass
