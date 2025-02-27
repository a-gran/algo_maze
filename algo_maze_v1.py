import pygame  # Импортируем библиотеку pygame для создания игры
'''Необходимые классы'''  # Заголовок секции с определением классов

# Базовый класс для всех спрайтов в игре
class GameSprite(pygame.sprite.Sprite):
    # Конструктор класса, принимает изображение, координаты и скорость
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()  # Вызываем конструктор родительского класса Sprite

        # Загружаем и масштабируем изображение спрайта до размера 55x55 пикселей
        self.image = pygame.transform.scale(pygame.image.load(player_image), (55, 55))
        self.speed = player_speed  # Устанавливаем скорость движения спрайта

        # Создаем прямоугольник для определения границ спрайта
        self.rect = self.image.get_rect()
        self.rect.x = player_x  # Устанавливаем начальную x-координату
        self.rect.y = player_y  # Устанавливаем начальную y-координату

    # Метод для отрисовки спрайта на экране
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс игрока, наследуется от GameSprite
class Player(GameSprite):
    # Метод обновления позиции игрока
    def update(self):
        keys = pygame.key.get_pressed()  # Получаем состояние всех клавиш
        # Проверяем нажатие клавиш и перемещаем игрока с учетом границ окна
        if keys[pygame.K_LEFT] and self.rect.x > 5:  # Движение влево
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - 80:  # Движение вправо
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 5:  # Движение вверх
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < win_height - 80:  # Движение вниз
            self.rect.y += self.speed

# Класс врага, наследуется от GameSprite
class Enemy(GameSprite):
    side = "left"  # Начальное направление движения врага
    
    # Метод обновления позиции врага
    def update(self):
        # Логика движения врага влево-вправо
        if self.rect.x <= 470:  # Если достигнута левая граница
            self.side = "right"
        if self.rect.x >= win_width - 85:  # Если достигнута правая граница
            self.side = "left"
        # Перемещение врага в зависимости от направления
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

# Класс для создания стен
class Wall(pygame.sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()  # Вызываем конструктор родительского класса
        # Сохраняем параметры стены
        self.color_1 = color_1  # Красный компонент цвета
        self.color_2 = color_2  # Зеленый компонент цвета
        self.color_3 = color_3  # Синий компонент цвета
        self.width = wall_width  # Ширина стены
        self.height = wall_height  # Высота стены

        # Создаем поверхность для стены и закрашиваем её
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((color_1, color_2, color_3))

        # Создаем прямоугольник для стены
        self.rect = self.image.get_rect()
        self.rect.x = wall_x  # Устанавливаем x-координату
        self.rect.y = wall_y  # Устанавливаем y-координату

    # Метод для отрисовки стены
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        # Дополнительно рисуем прямоугольник
        pygame.draw.rect(window, (self.color_1, self.color_2, self.color_3), (self.rect.x, self.rect.y, self.width, self.height))

'''Описание игры'''
# Настройки окна игры
win_width = 700  # Ширина окна
win_height = 500  # Высота окна
window = pygame.display.set_mode((win_width, win_height))  # Создаем окно игры
pygame.display.set_caption("Лабиринт")  # Устанавливаем заголовок окна
# Загружаем и масштабируем фоновое изображение
background = pygame.transform.scale(pygame.image.load("background.jpg"), (win_width, win_height))

# Создаем стены лабиринта
w1 = Wall(154, 205, 50, 100, 20 , 450, 10)  # Верхняя горизонтальная стена
w2 = Wall(154, 205, 50, 100, 480, 350, 10)  # Нижняя горизонтальная стена
w3 = Wall(154, 205, 50, 100, 20 , 10, 380)  # Левая вертикальная стена
w4 = Wall(154, 205, 50, 200, 130, 10, 350)  # Вертикальная стена в центре
w5 = Wall(154, 205, 50, 450, 130, 10, 360)  # Правая вертикальная стена
w6 = Wall(154, 205, 50, 300, 20, 10, 350)   # Дополнительная вертикальная стена
w7 = Wall(154, 205, 50, 390, 120, 130, 10)  # Дополнительная горизонтальная стена

# Создаем игровые объекты
packman = Player('hero.png', 5, win_height - 80, 4)  # Создаем игрока
monster = Enemy('cyborg.png', win_width - 80, 280, 2)  # Создаем врага
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)  # Создаем сокровище

# Инициализация игровых переменных
game = True  # Флаг работы игры
finish = False  # Флаг завершения уровня
clock = pygame.time.Clock()  # Создаем объект для отслеживания времени
FPS = 60  # Устанавливаем частоту обновления экрана

# Инициализация шрифтов
pygame.font.init()  # Инициализируем подсистему шрифтов
font = pygame.font.Font(None, 70)  # Создаем шрифт размером 70
win = font.render('YOU WIN!', True, (255, 215, 0))  # Создаем надпись "победа"
lose = font.render('YOU LOSE!', True, (180, 0, 0))  # Создаем надпись "проигрыш"

# Инициализация звуков
pygame.mixer.init()  # Инициализируем подсистему звука
pygame.mixer.music.load('jungles.ogg')  # Загружаем фоновую музыку
pygame.mixer.music.play()  # Запускаем проигрывание фоновой музыки

# Загружаем звуковые эффекты
money = pygame.mixer.Sound('money.ogg')  # Звук получения сокровища
kick = pygame.mixer.Sound('kick.ogg')  # Звук столкновения

# Основной игровой цикл
while game:
    pygame.display.update()  # Обновляем экран
    # Обрабатываем события
    for e in pygame.event.get():
        if e.type == pygame.QUIT:  # Если нажата кнопка закрытия окна
            game = False  # Завершаем игру
            
    if finish != True:  # Если игра не завершена
        window.blit(background,(0, 0))  # Отрисовываем фон
        packman.update()  # Обновляем позицию игрока
        monster.update()  # Обновляем позицию врага
        # Отрисовываем все объекты
        packman.reset()  # Отрисовываем игрока
        monster.reset()  # Отрисовываем врага
        final.reset()    # Отрисовываем сокровище
        # Отрисовываем все стены
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()
        
        # Проверяем условия проигрыша (столкновение с врагом или стенами)
        if (pygame.sprite.collide_rect(packman, monster) or
            pygame.sprite.collide_rect(packman, w1) or pygame.sprite.collide_rect(packman, w2) or
            pygame.sprite.collide_rect(packman, w3) or pygame.sprite.collide_rect(packman, w4) or
            pygame.sprite.collide_rect(packman, w5) or pygame.sprite.collide_rect(packman, w6) or
            pygame.sprite.collide_rect(packman, w7)):
            finish = True  # Завершаем игру
            window.blit(lose, (200, 200))  # Выводим сообщение о проигрыше
            kick.play()  # Воспроизводим звук столкновения
            
        # Проверяем условие победы (достижение сокровища)
        if pygame.sprite.collide_rect(packman, final):
            finish = True  # Завершаем игру
            window.blit(win, (200, 200))  # Выводим сообщение о победе
            money.play()  # Воспроизводим звук получения сокровища
            
    clock.tick(FPS)  # Устанавливаем частоту обновления игры