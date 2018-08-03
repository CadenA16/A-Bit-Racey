import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600
display_title = 'A Bit Racey'

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption(display_title)

black = (0,0,0)
white = (255,255,255)
red = (212,49,49)
orange = (255,90,0)
green = (0,255,93)
dark_red = (100,0,0)
bright_green = (0,255,34)

clock = pygame.time.Clock()

pause = True

imgWidth = int(display_height * 0.18)
imgHeight = int(display_width * 0.12)
carImg = pygame.image.load('SimpleOrangeCarTopView.png')
carImg = pygame.transform.scale(carImg,(imgHeight, imgWidth))
carImg = pygame.transform.rotate(carImg,90)
gameIcon = pygame.image.load('ABitRaceyIconImage.png')
pygame.display.set_icon(gameIcon)

#crash_sound = pygame.mixer.Sound("CrashSounds.wav")
#pygame.mixer.music.load('jazz.wav')
#pygame.mixer.music.play(-1)

def createRect_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, orange)
    gameDisplay.blit(text,(0,0))

def createRect(createRectx, createRecty, createRectw, createRecth, color):
    pygame.draw.rect(gameDisplay, color, [createRectx, createRecty, createRectw, createRecth])

def car(x,y):
    gameDisplay.blit(carImg, (x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, orange)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width * 0.50),(display_height * 0.12))
    gameDisplay.blit(TextSurf, TextRect)



    pygame.display.update()
    
    time.sleep(2)

    game_loop()


def crash():

    #pygame.mixer.Sound.play(crash_sound)
    #pygame.mixer.music.stop()
    
    message_display('You Crashed')

def quitgame():
    gameDisplay.fill(red)
    pygame.display.update()
    pygame.time.wait(100)
    pygame.quit()
    quit()

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
       
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("A Bit Racey", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!", 150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,dark_red,quitgame)

        pygame.display.update()
        clock.tick(15)


        mouse = pygame.mouse.get_pos()

        if 150+100 > mouse[0] > 150 and 450+50 > mouse[1] > 450:
            pygame.draw.rect(gameDisplay, bright_green, (150,450,100,50))
        else:
            pygame.draw.rect(gameDisplay, green,(150,450,100,50))

        if 550+100 > mouse[0] > 550 and 450+50 > mouse[1] > 450:
            pygame.draw.rect(gameDisplay, dark_red, (550,450,100,50))
        else:
            pygame.draw.rect(gameDisplay, red,(550,450,100,50))

        pygame.display.update()
        clock.tick(15)

def paused():

    pygame.mixer.music.pause()
    
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    global pause
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = False

        button("Continue",150,450,100,50,green,bright_green,unpause)
        button("Quit",550,450,100,50,red,dark_red,quitgame)

        pygame.display.update()
        clock.tick(15)

def unpause():

    global pause

    pygame.mixer.music.unpause()

    pause = False

def button(msg,x,y,w,h,ic,ac):
    mouse = pygame.mouse.get_pos()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRects = text_objects(msg, smallText)
    textRect.center = ( (x+(x/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    
    x_change = 0

    carSpeed_Left = -5
    carSpeed_Right = 5

    createRect_width = 100
    
    def randomX():
        return random.randrange(0, display_width - createRect_width)

    createRect_startx = randomX()
    createRect_starty = -600
    createRect_speed = 7
    createRect_height = 100

    createRectCount = 1

    dodged = 0

    gameExit = False
    
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                   x_change = carSpeed_Left
                elif event.key == pygame.K_RIGHT:
                    x_change = carSpeed_Right
                if event.key == pygame.K_SPACE:
                    paused()


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if (pygame.key.get_pressed()[pygame.K_RIGHT]):
                        x_change = carSpeed_Right
                    else:
                        x_change = 0
                elif event.key == pygame.K_RIGHT:
                    if (pygame.key.get_pressed()[pygame.K_LEFT]):
                        x_change = carSpeed_Left
                    else:
                        x_change = 0

        x += x_change
        gameDisplay.fill(black)
        car(x,y)

        # createRect(createRectx, createRecty, createRectw, createRecth, color)
        createRect(createRect_startx, createRect_starty, createRect_width, createRect_height, green)
        createRect_starty += createRect_speed
        createRect_dodged(dodged)

        if createRect_starty > display_height:
            createRect_starty = 0 - createRect_height
            createRect_startx = randomX()
            dodged += 1
            carSpeed_Left -= 1
            carSpeed_Right += 1
            createRect_speed += 1
            createRect_width += int(dodged * 1.2)
        
        bdry = 790-imgWidth
        if x > bdry:
            x = bdry
       
        bdry2 = 10
        if x < bdry2:
            x = bdry2

        # We don't check for the crash of the car on the object because we move it to the top!
        # Top of car is past the bottom of the rectangle
        if y < createRect_starty+createRect_height:

            # If left side of car is between the left side and the right side of the rectangle or the right side of the car is between the left and right of the rectangle
            Left_car_within_rect=x > createRect_startx and x < createRect_startx + createRect_width
            Right_car_within_rect=x+imgWidth > createRect_startx and x + imgWidth < createRect_startx+createRect_width

            # Never make car bigger than object!
            if Left_car_within_rect or Right_car_within_rect:
                crash()

        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
quitgame




