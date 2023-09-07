import pygame
import random
import json

pygame.init()

# Cấu hình cửa sổ game
WIDTH = 500
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Cấu hình màu sắc
WHITE = (255, 255, 255)

# Tải ảnh và âm thanh
bird_img = pygame.image.load("bird.png")
pipe_img = pygame.image.load("pipe.png")
background_img = pygame.image.load("background.png")
point_sound = pygame.mixer.Sound("point.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")

# Đặt kích thước và vị trí cho chim và ống
bird_size = bird_img.get_rect().size
bird_width = bird_size[0]
bird_height = bird_size[1]
bird_x = 50
bird_y = HEIGHT // 2 - bird_height // 2

pipe_width = pipe_img.get_width()
pipe_height = pipe_img.get_height()
pipe_gap = 200
pipe_x = WIDTH // 2
pipe1_y = random.randint(50, HEIGHT - 50 - pipe_gap)
pipe2_y = pipe1_y + pipe_gap

# Thiết lập tốc độ
clock = pygame.time.Clock()
fps = 60
bird_speed = 2
pipe_speed = 2

# Biến lưu điểm số và điểm cao
score = 0
high_score = 0
font = pygame.font.Font(None, 36)

# Biến lưu trạng thái trò chơi
game_over = False

def draw_objects():
    window.blit(background_img, (0, 0))
    window.blit(bird_img, (bird_x, bird_y))
    window.blit(pipe_img, (pipe_x, pipe1_y))
    window.blit(pipe_img, (pipe_x, pipe2_y))
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (10, 10))

def update_bird():
    bird_y += bird_speed

def update_pipes():
    pipe_x -= pipe_speed
    if pipe_x + pipe_width < 0:
        # Tạo ống mới khi ống cũ ra khỏi màn hình
        pipe_x = WIDTH
        pipe1_y = random.randint(50, HEIGHT - 50 - pipe_gap)
        pipe2_y = pipe1_y + pipe_gap

def check_collision():
    if (bird_y < 0 or bird_y + bird_height > HEIGHT) or \
            ((bird_x + bird_width > pipe_x and bird_x < pipe_x + pipe_width) and
             (bird_y < pipe1_y + pipe_height or bird_y + bird_height > pipe2_y)):
        # Xử lý va chạm khi chim chạm đường biên hoặc ống
        return True
    return False

def save_high_score():
    global high_score
    if score > high_score:
        high_score = score
        with open("high_score.json", "w") as file:
            json.dump(high_score, file)

def load_high_score():
    global high_score
    try:
        with open("high_score.json", "r") as file:
            high_score = json.load(file)
    except FileNotFoundError:
        high_score = 0

def reset_game():
    global bird_y, score, pipe_x, pipe1_y, pipe2_y, game_over
    bird_y = HEIGHT // 2 - bird_height // 2
    score = 0
    pipe_x = WIDTH // 2
    pipe1_y = random.randint(50, HEIGHT - 50 - pipe_gap)
    pipe2_y = pipe1_y + pipe_gap
    game_over = False

load_high_score()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over:
            bird_speed -= 5

    if not game_over:
        update_bird()
        update_pipes()

        if bird_x > pipe_x + pipe_width:
            score += 1
            point_sound.play()

        if check_collision():
            game_over = True
            point_sound.stop()
            gameover_sound.play()
            save_high_score()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and game_over:
        reset_game()

    draw_objects()
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
