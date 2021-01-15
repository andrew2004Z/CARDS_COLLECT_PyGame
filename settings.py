import os
import random
import sys
import datetime
import pygame
from pygame.locals import *
import entities
from functions import *
import datetime
from functions import *

# Настройки окна
date = str(datetime.date.today()).split('-')
x = 15
y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"
mainClock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption('Cards COLLECT')
WINDOWWIDTH = 1080
WINDOWHEIGHT = 720
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
display = pygame.Surface((200, 150))
# Добавление графики ----------------------------------------------------- #
date_info = get_date(str(datetime.date.today()).split('-'))
if date_info == 'Winter':
    ground_img = load_img('ground/ground3')
elif date_info == 'Winter_mini':
    ground_img = load_img('ground/ground2')
elif date_info == 'Summer':
    ground_img = load_img('ground/ground1')
elif date_info == 'Summer_hot':
    ground_img = load_img('ground/ground4')
elif date_info == 'New year':
    ground_img = load_img('ground/ground5')
else:
    ground_img = load_img('ground/ground')

player_standing = load_img('player/standing1')
player_jumping = load_img('player/jumping1')
player_dead = load_img('player/dead1')
plant_images = entities.load_sequence(
    'data/images/plant/plant_', 5)  # Картинки растений
cloud_images = entities.load_sequence(
    'data/images/cloud/cloud_', 5)  # Картинки облаков
jump_anim = entities.load_sequence('data/images/vfx/jump/', 7)  # Группа прыжка
turn_anim = entities.load_sequence(
    'data/images/vfx/turn/', 6)  # Группа поворота
sun, sun2 = load_img('sun/sun'), load_img('sun/sun2')  # Картинки солнца
# Метеориты
meteor_1 = load_img('meteor/meteor_4')
meteor_1_trail = load_img('meteor/meteor_4_trail')
meteor_2 = load_img('meteor/meteor_3')
meteor_2_trail = load_img('meteor/meteor_3_trail')
bullet_img = load_img('bullet')  # Пули
# Картинки карт
card_item_img = load_img('card_1')
card_item_img2 = load_img('card2')
card_back = load_img('card_back_1')
# Остальная графика
description = load_img('description_1')
select = load_img('select_1')
cancel = load_img('cancel_1')
heart = load_img('heart')
score_box = load_img('score_box_1')
death_img = load_img('death_1')
spikes = [load_img('spikes/spikes_1'),
          load_img('spikes/spikes_2'), load_img('spikes/spikes_3')]
tumbleweed = [load_img('tumbleweed/tumbleweed_1'), load_img(
    'tumbleweed/tumbleweed_2'), load_img('tumbleweed/tumbleweed_3')]
z_img = load_img('z1')
platform_img = load_img('platform')
instructions_img = load_img('instructions_1')
# Аудио ------------------------------------------------------ #
card_0_s = load_snd('card_0')
card_1_s = load_snd('card_1')
meteor_s = load_snd('meteor')
bullet_s = load_snd('bullet')
hurt_s = load_snd('hurt')
card_0_s.set_volume(0.4)
card_1_s.set_volume(0.25)
pygame.mixer.music.load('data/music/main.wav')
# Цвет фона ----------------------------------------------------- #
BACKGROUND = (102, 0, 255)
# Шрифт ------------------------------------------------------- #
font_dat = {'A': [3], 'B': [3], 'C': [3], 'D': [3], 'E': [3], 'F': [3], 'G': [3], 'H': [3], 'I': [3],
            'J': [3], 'K': [3], 'L': [3], 'M': [5], 'N': [3], 'O': [3], 'P': [3], 'Q': [3], 'R': [3],
            'S': [3], 'T': [3], 'U': [3], 'V': [3], 'W': [5], 'X': [3], 'Y': [3], 'Z': [3],
            'a': [3], 'b': [3], 'c': [3], 'd': [3], 'e': [3], 'f': [3], 'g': [3], 'h': [3], 'i': [1],
            'j': [2], 'k': [3], 'l': [3], 'm': [5], 'n': [3], 'o': [3], 'p': [3], 'q': [3], 'r': [2],
            's': [3], 't': [3], 'u': [3], 'v': [3], 'w': [5], 'x': [3], 'y': [3], 'z': [3],
            '.': [1], '-': [3], ',': [2], ':': [1], '+': [3], '\'': [1], '!': [1], '?': [3],
            '0': [3], '1': [3], '2': [3], '3': [3], '4': [3], '5': [3], '6': [3], '7': [3], '8': [3], '9': [3],
            '(': [2], ')': [2], '/': [3], '_': [5], '=': [3], '\\': [3], '[': [2], ']': [2], '*': [3], '"': [3], '<': [3], '>': [3], ';': [1]}
font = generate_font('data/fonts/small_font.png', font_dat, 5, 8, (1, 1, 1))
font_2 = generate_font('data/fonts/small_font.png', font_dat, 5, 8, (1, 1, 1))
# Переменные -------------------------------------------------- #
player = entities.entity(100, 129, 8, 14)
player_walking = entities.animation(
    [[0, 2], [1, 2], [2, 2], [3, 2]], 'data/images/player/walking/walking_1_', ['loop'])
player_key = player_walking.start(player.x, player.y)
player_grav = 0
right = False
left = False
last_dir = 'r'
jumps = 1
air_time = 0
health = 3
invincibility = 0
base_walls = [[-10, 0, 10, 150], [200, 0, 10, 150], [0, 143, 200, 7]]
plants = generate_plants(plant_images)  # Генерация растений на фоне
clouds = generate_clouds(cloud_images)  # Генерация облаков на фоне
base_spawn_rates = {'meteors': 2, 'bullet': 0, 'tumbleweed': 0}
spawn_rates = base_spawn_rates.copy()
spawn_rate_multipliers = {'meteors': 1,
                          'cards': 1, 'bullet': 1, 'tumbleweed': 1}
projectiles = []
static_images = []
circle_particles = []
base_cards = ['1 point', '1 point', '1 point', '1 point', 'double jump 5s', 'double jump 5s', 'double jump 5s', 'double jump 5s',
              'invincible 3s', 'speed 5s', 'double jump 5s',
              'invincible 3s', 'speed 5s', 'speed 5s', 'speed 5s']
cards = base_cards.copy()
card_types = ['reduce bullets 10s', 'speed 5s', 'triple jump 10s', 'platform', 'quick draw 5s',
              'reduce meteorites 10s', 'double jump 5s', 'invincible 3s', 'heal', '1 point']
card_chances = {'reduce bullets 10s': 1, 'speed 5s': 2, 'triple jump 10s': 1, 'platform': 4, 'quick draw 5s': 2,
                'reduce meteorites 10s': 2, 'double jump 5s': 3, 'invincible 3s': 2, 'heal': 3, '1 point': 100}
card_images = {}
deck = cards.copy()
hand = []
for card in card_types:
    # Генерация изображеницй карт
    card_images[card] = load_img('cards/' + card)
card_visuals = []
box_pos = 200
select_pos = -75
cancel_pos = -75
hovered_card = 0
paused = False
pause_cooldown = 0
card_items = []
particles = []
sun_timer = 0
score = 0
goal = 3
death_pos = -30
death_target = -30
time_since_card = 0
level = 1
z_pos = 200
z_pressed = False
jump_cap = [1, 0]
effects = []
fade = 0
dead_timer = -1
level_name = ['10:00AM - Day 1', 0]
spike_timer = 0
platforms = []
speed_multiplier = [1, 0]
animations = []
moved = False
instructions_pos = 200
instructions_target = 50
sun_pos = [18, 40]
# Музыка ------------------------------------------------------- #
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.45)
