import os
import random
import sys
import datetime
import pygame
from pygame.locals import *
import entities
import datetime
from functions import *
from settings import *


while True:
    # Фон --------------------------------------------- #
    if level_name[0][:2] == '10':
        sun_pos = [18, 40]
    elif level_name[0][:2] == '11':
        sun_pos = [100, 20]
    else:
        sun_pos = [195, 10]
    if hovered_card < 0:
        hovered_card = 0
    mx, my = pygame.mouse.get_pos()
    spawn_rate_multipliers = {'meteors': 1,
                              'cards': 1, 'bullet': 1, 'tumbleweed': 1}
    mx = int(mx / (WINDOWWIDTH / 200))
    my = int(my / (WINDOWHEIGHT / 150))
    tiles = base_walls.copy()
    for platform in platforms:
        tiles.append(platform)
    display.fill(BACKGROUND)
    display.blit(ground_img, (0, 143))
    sun_timer += 1
    # Солнце
    if sun_timer == 16:
        sun_timer = 0
    if sun_timer < 8:
        display.blit(sun, sun_pos)
    else:
        display.blit(sun2, sun_pos)
    for cloud in clouds:
        display.blit(cloud_images[cloud[2]], (cloud[0], cloud[1]))
    for plant in plants:
        height = plant_images[plant[1]].get_height()
        display.blit(plant_images[plant[1]], (plant[0], 143 - height))
    # Эффекты ------------------------------------------------ #
    ft_effects(effects, spawn_rate_multipliers)
    # Спавн ------------------------------------------------- #
    if paused == False:
        for hazard in spawn_rates:
            for i in range(int(spawn_rates[hazard] * spawn_rate_multipliers[hazard])):
                if random.randint(1, 600) == 1:
                    if hazard == 'meteors':
                        projectiles.append([random.choice(['meteor1', 'meteor2']), random.randint(
                            0, 200), -10, random.randint(0, 2) - 1, random.randint(2, 3), 0])
                    if hazard == 'bullet':
                        bullet_s.play()
                        direction = random.choice(['r', 'l'])
                        if direction == 'r':
                            x = 200
                            x_vel = -4
                        else:
                            x = -20
                            x_vel = 4
                        projectiles.append(
                            ['bullet', x, random.randint(20, 140), x_vel, 0])
                    if hazard == 'tumbleweed':
                        projectiles.append(['tumbleweed', 200, random.randint(
                            50, 130), random.randint(0, 1) - 2, 1, 0])
    # Анимация --------------------------------------------- #
    n = 0
    for anim in animations:
        # Анимация прыжка
        if anim[0] == 'jump':
            try:
                display.blit(jump_anim[int(anim[3])], (anim[1], anim[2]))
            except IndexError:
                animations.pop(n)
                n -= 1
        # Анимация поворота
        if anim[0] == 'turn':
            try:
                if anim[5] == False:
                    display.blit(turn_anim[int(anim[3])], (anim[1], anim[2]))
                else:
                    display.blit(
                        flip(turn_anim[int(anim[3])]), (anim[1], anim[2]))
            except IndexError:
                animations.pop(n)
                n -= 1
        if paused == False:
            anim[3] += anim[4]
        n += 1
    # Платформы ---------------------------------------------- #
    for platform in platforms:
        display.blit(platform_img, (platform[0], platform[1]))
    # Шипы ------------------------------------------------- #
    if paused == False:
        if spike_timer == 0:
            if random.randint(1, 800) == 1:
                spike_timer = 65
        else:
            spike_timer -= 1
    if spike_timer > 15:
        display.blit(spikes[0], (0, 139))
    elif spike_timer > 6:
        display.blit(spikes[2], (0, 139))
        spikesR = pygame.Rect(0, 139, 200, 4)
        if spikesR.colliderect(player.obj.rect):
            if invincibility == 0:
                hurt_s.play()
                health -= 1
                if health < 0:
                    health = 0
                invincibility = 30
    elif spike_timer > 3:
        display.blit(spikes[1], (0, 139))
    elif spike_timer > 0:
        display.blit(spikes[0], (0, 139))
    # Элементы Карты --------------------------------------------- #
    if paused == False:
        # Появление карт
        if len(deck) - len(card_items) > 0:
            time_since_card += 1
            if (random.randint(1, int(300 / spawn_rate_multipliers['cards'])) == 1) or (time_since_card > 300):
                x = random.randint(1, 194)
                y = random.randint(50, 134)
                dis = abs(x - player.x) + abs(y - player.y)
                if dis > 20:
                    time_since_card = 0
                    card_items.append([x, y, 0, 400])
                    card_0_s.play()
    n = 0
    for card in card_items:
        if (card[3] < 396) and (card[3] > 2):
            display.blit(card_item_img, (card[0], card[1] + int(card[2] / 20)))
        else:
            display.blit(card_item_img2,
                         (card[0], card[1] + int(card[2] / 20)))
        popped = False
        if paused == False:
            card[2] += 1
            if card[2] == 40:
                card[2] = 0
            card[3] -= 1
            if card[3] == 0:
                card_items.pop(n)
                n -= 1
                popped = True
        if card[3] > 2:
            if len(hand) < 5:
                cardR = pygame.Rect(card[0], card[1], 5, 7)
                if player.obj.rect.colliderect(cardR):
                    card[3] = 2
                    n -= 1
                    draw = random.randint(0, len(deck)-1)
                    hand.append(deck[draw])
                    deck.pop(draw)
                    card_1_s.play()
        n += 1
    # Частицы ---------------------------------------------- #
    ft_parcticles(particles, display)
    # Статические изображения ------------------------------------------ #
    for img in static_images:
        if img[0] == 'meteor1':
            display.blit(meteor_1_trail, (img[1], img[2]))
        elif img[0] == 'meteor2':
            display.blit(meteor_2_trail, (img[1], img[2]))
        img[1] += img[4]
        img[2] += img[5]
        img[3] -= 1
        if img[3] <= 0:
            try:
                static_images.pop(n)
                n -= 1
            except:
                pass
        n += 1
    # Игрок ------------------------------------------------- #
    if dead_timer > 0:
        dead_timer -= 1
    if health < 1:
        paused = False
        if dead_timer == -1:
            dead_timer = 80
    if speed_multiplier[0] != 1:
        speed_multiplier[1] -= 1
        if speed_multiplier[1] <= 0:
            speed_multiplier[0] = 1
    if paused == False:
        if jump_cap[0] != 1:
            jump_cap[1] -= 1
            if jump_cap[1] < 1:
                jump_cap = [1, 0]
        if invincibility > 0:
            invincibility -= 1
        air_time += 1
        player_grav += 0.25
    if player_grav > 3:
        player_grav = 3
    p_momentum = [0, player_grav]
    if dead_timer == -1:
        if right == True:
            p_momentum[0] += 2 * speed_multiplier[0]
        if left == True:
            p_momentum[0] -= 2 * speed_multiplier[0]
    # Проверка на последнее действие
    if paused == False:
        if p_momentum[0] > 0:
            if last_dir == 'l':
                animations.append(
                    ['turn', player.x - 2, player.y + 6, 0, 0.5, False])
            last_dir = 'r'
        elif p_momentum[0] < 0:
            if last_dir == 'r':
                animations.append(
                    ['turn', player.x - 2, player.y + 6, 0, 0.5, True])
            last_dir = 'l'
    if paused == True:
        p_momentum = [0, 0]
    else:
        p_collisions = player.move(p_momentum, tiles)
    if speed_multiplier[0] != 1:
        if p_momentum[0] != 0:
            if last_dir == 'r':
                particles.append([player.x + 2, player.y + 13, -random.randint(
                    1, 2) / 4, -random.randint(0, 4) / 4, (177, 158, 141), random.randint(2, 3)])
            else:
                particles.append([player.x + 2, player.y + 13, random.randint(
                    1, 2) / 4, -random.randint(0, 4) / 4, (177, 158, 141), random.randint(2, 3)])
    show = True
    if invincibility > 0:
        if random.randint(1, 3) == 1:
            show = False
    if p_collisions['bottom'] == True:
        player_grav = 0
        jumps = jump_cap[0]
        air_time = 0
    player.update_animation(player_walking, player_key)
    if dead_timer == -1:
        if show == True:
            if air_time > 3:
                if last_dir == 'r':
                    display.blit(player_jumping, (player.x, player.y))
                else:
                    display.blit(flip(player_jumping), (player.x, player.y))
            else:
                if p_momentum[0] > 0:
                    player_walking.play(player_key, display)
                elif p_momentum[0] < 0:
                    player_walking.play(player_key, display, True)
                elif last_dir == 'r':
                    display.blit(player_standing, (player.x, player.y))
                else:
                    display.blit(flip(player_standing), (player.x, player.y))
    else:
        if last_dir == 'r':
            display.blit(player_dead, (player.x, player.y))
        else:
            display.blit(flip(player_dead), (player.x, player.y))
    if player.y < 4:
        player.y = 4
        player.obj.y = 4
        player.obj.rect.y = 4
    # Частцы --------------------------------------- #
    n = 0
    for p in circle_particles:
        if paused == False:
            p[0] += p[2]
            p[1] += p[3]
            if p[2] > 0:
                p[2] -= 0.1
            elif p[2] < 0:
                p[2] += 0.1
            p[3] += 0.2
            p[4] -= 0.1
        r = pygame.draw.circle(
            display, p[5], (int(p[0]), int(p[1])), int(p[4]))
        popped = False
        if player.obj.rect.colliderect(r):
            if invincibility == 0:
                hurt_s.play()
                health -= 1
                if health < 0:
                    health = 0
                if invincibility < 30:
                    invincibility = 30
                popped = True
                circle_particles.pop(n)
                n -= 1
        if p[4] <= 1:
            if popped == False:
                circle_particles.pop(n)
                n -= 1
        n += 1
    # Снаряды -------------------------------------------- #
    n = 0
    for proj in projectiles:
        # Метеориты
        if proj[0][:6] == 'meteor':
            proj[5] += 1
            if proj[5] == 4:
                proj[5] = 0
                if paused == False:
                    static_images.append(
                        [proj[0], proj[1], proj[2], 2, proj[3], proj[4]])
                if proj[0][-1] == '1':
                    proj[0] = 'meteor2'
                else:
                    proj[0] = 'meteor1'
            if proj[0][-1] == '1':
                display.blit(meteor_1, (proj[1], proj[2]))
            else:
                display.blit(meteor_2, (proj[1], proj[2]))
            if paused == False:
                proj[1] += proj[3]
                proj[2] += proj[4]
            projR = pygame.Rect(proj[1], proj[2], 6, 6)
            popped = False
            if projR.colliderect(player.obj.rect):
                if invincibility == 0:
                    meteor_s.play()
                    hurt_s.play()
                    health -= 1
                    if health < 0:
                        health = 0
                    for i in range(4):
                        circle_particles.append([proj[1] + 2, proj[2] + 2, random.randint(
                            0, 4) - 2, -1.7, random.randint(4, 6), random.choice([(185, 57, 57), (119, 61, 60)])])
                    if invincibility < 30:
                        invincibility = 30
                    popped = True
                    projectiles.pop(n)
                    n -= 1
            for tile in tiles:
                tileR = pygame.Rect(tile[0], tile[1], tile[2], tile[3])
                if tileR.colliderect(projR):
                    meteor_s.play()
                    for i in range(4):
                        circle_particles.append([proj[1] + 2, proj[2] + 2, random.randint(
                            0, 4) - 2, -1.7, random.randint(4, 6), random.choice([(185, 57, 57), (119, 61, 60)])])
                    if popped == False:
                        try:
                            projectiles.pop(n)
                        except:
                            pass
                        n -= 1
        # Пуля
        if proj[0] == 'bullet':
            if paused == False:
                bulletR = pygame.Rect(proj[1], proj[2], 6, 4)
                if bulletR.colliderect(player.obj.rect):
                    if invincibility == 0:
                        hurt_s.play()
                        health -= 1
                        if health < 0:
                            health = 0
                        if invincibility < 30:
                            invincibility = 30
            if proj[3] > 0:
                display.blit(bullet_img, (proj[1], proj[2]))
                for i in range(4):
                    particles.append([proj[1], proj[2] + random.randint(0, 3), -(random.randint(
                        3, 6) / 4), (random.randint(0, 8) - 4) / 5, (177, 158, 141), random.randint(2, 3)])
                if proj[1] > 200:
                    projectiles.pop(n)
                    n -= 1
            else:
                display.blit(flip(bullet_img), (proj[1], proj[2]))
                for i in range(4):
                    particles.append([proj[1] + 6, proj[2] + random.randint(0, 3), random.randint(
                        3, 6) / 4, (random.randint(0, 8) - 4) / 5, (177, 158, 141), random.randint(2, 3)])
                if proj[1] < -20:
                    projectiles.pop(n)
                    n -= 1
            if paused == False:
                proj[1] += proj[3]
                proj[2] += proj[4]
        # Перекати-поле
        if proj[0] == 'tumbleweed':
            projR = pygame.Rect(proj[1], proj[2], 8, 8)
            if paused == False:
                proj[1] += proj[3]
                proj[2] += proj[4]
                proj[4] += 0.2
                bounce = False
                for tile in tiles:
                    tileR = pygame.Rect(tile[0], tile[1], tile[2], tile[3])
                    if tileR.colliderect(projR):
                        if bounce == False:
                            if proj[4] > 0:
                                proj[4] = -proj[4]
                                if proj[4] < -5:
                                    proj[4] = -5
                            bounce = True
            if projR.colliderect(player.obj.rect):
                if invincibility == 0:
                    hurt_s.play()
                    health -= 1
                    if health < 0:
                        health = 0
                    invincibility = 30
            proj[5] += 1
            if proj[5] == 9:
                proj[5] = 0
            if proj[5] < 3:
                display.blit(tumbleweed[0], (proj[1], proj[2]))
            elif proj[5] < 6:
                display.blit(tumbleweed[1], (proj[1], proj[2]))
            else:
                display.blit(tumbleweed[2], (proj[1], proj[2]))
            if proj[1] < -20:
                projectiles.pop(n)
                n -= 1
        n += 1
    # Графика ----------------------------------------------------- #
    for x in range(health):
        display.blit(heart, (2 + x * 7, 2))

    display.blit(score_box, (175, 2))
    show_text(str(score) + '/' + str(goal), 181, 7, 1, 185, font_2, display)
    overlay_surf = pygame.Surface((200, 150))

    if paused == False:
        if pause_cooldown > 0:
            pause_cooldown -= 1
        good = True
        for card in card_visuals:
            if card[2] < 150:
                good = False
        if good == True:
            card_visuals = []
            hovered_card = 0
    elif card_visuals == []:
        x = 0.05
        for card in hand:
            # id, x, y
            card_visuals.append([card, x * 40, 150])
            x += 1
    n = 0
    for card in card_visuals:
        overlay_surf.blit(card_back, (card[1], int(card[2])))
        overlay_surf.blit(card_images[card[0]], (card[1], int(card[2])))
        if paused == True:
            target_y = 120
            if n == hovered_card:
                target_y = 90
                display.blit(card_back, (card[1], int(card[2])))
                display.blit(card_images[card[0]], (card[1], int(card[2])))
        else:
            target_y = 160
        card[2] += (target_y - card[2]) / 6
        n += 1
    if card_visuals != []:
        overlay_surf.blit(description, (box_pos, 39))
        show_text(card_visuals[hovered_card][0],
                  box_pos + 5, 42, 1, 185, font_2, overlay_surf)
    if paused == False:
        target_x = 220
    else:
        target_x = 82
    box_pos += (target_x - box_pos) / 4
    if paused == False:
        target_x = -80
    else:
        target_x = 4
    instructions_target = 220
    if moved == False:
        instructions_target = 50
    instructions_pos += (instructions_target-instructions_pos) / 6
    display.blit(instructions_img, (instructions_pos, 26))
    target = 210
    if level == 1:
        if hand != []:
            if z_pressed == False:
                target = 180
    z_pos += (target - z_pos) / 6
    display.blit(z_img, (z_pos, 76))
    cancel_pos += (target_x - cancel_pos) / 6
    select_pos += (target_x - select_pos) / 4
    overlay_surf.blit(cancel, (cancel_pos, 60))
    overlay_surf.blit(select, (select_pos, 40))
    overlay_surf.set_colorkey((0, 0, 0))
    overlay_surf.set_alpha(500)
    display.blit(overlay_surf, (0, 0))
    death_pos += (death_target-death_pos) / 4
    display.blit(death_img, (80, death_pos))

    if level_name[1] < 60:
        if level_name[1] < 10:
            opacity = level_name[1] * 25.5
        elif level_name[1] > 50:
            opacity = 255-(level_name[1] - 50) * 25.5
        else:
            opacity = 255
        surf = pygame.Surface((200, 150))
        surf.set_colorkey((0, 0, 0))
        surf.set_alpha(opacity)
        show_text(
            level_name[0], 100 - int(len(level_name[0]) / 2) * 4, 50, 1, 185, font, surf)
        display.blit(surf, (0, 0))
        level_name[1] += 1

    if fade > 0:
        fade -= 25
        fade_surf = pygame.Surface((200, 150))
        fade_surf.fill((219, 210, 202))
        fade_surf.set_alpha(fade)
        display.blit(fade_surf, (0, 0))
    # Обработка кнопок ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # Управление
        if event.type == KEYDOWN:
            # Направо
            if event.key == K_RIGHT or event.key == K_d:
                right = True
                if paused == True:
                    hovered_card += 1
                    if hovered_card > len(card_visuals) - 1:
                        hovered_card = len(card_visuals) - 1
                    else:
                        card_1_s.play()  # Звук для карты
                moved = True
            # Налево
            if event.key == K_a or event.key == K_LEFT:
                left = True
                if paused == True:
                    hovered_card -= 1
                    if hovered_card < 0:
                        hovered_card = 0
                    else:
                        card_1_s.play()  # Звук для карты
                moved = True
            # Прыжок
            if event.key == K_w or event.key == K_UP or event.key == K_SPACE:
                if dead_timer == -1:
                    if jumps > 0:
                        animations.append(
                            ['jump', player.x - 2, player.y + 6, 0, 0.5, False])
                        jumps -= 1
                        player_grav = -5
                        air_time = 4
                        moved = True
            # Отображение карт после нажатия на кнопку "z"
            if event.key == K_z:
                if hand != []:
                    z_pressed = True
                if paused == False:
                    if pause_cooldown == 0:
                        paused = True
                        pause_cooldown = 40
                else:
                    paused = False
            # Выбор карты после нажатия на кнопку "x"
            if event.key == K_x:
                if paused == True:
                    if hand != []:
                        card_1_s.play()
                        used = hand[hovered_card]
                        if used == '1 point':
                            score += 1
                        elif used == 'double jump 5s':
                            jump_cap = [2, 200]
                            jumps += 1
                        elif used == 'heal':
                            health += 1
                            if health > 3:
                                health = 3
                        elif used == 'invincible 3s':
                            invincibility += 120
                        elif used == 'reduce meteorites 10s':
                            effects.append(['rm', 400])
                        elif used == 'reduce bullets 10s':
                            effects.append(['rb', 400])
                        elif used == 'quick draw 5s':
                            effects.append(['qd', 200])
                        elif used == 'platform':
                            platforms.append(
                                [player.x - 8, player.y - 10, 25, 7])
                        elif used == 'triple jump 10s':
                            jump_cap = [3, 400]
                            jumps += 2
                        elif used == 'speed 5s':
                            speed_multiplier = [1.5, 200]
                        hand.pop(hovered_card)
                        paused = False
        if event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_d:
                right = False
            if event.key == K_LEFT or event.key == K_a:
                left = False
    # Обновление ------------------------------------------------- #
    screen.blit(pygame.transform.scale(
        display, (WINDOWWIDTH, WINDOWHEIGHT)), (0, 0))
    pygame.display.update()
    mainClock.tick(40)
    # Переход уровней --------------------------------------- #
    if score == goal:  # Если набрано нужное количество очков
        invincible = 2
        pick_stage = 0
        if card_visuals == []:
            card_options = []
            for card in card_chances:
                for i in range(card_chances[card]):
                    card_options.append(card)
            new_cards = [random.choice(card_options), random.choice(
                card_options)]  # Выбор рандомных карт
            swap_cards = []
            # Генерируеться три карты
            while len(swap_cards) < 3:
                swap = random.choice(cards)
                if swap != '1 point':
                    swap_cards.append(swap)
                else:
                    c = 0
                    for card in cards:
                        if card == '1 point':
                            c += 1
                    if c >= 6:
                        swap_cards.append(swap)
            transition = True
            screenshot = display.copy()
            t = 0
            info_pos = -30
            info_target = -30
            desc_pos = 200
            desc_target = 220
            pygame.mixer.music.set_volume(0.2)
            while transition:
                if hovered_card < 0:
                    hovered_card = 0
                display.blit(screenshot, (0, 0))
                fade_surf = pygame.Surface((200, 150))
                fade_surf.fill((219, 210, 202))
                fade_surf.set_alpha(t)
                t += 5
                if t > 255:
                    t = 255
                    if pick_stage == 0:
                        pick_stage = 1
                        card_visuals = []
                        for card in new_cards:
                            card_visuals.append([card, 150])
                        hovered_card = 0
                display.blit(fade_surf, (0, 0))
                # Проверка на стадию выбора карты
                if pick_stage == 1:
                    info_target = 2
                    desc_target = 50
                    display.blit(description, (50, info_pos))
                    show_text('Choose a new card.', 55, info_pos +
                              4, 1, 200, font_2, display)
                    n = 0
                    for card in card_visuals:
                        target = 120
                        if n == hovered_card:
                            target = 90
                        card[1] += (target-card[1])/5
                        display.blit(card_back, (60 + n * 40, card[1]))
                        display.blit(
                            card_images[card[0]], (60 + n * 40, card[1]))
                        n += 1
                elif pick_stage == 2:
                    info_target = 2
                    display.blit(description, (50, info_pos))
                    show_text('Choose a new card.', 55, info_pos + 4,
                              1, 200, font_2, display)  # Текст для выбора карт
                    n = 0
                    for card in card_visuals:
                        target = 160
                        card[1] += (target-card[1]) / 5
                        display.blit(card_back, (60 + n * 40, card[1]))
                        display.blit(
                            card_images[card[0]], (60 + n * 40, card[1]))
                        n += 1
                    done = True
                    for card in card_visuals:
                        if card[1] < 150:
                            done = False
                    if done == True:
                        pick_stage = 3
                        card_visuals = []
                        for card in swap_cards:
                            card_visuals.append([card, 150])
                        hovered_card = 0
                elif pick_stage == 3:
                    info_target = 2
                    display.blit(description, (50, info_pos))
                    show_text('Choose a card to lose.', 55,
                              info_pos + 4, 1, 200, font_2, display)
                    n = 0
                    for card in card_visuals:
                        target = 120
                        if n == hovered_card:
                            target = 90
                        card[1] += (target - card[1]) / 5
                        display.blit(card_back, (40 + n * 40, card[1]))
                        display.blit(
                            card_images[card[0]], (40 + n * 40, card[1]))
                        n += 1
                elif pick_stage == 4:
                    info_target = -30
                    display.blit(description, (50, info_pos))
                    show_text('Choose a card to lose.', 55,
                              info_pos + 4, 1, 200, font_2, display)
                    n = 0
                    desc_target = 220
                    for card in card_visuals:
                        target = 160
                        card[1] += (target-card[1])/5
                        display.blit(card_back, (40 + n * 40, card[1]))
                        display.blit(
                            card_images[card[0]], (40 + n * 40, card[1]))
                        n += 1
                    done = True
                    for card in card_visuals:
                        if card[1] < 150:
                            done = False
                    if done == True:
                        pick_stage = 5
                info_pos += (info_target-info_pos)/4
                desc_pos += (desc_target-desc_pos)/3
                display.blit(description, (desc_pos, 60))
                if len(card_visuals) > hovered_card:
                    show_text(card_visuals[hovered_card][0],
                              desc_pos + 5, 65, 1, 200, font_2, display)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == K_RIGHT:
                            hovered_card += 1
                            if hovered_card > len(card_visuals) - 1:
                                hovered_card = len(card_visuals) - 1
                            else:
                                card_1_s.play()
                        if event.key == K_LEFT:
                            hovered_card -= 1
                            if hovered_card < 0:
                                hovered_card = 0
                            else:
                                card_1_s.play()
                        if event.key == K_x:
                            if pick_stage == 1:
                                new_card = card_visuals[hovered_card][0]
                                pick_stage = 2
                                card_1_s.play()
                            elif pick_stage == 3:
                                remove_card = card_visuals[hovered_card][0]
                                pick_stage = 4
                                card_1_s.play()
                screen.blit(pygame.transform.scale(
                    display, (WINDOWWIDTH, WINDOWHEIGHT)), (0, 0))
                pygame.display.update()
                mainClock.tick(40)
                if pick_stage == 5:
                    transition = False
            cards.remove(remove_card)
            cards.append(new_card)
            card_visuals = []
            paused = False
            pause_cooldown = 0
            health = 3  # Количество жизней на следующий уровень
            # Генерируються растения для следущего уровня
            plants = generate_plants(plant_images)
            # Генерируються облака для следущего уровня
            clouds = generate_clouds(cloud_images)
            projectiles = []
            static_images = []
            circle_particles = []
            deck = cards.copy()  # Копируються список карт
            hand = []
            effects = []  # Очищаються эффекты
            dead_timer = -1
            goal = 3  # Сколько нужно собрать очков для следущего уровня
            card_items = []  # Удаляються все собранные карты на предыдущем уровне
            platforms = []  # Удаляються все платвормы предыдущего уровня
            speed_multiplier = [1, 0]
            death_target = -30
            score = 0  # Обнуляеться количество очков
            fade = 255
            level += 1  # Увеличиваеться счетчик уровня
            animations = []
            spike_timer = 0  # Обнуляеться таймер шипов
            # Увеличиваеться шанс спавна метеоритов
            spawn_rates['meteors'] += 1
            spawn_rates['bullet'] += 1  # Увеличиваеться шанс спавна пули
            right = False
            left = False
            pygame.mixer.music.set_volume(0.45)  # Громкость музыки на фоне
            # Формируеться название уровня
            if level % 3 == 1:
                level_name = ['10:00AM - Day ' +
                              str(int((level - (level % 3)) / 3 + 1)), 0]
            elif level % 3 == 2:
                level_name = ['11:00AM - Day ' +
                              str(int((level - (level % 3)) / 3 + 1)), 0]
            else:
                level_name = ['High Noon - Day ' +
                              str(int((level - (level % 3)) / 3 + 1)), 0]
                spawn_rates['meteors'] += 2
                spawn_rates['bullet'] += 1
                spawn_rates['tumbleweed'] += 1
    # Смерть -------------------------------------------------- #
    if dead_timer == 0:
        dead = True
        screenshot = display.copy()
        t = 0
        pygame.mixer.music.set_volume(0.2)
        while dead:
            display.blit(screenshot, (0, 0))
            fade_surf = pygame.Surface((200, 150))
            fade_surf.fill((219, 210, 202))
            fade_surf.set_alpha(t)
            t += 5
            if t > 255:
                t = 255
            display.blit(fade_surf, (0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    dead = False
                if event.type == MOUSEBUTTONDOWN:
                    dead = False
            death_target = 50
            death_pos += (death_target-death_pos) / 4
            display.blit(death_img, (80, death_pos))
            screen.blit(pygame.transform.scale(
                display, (WINDOWWIDTH, WINDOWHEIGHT)), (0, 0))
            pygame.display.update()
            mainClock.tick(40)
        # Возвращение значений к базовым
        spawn_rates = base_spawn_rates.copy()
        paused = False
        pause_cooldown = 0
        health = 3
        cards = base_cards.copy()
        spawn_rates = base_spawn_rates.copy()
        plants = generate_plants(plant_images)
        clouds = generate_clouds(cloud_images)
        projectiles = []
        static_images = []
        circle_particles = []
        deck = cards.copy()
        hand = []
        effects = []
        dead_timer = -1
        goal = 3
        card_items = []
        platforms = []
        speed_multiplier = [1, 0]
        death_target = -30
        score = 0
        fade = 255
        right = False
        left = False
        level = 1
        animations = []
        level_name = ['10:00AM - Day 1', 0]
        spike_timer = 0
        pygame.mixer.music.set_volume(0.45)
