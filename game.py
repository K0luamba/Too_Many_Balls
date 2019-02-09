import pygame
import random
import sys
import time

class Menu:
    def __init__(self, punkts = [124, 140, u'Punkt', (250,250,30), (250,30,250)]):
        self.punkts = punkts
    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30)) #if need to highlight
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30)) #by default
    def menu(self):
        done = True
        font_menu = pygame.font.Font(None, 50)
        pygame.key.set_repeat(0,0)
        pygame.mouse.set_visible(True)
        punkt = 0
        while done:
            info_string.fill((0, 100, 200))
            screen.fill((0, 100, 200))

            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0]>i[0] and mp[0]<i[0]+155 and mp[1]>i[1] and mp[1]<i[1]+50:
                    punkt = i[5]
            self.render(screen, font_menu, punkt)
                
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts)-1:
                            punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1: #tappaing mouse on point of menu
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        sys.exit()

            win.blit(info_string, (0, 0))
            win.blit(screen, (0, 0))
            pygame.display.flip()

pygame.init()
win = pygame.display.set_mode((500,530))
info_string = pygame.Surface((500,30))
end_string = pygame.Surface((500,60))
start_string = pygame.Surface((500,90))
screen = pygame.Surface((500,500))
info_string.fill((45,80,40))
pygame.display.set_caption("Balls Game")
clock = pygame.time.Clock()
#sprites
bg = pygame.image.load('grass.jpg')
#characteristics of objects
x = 10
y = 280
width = 10
height = 100
speed = 8
speedBall = 10
run = True
balls = []
lost = 0 #counter of lost balls
playTime = 0
boostAmount = 100
#using fonts
pygame.font.init()
inf_font = pygame.font.SysFont('Comic Sans MS', 24)
#menu information and menu output, doesn't work correct sometimes, won't make it
#punkts = [(120, 140, u'Game', (0, 0, 0), (250, 0, 0), 0),
          #(130, 210, u'Quit', (0, 0, 0), (250, 0, 0), 0)]
#game = Menu(punkts)
#game.menu()

class Gameball():
    def __init__(self, x, y, radius, colour, facingX, facingY, speedX, speedY):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.facingX = facingX
        self.facingY = facingY
        self.speedX = speedX
        self.speedY = speedY
    def move(self):
        global x,y, height, width, lost, speedBall
        self.x += self.speedX*self.facingX
        self.y += self.speedY*self.facingY
        #check for going out in any direction
        if self.y < self.radius + 30:
            self.y = self.radius + 30 + (self.radius + 30 - self.y)
            self.facingY = 1
        if self.y > 530 - self.radius:
            self.y = 530 - self.radius - (self.y - 530 + self.radius)
            self.facingY = -1
        if self.x > 500 - self.radius:
            self.x = 500 - self.radius - (self.x - 500 + self.radius)
            self.facingX = -1
        #hitting the racket
        if self.y + self.radius > y and self.y - self.radius < y + height and self.x - self.radius < x + width and x + width - self.x < self.speedX and self.facingX == -1:
            self.speedX = round(speedBall - abs(self.y - (y + (height/2)))/8)
            self.speedY = round(speedBall * abs(self.y - (y + (height/2)))/50)
            self.x = x + width + abs(x + 2*width - self.x + self.radius)
            if self.y <= y + height/2:
                self.facingY = -1
            else:
                self.facingY = 1
            self.facingX = 1
        if  self.x - self.radius < 0: #going out
            lost += 1
            raise Exception("Lost balls - " + str(lost))
    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.radius)
        

def DrawWindow():
    #drawing current info
    win.blit(info_string,(0,0))
    info_string.fill((63, 224, 52))
    win.blit(bg, (0,30))
    info_string.blit(inf_font.render('Lost balls: ' + str(lost), 1, (255, 255, 255)), (10, 0))
    info_string.blit(inf_font.render('Boost: ' + str(boostAmount), 1, (255, 255, 255)), (220, 0))
    info_string.blit(inf_font.render('Time: ' + str(round(playTime/30)), 1, (255, 255, 255)), (400, 0))  
    #he game field itself
    pygame.draw.rect(win, (0,0,0), pygame.Rect(x,y,width,height)) #draw player
    for ball in balls:
       ball.draw(win) #in this moment we have correct x and y
    pygame.display.update()
    
#printing out stert info
start_string.fill((63, 224, 52))
start_string.blit(inf_font.render('Move your racket with arrows', 1, (255, 255, 255)), (100, 0))
start_string.blit(inf_font.render('To boost press Space', 1, (255, 255, 255)), (100, 28))
start_string.blit(inf_font.render('Tap Space to start', 1, (255, 255, 255)), (100, 58))
win.blit(start_string,(0,0))
win.blit(bg, (0,90))
pygame.display.update()
run = True
while run:
    clock.tick(60)
    pygame.time.delay(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() #exit from cycle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]: #exit using key
        run = False
balls.append(Gameball(250, 280, 11, (0, 0, 220), 1, 1, speedBall, 0)) #default position and speeds of the ball
run = True
while run:
    clock.tick(60)
    pygame.time.delay(25)
    playTime += 1
    if playTime >= 900: #player have limited time for game - 30 sec
        run = False
    if playTime % 120 == 0: #adding new balls in random directions
        xx = random.randint(5,speedBall)
        yy = random.randint(5,speedBall)
        balls.append(Gameball(250, 280, 11, (0,0,220), 1, 1, xx, yy))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #exit from cycle

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: #exit using key
        run = False

    cash = speed
    if keys[pygame.K_SPACE] and boostAmount > 0: #boost
        boostAmount -= 1
        speed *= 3 
    if keys[pygame.K_LEFT] and x > speed:
        x -= speed
    if keys[pygame.K_UP] and y > 30 + speed:
        y -= speed
    if keys[pygame.K_RIGHT] and x < 500 - width:
        x += speed
    if keys[pygame.K_DOWN] and y < 530 - height:
        y += speed
    speed = cash

    for ball in balls:
        try:
            ball.move() #calculate correct coordinates of ball after this cycle
        except Exception as ex:
            balls.pop(balls.index(ball))
            #print(ex)
    DrawWindow()
#printing out the results
end_string.fill((63, 224, 52))
end_string.blit(inf_font.render('Game over. Lost balls: ' + str(lost) + '.', 1, (255, 255, 255)), (10, 0))
if lost <= 2:
    end_string.blit(inf_font.render('Nice!', 1, (255, 255, 255)), (290, 0))
elif lost <= 5:
    end_string.blit(inf_font.render('Good.', 1, (255, 255, 255)), (290, 0))
else:
    end_string.blit(inf_font.render('Good luck later :)', 1, (255, 255, 255)), (290, 0))
end_string.blit(inf_font.render('Press Esc to exit', 1, (255, 255, 255)), (100, 28))
win.blit(end_string,(0,0))
win.blit(bg, (0,60))
pygame.display.update()
run = True
while run:
    clock.tick(60)
    pygame.time.delay(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #exit from cycle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: #exit using key
        run = False
pygame.quit()
print("Lost balls - " + str(lost))
