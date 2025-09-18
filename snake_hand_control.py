import pygame
import random
import cv2
import mediapipe as mp
import sys
from collections import deque
import math

# --- PYGAME SETUP ---
pygame.init()
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Hand Gestures")

# Colors
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
RED = (255, 50, 50)
SNAKE_GRADIENT = [(0, 255, 0), (0, 200, 0), (0, 150, 0), (0, 100, 0)]

clock = pygame.time.Clock()

# --- SNAKE SETUP ---
snake = [(100, 50), (90, 50), (80, 50)]
snake_direction = "RIGHT"
food = (WIDTH//2, HEIGHT//2)

# --- HAND GESTURE SETUP ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
POSITION_HISTORY = 5
positions = deque(maxlen=POSITION_HISTORY)

# --- FUNCTIONS ---
def draw_gradient_background():
    for y in range(HEIGHT):
        color_value = int(30 + (y / HEIGHT) * 50)
        pygame.draw.line(screen, (color_value, color_value, color_value), (0, y), (WIDTH, y))

def draw_snake(snake):
    for i, segment in enumerate(snake):
        color = SNAKE_GRADIENT[i % len(SNAKE_GRADIENT)]
        pygame.draw.circle(screen, color, (segment[0]+CELL_SIZE//2, segment[1]+CELL_SIZE//2), CELL_SIZE//2)

def draw_food(food, frame_count):
    # Pulsing effect
    pulse = 5 * math.sin(frame_count * 0.2)
    radius = CELL_SIZE//2 + pulse
    pygame.draw.circle(screen, RED, (food[0]+CELL_SIZE//2, food[1]+CELL_SIZE//2), int(radius))

def detect_gesture_velocity():
    global snake_direction
    ret, frame = cap.read()
    if not ret:
        return
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        positions.append((index_tip.x, index_tip.y))

        if len(positions) >= 2:
            dx = positions[-1][0] - positions[0][0]
            dy = positions[-1][1] - positions[0][1]
            threshold = 0.03
            if abs(dx) > abs(dy):
                if dx > threshold and snake_direction != "LEFT":
                    snake_direction = "RIGHT"
                elif dx < -threshold and snake_direction != "RIGHT":
                    snake_direction = "LEFT"
            else:
                if dy > threshold and snake_direction != "UP":
                    snake_direction = "DOWN"
                elif dy < -threshold and snake_direction != "DOWN":
                    snake_direction = "UP"
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Gestures", frame)
    cv2.waitKey(1)

def game_loop():
    global snake, snake_direction, food
    snake = [(100, 50), (90, 50), (80, 50)]
    snake_direction = "RIGHT"
    food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
    score = 0
    running = True
    frame_count = 0

    while running:
        frame_count += 1
        screen.fill(BLACK)
        draw_gradient_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()

        detect_gesture_velocity()

        # Snake movement
        head_x, head_y = snake[0]
        if snake_direction == "UP":
            head_y -= CELL_SIZE
        elif snake_direction == "DOWN":
            head_y += CELL_SIZE
        elif snake_direction == "LEFT":
            head_x -= CELL_SIZE
        elif snake_direction == "RIGHT":
            head_x += CELL_SIZE

        # Wrap-around borders
        head_x %= WIDTH
        head_y %= HEIGHT

        new_head = (head_x, head_y)
        snake.insert(0, new_head)

        # Eat food with margin
        if abs(new_head[0] - food[0]) < CELL_SIZE and abs(new_head[1] - food[1]) < CELL_SIZE:
            score += 1
            food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        else:
            snake.pop()

        # Self collision triggers restart
        if new_head in snake[1:]:
            return

        draw_snake(snake)
        draw_food(food, frame_count)

        font = pygame.font.SysFont("Arial", 25, True)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(12)

def main():
    while True:
        game_loop()

if __name__ == "__main__":
    main()
