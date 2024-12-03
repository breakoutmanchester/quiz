import pygame
import serial
import threading

# Initialize Pygame
pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font settings
FONT_SIZE = 72
font = pygame.font.SysFont(None, FONT_SIZE)

# Define the COM ports to listen to
com_ports = ['COM3', 'COM5', 'COM6', 'COM8', 'COM9']

# Dictionary to hold serial port objects and their last messages
serial_ports = {}
last_messages = {}

# Pygame screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Serial Messages")

def serial_listener(port):
    """Function to listen to serial port and update last message"""
    ser = serial.Serial(port, 9600)  # Adjust baud rate as needed
    serial_ports[port] = ser
    print(f"Listening to {port}")
    while True:
        try:
            message = ser.readline().decode().strip()
            if message in last_messages:
                last_messages[message] += 1
            else:
                last_messages.clear()  # Clear previous messages
                last_messages[message] = 1
        except Exception as e:
            print(f"Error reading from {port}: {e}")
            break

# Start a thread for each serial port
threads = []
for port in com_ports:
    thread = threading.Thread(target=serial_listener, args=(port,))
    thread.daemon = True
    thread.start()
    threads.append(thread)

# Main Pygame loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Display messages
    middle_y = SCREEN_HEIGHT // 2
    for message, count in last_messages.items():
        if message:
            # Display the message
            if count > 1:
                message_with_count = f"{message} (x{count})"
            else:
                message_with_count = message
            text = font.render(message_with_count, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, middle_y))
            screen.blit(text, text_rect)
            break  # Only display one message at a time

    # Update the display
    pygame.display.flip()

# Close serial ports
print("\nClosing serial ports...")
for port in serial_ports.values():
    port.close()
print("Serial ports closed.")

# Quit Pygame
pygame.quit()
