import pygame
import cv2
import mediapipe as mp
import numpy as np
import threading
import time
import random
from PIL import Image

# global control variables
global GESTURE_STATE, HAND_CENTER_X, CAMERA_FRAME, CV_READY
GESTURE_STATE = 'stop'
HAND_CENTER_X = 0.5
CAMERA_FRAME = None 
CAMERA_LOCK = threading.Lock() # lock for thread-safe camera frame access
CV_READY = False 

# game state constants
LOADING = 0
RUNNING = 1
GAME_OVER = 2
QUITTING = 3 

# gesture detection logic (reverted to reliable Y-axis check)
def get_gesture(hand_landmarks):
    # classifies the current hand gesture based on keypoint Y-position
    
    landmarks = hand_landmarks.landmark
    
    # helper to check if a finger is extended (tip Y is lower than knuckle Y)
    def is_extended(tip_idx, knuckle_idx, threshold=0.03):
        # tip y is lower than knuckle y in normalized coords
        return landmarks[tip_idx].y < landmarks[knuckle_idx].y - threshold

    # use a very loose threshold for the thumb (0.01) and standard for others (0.03)
    thumb_extended = is_extended(mp.solutions.hands.HandLandmark.THUMB_TIP, mp.solutions.hands.HandLandmark.THUMB_IP, threshold=0.01)
    index_extended = is_extended(mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP, mp.solutions.hands.HandLandmark.INDEX_FINGER_PIP)
    middle_extended = is_extended(mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP, mp.solutions.hands.HandLandmark.MIDDLE_FINGER_PIP)
    ring_extended = is_extended(mp.solutions.hands.HandLandmark.RING_FINGER_TIP, mp.solutions.hands.HandLandmark.RING_FINGER_PIP)
    pinky_extended = is_extended(mp.solutions.hands.HandLandmark.PINKY_TIP, mp.solutions.hands.HandLandmark.PINKY_PIP)
    
    
    # check if index, middle, ring, and pinky are all curled
    fingers_curled = (not index_extended and not middle_extended and not ring_extended and not pinky_extended)


    # classification logic (using unambiguous, Y-axis friendly gestures)
    
    # 1. shoot: index and thumb extended, others curled ("gun" gesture)
    if index_extended and thumb_extended and not middle_extended and not ring_extended and not pinky_extended:
        return 'SHOOT'
        
    # 2. speed up: only thumb extended ("thumbs up")
    if thumb_extended and not index_extended and not middle_extended and not ring_extended and not pinky_extended:
        return 'SPEED_UP'

    # 3. speed down: only pinky extended ("pinky up")
    if pinky_extended and not thumb_extended and not index_extended and not middle_extended and not ring_extended:
        return 'SPEED_DOWN'
    
    # 4. stop: all fingers curled (closed fist)
    if fingers_curled and not thumb_extended:
        return "SPEED_DOWN"
        #return 'STOP'
        
    # 5. fallback
    return 'UNKNOWN'


# computer vision thread
def cv_thread_function(cap, hands):
    # runs the mediapipe tracking loop
    global GESTURE_STATE, HAND_CENTER_X, CAMERA_FRAME, CV_READY

    if not cap.isOpened():
        GESTURE_STATE = 'QUIT'
        return

    print("info: cv thread started.")
    CV_READY = True # signal main thread

    while cap.isOpened() and GESTURE_STATE != 'QUIT':
        try:
            success, image = cap.read()
            if not success:
                time.sleep(0.01)
                continue

            image = cv2.flip(image, 1) # flip camera feed
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            results = hands.process(image_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    
                    GESTURE_STATE = get_gesture(hand_landmarks)
                    
                    # calculate normalized hand x center (0.0 to 1.0)
                    x_coords = [lm.x for lm in hand_landmarks.landmark]
                    HAND_CENTER_X = np.mean(x_coords) 
                    
                    # draw landmarks
                    mp.solutions.drawing_utils.draw_landmarks(
                        image, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS,
                        mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                        mp.solutions.drawing_styles.get_default_hand_connections_style())

                    # draw gesture text
                    cv2.putText(image, GESTURE_STATE, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                GESTURE_STATE = 'NO_HAND'
            
            # convert back to bgr and update shared frame
            image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            with CAMERA_LOCK:
                CAMERA_FRAME = image_bgr
            
            time.sleep(0.005) 

        except Exception as e:
            print(f"fatal error in cv thread: {e}")
            GESTURE_STATE = 'QUIT'
            break

    print("info: cv thread cleaning up.")


# pygame loop (main thread)

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CAMERA_FEED_WIDTH = 300
CAMERA_FEED_HEIGHT = 225 
MIN_SPEED = 3.0
MAX_SPEED = 15.0
ACCELERATION = 0.5
BULLET_SPEED = 12
SHOOT_COOLDOWN_MS = 300 
PLAYER_SIZE = 50
SMOOTHING_FACTOR = 0.1

# setup pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("gesture shooter game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)
title_font = pygame.font.Font(None, 100)
white = (255, 255, 255)
red = (255, 0, 0)
gray = (100, 100, 100)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE])
        self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 30
        self.speed = 5
        self.last_shot_time = 0
        self.shots = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([5, 15])
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        
    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    # class-level float variable for global enemy speed
    global_speed = 3.0
    
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - 40)
        self.rect.y = random.randrange(-100, -50)
        
        # initialize float position for precise movement
        self.y_float = float(self.rect.y) 

    def update(self):
        # update the float position
        self.y_float += Enemy.global_speed
        
        # update the integer rect position by rounding
        self.rect.y = int(round(self.y_float)) 
        
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(SCREEN_WIDTH - 40)
            self.rect.y = random.randrange(-100, -50)
            self.y_float = float(self.rect.y) # reset float position

def fire_bullet(player, all_sprites, bullets):
    # fires a bullet if cooldown is over
    current_time = pygame.time.get_ticks()
    if current_time - player.last_shot_time > SHOOT_COOLDOWN_MS:
        bullet = Bullet(player.rect.centerx, player.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        player.last_shot_time = current_time
        player.shots += 1

def draw_camera_feed(screen):
    # converts the frame to a pygame surface and draws it
    global CAMERA_FRAME
    
    with CAMERA_LOCK:
        frame_to_draw = CAMERA_FRAME
        
    if frame_to_draw is not None:
        frame_rgb = cv2.cvtColor(frame_to_draw, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        pil_image = pil_image.resize((CAMERA_FEED_WIDTH, CAMERA_FEED_HEIGHT))
        pygame_image = pygame.image.frombuffer(pil_image.tobytes(), pil_image.size, "RGB")
        screen.blit(pygame_image, (SCREEN_WIDTH - CAMERA_FEED_WIDTH, 0))

def draw_loading_screen(screen):
    # draws the initial loading screen
    screen.fill((20, 20, 40))
    
    title_text = large_font.render("loading gesture system", True, white)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(title_text, title_rect)
    
    status = "connecting to camera and mediapipe"
    color = gray

    if GESTURE_STATE == 'QUIT':
        status = "camera could not start"
        color = red
    
    status_text = font.render(status, True, color)
    status_rect = status_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(status_text, status_rect)
    
    pygame.display.flip()

def draw_game_over_screen(screen):
    # draws the game over screen
    screen.fill((40, 0, 0))
    
    title_text = title_font.render("game over", True, red)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(title_text, title_rect)

    restart_text = font.render("press space to restart or esc to quit", True, white)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, restart_rect)
    
    pygame.display.flip()
    
def game_loop():
    # main pygame loop
    global GESTURE_STATE, HAND_CENTER_X
    
    current_game_state = LOADING
    
    # helper to create/reset game assets
    def initialize_game_assets():
        all_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        
        player = Player()
        all_sprites.add(player)
        
        for _ in range(5):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            
        # reset the global speed when restarting the game
        Enemy.global_speed = 3.0
        
        return all_sprites, bullets, enemies, player

    all_sprites, bullets, enemies, player = initialize_game_assets()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GESTURE_STATE = 'QUIT'
                running = False
            
            if current_game_state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # reset game state and assets
                        all_sprites, bullets, enemies, player = initialize_game_assets()
                        current_game_state = RUNNING
                    elif event.key == pygame.K_ESCAPE:
                        GESTURE_STATE = 'QUIT'
                        running = False
        
        if GESTURE_STATE == 'QUIT':
            running = False

        if current_game_state == LOADING:
            # wait for cv thread to initialize
            if CV_READY:
                current_game_state = RUNNING
            else:
                draw_loading_screen(screen)
        
        elif current_game_state == RUNNING:
            
            # gesture processing
            if GESTURE_STATE == 'SPEED_UP':
                # increment speed, clamped by max_speed
                Enemy.global_speed = min(MAX_SPEED, Enemy.global_speed + 0.1)
                
            elif GESTURE_STATE == 'SPEED_DOWN':
                # decrement speed, clamped by min_speed
                Enemy.global_speed = max(MIN_SPEED, Enemy.global_speed - 0.1)
                
            elif GESTURE_STATE in ('STOP', 'NO_HAND', 'UNKNOWN'):
                # smooth player speed decay
                if player.speed > 5:
                    player.speed -= ACCELERATION / 2
                elif player.speed < 5:
                    player.speed += ACCELERATION / 2

            # directional control (position mapping)
            target_x = int(HAND_CENTER_X * SCREEN_WIDTH)
            current_x = player.rect.centerx
            # apply smoothing factor
            new_center_x = current_x + (target_x - current_x) * SMOOTHING_FACTOR
            player.rect.centerx = int(new_center_x)

            # shoot action
            if GESTURE_STATE == 'SHOOT':
                fire_bullet(player, all_sprites, bullets)

            # game updating
            all_sprites.update() 
            # keep player within screen bounds
            player.rect.x = max(0, min(player.rect.x, SCREEN_WIDTH - player.rect.width))

            # collision checks: bullets vs enemies
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                new_enemy = Enemy()
                all_sprites.add(new_enemy)
                enemies.add(new_enemy)
                
            # collision checks: player vs enemies
            if pygame.sprite.spritecollide(player, enemies, False):
                print("game over! player hit an obstacle.")
                current_game_state = GAME_OVER 

            # drawing
            screen.fill((50, 50, 50)) 
            all_sprites.draw(screen)
            draw_camera_feed(screen)

            # display debugging text
            speed_text = font.render(f"enemy speed: {Enemy.global_speed:.1f}", True, white)
            gesture_text = font.render(f"gesture: {GESTURE_STATE}", True, white)
            hand_pos_text = font.render(f"hand x: {HAND_CENTER_X:.2f}", True, white)
            shots_text = font.render (f"shots fired: {player.shots}", True, white)
            screen.blit(speed_text, (10, 10))
            screen.blit(gesture_text, (10, 50))
            screen.blit(hand_pos_text, (10, 90))
            screen.blit(shots_text, (10, 130))
            
            pygame.display.flip()

        elif current_game_state == GAME_OVER:
            draw_game_over_screen(screen)

        clock.tick(60) 

    pygame.quit()
    GESTURE_STATE = 'QUIT' # signal cv thread to stop

if __name__ == "__main__":
    print("starting program")

    # initialize mediapipe
    mp_hands = mp.solutions.hands
    hands_model = mp_hands.Hands(
        static_image_mode=False, max_num_hands=1, min_detection_confidence=0.4, min_tracking_confidence=0.2
    )
    
    # initialize camera
    print("initializing camera")
    cap_device = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION) 
    
    if not cap_device.isOpened():
        print("error: camera couldn't open")
        GESTURE_STATE = 'QUIT'

    # start cv thread
    if GESTURE_STATE != 'QUIT':
        cv_thread = threading.Thread(target=cv_thread_function, args=(cap_device, hands_model))
        cv_thread.daemon = True
        cv_thread.start()
    
    # start pygame loop
    print("starting game window")
    try:
        game_loop()
    except Exception as e:
        print(f"error: pygame loop crashed: {e}")
        GESTURE_STATE = 'QUIT'
    
    # cleanup
    GESTURE_STATE = 'QUIT'
    
    if cap_device.isOpened():
        cap_device.release()
    
    if 'cv_thread' in locals() and cv_thread.is_alive():
        cv_thread.join()
        
    print("program finished")