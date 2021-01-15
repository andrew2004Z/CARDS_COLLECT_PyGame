import pygame
from pygame.locals import *

# Физика


def CollisionTest(Object1, ObjectList):
    CollisionList = []
    for Object in ObjectList:
        ObjectRect = pygame.Rect(Object[0], Object[1], Object[2], Object[3])
        if ObjectRect.colliderect(Object1):
            CollisionList.append(ObjectRect)
    return CollisionList


class PhysicsObject(object):
    def __init__(self, x, y, x_size, y_size):
        self.width = x_size
        self.height = y_size
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.x = x
        self.y = y

    def Move(self, Movement, platforms):
        self.x += Movement[0]
        self.rect.x = int(self.x)
        block_hit_list = CollisionTest(self.rect, platforms)
        collision_types = {'top': False, 'bottom': False,
                           'right': False, 'left': False}
        for block in block_hit_list:
            if Movement[0] > 0:
                self.rect.right = block.left
                collision_types['right'] = True
            elif Movement[0] < 0:
                self.rect.left = block.right
                collision_types['left'] = True
            self.x = self.rect.x
        self.y += Movement[1]
        self.rect.y = int(self.y)
        block_hit_list = CollisionTest(self.rect, platforms)
        for block in block_hit_list:
            if Movement[1] > 0:
                self.rect.bottom = block.top
                collision_types['bottom'] = True
            elif Movement[1] < 0:
                self.rect.top = block.bottom
                collision_types['top'] = True
            self.change_y = 0
            self.y = self.rect.y
        return collision_types


global entity_ID
entity_ID = 0


class entity(object):

    def __init__(self, x, y, x_size, y_size):
        global entity_ID
        self.ID = entity_ID
        entity_ID = entity_ID + 1
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size
        self.obj = PhysicsObject(self.x, self.y, self.x_size, self.y_size)

    def move(self, movement, collisions):
        collision_feedback = self.obj.Move(movement, collisions)
        self.x = self.obj.x
        self.y = self.obj.y
        return collision_feedback

    def push(self, movement, collisions, objects):
        new_list = []
        for collision in collisions:
            new_list.append([collision[0], collision[1],
                             collision[2], collision[3], 'solid'])
        obj_list = []
        for obj in objects:
            new_list.append([obj.obj.rect.x, obj.obj.rect.y,
                             obj.obj.rect.width, obj.obj.rect.height, 'obj', obj, obj.ID])
            obj_list.append([obj.obj.rect.x, obj.obj.rect.y,
                             obj.obj.rect.width, obj.obj.rect.height, 'obj', obj, obj.ID])
        testR = pygame.Rect(
            self.x+movement[0], self.y+movement[1], self.x_size, self.y_size)
        for obj in new_list:
            if obj[4] == 'obj':
                objR = pygame.Rect(obj[0], obj[1], obj[2], obj[3])
                if testR.colliderect(objR):
                    dist_x = obj[0] - self.x
                    if dist_x > 0:
                        dist_x -= self.x_size
                    elif dist_x < 0:
                        dist_x += obj[5].x_size
                    power_x = movement[0]-dist_x
                    dist_y = obj[1]-self.y
                    if dist_y > 0:
                        dist_y -= self.y_size
                    elif dist_y < 0:
                        dist_y += obj[5].y_size
                    power_y = movement[1] - dist_y
                    if movement[0] == 0:
                        power_x = 0
                    if movement[1] == 0:
                        power_y = 0
                    spec_list = objects.copy()
                    for item in spec_list:
                        if item.ID == obj[6]:
                            spec_list.remove(item)
                    obj[5] = obj[5].push(
                        [power_x, power_y], collisions, spec_list)
                    obj[0] = obj[5].rect.x
                    obj[1] = obj[5].rect.y
        self.move(movement, new_list)
        return self.obj

    def update_animation(self, anim, key):
        anim.move(key, self.x, self.y)


global animation_database
animation_database = {}

# Генерация анимаций


def animation_sequence(sequence, base_path, colorkey=(255, 255, 255), transparency=255):
    global animation_database
    result = []
    for frame in sequence:
        image_id = base_path + str(frame[0])
        image = pygame.image.load(image_id + '.png').convert()
        image.set_colorkey(colorkey)
        image.set_alpha(transparency)
        animation_database[image_id] = image.copy()
        for i in range(frame[1]):
            result.append(image_id)
    return result

# Генерация групп изображений


def load_sequence(base_path, amount, colorkey=(255, 255, 255)):
    result = []
    for image in range(amount):
        img = pygame.image.load(base_path + str(image) + '.png').convert()
        img.set_colorkey(colorkey)
        result.append(img.copy())
    return result


class animation(object):
    def __init__(self, sequence, base_path, attributes=[], colorkey=(255, 255, 255), transparency=255):
        self.sequence = animation_sequence(
            sequence, base_path, colorkey, transparency)
        self.attributes = attributes
        self.key_num = 0
        self.active_animations = {}

    def start(self, x, y):
        self.key_num += 1
        self.active_animations[self.key_num] = [x, y, 0, None]
        return self.key_num

    def play(self, key, surf, flip=False, show=True, offset=[0, 0], transparency=255):
        global animation_database
        anim_read = self.active_animations[key]
        animation_database[self.sequence[anim_read[2]]].set_alpha(transparency)
        if anim_read[3] == None:
            if flip == False:
                surf.blit(animation_database[self.sequence[anim_read[2]]],
                          (anim_read[0] + offset[0], anim_read[1] + offset[1]))
            else:
                surf.blit(pygame.transform.flip(animation_database[self.sequence[anim_read[2]]], True, False), (
                    anim_read[0] + offset[0], anim_read[1] + offset[1]))
        else:
            if flip == False:
                surf.blit(anim_read[3], (anim_read[0] +
                                         offset[0], anim_read[1] + offset[1]))
            else:
                surf.blit(pygame.transform.flip(
                    anim_read[3], True, False), (anim_read[0] + offset[0], anim_read[1] + offset[1]))
            self.active_animations[key][3] = None
        self.active_animations[key][2] += 1
        if self.active_animations[key][2] >= len(self.sequence):
            if 'continuous' in self.attributes:
                self.active_animations[key][2] -= 1
            elif 'loop' in self.attributes:
                self.active_animations[key][2] = 0
            else:
                del self.active_animations[key]
        return self.active_animations[key][2]

    def move(self, key, x, y):
        self.active_animations[key][0] = x
        self.active_animations[key][1] = y
