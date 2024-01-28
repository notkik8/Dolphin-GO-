import os
import sys
import pygame
import random
from pygame.locals import *
import math



# Инициализация Pygame
pygame.init()
pygame.font.init()


all_sprites = pygame.sprite.Group()

# Размеры окна
size = width, height = 400, 600

background_image = pygame.image.load('data/bg.png')  # Замените 'background.jpg' на путь к вашему изображению
background_rect = background_image.get_rect()

# подкл фоновой музыки
pygame.mixer.music.load(os.path.join('data', 'music.wav'))
pygame.mixer.music.set_volume(0.1)

# Устанавливаем событие завершения воспроизведения музыки
pygame.mixer.music.set_endevent(pygame.USEREVENT)
pygame.mixer.music.play()

# Зацикливание музыки при её завершении
pygame.event.set_allowed(pygame.USEREVENT)


# Колличество очков
score = 0

screen = pygame.display.set_mode(size)
pygame.display.set_caption("DolphinYo!")
pygame.mouse.set_cursor(*pygame.cursors.tri_left)


Flag = True

# Функция для загрузки изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

dolphin_image = load_image("dolphin.png")
wave_image = load_image("wave.png")



def show_start_screen():
    global Flag, speed, spawn_interval

    screen.fill((0, 0, 0))  # Заливка экрана черным цветом

    # Отображение текста "Press E to Easy mod or H to Hard"
    font = pygame.font.Font('CaptainComicBold.ttf', 36)
    text = font.render("Press E to Easy mod or H to Hard", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)

    # Отображение изображения "start.png"
    start_image = pygame.image.load('data/start.png')
    start_rect = start_image.get_rect(center=(width // 2, height // 2))
    screen.blit(start_image, start_rect)

    pygame.display.flip()

    # Ожидание нажатия клавиши "SPACE"
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_e:
                waiting = False
                Flag = False
                speed = 0.05
                spawn_interval = 1000
            elif event.type == KEYDOWN and event.key == K_h:
                waiting = False
                Flag = False
                speed = 0.25
                spawn_interval = 250
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()


def show_end_screen():
    global Flag, speed, spawn_interval, score




    # Отображение изображения "end.png"
    start_image = pygame.image.load('data/end.png')
    start_rect = start_image.get_rect(center=(width // 2, height // 2))
    screen.blit(start_image, start_rect)

    # Отображение текста "Press E to Easy mod or H to Hard"
    font = pygame.font.Font('CaptainComicBold.ttf', 36)
    text2 = font.render(f"Score: {int(score)}", True, (0, 0, 0))
    text_rect2 = text2.get_rect(center=(width // 2, height // 3))
    screen.blit(text2, text_rect2)





    pygame.display.flip()

    # Ожидание нажатия клавиши
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_e:
                start()
                speed = 0.05
                spawn_interval = 1000
                waiting = False
                Flag = False
            elif event.type == KEYDOWN and event.key == K_h:
                start()
                waiting = False
                Flag = False
                speed = 0.25
                spawn_interval = 250
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()








class Board():
    # Создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # Значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # Настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # Отрисовка поля
    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, (255, 255, 255), (self.left + i * self.cell_size, self.top + j * self.cell_size, self.cell_size, self.cell_size), 1)





class Wave(pygame.sprite.Sprite):
    def __init__(self, column, cell_size, speed=1):
        super().__init__(all_sprites)
        self.column = column
        self.cell_size = cell_size
        self.row = -1
        self.speed = speed
        self.amplitude = 2  # Амплитуда тряски
        self.angle = 0  # Угол для тряски

        # Используем картинку волны
        self.image = wave_image
        self.rect = self.image.get_rect()

        # Устонавливаем позицию волны
        self.rect.topleft = (self.column * self.cell_size, self.row * self.cell_size)

        # Создаем маску для волны
        self.mask = pygame.mask.from_surface(self.image)

    def move_down(self):
        self.row += self.speed
        self.rect.y += self.speed * self.cell_size

        # Добавляем тряску к волне
        self.angle += 1
        self.rect.x += int(self.amplitude * math.sin(self.angle))

    def is_out_of_screen(self, screen_height):
        return self.row * self.cell_size > screen_height

    def draw(self, screen):
        # Успользуем метод blit
        screen.blit(self.image, self.rect.topleft)

    def get_mask(self):
        return self.mask







class Player(pygame.sprite.Sprite):
    def __init__(self, column, cell_size):
        super().__init__(all_sprites)
        self.column = column
        self.cell_size = cell_size
        self.row = height // self.cell_size - 1

        # Используем картинку дельфина
        self.image = dolphin_image
        self.rect = self.image.get_rect()

        # Устонавливаем позицию для дельфина
        self.rect.topleft = (self.column * self.cell_size, self.row * self.cell_size)

        # Создаем маску для игрока
        self.mask = pygame.mask.from_surface(self.image)

    def move_up(self):
        if self.row > 0:
            self.row -= 1
            self.rect.y -= self.cell_size

    def move_down(self):
        if self.row < height // self.cell_size - 1:
            self.row += 1
            self.rect.y += self.cell_size

    def move_left(self):
        if self.column > 0:
            self.column -= 1
            self.rect.x -= self.cell_size

    def move_right(self):
        if self.column < width // self.cell_size - 1:
            self.column += 1
            self.rect.x += self.cell_size

    def draw(self, screen):
        # Успользуем метод blit
        screen.blit(self.image, self.rect.topleft)

    def get_mask(self):
        return self.mask


def start():
    player = Player(2, board.cell_size)

def reset_game():
    global score, waves, all_sprites, player
    score = 0
    waves = []
    all_sprites.empty()  # Удаляем все спрайты
    player = Player(2, board.cell_size)

# Поле 4 на 6
board = Board(4, 6)
board.set_view(0, 0, 100)

player = Player(2, board.cell_size)
waves = []  # Список объектов Wave

clock = pygame.time.Clock()
spawn_timer = 0  # Таймер для спавна волн
spawn_interval = 1000  # Интервал спавна волн в миллисекундах (1 секунда)

running = True

speed = 0.05




while running:
    if Flag:
        show_start_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.move_up()
            elif event.key == pygame.K_s:
                player.move_down()
            elif event.key == pygame.K_a:
                player.move_left()
            elif event.key == pygame.K_d:
                player.move_right()
        elif event.type == pygame.USEREVENT:
        # Событие завершения воспроизведения музыки, воспроизводим её заново
            pygame.mixer.music.play()

    spawn_timer += clock.tick(30)  # Получение прошедшего времени с момента последнего кадра

    if spawn_timer >= spawn_interval:
        # Если прошло достаточно времени, создаем новую волну и сбрасываем таймер
        waves.append(Wave(random.randrange(0, 4), board.cell_size, speed))
        spawn_timer = 0

    for wave in waves:
        wave.move_down()

    # Удаление объектов Wave, которые вышли за пределы экрана
    waves = [wave for wave in waves if not wave.is_out_of_screen(height)]


    board.render(screen)
    screen.blit(background_image, background_rect)



    for wave in waves:
        wave.draw(screen)

    player.draw(screen)

    # Проверка столкновения игрока с волной
    for wave in waves:
        player_mask = player.get_mask()
        wave_mask = wave.get_mask()

        hits = pygame.sprite.collide_mask(wave, player)


        offset = (int(player.column * player.cell_size - wave.column * wave.cell_size),
                  int(player.row * player.cell_size - wave.row * wave.cell_size))

        if hits:
            # Сохранение количества очков в текстовый файл
            with open('score.txt', 'w') as file:
                file.write(str(int(score)))
            show_end_screen()
            reset_game()





        # Увеличение количества очков при жизни игрока
        score += 0.05

        # Отображение количества очков в правом верхнем углу
        font = pygame.font.Font('CaptainComicBold.ttf', 36)
        score_text = font.render(f"Score: {int(score)}", True, (0, 0, 0))
        screen.blit(score_text, (width - 200, 10))


        pygame.display.flip()

pygame.quit()
sys.exit()