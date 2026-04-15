import pygame
import random

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1500, 800))  ### Можно добавить в котёж flags = pygame.NOFRAME
pygame.display.set_caption("Новая игра")  ### Название игры в окне
icon = pygame.image.load("Иконка игры.png").convert_alpha()
pygame.display.set_icon(icon)

### Выводим новый объект на экран
bg = pygame.image.load("Изображения\Задний фон карт\Начальная локация\Bg_forest.png").convert_alpha()
bg = pygame.transform.scale(bg, screen.get_size())

### Создаём монстра орла, загружаем его изображение
monster_eagle = [
    pygame.image.load("Изображения/Противник/Eagle_sprite/Anim_sprite/Eagle_1(100,80).png").convert_alpha(),
    pygame.image.load("Изображения/Противник/Eagle_sprite/Anim_sprite/Eagle_2(100,80).png").convert_alpha(),
    pygame.image.load("Изображения/Противник/Eagle_sprite/Anim_sprite/Eagle_3(100,80).png").convert_alpha(),
    pygame.image.load("Изображения/Противник/Eagle_sprite/Anim_sprite/Eagle_4(100,80).png").convert_alpha(),
    pygame.image.load("Изображения/Противник/Eagle_sprite/Anim_sprite/Eagle_5(100,80).png").convert_alpha(),

]
### Создаём монстра, загружаем его изображение
monster_reptail = [
    pygame.image.load("Изображения/Противник/Reptail_srite/Srint_sreti/Reptail_1(64).png").convert_alpha(),
    pygame.image.load("Изображения/Противник/Reptail_srite/Srint_sreti/Reptail_3(64).png").convert_alpha(),
    pygame.image.load("Изображения/Противник/Reptail_srite/Srint_sreti/Reptail_6(64).png").convert_alpha(),
    pygame.image.load("Изображения/Противник/Reptail_srite/Srint_sreti/Reptail_7(64).png").convert_alpha(),
]
### Создвём новый список, Создаём игрока стоящего на месте
walk_stay = [
    pygame.image.load("Изображения/worth_stay.png").convert_alpha()
]
### Создаём новый список, Создаём игрока бегущего в право
walk_right = [
    pygame.image.load("Изображения/right_sprite_step/right_sprite_1(smole).png").convert_alpha(),
    pygame.image.load("Изображения/right_sprite_step/right_sprite_2(smole).png").convert_alpha()
]
### Создаём новый список, Создаём игрока бегущего в лево
walk_left = [
    pygame.image.load("Изображения/left_sprite_step/left_sprite_1(smole).png").convert_alpha(),
    pygame.image.load("Изображения/left_sprite_step/left_sprite_2(smole).png").convert_alpha()
]

### Создаём переменную для замедления анимации
last_update = 0
animation_delay = 250  ### (0.25 секунды)
### Для всех монстров
monster_anim_count = 0
### Для анимации орла отдельно
eagle_anim_count = 0

### Для автоматического создания монстров - ОТДЕЛЬНЫЕ СПИСКИ ДЛЯ КАЖДОГО ТИПА МОНСТРОВ
reptail_list_in_game = []
eagle_list_in_game = []

player_anim_stay = 0
player_anim_count = 0
bg_x = 0

### Ходьба и прыжок
player_speed = 7
player_x = 100
player_y = 550

### Переменные для прыжка
is_jump = False
jump_count = 8

### Переменные для двойного прыжка
jumps_available = 2  ### Доступные прыжки
spawn_y = 550  ### Позиция спавна игрока (земля)

### Звук леса на фоне
bg_audio_forest = pygame.mixer.Sound("Audio\les.mp3")
bg_audio_forest.play()

### Создаём автоматическое создание монстров для рептилии
Reptail_timer = pygame.USEREVENT + 1
### Создаём автоматическое создание монстров для Орла
Eagle_timer = pygame.USEREVENT + 2

### ЗАПУСКАЕМ ТАЙМЕРЫ СО СЛУЧАЙНЫМИ ИНТЕРВАЛАМИ ПРИ СТАРТЕ
pygame.time.set_timer(Reptail_timer, random.randint(3000, 8000)) ### Значение в миллисекундах
pygame.time.set_timer(Eagle_timer, random.randint(4000, 9000)) ### Значение в миллисекундах

### Вывод на экран надписи после проигрыша(соприкосновения с врагом)
label = pygame.font.Font("Шрифт/BBHSansBogle-Regular.ttf", 40)
label_big = pygame.font.Font("Шрифт/BBHSansBogle-Regular.ttf", 120)
lose_label = label_big.render("You loss!", False, (230, 5, 5))
### Рестарт
restart_label = label.render("Try again?", False, (5, 230, 23))
restart_label_rect = restart_label.get_rect(topleft=(693, 600))
### Индикатор жизни игрока
gameplay = True

running = True
while running:

    ### Установка кадров в секунду
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()

    ### Инициализируем игрока
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1500, 0))

    ### Если игрок жив
    if gameplay:
        ### Рисуем квадрат вокруг игрока для проверки столкновений
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        ### Обрабатываем орлов в воздухе
        if eagle_list_in_game:
            for (i, el) in enumerate(eagle_list_in_game):
                ### Создаём отдельный прямоугольник для каждого орла
                eagle_rect = monster_eagle[eagle_anim_count].get_rect(topleft=(el.x, el.y))
                screen.blit(monster_eagle[eagle_anim_count], el)
                el.x -= 12
                ###Удаляем врага
                if el.x < -80:
                    eagle_list_in_game.pop(i)

                ### Проверяем столкновение игрока с орлом
                if player_rect.colliderect(eagle_rect):
                    gameplay = False

        ### Обрабатываем рептилий на земле
        if reptail_list_in_game:
            for (i, el) in enumerate(reptail_list_in_game):
                ### Создаём отдельный прямоугольник для каждой рептилии
                reptail_rect = monster_reptail[monster_anim_count].get_rect(topleft=(el.x, el.y))
                screen.blit(monster_reptail[monster_anim_count], el)
                el.x -= 7
                ###Удаляем врага
                if el.x < -80:
                    reptail_list_in_game.pop(i)

                ### Проверяем столкновение игрока с рептилией
                if player_rect.colliderect(reptail_rect):
                    gameplay = False

        ### Инициализируем игрока на экране после фона
        ### Отслеживание перемещения игрока
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 1350:
            player_x += player_speed

        ### Логика прыжка/Характеристики прыжка(сила, скорость, высота)
        if is_jump:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 1.5
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 0.75
            else:
                is_jump = False
                jump_count = 8

        ### Проверка приземления - всегда приземляемся в 550
        if not is_jump:
            player_y = spawn_y  ### Всегда возвращаем на землю когда не в прыжке
            jumps_available = 2  ### Восстанавливаем прыжки

        ### Замедление Анимации Игрока и Монстров без ущерба кадрам
        if current_time - last_update >= animation_delay:
            player_anim_count = (player_anim_count + 1) % len(walk_right)
            monster_anim_count = (monster_anim_count + 1) % len(monster_reptail)
            eagle_anim_count = (eagle_anim_count + 1) % len(monster_eagle)
            last_update = current_time

        bg_x -= 5
        if bg_x == -1500:
            bg_x = 0
    ### Экран проигрыша
    else:
        ### Обнуляем таймер спавна персонажей
        pygame.time.set_timer(Reptail_timer, 0)
        pygame.time.set_timer(Eagle_timer, 0)

        ### Используем последний активный кадр
        screen.blit(walk_right[player_anim_count], (player_x, player_y))
        ### Рептилия с последним кадром
        for el in reptail_list_in_game:
            screen.blit(monster_reptail[monster_anim_count], el)
        # Орлы с их последним кадром
        for el in eagle_list_in_game:
            screen.blit(monster_eagle[eagle_anim_count], el)

        s = pygame.Surface((1500, 800), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        screen.blit(s, (0, 0))
        screen.blit(lose_label,(570, 250))
        screen.blit(restart_label, restart_label_rect)

        ### Кнопка рестарт и спавн персонажа
        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 100
            eagle_list_in_game.clear()
            reptail_list_in_game.clear()
            ### ПЕРЕЗАПУСКАЕМ ТАЙМЕРЫ СО СЛУЧАЙНЫМИ ИНТЕРВАЛАМИ ПРИ РЕСТАРТЕ
            pygame.time.set_timer(Reptail_timer, random.randint(3000, 8000))
            pygame.time.set_timer(Eagle_timer, random.randint(4000, 9000))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            ### Обработка прыжка по нажатию пробела
            if event.key == pygame.K_SPACE:
                if jumps_available > 0:
                    is_jump = True
                    jumps_available -= 1
                    jump_count = 8
        ### Создаём рептилий по таймеру
        elif event.type == Reptail_timer:
            reptail_list_in_game.append(monster_reptail[monster_anim_count].get_rect(topleft=(1600,550)))
            ### УСТАНАВЛИВАЕМ СЛЕДУЮЩИЙ ТАЙМЕР СО СЛУЧАЙНЫМ ИНТЕРВАЛОМ СРАЗУ ПОСЛЕ СПАВНА
            pygame.time.set_timer(Reptail_timer, random.randint(3000, 8000))
        ### Создаём орлов по таймеру
        elif event.type == Eagle_timer:
            eagle_list_in_game.append(monster_eagle[eagle_anim_count].get_rect(topleft=(1600,300)))  ### Орел летает выше
            ### УСТАНАВЛИВАЕМ СЛЕДУЮЩИЙ ТАЙМЕР СО СЛУЧАЙНЫМ ИНТЕРВАЛОМ СРАЗУ ПОСЛЕ СПАВНА
            pygame.time.set_timer(Eagle_timer, random.randint(4000, 9000))