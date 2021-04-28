import pygame  # pygame package which is used to build games in python & this much be install from online using pip
import random
from math import sqrt
import os
from time import sleep

# to initial the modules in pygame
pygame.init()

# sounds
welcome_music = pygame.mixer.Sound("welcome.wav")
help_music = pygame.mixer.Sound("help_player.wav")
info_music = pygame.mixer.Sound("info.wav")
play_music = pygame.mixer.Sound("play.wav")

bullet = pygame.mixer.Sound("d_shooter.wav")
dragon_= pygame.mixer.Sound("hitvillain.wav")
_villain = pygame.mixer.Sound("v_shooter.wav")
tree_music = pygame.mixer.Sound("hitvillain.wav")
# ex = pygame.mixer.Sound(".wav")
blast = pygame.mixer.Sound("v_shooter.wav")

no = pygame.mixer.Sound("youlose.wav")
win = pygame.mixer.Sound("You_Win.wav")
# lose = pygame.mixer.Sound("you_Lose.wav")


width = 1101  # width of the window screen in game
higth = 600  # higth of the window screen in game

# colours declaring
white = (255, 255, 255)
black = (0, 0, 0)
ligth_blue = (0, 0, 255)
blue = (0, 0, 150)
red = (150, 0, 0)
ligth_red = (255, 0, 0)
green = (0, 150, 0)
ligth_green = (0, 255, 0)
yellow = (150, 150, 0)
ligth_yellow = (255, 255, 0)
color_h = (213, 45, 177)
music_off = (50, 50, 50)
music_on = (150, 150, 150)

# scores
total_score = 0
score = 0
h_score = 0
level = 1


def highest_score():
    global h_score

    if not os.path.exists("h_score.txt"):
        with open("h_score.txt", "wt") as point:
            point.write(f"{h_score}")

    with open("h_score.txt", "rt") as point:
        h_score = point.read()

    h_score = int(h_score)

    if total_score > h_score:
        h_score = total_score
        with open("h_score.txt", "wt") as point:
            point.write(f"{h_score}")


def highest_level():
    if not os.path.exists("level.txt"):
        with open("level.txt", "wt") as point:
            point.write(f"{5}")

    with open("level.txt", "rt") as point:
        high_level = point.read()

    high_level = int(high_level)

    if level > high_level:
        high_level = level
        with open("level.txt", "wt") as point:
            point.write(f"{high_level}")

    return high_level


def scores(increment=0):
    global score
    score = score + increment


# loading the image
logo = pygame.image.load('dragon.png')
bns = pygame.image.load('bns.jpg')
playing_pg = pygame.image.load('fbg.png')
lives = pygame.image.load("energy.png")
finish_fire = pygame.image.load("fire.png")

# changing the size
logo = pygame.transform.scale(logo, (350, 250))
bns = pygame.transform.scale(bns, (350, 250))
playing_pg = pygame.transform.scale(playing_pg, (width, higth))
lives = pygame.transform.scale(lives, (20, 20))
finish_fire = pygame.transform.scale(finish_fire, (50, 50))

# window screen
screen = pygame.display.set_mode((width, higth))

# name of the game
pygame.display.set_caption('DRAGON FIRE')

# setting the logo to the title
pygame.display.set_icon(logo)


# dragon declaration
class Player:
    def __init__(self):
        self.dragon = pygame.image.load("dragon3.png")
        self.dragon = pygame.transform.scale(self.dragon, (100, 100))
        self.dragon_x = width - 400  # constant because dragon cannot move in x direction
        self.dragon_y = random.randint(0, higth - 90)
        self.dragon_change = 0

        # dragon fire
        self.d_fire = pygame.image.load("d_fire.png")
        self.d_fire = pygame.transform.scale(self.d_fire, (32, 32))
        self.fire_list = []
        self.fire_x = 0
        self.fire_y = 0

    def dragon_create(self):

        if self.dragon_y <= 0:
            self.dragon_y = 0
        if self.dragon_y >= higth - 90:
            self.dragon_y = higth - 90
        self.dragon_y += self.dragon_change
        screen.blit(self.dragon, (self.dragon_x, self.dragon_y))

    def fire_dragon(self):
        self.fire_x = self.dragon_x - 10
        self.fire_y = self.dragon_y + 20

        self.fire_list.append([self.fire_x, self.fire_y])

    def fire(self):

        # position are in list in list
        for i in self.fire_list:
            i[0] -= 5
            screen.blit(self.d_fire, i)

            # checking the border
            if i[0] < 0:
                self.fire_list.remove(i)

    def send_position_dragon(self):
        pos = [self.dragon_x, self.dragon_y + 25]
        return pos

    def send_position_fire(self, place):
        pos = self.fire_list[place]  # index of the position is send by parameter
        return pos


# enemy declaration
class Enemy:

    def __init__(self):
        self.villain = pygame.image.load("villain.png")
        self.villain = pygame.transform.scale(self.villain, (100, 100))
        self.villain_x = random.randint(0, 230)
        self.villain_y = random.randint(0, higth - 70)
        self.velocity_x = 1
        self.velocity_y = 1

    def villain_create(self):

        if self.villain_x < 0 or self.villain_x > 230:
            self.velocity_x = -self.velocity_x

        if self.villain_y > higth - 70 or self.villain_y < 0:
            self.velocity_y = -self.velocity_y

        self.villain_x += self.velocity_x
        self.villain_y += self.velocity_y
        screen.blit(self.villain, (self.villain_x, self.villain_y))

    def send_position_villain(self):
        pos = [self.villain_x, self.villain_y + 20]
        return pos


class Shooter:

    def __init__(self):
        # shooter declaration
        self.shooter = pygame.image.load("cannon.png")
        self.shooter = pygame.transform.scale(self.shooter, (64, 64))
        self.shooter_x = 300  # constant position of shooter
        self.shooter_y = 0

        # shooter fire
        self.s_fire = pygame.image.load("fireball.png")
        self.s_fire = pygame.transform.scale(self.s_fire, (32, 32))
        self.fire_x = 0
        self.fire_y = 0
        self.speed = 2
        self.status = "ready"

    def create_shooter(self):
        screen.blit(self.shooter, (self.shooter_x, self.shooter_y))

    def send_position_fireball(self):
        pos = [self.fire_x, self.fire_y]
        return pos

    def send_position_shooter(self):
        pos = [self.shooter_x, self.shooter_y]
        return pos

    def fire_bullet(self):
        self.fire_x += self.speed

        screen.blit(self.s_fire, (self.fire_x, self.fire_y))
        if self.fire_x > width - 230:
            self.become_ready()

    def become_ready(self):
        self.status = "ready"
        self.fire_x = self.shooter_x + 60
        self.fire_y = self.shooter_y + 15


# information of the programmer
def info():
    info_music.play(-1)
    global total_score

    # texts
    t1 = "Name  : SHARATH B N"
    t2 = "AGE : 19"
    t3 = "Date of the game made : 4/10/2020"
    t4 = "This is my first every game, if any problem or suggestion please tell me."
    t5 = "THANK YOU VERY MUCH "
    t6 = "contact no : 8884613804"

    # calling function to give rendered text
    text1 = text_generator(t1, color_h, 36)
    text2 = text_generator(t2, color_h, 36)
    text3 = text_generator(t3, color_h, 36)
    text4 = text_generator(t4, green, 40)
    text5 = text_generator(t5, green, 52)
    text6 = text_generator(t6, color_h, 36)
    # main loop
    run = True
    while run:
        # drawing and filling the images & texts to screen
        screen.fill(white)
        screen.blit(playing_pg, (0, 0))
        screen.blit(bns, (width - 500, 50))
        screen.blit(text1, (150, 150))
        screen.blit(text2, (150, 200))
        screen.blit(text3, (150, 250))
        screen.blit(text6, (150, 300))
        screen.blit(text4, (100, 350))
        screen.blit(text5, (350, 400))

        # bottons
        button_generator(green, 200, higth - 100, "play", black)
        button_generator(red, 800, higth - 100, "back", black)

        # events chicking loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    info_music.stop()
                    play(level)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    info_music.stop()
                    run = False

            if event.type == pygame.MOUSEMOTION:
                if (200 < event.pos[0] < 200 + 100) and (higth - 100 < event.pos[1] < higth - 100 + 50):
                    button_generator(ligth_green, 200, higth - 100, "play", black)

                if (800 < event.pos[0] < 800 + 100) and (higth - 100 < event.pos[1] < higth - 100 + 50):
                    button_generator(ligth_red, 800, higth - 100, "back", black)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (200 < event.pos[0] < 200 + 100) and (higth - 100 < event.pos[1] < higth - 100 + 50):
                    info_music.stop()
                    total_score = 0
                    play(1)

                if (800 < event.pos[0] < 800 + 100) and (higth - 100 < event.pos[1] < higth - 100 + 50):
                    info_music.stop()
                    run = False

        pygame.display.update()


# creating the texts
def text_generator(t_text, t_color, f_size):
    # declaring font class with has font style is default system(none specifies) & 60 is size
    font = pygame.font.Font(None, f_size)
    # rendering text of user to image
    text = font.render(t_text, True, t_color)
    return text


# creating botton
def button_generator(b_color, b_x, b_y, t_text, t_color):
    # calling function to get text
    text = text_generator(t_text, t_color, 40)

    # drawing the rectangle for botton
    pygame.draw.rect(screen, b_color, (b_x, b_y, 100, 50), 0)
    # blitting the text
    screen.blit(text, (b_x + 20, b_y + 10))


# level declaration
def levels(increase=0):
    global level

    level += increase
    highest_level()
    #  sleep(3)
    return


# this function helps how to play & what kind of game is.
def help_player():
    help_music.play(-1)
    global total_score
    global level
    # tests
    t8 = "IF TREE BURNS YOU LOSE 50 O2."
    t1 = "SAVE THE TREE TO SURVIVE. "
    t2 = "--> USE THE ARROW KEYS UP & DOWN FOR PLAYER MOVEMENT. "
    t3 = "--> USE THE SPACES KEY FOR FIRING."
    t5 = " 1 O2 FOR BURNING FIREBALL."
    t6 = " 5 O2 FOR BURNING SHOOTER."
    t7 = " 10 O2 FOR BURNING VILLAIN."
    t4 = "--> USE THE 'H' KEY FOR HELP."

    # Calling function to give the rendered test
    text1 = text_generator(t1, ligth_green, 72)
    text2 = text_generator(t2, color_h, 36)
    text3 = text_generator(t3, color_h, 36)
    text4 = text_generator(t4, color_h, 36)
    text5 = text_generator(t5, ligth_red, 36)
    text6 = text_generator(t6, ligth_red, 36)
    text7 = text_generator(t7, ligth_red, 36)
    text8 = text_generator(t8, ligth_red, 36)

    # main loop
    run = True
    while run:
        # drawing & filling the text & images to screen
        screen.fill(white)
        screen.blit(playing_pg, (0, 0))
        screen.blit(text1, (150, 50))
        screen.blit(text2, (150, 150))
        screen.blit(text3, (150, 200))
        screen.blit(text4, (150, 250))
        screen.blit(text5, (150, 300))
        screen.blit(text6, (150, 350))
        screen.blit(text7, (150, 400))
        screen.blit(text8, (150, 450))

        # bottons

        button_generator(green, 200, higth - 100, "play", black)
        button_generator(red, 800, higth - 100, "back", black)

        # events chicking loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    help_music.stop()
                    play(level)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    help_music.stop()
                    run = False

            if event.type == pygame.MOUSEMOTION:
                if (200 < event.pos[0] < 200 + 100) and (higth - 100 < event.pos[1] < higth - 100 + 50):
                    button_generator(ligth_green, 200, higth - 100, "play", black)

                if (800 < event.pos[0] < 800 + 100) and (higth - 100 < event.pos[1] < higth - 100 + 50):
                    button_generator(ligth_red, 800, higth - 100, "back", black)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (200 < event.pos[0] < 200 + 100) and (higth - 100 < event.pos[1] < higth - 100 + 50):
                    help_music.stop()
                    level = 1
                    total_score = 0
                    play(level)

                if (800 < event.pos[0] < 800 + 100) and (higth - 100 < event.pos[1] < higth - 100 + 50):
                    help_music.stop()
                    run = False

        pygame.display.update()
    return


def play_again(text, reason, condition):
    welcome_music.play(-1)

    global total_score
    total_score += score
    levels(1)
    level_image = text_generator("LEVEL : " + str(level), green, 100)
    totalscore_image = text_generator("Total score: " + str(total_score) + " O2", ligth_green, 100)
    retry_image = text_generator("To play again, press retry by losing 50 scores in total score.", ligth_blue, 50)

    reason_image = text_generator(reason, ligth_red, 64)
    # main loop
    run = True
    while run:
        # drawing & filling the text & images to screen
        screen.fill(white)
        screen.blit(playing_pg, (0, 0))
        screen.blit(level_image, (400, 100))
        screen.blit(totalscore_image, (250, 200))
        screen.blit(reason_image, (250, 400))

        if condition is False:
            screen.blit(retry_image, (50, 30))
        # bottons

        button_generator(green, 200, higth - 100, text, black)
        button_generator(red, 800, higth - 100, "back", black)

        # events chicking loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    if condition is False:
                        welcome_music.stop()

                        if total_score >= 50:
                            total_score -= 50
                            play(level)
                        else:
                            welcome_music.stop()
                            welcome()
                    else:
                        welcome_music.stop()

                        play(level)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    welcome_music.stop()

                    welcome()

            if event.type == pygame.MOUSEMOTION:
                if (200 < event.pos[0] < 200 + 100) and (higth - 100 < event.pos[1] < higth - 100 + 50):
                    button_generator(ligth_green, 200, higth - 100, text, black)

                if (800 < event.pos[0] < 800 + 100) and (higth - 100 < event.pos[1] < higth - 100 + 50):
                    button_generator(ligth_red, 800, higth - 100, "back", black)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (200 < event.pos[0] < 200 + 100) and (higth - 100 < event.pos[1] < higth - 100 + 50):
                    if condition is False:
                        welcome_music.stop()

                        if total_score >= 50:
                            total_score -= 50
                            welcome_music.stop()
                            play(level)
                        else:
                            welcome_music.stop()

                            welcome()
                    else:
                        welcome_music.stop()
                        play(level)

                if (800 < event.pos[0] < 800 + 100) and (higth - 100 < event.pos[1] < higth - 100 + 50):
                    welcome_music.stop()

                    welcome()

        pygame.display.update()
    return


# this is the main game playing function
def play(level_start):

    global score, h_score
    score = 0
    lives_image = text_generator("Lives", blue, 60)
    score_image = text_generator("Score: ", green, 50)

    # lives of dradon
    lives_list = []
    for l in range(3):
        lives_list.append([width - 200 + (l * 25), 200])

    # enemy object list
    enemy_list = []
    for i in range(level_start):
        enemy_list.append(Enemy())

    # player object
    player = Player()

    # shooter object
    shooter_list = []
    for i in range(0, 9):  # higth/65 =9. something
        shooter_list.append(Shooter())
        shooter_list[i].shooter_y = i * 65
        shooter_list[i].become_ready()

    tree = pygame.image.load("tree.png")
    tree = pygame.transform.scale(tree, (64, 64))
    tree_position = []
    for i in range(0, 9):
        tree_x = width - 300
        tree_y = i * 65
        tree_position.append([tree_x, tree_y])

    # main loop
    run = True
    play_music.play(-1)

    while run:

        score_image1 = text_generator(str(score) + " O2", ligth_green, 50)

        # drawing & filling the images and tests
        screen.fill(white)
        screen.blit(playing_pg, (0, 0))
        screen.blit(lives_image, (width - 200, 150))
        screen.blit(score_image, (width - 200, 250))
        screen.blit(score_image1, (width - 200, 300))
        player.dragon_create()

        # lives creation
        for i in lives_list:
            screen.blit(lives, i)

        # tree creation
        for i in tree_position:
            screen.blit(tree, i)

        # enemy creation
        for i in enemy_list:
            i.villain_create()

        # shooter creation
        for i in shooter_list:
            i.create_shooter()

        # events checking loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
            # checking the arrow key to move dragon
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.dragon_change = -5

                if event.key == pygame.K_DOWN:
                    player.dragon_change = 5

            # checking the arrow key release
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.dragon_change = 0

            # checking the fire key of space
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.fire_dragon()

            # cheching of help key h
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    play_music.stop()
                    help_player()

        # firing of player
        if player.fire_list != []:
            player.fire()

        # firing of shooter when the villain meets shooter
        for i in enemy_list:
            for j in shooter_list:
                if near_by(i.send_position_villain(), j.send_position_shooter()) < 100:
                    j.status = "firing"

        # fireball movement
        for i in shooter_list:
            if i.status == "firing":
                i.fire_bullet()

        # collision between tree(lifes) & fireball

        for i in shooter_list:
            for k in tree_position:
                a = i.send_position_fireball()
                b = k
                d = near_by(a, b)
                if d < 20:
                    tree_music.play()  # sound

                    tree_position.remove(k)
                    i.become_ready()
                    screen.blit(finish_fire, k)
                    scores(-50)

        # collision in playing
        for i in shooter_list:
            for k in player.fire_list:
                a = i.send_position_fireball()  # position of shooter fire

                b = player.send_position_fire(player.fire_list.index(k))  # position of dragon fire

                c = i.send_position_shooter()  # position of shooter

                dragon_fire_fireball = near_by(a, b)

                shooter_dragonfire = near_by(b, c)

                # collision between shooter & dragon fire
                if shooter_dragonfire < 40:
                    blast.play()

                    player.fire_list.remove(k)
                    shooter_list.remove(i)
                    screen.blit(finish_fire, c)
                    scores(5)

                # collision between fire ball & dragon fire
                if dragon_fire_fireball < 20 and i.status != "ready":
                    bullet.play()

                    i.become_ready()
                    player.fire_list.remove(k)
                    screen.blit(finish_fire, a)
                    scores(1)

        # collision between villain & dragon fire
        for i in enemy_list:
            for k in player.fire_list:
                a = i.send_position_villain()  # position of villain
                b = player.send_position_fire(player.fire_list.index(k))  # position of dragon fire
                fire_enmey = near_by(a, b)

                if fire_enmey < 50:
                    _villain.play()

                    enemy_list.remove(i)
                    player.fire_list.remove(k)
                    screen.blit(finish_fire, a)
                    score += 10

        # collision between fireball & dragon
        for i in shooter_list:
            a = i.send_position_fireball()  # position of shooter fire
            b = player.send_position_dragon()  # position of dragon
            dragon_fireball = near_by(a, b)

            if dragon_fireball < 45:
                dragon_.play()

                i.become_ready()
                lives_list.pop()
                if lives_list == []:
                    play_music.stop()
                    no.play()
                    run = False
                    screen.blit(finish_fire, b)
                    sleep(1)
                    play_again("retry", "YOUR LIVES ARE OVER", False)

        # next level
        if enemy_list == []:
            play_music.stop()
            win.play()
            run = False
            sleep(1)

            play_again("next", "YOU KILLED THE MONSTER", True)

        # game over
        if tree_position == []:
            play_music.stop()
            no.play()
            run = False
            sleep(1)
            play_again("retry", "YOU DID NOT SAVE THE TREE, SO DIED", False)
        pygame.display.update()

    return


def near_by(a, b):
    distance = sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))
    return distance


# this is the home page or first page of the game
def welcome():
    highest_score()

    highscore_image = text_generator("High score: " + str(h_score), ligth_green, 100)
    level_image = text_generator("Highest level: " + str(highest_level()), green, 80)

    global total_score
    total_score = 0

    # highest level storing & printing

    global level
    level = 1

    # main loop
    run = True
    while run:
        welcome_music.play(-1)
        # drawing & filling screen
        screen.fill(white)
        screen.blit(playing_pg, (0, 0))
        screen.blit(logo, (width - 500, 50))
        screen.blit(highscore_image, (350, higth - 150))
        screen.blit(level_image, (350, higth - 80))

        # bottons

        button_generator(green, 250, 50, "play", black)
        button_generator(yellow, 250, 150, "help", black)
        button_generator(red, 250, 250, "quit", black)
        button_generator(blue, 250, 350, "info", black)

        # events loops
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # shortcut to play , help , info ,quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    welcome_music.stop()
                    play(level)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    welcome_music.stop()
                    help_player()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    welcome_music.stop()
                    info()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    welcome_music.stop()
                    quit()

            # mouse motin & mouse click event checking
            if event.type == pygame.MOUSEMOTION:
                if 250 < event.pos[0] < 250 + 100 and 50 < event.pos[1] < 50 + 50:
                    button_generator(ligth_green, 250, 50, "play", black)

                if 250 < event.pos[0] < 250 + 100 and 150 < event.pos[1] < 150 + 50:
                    button_generator(ligth_yellow, 250, 150, "help", black)

                if 250 < event.pos[0] < 250 + 100 and 250 < event.pos[1] < 250 + 50:
                    button_generator(ligth_red, 250, 250, "quit", black)

                if 250 < event.pos[0] < 250 + 100 and 350 < event.pos[1] < 350 + 50:
                    button_generator(ligth_blue, 250, 350, "info", black)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 250 < event.pos[0] < 250 + 100 and 50 < event.pos[1] < 50 + 50:
                    welcome_music.stop()
                    play(level)

                if 250 < event.pos[0] < 250 + 100 and 150 < event.pos[1] < 150 + 50:
                    welcome_music.stop()
                    help_player()

                if 250 < event.pos[0] < 250 + 100 and 250 < event.pos[1] < 250 + 50:
                    run = False
                    quit()

                if 250 < event.pos[0] < 250 + 100 and 350 < event.pos[1] < 350 + 50:
                    welcome_music.stop()
                    info()

        pygame.display.update()


welcome()
pygame.quit()
quit()
