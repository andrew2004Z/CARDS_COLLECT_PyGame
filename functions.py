import os
import random
import sys
import datetime
import pygame
from pygame.locals import *
import entities
from copy import deepcopy
import datetime

# Показ текста


def show_text(text, X, Y, Spacing, WidthLimit, Font, surface, double=1, overflow='normal'):
    text += ' '
    OriginalX = X
    OriginalY = Y
    CurrentWord = ''
    if overflow == 'normal':
        for char in text:
            if char not in [' ', '\n']:
                try:
                    Image = Font[str(char)][1]
                    CurrentWord += str(char)
                except KeyError:
                    pass
            else:
                WordTotal = 0
                for char2 in CurrentWord:
                    WordTotal += Font[char2][0]
                    WordTotal += Spacing
                if WordTotal + X - OriginalX > WidthLimit:
                    X = OriginalX
                    Y += Font['Height']
                for char2 in CurrentWord:
                    Image = Font[str(char2)][1]
                    surface.blit(pygame.transform.scale(Image, (Image.get_width(
                    ) * double, Image.get_height() * double)), (X * double, Y * double))
                    X += Font[char2][0]
                    X += Spacing
                if char == ' ':
                    X += Font['A'][0]
                    X += Spacing
                else:
                    X = OriginalX
                    Y += Font['Height']
                CurrentWord = ''
            if X-OriginalX > WidthLimit:
                X = OriginalX
                Y += Font['Height']
        return X, Y
    if overflow == 'cut all':
        for char in text:
            if char not in [' ', '\n']:
                try:
                    Image = Font[str(char)][1]
                    surface.blit(pygame.transform.scale(Image, (Image.get_width(
                    ) * double, Image.get_height() * double)), (X * double, Y * double))
                    X += Font[str(char)][0]
                    X += Spacing
                except KeyError:
                    pass
            else:
                if char == ' ':
                    X += Font['A'][0]
                    X += Spacing
                if char == '\n':
                    X = OriginalX
                    Y += Font['Height']
                CurrentWord = ''
            if X - OriginalX > WidthLimit:
                X = OriginalX
                Y += Font['Height']
        return X, Y

# Генерация шрифта


def generate_font(FontImage, FontSpacingMain, TileSize, TileSizeY, color):
    FontSpacing = deepcopy(FontSpacingMain)
    FontOrder = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
                 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                 'w', 'x', 'y', 'z', '.', '-', ',', ':', '+', '\'', '!', '?', '0', '1', '2', '3',
                 '4', '5', '6', '7', '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"',
                 '<', '>', ';']
    FontImage = pygame.image.load(FontImage).convert()
    NewSurf = pygame.Surface(
        (FontImage.get_width(), FontImage.get_height())).convert()
    NewSurf.fill(color)
    FontImage.set_colorkey((0, 0, 0))
    NewSurf.blit(FontImage, (0, 0))
    FontImage = NewSurf.copy()
    FontImage.set_colorkey((255, 255, 255))
    num = 0
    for char in FontOrder:
        FontImage.set_clip(pygame.Rect(
            ((TileSize + 1) * num), 0, TileSize, TileSizeY))
        CharacterImage = FontImage.subsurface(FontImage.get_clip())
        FontSpacing[char].append(CharacterImage)
        num += 1
    FontSpacing['Height'] = TileSizeY
    return FontSpacing

# Работа с эфектами


def ft_effects(effects, spawn_rate_multipliers):
    n = 0
    for effect in effects:
        if paused == False:
            effect[1] -= 1
            if effect[1] <= 0:
                effects.pop(n)
                n -= 1
        if effect[0] == 'rm':
            spawn_rate_multipliers['meteors'] /= 2
        if effect[0] == 'rb':
            spawn_rate_multipliers['bullet'] /= 2
        if effect[0] == 'qd':
            spawn_rate_multipliers['cards'] *= 3
        n += 1

# Поворот изображения


def flip(img):
    return pygame.transform.flip(img, True, False)

# Генерация растений


def generate_plants(plants):
    plant_list = []
    x = -14
    while x < 200:
        x += random.randint(14, 36)
        plant_list.append([x, random.randint(0, len(plants) - 1)])
    return plant_list

# Генерация облаков


def generate_clouds(clouds):
    cloud_list = []
    for i in range(random.randint(10, 15)):
        cloud_list.append([random.randint(-30, 190), random.randint(2,
                                                                    100), random.randint(0, len(clouds) - 1)])
    return cloud_list

# Подгрузка изображения


def load_img(path):
    img = pygame.image.load('data/images/' + path + '.png').convert()
    img.set_colorkey((255, 255, 255))
    return img

# Подгрузка музыки


def load_snd(name):
    return pygame.mixer.Sound('data/sfx/' + name + '.wav')

# Взависимости от даты генерируем графику


def get_date(date):
    if date[1] == '10' and date[2] == '31':
        return 'Halloween'
    elif date[1] == '01':
        return 'New year'
    elif date[1] == '02':
        return 'Winter'
    elif date[1] == '03' or date[1] == '12':
        return 'Winter_mini'
    elif date[1] == '04' or date[1] == '05':
        return 'Spring'
    elif date[1] == '06' or date[1] == '07':
        return 'Summer'
    elif date[1] == '08':
        return 'Summer_hot'
    elif date[1] == '09' or date[1] == '10' or date[1] == '11':
        return 'Autumn'

# Генерация частиц


def ft_parcticles(particles, display):
    n = 0
    for particle in particles:
        particle[0] += particle[2]
        particle[1] += particle[3]
        display.set_at((int(particle[0]), int(particle[1])), particle[4])
        particle[5] -= 1
        if particle[5] <= 0:
            particles.pop(n)
            n -= 1
        n += 1
