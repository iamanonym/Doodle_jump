import pygame
import os
import sys
import random


def load_image(name, x=None, y=None, colorkey=None):
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
    if x and y:
        return pygame.transform.scale(image, (x, y))
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["DOODLE JUMP", "ЗАСТАВКА", "",
                  "Чтобы увидеть справку,", "Нажмите F1", "",
                  "Чтобы начать, нажмите", "Любую клавишу, кроме F1,",
                  "или любую кнопку мыши"]
    fon = pygame.transform.scale(load_image('fon.png'), (800, 500))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('data/freesansbold.ttf', 25)
    font2 = pygame.font.Font('data/freesansbold.ttf', 35)
    text_coord = 50
    booly = True
    for line in intro_text:
        if not booly:
            string_rendered = font.render(line, 1, pygame.Color('black'))
        else:
            string_rendered = font2.render(line, 1, (100, 150, 100))
            booly = False
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 400
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return None
        pygame.display.flip()


def get_coords(number):
    list = [0, 1, 2, 3, 4, 5]
    number2 = random.randint(1, 6)
    platforms = random.sample(list, number2)
    return {(platform * 100, number) for platform in platforms}


def waste(group):
    for sprite in group:
        sprite.kill()


def take_down(group, group2, height):
    for sprite in group:
        sprite.__class__(group2, all_sprites,
                         sprite.get_x(), height)
        sprite.kill()


def make_group(group, height, level):
    number = random.randint(0, 5) if level > 8 else 1
    if number:
        coords = get_coords(height)
        for coord in coords:
            if len(coords) >= 1:
                number = random.randint(0, 3)
                if number == 1 and coord[0] != 300:
                    Breaking(group, all_sprites, *coord)
                elif number == 2:
                    Spring(group, all_sprites, *coord)
                elif number == 3:
                    Snow(group, all_sprites, *coord)
                else:
                    Stand(group, all_sprites, *coord)
            else:
                Stand(group, all_sprites, *coord)
            if (300, height) not in coords:
                Stand(group, all_sprites, 300, height)
    else:
        Moving(group, all_sprites, 0, height)


class Hero(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = doodle_im
        self.rect = self.image.get_rect()
        self.rect.x = 330
        self.rect.y = 485
        self.speed = 300
        self.way = 220
        self.right = True
        self.level = 1

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
        for sprite in down_site:
            if sprite.__class__ == Moving:
                sprite.move()
        for sprite in mid_site:
            if sprite.__class__ == Moving:
                sprite.move()
        for sprite in up_site:
            if sprite.__class__ == Moving:
                sprite.move()

    def check_group(self, group, height):
        booly = False
        for sprite in group:
            if pygame.sprite.collide_mask(self, sprite):
                if height - 10 < self.rect.y + self.rect.height < height and \
                                self.speed < 0:
                    if sprite.__class__ == Stand \
                            or sprite.__class__ == Moving:
                        self.speed, self.way = 300, 250
                        booly = True
                    elif sprite.__class__ == Spring:
                        self.speed, self.way = 300, 400
                        booly = True
                    elif sprite.__class__ == Snow:
                        self.speed, self.way = 300, 250
                        booly = True
                        sprite.kill()
                    elif sprite.__class__ == Breaking:
                        sprite.kill()
        return booly

    def check_field(self):
        self.check_group(down_site, 560)
        booly = int(self.check_group(mid_site, 360))
        temp = self.check_group(up_site, 160)
        if temp:
            booly = 2
        if booly == 1:
            self.level += 1
            waste(down_site)
            take_down(mid_site, down_site, 550)
            take_down(up_site, mid_site, 350)
            make_group(up_site, 150, self.level)
            self.move_down(550 - self.rect.height)
        elif booly == 2:
            self.level += 1
            waste(down_site)
            waste(mid_site)
            take_down(up_site, down_site, 550)
            make_group(up_site, 150, self.level)
            make_group(mid_site, 350, self.level)
            self.move_down(550 - self.rect.height)

    def move_x(self, direct):
        self.rect.x += direct * abs(self.speed) / fps
        if direct:
            self.turn(direct)
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + self.rect.width > 700:
            self.rect.x = 700 - self.rect.width

    def move_down(self, new_y):
        self.rect.y = new_y

    def turn(self, direct):
        if direct > 0 and not self.right:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.right = True
        elif direct < 0 and self.right:
            self.image = pygame.transform.flip(self.image, -1, 0)
            self.right = False


class Platf(pygame.sprite.Sprite):
    def __init__(self, group, base_group, x, y, img):
        super().__init__(group, base_group)
        self.image = platf_ims[img]
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y


class Stand(Platf):
    def __init__(self, group, base_group, x, y):
        super().__init__(group, base_group, x, y, 'stand')


class Breaking(Platf):
    def __init__(self, group, base_group, x, y, is_snow=False):
        if not is_snow:
            super().__init__(group, base_group, x, y, 'break')
        else:
            super().__init__(group, base_group, x, y, 'snow')


class Moving(Platf):
    def __init__(self, group, base_group, x, y):
        super().__init__(group, base_group, x, y, 'move')
        self.moving = 50
        self.dir = 1

    def move(self):
        self.rect.x += self.dir * self.moving / fps
        if self.rect.x == 0:
            self.dir = 1
        if self.rect.x + self.rect.width == 700:
            self.dir = -1


class Spring(Platf):
    def __init__(self, group, base_group, x, y):
        super().__init__(group, base_group, x, y, 'spring')


class Snow(Breaking):
    def __init__(self, group, base_group, x, y):
        super().__init__(group, base_group, x, y, is_snow=True)


pygame.init()
running = True
started = False
screen = pygame.display.set_mode((800, 500))
start_screen()
screen = pygame.display.set_mode((700, 600))
doodle_im = load_image('doodle.png', 70, 65, -1)
platf_ims = {'stand': load_image('platf0.png', 100, 20, -1),
             'break': load_image('platf1.png', 100, 20, -1),
             'move': load_image('platf2.png', 100, 20, -1),
             'spring': load_image('platf3.png', 100, 20, -1),
             'snow': load_image('platf4.png', 100, 20, -1),
             'blast1': load_image('platf5_1.png', 100, 20, -1),
             'blast2': load_image('platf5_2.png', 100, 20, -1)}
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
            terminate()
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
