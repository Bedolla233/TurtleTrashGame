import pygame
from pygame.locals import(RLEACCEL, K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,KEYDOWN,QUIT)
import random
import os

filePath = os.path.abspath(__file__)
dName = os.path.dirname(filePath)
os.chdir(dName)

pygame.init()
pygame.mixer.init()#for sound

#colors
red = (169, 149, 123)
blue = (51, 77, 125)
pink = (237,165,161)
black = (0,0,0)

#sets size of screen
WIDTH = 1200 #screen width
LENGTH = 800 #screen length
size = (WIDTH,LENGTH) #size of screen
screen = pygame.display.set_mode(size) #sets screen
pygame.display.set_caption("Trash Dash") #name of display
clock = pygame.time.Clock() #sets time for gaame

#Background image
back = pygame.image.load("Images/Ocean1.png").convert()
back2 = pygame.image.load("Images/Ocean2.png").convert()
backX = 0 # move background
back2X = back.get_width()

 #animates player
imageP = []
imageP.append( pygame.image.load("Images/t1.png").convert())
imageP[0] = pygame.transform.scale(imageP[0], (100,70))
imageP.append(pygame.image.load("Images/t2.png").convert())
imageP[1] = pygame.transform.scale(imageP[1], (100,70))
imageP.append(pygame.image.load("Images/t3.png").convert())
imageP[2] = pygame.transform.scale(imageP[2], (100,70))
#turtle on Main screen
mainScreenTurtle = pygame.image.load("Images/main.png").convert()
pygame.transform.scale(mainScreenTurtle,(200,200))
mainTurtleRect = mainScreenTurtle.get_rect( center = (WIDTH//2,LENGTH//2-50))
mainScreenTurtle.set_colorkey((255,255,255),RLEACCEL)

#enemy animations
imageEnemyArray = []
imageEnemyArray.append(pygame.image.load("Images/e.png").convert())
imageEnemyArray[0]= pygame.transform.scale(imageEnemyArray[0],((25,15)))
imageEnemyArray.append(pygame.image.load("Images/e2.png").convert())
imageEnemyArray.append(pygame.image.load("Images/e3.png").convert())
imageEnemyArray.append(pygame.image.load("Images/e4.png").convert())
imageEnemyArray.append(pygame.image.load("Images/e5.png").convert())

#jellyfish animation
imageJelly = []
imageJelly.append(pygame.image.load("Images/jelly1.png").convert())
imageJelly[0]= pygame.transform.scale(imageJelly[0],((imageJelly[0].get_rect().width * 1.5,imageJelly[0].get_rect().height * 1.5)))
imageJelly.append(pygame.image.load("Images/jelly2.png").convert())
imageJelly[1]= pygame.transform.scale(imageJelly[1],((imageJelly[1].get_rect().width * 1.5,imageJelly[1].get_rect().height * 1.5)))


#Start button
startButton = []
startButton.append(pygame.image.load("Images/button1.png").convert())
startButton.append(pygame.image.load("Images/button2.png").convert())
buttonRect = startButton[0].get_rect( center = (WIDTH//2,LENGTH-200))
startButton[1].set_colorkey(black,RLEACCEL)
startButton[0].set_colorkey(black,RLEACCEL)
#Keys Button
KeysButton = []
KeysButton.append(pygame.image.load("Images/Keys1.png").convert())
KeysButton.append(pygame.image.load("Images/Keys2.png").convert())
KeysButtonRect = KeysButton[0].get_rect( center = (WIDTH//2,LENGTH-200))
KeysButton[0].set_colorkey(black,RLEACCEL)
KeysButton[1].set_colorkey(black,RLEACCEL)

#Mouse Button
MouseButton = []
MouseButton.append(pygame.image.load("Images/MosB1.png").convert())
MouseButton.append(pygame.image.load("Images/MosB2.png").convert())
MousebuttonRect = MouseButton[0].get_rect( center = (WIDTH//2,LENGTH-200))
MouseButton[0].set_colorkey(black,RLEACCEL)
MouseButton[1].set_colorkey(black,RLEACCEL)

mouseOverButton = False
class button(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super(button,self).__init__()
        self.state1 = x 
        self.state2 = y
        self.create()

    def create(self):
        self.surf = self.state1
        self.rect = self.surf.get_rect( center = (WIDTH//2,LENGTH-200) )
    def update(self):
        global mouseOverButton
        point = pygame.mouse.get_pos() 
        if(self.rect.collidepoint(point)):
            self.surf = self.state2
            mouseOverButton = True
        else:
            self.surf = self.state1
            mouseOverButton = False

press = button(startButton[0],startButton[1])

ChooseKeys = button(KeysButton[0],KeysButton[1])

ChooseMouse = button(MouseButton[0],MouseButton[1])

#Score
scoreTotal = 0
Font = pygame.font.SysFont('calibri',40)
TitleFont = pygame.font.SysFont('calibri',80,True)
score = Font.render('Score: '+str(scoreTotal),True, black)
tRect = score.get_rect() #rect for objects
tRect.center = (WIDTH//2,20)

#game over
gameOverText = TitleFont.render('Game Over',True,pink)
gameOverTextRect = gameOverText.get_rect()
gameOverTextRect.center = (WIDTH//2,LENGTH//2)
returningText = Font.render('Returning to Main Screen...',True,pink)
returningTextRect = returningText.get_rect()
returningTextRect.center = (WIDTH//2,LENGTH//2+50)
#music 
pygame.mixer.music.load("GameMusic.mp3")
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(loops=-1)

jellyFishPoint = pygame.mixer.Sound("JellyFishPoints.mp3")
jellyFishPoint.set_volume(.5)

loseSound = pygame.mixer.Sound("GameLose.mp3")
loseSound.set_volume(5.0)

class Player(pygame.sprite.Sprite):
    def __init__(self): #construcotr, tells sprite what it starts with
        super(Player, self).__init__() #has all the upper class members
        self.index = 0
        self.surf = imageP[self.index] #creates surface for sprite
        self.surf.set_colorkey((255,255,255),RLEACCEL) #gives the color
        self.upDown = 1 #will loop through sprite states
        self.rect = self.surf.get_rect( #sets it to its place, center is used for center of sprite
            center = (60, LENGTH/2)
        )
        

    def mouseMove(self):
        #Makes mouse invisible
        pygame.mouse.set_visible(False)
        self.rect.center= pygame.mouse.get_pos()
        if self.rect.left < 0: #checks to see if it hits edge
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 50:
            self.rect.top = 50
        if self.rect.bottom >= LENGTH:
            self.rect.bottom = LENGTH

        
    def animate(self):
        
        self.surf = imageP[self.index]
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        if self.index >= 2:
            self.upDown = -1
        elif(self.index <=0):
            self.upDown = 1
        self.index += self.upDown
        
    def update(self,pressed_keys): #what happens if they press a certain key 
        
        if(pressed_keys[K_UP] or pressed_keys[pygame.K_w]):
            self.rect.move_ip(0,-10)
        if pressed_keys[K_DOWN] or pressed_keys[pygame.K_s]:
            self.rect.move_ip(0,10)
        if pressed_keys[K_LEFT]or pressed_keys[pygame.K_a]:
            self.rect.move_ip(-10,0)
        if pressed_keys[K_RIGHT] or pressed_keys[pygame.K_d]:
            self.rect.move_ip(10,0)

        if self.rect.left < 0: #checks to see if it hits edge
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 50:
            self.rect.top = 50
        if self.rect.bottom >= LENGTH:
            self.rect.bottom = LENGTH

class Enemy(pygame.sprite.Sprite): #creates enemy class
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = imageEnemyArray[random.randint(0,4)]

        self.surf.set_colorkey(black,RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (random.randint(WIDTH+20,WIDTH+100),random.randint(50, LENGTH-100))
        )
        self.speed = random.randint(5,20)#gives enemy random speed

    def update(self):
        self.rect.move_ip(-self.speed,0) #moves left at given speed. STays in same y position
        if self.rect.right <0:
            self.kill()#removes sprite

        if player not in allSprites: #added myself :D 0 help
            self.speed = 0 #if player dies, all sprites stop moving
            pygame.time.set_timer(addEnemy, 0)

class JellyFish(pygame.sprite.Sprite):
    def __init__(self):
        super(JellyFish,self).__init__()
        self.index = 0
        self.surf = imageJelly[0]
        self.surf.set_colorkey(black,RLEACCEL)
        self.rect = self.surf.get_rect( center = (random.randint(WIDTH+20,WIDTH+100),random.randint(50, LENGTH-100)))
        self.speed = 5
    
    def spriteChange(self):
        self.surf = imageJelly[self.index]
        self.surf.set_colorkey(black,RLEACCEL)
        self.index += 1
        if self.index >= 2:
            self.index = 0

    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right <0:
            self.kill()#removes sprite

        if player not in allSprites: #added myself :D 0 help
            self.speed = 0 #if player dies, all sprites stop moving
            pygame.time.set_timer(addJelly, 0)
    
#main game loop
carry_on = True #keeps main running
screen.blit(back,screen.get_rect())
addEnemy = pygame.USEREVENT + 1 # will be used to add enemy
pygame.time.set_timer(addEnemy, 300)#will set a timer for enemy
animate = pygame.USEREVENT + 2 #will animate turtle
pygame.time.set_timer(animate, 180)

addJelly = pygame.USEREVENT + 3
pygame.time.set_timer(addJelly, 2000)

#makes player
player = Player()
enemies = pygame.sprite.Group()# groups all enemies
jellies = pygame.sprite.Group()
allSprites = pygame.sprite.Group()
allSprites.add(player)#groups all sprites including plyer


def Main():
    global backX, back2X, carry_on, scoreTotal, loseSound,jellyFishPoint
    while(carry_on):
        #events done in game
        for event in pygame.event.get():
            if event.type ==KEYDOWN: #was a key pressed?
                if(event.key == K_ESCAPE): #was the key esc?
                    carry_on = False
            if event.type == QUIT:
                carry_on = False
                pygame.quit()
        
            elif event.type == addEnemy: #when timer goes off
                newEnemy = Enemy() #crete new enemy
                enemies.add(newEnemy) #add enemy to enemy group
                allSprites.add(newEnemy) #add enemy to all sprites
            if event.type == addJelly:
                newJelly = JellyFish()
                jellies.add(newJelly)
                allSprites.add(newJelly)
            
            if event.type == animate:
                scoreTotal+=1
                player.animate()
                for entity in jellies:
                    entity.spriteChange()
            

        if(keys == False):
            player.mouseMove()
        else:
            pressed_keys = pygame.key.get_pressed()#gets pressed key
            player.update(pressed_keys)#moves based on input
        enemies.update() #updates all enemies
        jellies.update()

        if player in allSprites:
            backX -=2
            back2X -= 2
            if backX < back.get_width()*-1:
                backX = back.get_width()
            if back2X < back.get_width()*-1:
                back2X = back.get_width()
        else:
            pygame.mouse.set_visible(True)
        
        #update score
        score = Font.render('Score: '+str(scoreTotal),True, (0,0,0))        
        screen.blit(back,(backX,0))
        screen.blit(back,(back2X,0))
        screen.blit(score, tRect)
        

        for entity in allSprites:
            screen.blit(entity.surf, entity.rect) #draws all sprites onto screen
    
        if(pygame.sprite.spritecollideany(player, enemies)):
            enemies.speed = 0
            #pygame.time.set_timer(animate, 0)
            screen.blit(gameOverText,gameOverTextRect)
            screen.blit(returningText,returningTextRect)
            carry_on = False
            for entity in allSprites:
                entity.kill()
            pygame.mixer.Sound.play(loseSound)
            

        
        elif(pygame.sprite.spritecollide(player, jellies,True)):
            scoreTotal += 50
            pygame.mixer.Sound.play(jellyFishPoint)
            
            
        pygame.display.flip() 
        clock.tick(45) #30 fps
    

keys = True
buttonGroup = pygame.sprite.Group()
willContinue = True

#sets high score
highScoreNum = 0
highScoreText = Font.render('HighScore: '+str(highScoreNum),True, (0,0,0))
highScoreRect = highScoreText.get_rect()
highScoreRect.center = (WIDTH//2,200)

def reset():
    global scoreTotal, carry_on, allSprites, player, highScoreNum
    pygame.mouse.set_visible(True)
    pygame.time.delay(3000)
    carry_on = True
    allSprites.add(player)
    if(highScoreNum<scoreTotal):
        highScoreNum = scoreTotal
    scoreTotal = 0


def StartScreen():
    global scoreTotal, mouseOverButton, keys, carry_on, highScoreNum, highScoreRect, highScoreText
    start = TitleFont.render('Turtle Trash',True, (0,0,0))
    sRect = start.get_rect() #rect for objects
    sRect.center = (WIDTH//2,150)
    helpW = Font.render('Press H for Help',True,(0,0,0))
    hRect = helpW.get_rect()
    hRect.center = (WIDTH//2,LENGTH//2+70)
    pressH = False
    mainS = True
    MainButton = True
    buttonGroup.add(press)

    while(mainS):
        screen.fill(pink)
        screen.blit(start,sRect)
        screen.blit(mainScreenTurtle,mainTurtleRect)
        screen.blit(helpW,hRect)
        screen.blit(highScoreText,highScoreRect)
        
        for event in pygame.event.get():
            highScoreText = Font.render('HighScore: '+str(highScoreNum),True, (0,0,0))
            screen.blit(highScoreText,highScoreRect)

            if event.type ==KEYDOWN: #was a key pressed?
                if(event.key == K_ESCAPE): #was the key esc?
                    mainS = False
                if(event.key == pygame.K_h):
                    pressH = True
            mousePressed = pygame.mouse.get_pressed()
            if(MainButton):
                press.update()
                if(event.type == pygame.MOUSEBUTTONDOWN):
                    if((mousePressed[0]) and press.surf==startButton[1]):
                        MainButton = False
                        press.kill()
                        buttonGroup.add(ChooseKeys)
                        ChooseKeys.rect = ChooseKeys.surf.get_rect( center = (WIDTH//2-200,LENGTH-200) )
                        buttonGroup.add(ChooseMouse)
                        ChooseMouse.rect = ChooseMouse.surf.get_rect( center = (WIDTH//2+200,LENGTH-200) )
            else:
                ChooseKeys.update()
                ChooseMouse.update()
                if(event.type == pygame.MOUSEBUTTONDOWN):
                    if((mousePressed[0]) and ChooseKeys.surf == KeysButton[1]):
                        keys = True
                        Main()
                        reset()  

                if(event.type == pygame.MOUSEBUTTONDOWN):
                    if((mousePressed[0]) and ChooseMouse.surf == MouseButton[1]):
                        keys = False
                        Main()
                        reset()
                        
            if event.type == QUIT:
                mainS = False
            if pressH==True:
                hRect.center = (WIDTH//2-200,LENGTH//2+100)
                helpW = Font.render('Help Tiny Tim Avoid Trash and Eat Jellyfish:)',True,(0,0,0))
                screen.blit(helpW,hRect)

            
            for entity in buttonGroup:
                screen.blit(entity.surf, entity.rect) #draws all sprites onto screen  
            pygame.display.flip()
    


StartScreen()
pygame.quit()