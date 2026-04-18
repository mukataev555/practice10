import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 600, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game: Мукатаев Алибек")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Настройки шрифтов
font_style = pygame.font.SysFont("Roboto", 25)
score_font = pygame.font.SysFont("Roboto", 30)

# Параметры змейки
SNAKE_BLOCK = 20 

def show_stats(score, level):
    value = score_font.render(f"Score: {score}  Level: {level}", True, WHITE)
    SCREEN.blit(value, [10, 10])

def generate_food(snake_body):
    while True:
        food_x = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
        food_y = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0
        
        # Проверяем, не попала ли еда на тело змейки
        if [food_x, food_y] not in snake_body:
            return food_x, food_y

def game_loop():
    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    # Тело змейки
    snake_body = []
    length_of_snake = 1
    
    #параметры 
    score = 0
    level = 1
    snake_speed = 10 

    # Создаем еду 
    food_x, food_y = generate_food(snake_body)

    clock = pygame.time.Clock()

    while not game_over:

        while game_close == True:
            SCREEN.fill(BLACK)
            message = font_style.render("Game Over! Press Q-Quit or C-Play Again", True, RED)
            SCREEN.blit(message, [WIDTH / 6, HEIGHT / 3])
            show_stats(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        #Проверка столкновения со стенами
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        SCREEN.fill(BLACK)

        # Рисуем еду
        pygame.draw.rect(SCREEN, BLUE, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])

        # Обновление тела змейки
        snake_head = [x1, y1]
        snake_body.append(snake_head)
        if len(snake_body) > length_of_snake:
            del snake_body[0]

        # Проверка столкновения головы с собственным телом
        for x in snake_body[:-1]:
            if x == snake_head:
                game_close = True

        # Отрисовка змейки
        for segment in snake_body:
            pygame.draw.rect(SCREEN, GREEN, [segment[0], segment[1], SNAKE_BLOCK, SNAKE_BLOCK])

        show_stats(score, level)
        pygame.display.update()

        #Логика поедания еды и уровней
        if x1 == food_x and y1 == food_y:
            food_x, food_y = generate_food(snake_body)
            length_of_snake += 1
            score += 1
            
            #Переход на новый уровень каждые 5 еды
            if score % 5 == 0:
                level += 1
                snake_speed += 3 
                print(f"Level Up! Current speed: {snake_speed}")

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()