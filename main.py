import pygame

pygame.init()
w, h = 640, 480
sc = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()
fps = 60
score1 = 0
score2 = 0
font = pygame.font.SysFont("Arial", 40)
font2 = pygame.font.Font("font/DTM-Sans.otf", 54)

sound = pygame.mixer.Sound("Hit.ogg")

back_img = pygame.image.load("background.png")
pong_img = pygame.image.load("pong2.png")
ball_img = pygame.image.load("ball.png")

win1_text = font2.render("Player1 win", True, (10,255,0))
win2_text = font2.render("Player2 win", True, (10,255,0))

class GameObject:
    def __init__(self,x,y,width,height,img):
        self.rect = pygame.Rect(x,y,width,height)
        self.img = pygame.transform.scale(img, (self.rect.width, self.rect.height))
    def draw(self):
        sc.blit(self.img, (self.rect.x, self.rect.y))
class Ball(GameObject):
    def __init__(self,x,y,w,h,img):
        super().__init__(x,y,w,h,img)    
        self.dx, self.dy = 1, -1
        self.speed = 4
    def movement(self):
        self.rect.x += self.speed*self.dx
        self.rect.y += self.speed*self.dy
        if self.rect.y <= 0:
            self.dy = 1
        if self.rect.y >= h-self.rect.height:
            self.dy = -1
    def collision(self, player, player2):
        if self.rect.colliderect(player.rect) and self.dx == -1:
            self.dx = 1
            self.speed += 0.2
            sound.play()
        if self.rect.colliderect(player2.rect) and self.dx == 1:
            self.dx = -1
            self.speed += 0.2
            sound.play()
class Player(GameObject):
    def __init__(self,x,y,w,h,img):
        super().__init__(x,y,w,h,img)
        self.speed = 5
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y >= 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom <= h:
            self.rect.y += self.speed
    def movement2(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y >= 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom <= h:
            self.rect.y += self.speed

player = Player(0,h/2-50,50,70, pong_img)
player2 = Player(w-50,h/2-50,50,70, pygame.transform.flip(pong_img, True, False))
ball = Ball(w/2, h/2, 16,16,ball_img)
game = True
pause = False
win = False
while game:
    sc.fill((0,0,0))
    sc.blit(back_img, (0,0))
    score_player1 = font.render(str(score1), True, (255,255,255))
    score_player2 = font.render(str(score2), True, (255,255,255))
    sc.blit(score_player1, (100, 20))
    sc.blit(score_player2, (540, 20))
    player.draw()
    player2.draw()
    ball.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            game = False
    if not pause and not win:
        ball.movement()
        player.movement()
        player2.movement2()
        ball.collision(player, player2)
    if ball.rect.x >= w+ball.rect.width:
        ball.speed = 4
        player.rect.x, player.rect.y = 0,h/2-50
        player2.rect.x, player2.rect.y = w-50,h/2-50
        score1 += 1
        ball.rect.x, ball.rect.y = player2.rect.left-ball.rect.width,h/2-16
        ball.dx, ball.dy = 1,1
        pause = True
    if ball.rect.x <= -ball.rect.width:
        ball.speed = 4
        player.rect.x, player.rect.y = 0,h/2-50
        player2.rect.x, player2.rect.y = w-50,h/2-50
        score2 += 1
        ball.rect.x, ball.rect.y = player.rect.right,h/2-16
        ball.dx, ball.dy = -1,-1
        pause = True
    if score1 >= 15:
        sc.blit(win1_text, (w/2-150, h/2-40))
        win = True
    if score2 >= 15:
        sc.blit(win2_text, (w/2-150, h/2-40))
        win = True
    key = pygame.key.get_pressed()
    if key[pygame.K_RETURN] and pause: pause = False
    pygame.display.update()
    clock.tick(fps)
