from pygame import *

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite): #и наследник от sprite.Sprite
    #конструктор класса
    #для создания свойств объекта и передачи их ему
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
        super().__init__()
        #каждый спрайт должен хранить свойство image
        self.image = transform.scale(image.load(player_image), (wight, height)) #подгружаем картинку и указываем размер
        self.speed = player_speed
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x #rect.x - координата прямоугольника по x
        self.rect.y = player_y #rect.y - координата прямоугольника по y
    #метод, отрисовывающий героя на окне
    def reset(self): #метод отрисовки героя
        window.blit(self.image, (self.rect.x, self.rect.y)) #Отрисовывает героя в данных координатах

class Player(GameSprite):
    def updateR(self): #метод передвижения персонажа по нажатию клавиши
        keys = key.get_pressed() #метод подключения кнопок
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def updateL(self): #метод передвижения персонажа по нажатию клавиши
        keys = key.get_pressed() #метод подключения кнопок
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

#окно
win_width = 700
win_height = 500
display.set_caption("Ping-Pong")
window = display.set_mode((win_width, win_height))
background = (143, 233, 222)
window.fill(background) 

#спрайты
player1 = Player('player.png', 30, 200, 4, 50, 150)
player2 = Player('player.png', 520, 200, 4, 50, 150)
ball = GameSprite('ball.png', 200, 200, 4, 50, 50)

#надписи
font.init()
font1 = font.SysFont('Arial', 35)
lose1 = font1.render('Проиграл 1 игрок!', True, (180, 0, 0))
lose2 = font1.render('Проиграл 2 игрок!', True, (180, 0, 0))

#флаги
finish = False #переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
game = True #флаг сбрасывается кнопкой закрытия окна
FPS = 60
clock = time.Clock()

score1 = 0
score2 = 0
speed_x = 3
speed_y = 3

#основной цикл
while game:
    #событие нажатия на кнопку закрыть
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if finish != True:
        window.fill(background)
        player1.updateL()
        player2.updateR()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(player1, ball) or sprite.collide_rect(player2, ball):
            speed_x *= -1
            speed_y *= 1
        
        #если мяч достигает границ экрана меняем направление его движения
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1
        
        #если мяч улетел дальше ракетки, выводим условие проигрыша для первого игрока
        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (200, 200))
            game_over = True 
        
        #если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока
        if ball.rect.x > win_width:
            finish = True
            window.blit(lose2, (200, 200))
            game_over = True

        player1.reset()
        player2.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)