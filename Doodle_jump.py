import pygame
import os
import sys
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def get_coords(number):
    list = [0, 1, 2, 3, 4, 5, 6]
    number2 = random.randint(1, 6)
    platforms = random.sample(list, number2)
    return [(platform * 100, number) for platform in platforms]


class Hero(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = doodle_im
        self.rect = self.image.get_rect()
        self.rect.x = 310
        self.rect.y = 455
        self.speed = 150
        self.way = 220

    def move(self):
        self.rect.y -= self.speed / fps
        if self.way <= 0:
            if self.speed > 0:
                self.speed = -self.speed
            self.check_field()
        else:
            self.way -= self.speed / fps
        if 10 > self.speed > 0:
            self.speed = -50

    def check_field(self):
        booly = False
        for sprite in down_site:
            if pygame.sprite.collide_mask(self, sprite):
                if self.rect.y + self.rect.height < 560:
                    self.speed, self.way = 150, 250
        for sprite in mid_site:
            if pygame.sprite.collide_mask(self, sprite):
                if self.rect.y + self.rect.height < 360:
                    self.speed, self.way = 150, 250
                    booly = True
        for sprite in up_site:
            if pygame.sprite.collide_mask(self, sprite):
                if self.rect.y + self.rect.height < 160:
                    self.speed, self.way = 150, 250
                    booly = True
        if booly:
            for sprite in down_site:
                sprite.kill()
            for sprite in mid_site:
                Stand(down_site, all_sprites,
                      sprite.get_x(), 550)
                sprite.kill()
            for sprite in up_site:
                Stand(mid_site, all_sprites,
                      sprite.get_x(), 350)
                sprite.kill()
            coords = get_coords(150)
            for coord in coords:
                Stand(up_site, all_sprites, *coord)
            self.move_down()

    def move_x(self, dir):
        self.rect.x += dir * abs(self.speed) / fps

    def move_down(self):
        self.rect.y += 150


class Stand(pygame.sprite.Sprite):
    def __init__(self, group, base_group, x, y):
        super().__init__(group, base_group)
        self.image = platf_ims['stand']
        self.image = pygame.transform.scale(self.image, (100, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y


pygame.init()
running = True
started = False
screen = pygame.display.set_mode((700, 600))
doodle_im = load_image('doodle.png', -1)
platf_ims = {'stand': load_image('platf0.png', -1)}
all_sprites = pygame.sprite.Group()
up_site = pygame.sprite.Group()
mid_site = pygame.sprite.Group()
down_site = pygame.sprite.Group()
doodle = Hero(all_sprites)
Stand(down_site, all_sprites, 320, 550)
Stand(mid_site, all_sprites, 100, 350)
Stand(up_site, all_sprites, 400, 150)
clock = pygame.time.Clock()
fps = 50
moving = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not started:
                if event.key == pygame.K_UP:
                    started = True
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                moving = 1
            if keys[pygame.K_LEFT]:
                moving = -1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                moving = 0
    screen.fill((255, 255, 255))
    if started:
        doodle.move()
        doodle.move_x(moving)
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
