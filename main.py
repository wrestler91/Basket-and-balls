import sys
import pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
import ball as bl
from random import randint
import basket as bsk
from menu import PauseMenu, FinishMenu
from configs import *
import pygame_textinput
import sqlite3 as sq

# переменные игры
game_score = 0
game_speed = 0
max_score = 0
speed_bask = 10

# создаем пользовательские события для вызова шаров, бафов и дебафов 
# каждые 2 секунды генерирует событие pygame.USEREVENT в главном цикле
reveal_ball = pygame.USEREVENT +1
pygame.time.set_timer(reveal_ball, 750)

reveal_buff = pygame.USEREVENT +2
pygame.time.set_timer(reveal_buff, 15000)

reveal_debuff = pygame.USEREVENT +3
pygame.time.set_timer(reveal_debuff, 10000)

# создание экрана
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption('Игра на pygame')
# создание встроенного таймера для регулирования скорости обработки событий в главном цикле 
clock = pygame.time.Clock() 
# задний фон
back = pygame.image.load('C:/Users/Арутюн/Desktop/python/проекты/игра2/images/back.bmp').convert()
pygame.transform.scale(back, (W, H))



# звуковые эффекты
sound = pygame.mixer.Sound(sound_path + 'SFX_Pickup_06.wav')
buff_sound = pygame.mixer.Sound(sound_path + 'Buff.wav')
debuff_sound = pygame.mixer.Sound(sound_path + 'Debuff.wav')
lose_sound = pygame.mixer.Sound(sound_path + 'No_Hope.ogg')
# загружаем звуковой файл
pygame.mixer.music.load(sound_path + 'birds-in-the-morning-24147.mp3')
# проигрываем музыку бесконечно
pygame.mixer.music.play(-1)

# создаем шары
# словарь в котором кранятся имя объекта и его ценность
balls_data = ({'name': 'ball.png', 'score': 5},
              {'name': 'balloon_dog_PNG14.png', 'score': 10},
              {'name': 'balloon_PNG4960.png', 'score': 15})
# создаем список поверхностей для каждой картинки из данных словаря
balls_surf = [pygame.image.load(image_path+data['name']).convert_alpha() for data in balls_data]
balls = pygame.sprite.Group()

# бафы и дебафы
buff_name, buff_value = 'buff.png', 2
buff_surf = pygame.image.load(image_path+buff_name).convert_alpha()
buffs = pygame.sprite.Group()

debuff_name, debuff_value = 'debuff.png', -2
debuff_surf = pygame.image.load(image_path+debuff_name).convert_alpha()
debuffs = pygame.sprite.Group()

# корзинка
baskets = pygame.sprite.Group()
basket_img = 'Basket2.png'
basket_surf = pygame.image.load(image_path+basket_img).convert_alpha()
# создаем ЭК (спрайт) корзинки
basket = bsk.Basket((W//2, H-40), speed_bask, basket_surf, baskets)

# создаем шрифты для отображения счета 
score_font = pygame.font.SysFont('rage', 36)
record_font = pygame.font.SysFont('rage', 36)



# Функции привязанные к кнопкам меню
def quit() -> None:
    '''
    Привязанная к опции выхода из игры
    Вызывается при нажатии кнопки выхода из меню паузы и меню при поражении
    Перед выходом выводит на экран таблицу лидеров и задерживает ее на 7 секунд
    затем закрывает программу
    '''
    global flag
    global max_score
    screen.blit(back, (0, 0))
    records = write_record(max_score)
    text_surf = record_font.render('Records:', True, BLACK)
    screen.blit(text_surf, (50, 10))
    for i, record in enumerate(records, 1):
        record = f'{record[0]}: Score: {record[1]}, Date: {record[2]}'
        record_surf = record_font.render(record, True, GOLD)
        screen.blit(record_surf, (50, i*45))
    max_score = 0
    pygame.display.update()
    pygame.time.delay(7000)
    flag = False
    pygame.quit()
    sys.exit()

def contin() -> None:
    '''
    Привязанная к опции продолжения игры
    Вызывается при нажатии кнопки продолжения из меню паузы
    Меняет значение флага паузы, возобнавляет фоновую музыку и делает снова видимым корзинку
    '''
    global pause
    pause = False
    pygame.mixer.music.unpause()
    baskets.sprites()[0].image.set_alpha(255)

def play_again()-> None:
    '''
    Привязанная к опции игры заново
    Вызывается при нажатии кнопки заново из меню при поражении
    Возобнавляет фоновую музыку, делает снова видимым корзинку, обновляет счет и вызывает функцию записи результата
    '''
    global lose_sound_flag
    global game_score
    global max_score
    game_score = 0
    # pygame.mixer.Sound.stop(lose_sound)
    pygame.mixer.music.unpause()
    baskets.sprites()[0].image.set_alpha(255)
    write_record(max_score)
    max_score = 0
    lose_sound_flag = False

def start_game() -> None:
    '''
    Привязанная к опции начала игры
    Вызывается при нажатии кнопки старт из стартового меню
    Меняет значение флага старта игры
    '''
    global start_game_fl
    start_game_fl = True

# 
def show_score() -> None:
    '''
    Привязанная к опции показа кол-ва баллов игрока
    Вызывается при нажатии кнопки show score из меню паузы и конца игры
    Выводит на экран максимальное кол-во набранных баллов игроком в текущей сессии игры
    '''
    font = pygame.font.SysFont('rage', 56)
    score_surface = font.render(f'{max_score}', True, BLUE)
    score_rect = score_surface.get_rect(center = (W//2+150, H//2-90))
    screen.blit(score_surface, score_rect)


# меню паузы
pause_font = pygame.font.SysFont('Arial', 56)
pause_menu = PauseMenu(pause_font)
pause_menu.append_option('Exit', quit, RED)
pause_menu.append_option('Continue', contin, GREEN)
pause_menu.append_option(f'Show score', show_score, BLUE)


# меню при поражении
finish_font = pygame.font.SysFont('gigi', 56)
finish_menu = FinishMenu(finish_font)
finish_menu.append_option(f'You Lost', None, RED)
finish_menu.append_option(f'Show score', show_score, BLUE)
finish_menu.append_option(f'Do you want play again?', None, BLACK)
finish_menu.append_option('No', quit, RED)
finish_menu.append_option('Yes', play_again, GREEN)

# стартовое меню 
start_font = pygame.font.SysFont('Arial', 56)
start_menu = FinishMenu(start_font)
start_menu.append_option('Start', start_game, GREEN)
name_input = pygame_textinput.TextInputVisualizer(font_color=GOLD)
name_input.manager.cursor_pos = len(name_input.manager.value)
name_input.value = 'Player1'


# функция создающая объекты - шары
def create_ball(group) -> object:
    '''
    Принимает группу спрайтов для шариков
    генерирует случайную координату где будет падать шар и его скорость
    возвращает ЭК шара
    '''
    global game_speed
    # скорость рассчитывается из уровня игры
    # уровень игры - это каждые 100 очков набранные игроком
    # с уменьшением кол-ва балов, набранных игроком, скорость не падает, 
    # т.к. расчитывается из максимального значения текущего уровня и его предыдущего значения
    game_speed = max(game_score // 100, game_speed)
    # индекс случайного объекта из списка поверхностей
    indx = randint(0, len(balls_surf)-1)
    # случайная координата на экране
    x = randint(20, W-20)
    # скорость шара в диапазаоне от минимального до максимальной скорости
    # плюс уровень игры
    speed = randint(min_speed + game_speed, max_speed + game_speed)
    return bl.Ball(x, speed, balls_surf[indx], balls_data[indx]['score'], group)

def create_buff_debuff(group: object, cls: object, surf: object, value: int) -> object:
    '''
    Принимает группу спрайтов, класс, поверхность спрайта, значение бафа
    генерирует случайную координату где будет падать бафф и его скорость
    возвращает ЭК бафа
    '''
    x = randint(20, W-20)
    speed = max_speed - min_speed + game_speed
    return cls(x, speed, surf, value, group)

def collide_buff_debuff(buffer_group: object)-> None:
    '''
    Проверяет пересекает ли баф корзинку для ловли
    если да, то придает корзинке эффект бафа
    и удаляет спрайт бафа при попадании в корзинку или достижении дна
    '''
    global speed_bask
    # перебираем группу для шаров
    for buffer in buffer_group:
        # если центр шара пересекся с объектом корзинки
        if basket.rect.collidepoint(buffer.rect.center):
            # увеличиваем счет на стоимость шара
            basket.speed += buffer.score

            if basket.speed > 20:
                basket.speed = 20
            elif basket.speed < 2:
                basket.speed = 2
            # проигрываем звук ловли
            if isinstance(buffer, bl.Buff):
                buff_sound.play()
            else:
                debuff_sound.play()
            # удаляем шар
            buffer.kill()


# функция контроля столкновений
def collideBalls() -> None:
    '''
    Проверяет пересекает ли шар корзинку для ловли
    если да, то увеличивает счет игрока
    и удаляет спрайт шара при попадании в корзинку или достижении дна
    '''
    global game_score
    global max_score
    # перебираем группу для шаров
    for ball in balls:
        # если центр шара пересекся с объектом корзинки
        if basket.rect.collidepoint(ball.rect.center):
            # увеличиваем счет на стоимость шара
            game_score += ball.score
            # проигрываем звук ловли
            sound.play()
            # удаляем шар
            ball.kill()
        elif ball.rect.y >= H - 20:
            game_score -= ball.score
    max_score = max(max_score, game_score)


def write_record(score: int) -> list:
    '''
    Принимает балы игрока и вносить в базу данных имя, балы и дату записи
    Возвращает список рекордов из БД
    '''
    from datetime import datetime
    record = [score, name, str(datetime.now().date())]
    # подключаемся к БД
    with sq.connect('game.db') as conn:
        # создаем курсор и таблицу
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS records (
        name TEXT,
        score INTEGER,
        date TEXT
        )
        ''')
        cur.execute('''SELECT * FROM records
        ORDER BY score desc
        ''')
        records = cur.fetchall()
        # если еще не все записи есть, дозаписываем
        if len(records) < 10:
            cur.execute(f'''
            INSERT INTO records (name, score, date) VALUES('{record[1]}', '{record[0]}', '{record[2]}');
            ''')
            cur.execute('''SELECT * FROM records
            ORDER BY score desc
            ''')
            records = cur.fetchall()
        # если записей уже 10 
        # проверяем больше ли рекорд игрока минимального значения в записях
        # если да, то удаляем мин значение и записыаем новый рекорд  
        else:
            cur.execute('''SELECT
            MIN(score)
            FROM records
            ''')
            min_score = cur.fetchall()
            if score > min_score[0][0]:
                cur.execute(f'''
                DELETE FROM records
                WHERE score = '{min_score[0][0]}'
                ''')
                cur.execute(f'''
                INSERT INTO records (name, score, date) VALUES('{record[1]}', '{record[0]}', '{record[2]}');
                ''')
                cur.execute('''SELECT * FROM records
                ORDER BY score desc
                ''')
                records = cur.fetchall()
    return records


def pause_function(menu: object, xs: tuple or int, ys: tuple or int) -> None:
    '''
    Вызывается когда игра ставится на паузу или игрок проиграл. Отрисовывает соответсвующее меню
    Функция принимает в аргементы класс Menu, и координаты опций меню в виде кортежей или целых чисел
    Удаляет шары, делает невидимым корзинку и ставит музыку на паузу
    Прорисовывает меню на экране и реализует взаимодействие с ним
    '''
    for ball in balls.sprites():
            ball.kill()
    pygame.mixer.music.pause()
    baskets.sprites()[0].image.set_alpha(0)
    # прорисовывает меню
    menu.draw(screen, xs, ys)
    # pause_options.draw(screen)
    pygame.display.update()
    # если нажата кнопка мышки и курсор на поверхности некой опции
    # то вызывается функция привязанная к этой опции
    if pygame.mouse.get_pressed(num_buttons=3)[0]:
        pos = pygame.mouse.get_pos()
        menu.call_option(pos)


# некоторые дополнительные флаги и маркеры, для более корректной работы программы
# маркер для проигровки музыки поражения
lose_sound_flag = False
# флаг для определения стоит ли игра на паузе
pause = False
# флаг для выхода из игры, т.к. при выходе через функцию возникает ошибка
flag = True
# флаг для начала игры, связана с функцией start_game()
start_game_fl = False

create_ball(balls)
while True:
    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:
        # для проверки типа события используется конструкция event.type
        # pygame.QUIT - событие при нажатии красного крестика (выхода из приложения)
        if event.type == pygame.QUIT:
            flag = False
            if not flag:
            # если событие сработало. Выходит из всей программы
                write_record(max_score)
                max_score = 0
                pygame.quit()
                sys.exit()
        
        # при генерации события, которое мы обозначили в начале
        elif event.type == reveal_ball:
            # создаем новый объект (шар)
            if game_score >= 0 and not pause and start_game_fl:
                create_ball(balls)
        
        elif event.type == reveal_buff:
            if game_score >= 0 and not pause and start_game_fl:
                create_buff_debuff(buffs, bl.Buff, buff_surf, buff_value)

        elif event.type == reveal_debuff:
            if game_score >= 0 and not pause and start_game_fl:
                create_buff_debuff(debuffs, bl.DeBuff, debuff_surf, debuff_value)

        # меняем громкость музыки при кручении колесика мышки
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                volume += 1
            elif event.button == 5:
                volume -= 1
            pygame.mixer.music.set_volume(volume)
        
        # если нажата кнопка выхода или пробела, ставит игру на паузу
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                pause = True
        
    screen.blit(back, (0, 0))
    name_input.update(events)
    # если игра еще не началась
    # отрисовывает стартовое меню
    if not start_game_fl:
        x, y = W//2, H//2 + 100
        start_menu.draw(screen, x, y)
        screen.blit(name_input.surface, (W//2-50, H//2 - 50))
        pygame.display.update()
        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            pos = pygame.mouse.get_pos()
            start_menu.call_option(pos)
        name = name_input.manager.value
    else:
        # функция контроля столкновений шаров, бафов, дебафов с корзинкой и дном
        collideBalls()
        collide_buff_debuff(buffs)
        collide_buff_debuff(debuffs)
        keys = pygame.key.get_pressed()

        # обновляем счет
        text_surf = score_font.render(f'Score {game_score}', True, BLUE)
        # отображаем счет
        screen.blit(text_surf, (20, 20))

        # отрисовываем спрайты шаров, бафов, дебафов, корзинки
        debuffs.draw(screen)
        debuffs.update(H)
        buffs.draw(screen)
        buffs.update(H)
        balls.draw(screen)
        balls.update(H)
        basket.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT], W)
        baskets.draw(screen)
        
        if pause:
            xs = (W//2-100, W//2+100, W//2)
            ys = (H//2, H//2, H//2-100)
            pause_function(pause_menu, xs, ys)
                
        if game_score < 0:
            lose_sound_flag = True
            xs = (W//2-50, W//2-50, W//2, W//2-100, W//2+100)
            ys = (H//2-200, H//2-100, H//2, H//2+75, H//2+75)
            pause_function(finish_menu, xs, ys)
            pygame.mixer.Sound.stop(sound)

            if lose_sound_flag:
                lose_sound.play()
            else:
                pygame.mixer.Sound.stop(lose_sound)

    pygame.display.update()