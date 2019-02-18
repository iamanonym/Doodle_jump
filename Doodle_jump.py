from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import pygame
import os
import sys
import random


def load_image(name, x=None, y=None, colorkey=None):  # Загрузка изображения
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


def terminate():  # Конец игры
    pygame.quit()
    sys.exit()


def start_screen():  # Окно заставки
    intro_text = ["DOODLE JUMP", "ЗАСТАВКА", "", "Чтобы начать, нажмите",
                  "любую клавишу или любую", "кнопку мыши"]
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


def get_coords(number):  # Выбор расположения платформ на уровне
    list = [0, 1, 2, 3, 4, 5]
    number2 = random.randint(1, 6)
    platforms = random.sample(list, number2)
    return {(platform * 100, number) for platform in platforms}


def count_best():  # Нахождение лучших игроков
    result = {}
    for login in sorted(LOGINS):
        file = open('Accounts/{}.txt'.format(login))
        try:
            level = int(file.read().split()[0])
            result[level] = result.get(level, []) + [login]
        except IndexError:
            pass
        file.close()
    best = []
    for level in sorted(result)[-5:][::-1]:
        for login in result[level]:
            best.append('{} - {}'.format(login, level))
        if len(best) >= 5:
            break
    return best


def change_result(name, new_levels, new_stars):  # Обновление
    file_name = 'Accounts/{}.txt'.format(name)  # личной информации
    file = open(file_name)
    text = file.read()
    levels, stars = 0, 0
    if not text:
        pass
    else:
        levels, stars = tuple(map(lambda x: int(x), text.split()))
    file.close()
    levels = new_levels if new_levels > levels else levels
    stars += new_stars
    file2 = open(file_name, 'w')
    file2.write('{} {}'.format(levels, stars))
    file2.close()


def waste(group):  # Очистка группы спрайтов
    for sprite in group:
        sprite.kill()


def take_down(group, group2, height):  # Опустить группу на уровень ниже
    for sprite in group:
        sprite.__class__(group2, all_sprites, sprite.get_x(),
                         height, blast=sprite.is_blast())
        sprite.kill()


def make_group(group, height, level):  # Отрисовка уровня
    number = random.randint(0, 5) if level > 8 else 1
    if number:
        coords = get_coords(height)
        for coord in coords:
            if len(coords) >= 1:
                temp = level // 5 if level <= 20 else 4
                number = random.randint(0, temp)
                if number == 1 and coord[0] != 300:
                    Breaking(group, all_sprites, *coord)
                elif number == 2:
                    Spring(group, all_sprites, *coord)
                elif number == 3:
                    Snow(group, all_sprites, *coord)
                elif number == 4:
                    Stand(group, all_sprites, *coord, blast=True)
                else:
                    Stand(group, all_sprites, *coord)
            else:
                Stand(group, all_sprites, *coord)
            if (300, height) not in coords:
                Stand(group, all_sprites, 300, height)
    else:
        Moving(group, all_sprites, 0, height)


def show_result(levels, stars):  # Окно вывода результата
    screen = pygame.display.set_mode((300, 300))
    intro_text = ["Пройдено уровней: {}".format(str(levels)),
                  "Получено звезд: {}".format(str(stars))]
    screen.fill((255, 255, 255))
    font = pygame.font.Font('data/freesansbold.ttf', 25)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 0
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    b1 = Button((0, 100, 300, 100), 'Начать заново')
    b1.draw()
    b2 = Button((0, 200, 300, 100), 'Таблица результатов', font=20)
    b2.draw()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if b1.is_inside(*event.pos):
                    main(user_name)
                elif b2.is_inside(*event.pos):
                    create_table()
        pygame.display.flip()


def create_table():  # Окно таблицы лучших результатов
    intro_text = count_best()
    screen = pygame.display.set_mode((300, 50 * (len(intro_text) + 2)))
    screen.fill((255, 255, 255))
    font = pygame.font.Font('data/freesansbold.ttf', 30)
    text_coord = -10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 0
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    btn = Button((0, len(intro_text) * 50, 300, 100), 'Начать заново')
    btn.draw()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn.is_inside(*event.pos):
                    main(user_name)
        pygame.display.flip()


def main(name):  # Основная игровая функция
    screen = pygame.display.set_mode((700, 600))
    doodle = Hero(all_sprites)
    Stand(down_site, all_sprites, 320, 550)
    Stand(mid_site, all_sprites, 100, 350)
    Stand(up_site, all_sprites, 400, 150)
    clock = pygame.time.Clock()
    moving = 0
    end = None
    started = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:  # Изменение направления
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
            end, level = doodle.move()
            doodle.move_x(moving)
        if end:  # Проигрыщ
            waste(all_sprites)
            change_result(user_name, level, level // 5)
            show_result(level, level // 5)
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()


class PasswordWindow(QMainWindow):  # Окно авторизации
    def __init__(self):  # Инициализация
        super().__init__()
        uic.loadUi('data/Password_design.ui', self)
        self.sign_in.clicked.connect(self.signing)
        self.sign_up.clicked.connect(self.signing)
        self.is_new = False

    def check(self, mode='s'):  # Проверка логина и пароля
        self.log = self.login.text()
        self.word = self.password.text()
        if mode == 'e' and self.log not in LOGINS:
            return 'Несуществующий логин'
        elif mode == 'e' and LOGINS[self.log] != self.word:
            return 'Неверный пароль'
        elif mode == 's' and self.log in LOGINS:
            return 'Логин уже существует'
        elif len(self.log) < 8 or len(self.word) < 8:
            return 'Недостаточно символов'
        elif self.word.isdigit() or self.word.isalpha():
            return 'Пароль состоит из символов одного вида'
        elif set(self.log).intersection({',', '.', '!', '?', '/', '\\',
                                         ';', '(', ')', '&', '[', ']',
                                         '<', '>', '*', '|', ':', '"'}):
            return 'Недопустимые символы в логине'
        elif set(self.word).intersection({',', '.', '!', '?', '/', '\\',
                                          ';', '(', ')', '&', '[', ']',
                                          '<', '>', '*', '|', ':', '"'}):
            return 'Недопустимые символы в пароле'

    def signing(self):
        if self.sender().text() == 'Вход':
            self.checking = self.check(mode='e')
        else:
            self.checking = self.check()
            self.is_new = True
        if self.checking:
            self.comment.setText(self.checking)
            self.comment.adjustSize()
        else:
            self.name = 'Accounts/{}'.format(self.log)
            if self.is_new:
                with open('Accounts/Accounts_list.txt', 'a') as file:
                    file.write('{} {}\n'.format(self.log, self.word))
                    file.close()
                self.file = open(self.name + '.txt', 'w')
                self.is_new = False
            self.close()

    def get_log(self):  # Возвращает логин
        try:
            return self.log
        except AttributeError:
            return None

    def get_pswd(self):  # Возвращает пароль
        try:
            return self.word
        except AttributeError:
            return None


class Button:  # Класс кнопки для окна PyGame
    def __init__(self, size, text, font=30):  # Инициализация кнопки
        self.x, self.y, self.width, self.height = self.size = size
        self.text = text
        self.font = font

    def draw(self):  # Отрисовка кнопки
        pygame.draw.rect(screen, (0, 0, 0), self.size, 1)
        font = pygame.font.Font('data/freesansbold.ttf', self.font)
        string_rendered = font.render(self.text, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = \
            self.x + self.width // 10, self.y + self.height // 3
        screen.blit(string_rendered, intro_rect)

    def is_inside(self, x, y):  # Проверка, нажата ли кнопка
        return self.x <= x <= self.x + self.width and \
               self.y <= y <= self.y + self.height


class Hero(pygame.sprite.Sprite):  # Класс героя
    def __init__(self, group):  # Инициализация
        super().__init__(group)
        self.image = doodle_im
        self.rect = self.image.get_rect()
        self.rect.x = 330
        self.rect.y = 485
        self.speed = 300
        self.way = 220
        self.right = True
        self.level = 0

    def move(self):  # Передвижение с течением времени
        self.rect.y -= self.speed / fps
        if self.way <= 0:
            if self.speed > 0:
                self.speed = -self.speed
            self.check_field()
        else:
            self.way -= self.speed / fps
        if 10 > self.speed > 0 or self.rect.y <= 0:
            self.speed = -50
        if self.rect.y + self.rect.height >= 600:
            return True, self.level
        for group in [down_site, mid_site, up_site]:
            for sprite in group:
                if sprite.__class__ == Moving:
                    sprite.move()
        return False, None

    def check_group(self, group, height):
        # Проверка, соприкоснулся ли герой с какой-либо платформой
        booly = False
        for sprite in group:
            if pygame.sprite.collide_mask(self, sprite):
                if height - 10 < self.rect.y + self.rect.height < height and \
                                self.speed < 0:
                    if sprite.__class__ == Stand \
                            or sprite.__class__ == Moving:
                        sounds['stand'].play()
                        self.speed, self.way = 300, 250
                        booly = True
                        if sprite.is_blast():
                            x, y = sprite.get_x(), sprite.get_y()
                            sprite.kill()
                            Breaking(group, all_sprites, x, y, blast=True)
                    elif sprite.__class__ == Spring:
                        sounds['spring'].play()
                        self.speed, self.way = 300, 400
                        booly = True
                    elif sprite.__class__ == Snow:
                        sounds['stand'].play()
                        self.speed, self.way = 300, 250
                        booly = True
                        sprite.kill()
                    elif sprite.__class__ == Breaking:
                        sounds['break'].play()
                        sprite.kill()
        return booly

    def check_field(self):  # Проверка необходимости изменить поле
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
            self.level += 2
            waste(down_site)
            waste(mid_site)
            take_down(up_site, down_site, 550)
            make_group(up_site, 150, self.level)
            make_group(mid_site, 350, self.level)
            self.move_down(550 - self.rect.height)

    def move_x(self, direct):  # Движение под действием кнопок
        self.rect.x += direct * abs(self.speed) / fps
        if direct:
            self.turn(direct)
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + self.rect.width > 700:
            self.rect.x = 700 - self.rect.width

    def move_down(self, new_y):  # Задать ординату героя программно
        self.rect.y = new_y

    def turn(self, direct):  # Поворот в зависимости от направления движения
        if direct > 0 and not self.right:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.right = True
        elif direct < 0 and self.right:
            self.image = pygame.transform.flip(self.image, -1, 0)
            self.right = False


class Platf(pygame.sprite.Sprite):  # Базовый класс платформы
    # Инициализация
    def __init__(self, group, base_group, x, y, img, blast=None):
        super().__init__(group, base_group)
        self.image = platf_ims[img]
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.blast = blast

    def get_x(self): # Возвращает абсциссу
        return self.rect.x

    def get_y(self):  # Возвращает ординату
        return self.rect.y

    def is_blast(self):  # Возвращается, является ли взрывной
        return self.blast


class Stand(Platf):  # Стандартная платформа
    def __init__(self, group, base_group, x, y, blast=False):
        if not blast:
            super().__init__(group, base_group, x, y, 'stand')
        else:
            super().__init__(group, base_group, x, y, 'blast1', blast=True)


class Breaking(Platf):  # Ломающася платформа
    def __init__(self, group, base_group, x, y, blast=False):
        if not blast:
            super().__init__(group, base_group, x, y, 'break')
        else:
            super().__init__(group, base_group, x, y, 'blast2', blast=True)


class Moving(Platf):  # Движущаяся платформа
    def __init__(self, group, base_group, x, y, blast=False):
        super().__init__(group, base_group, x, y, 'move')
        self.moving = 50
        self.dir = 1

    def move(self):
        self.rect.x += self.dir * self.moving / fps
        if self.rect.x == 0:
            self.dir = 1
        if self.rect.x + self.rect.width == 700:
            self.dir = -1


class Spring(Platf):  # Платформа-пружина
    def __init__(self, group, base_group, x, y, blast=False):
        super().__init__(group, base_group, x, y, 'spring')


class Snow(Platf):  # Снежная платформа
    def __init__(self, group, base_group, x, y, blast=False):
        super().__init__(group, base_group, x, y, 'snow')


LOGINS = {}  # Словарь логинов и паролей
try:
    LOGINS = {x.split()[0]: x.split()[1]
              for x in open('Accounts/Accounts_list.txt').readlines()}
except FileNotFoundError:
    pass
except IndexError:
    pass
user_name, pswd = None, None
if __name__ == '__main__':  # Авторизация
    app = QApplication(sys.argv)
    pw = PasswordWindow()
    pw.show()
    app.exec_()
    user_name, pswd = pw.get_log(), pw.get_pswd()
if not user_name:
    sys.exit()
if user_name not in LOGINS:
    LOGINS[user_name] = pswd
pygame.init()
screen = pygame.display.set_mode((800, 500))
start_screen()
doodle_im = load_image('doodle.png', 70, 65, -1)
# Словари с графической и звуковой информацией
platf_ims = {'stand': load_image('platf0.png', 100, 20, -1),
             'break': load_image('platf1.png', 100, 20, -1),
             'move': load_image('platf2.png', 100, 20, -1),
             'spring': load_image('platf3.png', 100, 20, -1),
             'snow': load_image('platf4.png', 100, 20, -1),
             'blast1': load_image('platf5_1.png', 100, 20, -1),
             'blast2': load_image('platf5_2.png', 100, 20, -1)}
sounds = {'stand': pygame.mixer.Sound('data/stand.ogg'),
          'break': pygame.mixer.Sound('data/break.ogg'),
          'spring': pygame.mixer.Sound('data/spring.ogg')}
all_sprites = pygame.sprite.Group()
up_site = pygame.sprite.Group()
mid_site = pygame.sprite.Group()
down_site = pygame.sprite.Group()
fps = 50
main(user_name)
