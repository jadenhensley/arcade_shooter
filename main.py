from pickle import TRUE
import pygame, sys, path_util, random

PROJECT_PATH = path_util.get_project_directory()

pygame.init()
pygame.font.init()
pygame.mixer.init()

sWidth = 800
sHeight = 800

pygame.display.set_caption("Arcade Shooter by @jadenhensley (GitHub)")
screen = pygame.display.set_mode((sWidth, sHeight))

BACKGROUND_IMG = pygame.image.load(f"{PROJECT_PATH}/sprites/black.png")
ENEMY_IMAGES = [
    pygame.image.load(f"{PROJECT_PATH}/sprites/enemyBlack1.png"),
    pygame.image.load(f"{PROJECT_PATH}/sprites/enemyBlue1.png"),
    pygame.image.load(f"{PROJECT_PATH}/sprites/enemyGreen1.png"),
    pygame.image.load(f"{PROJECT_PATH}/sprites/enemyRed1.png"),
]
METEOR_IMAGES = [
    pygame.image.load(f"{PROJECT_PATH}/sprites/meteorGrey_med1.png"),
    pygame.image.load(f"{PROJECT_PATH}/sprites/meteorGrey_med2.png"),
    pygame.image.load(f"{PROJECT_PATH}/sprites/meteorGrey_small1.png"),
    pygame.image.load(f"{PROJECT_PATH}/sprites/meteorGrey_small2.png")
]

PLAYER_IMG = pygame.image.load(f"{PROJECT_PATH}/sprites/playerShip3_red.png")
P_LASER_IMG = pygame.image.load(f"{PROJECT_PATH}/sprites/laserBlue02.png")
E_LASER_IMG = pygame.image.load(f"{PROJECT_PATH}/sprites/laserRed02.png")

clock = pygame.time.Clock()
monogram = pygame.font.Font(f"{PROJECT_PATH}/font/monogram.ttf", 32)
monogramXL = pygame.font.Font(f"{PROJECT_PATH}/font/monogram.ttf", 56)
# forgot

def printg(text, x, y, color=(255,255,255)):
    text = monogram.render(text, True, color)
    screen.blit(text, (x, y))

def printgLarge(text, x, y, color=(255,255,255)):
    text = monogramXL.render(text, True, color)
    screen.blit(text, (x, y))

laser_group = []

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(ENEMY_IMAGES)
        self.image = pygame.transform.scale(self.image, (self.image.get_width()//2, self.image.get_height()//2))
        self.rect = self.image.get_rect()
        self.rect.top = 100
        self.rect.left = random.randint(100, sWidth - 100)
        self.direction = "right"
        
    def update(self):
        screen.blit(self.image, self.rect.topleft)
        if self.direction == "right":
            self.rect.right += random.randint(10,20)
        if self.direction == "left":
            self.rect.left -= random.randint(10,10)
        if self.rect.left < 0:
            self.direction = "right"
            self.rect.y += 50
        if self.rect.right > sWidth:
            self.direction = "left"
            self.rect.y += 50
        # if self.rect.colliderect(PlayerLaser()):
        for laser in laser_group:
            if self.rect.colliderect(laser.rect):
                p.score += 1
                self.kill()
        if self.rect.colliderect(p.rect):
            p.kill()
            g.current_scene = "game_over"

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(METEOR_IMAGES)
        self.rect = self.image.get_rect()
        self.rect.centery = random.randint(0, sHeight // 2)
        self.rect.centerx = random.randint(0, sWidth // 2)
    
    def update(self):
        screen.blit(self.image, self.rect.topleft)
        self.rect.bottom += 10
        self.rect.left += 10

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect()
        self.rect.bottom = sHeight - 100
        self.rect.centerx = sWidth // 2 - 30
        self.RIGHT, self.LEFT, self.SPACE = False, False, False
        self.lasercount = 0
        self.max_lasers = 8
        self.lastTick = 0
        self.score = 0

    def update(self):
        screen.blit(self.image, self.rect.topleft)
        if self.RIGHT:
            self.rect.right += 10
        if self.LEFT:
            self.rect.left -= 10
        if self.SPACE:
            if self.lasercount < self.max_lasers:
                temp = PlayerLaser()
                e.add(temp)
                laser_group.append(temp)
                self.lasercount += 1

class PlayerLaser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = P_LASER_IMG
        self.rect=self.image.get_rect()
        self.rect.bottom = p.rect.top
        self.rect.centerx = p.rect.centerx
    
    def update(self):
        screen.blit(self.image, self.rect.topleft)
        self.rect.bottom -= 10
        

class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = E_LASER_IMG
        self.rect=self.image.get_rect()
        # need to get position from specific enemy


    def update(self):
        screen.blit(self.image, self.rect.topleft)



class Game:
    def __init__(self):
        self.current_scene = 'start'
    
    def state_machine(self):
        if self.current_scene == 'start':
            self.start()
        elif self.current_scene == 'game':
            self.game()
        elif self.current_scene == 'game_over':
            self.game_over()


    def start(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.current_scene = "game"

        screen.fill((40,40,40))
        printgLarge("Arcade Shooter", sWidth // 4, sHeight // 2, (0,255,0))
        printgLarge("Press Enter/Return key to start.", sWidth // 8, sHeight // 2 + 50, (255,255,255))
        clock.tick(60)
        pygame.display.update()
        pygame.display.flip() # forgot


    def game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    p.LEFT, p.RIGHT = True, False
                if event.key == pygame.K_RIGHT:
                    p.RIGHT, p.LEFT = True, False
                if event.key == pygame.K_SPACE:
                    p.SPACE = True
            if event.type == pygame.KEYUP: # KEYUP / KEYDOWN, not pygame.key.get_pressed()
                if event.key == pygame.K_LEFT:
                    p.LEFT = False
                if event.key == pygame.K_RIGHT:
                    p.RIGHT = False
                if event.key == pygame.K_SPACE:
                    p.SPACE = False

        screen.fill((40,40,40))
        clock.tick(60)

        ticks = pygame.time.get_ticks()
        if ticks % 50 == 0:
            e.add(Enemy())
            p.lasercount = 0
        if ticks % 100 == 0:
            e.add(Enemy())
            p.lasercount = 0
        if ticks % 5 == 0:
            e.add(Meteor())


        p.update()
        e.update()

        printgLarge(f"score: {p.score}", sWidth // 12, 10, (255,215,40))
        pygame.display.update()
        pygame.display.flip() # forgot


    def game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.current_scene = "game"

        screen.fill((40,40,40))
        printgLarge("Game Over", sWidth // 4, sHeight // 2, (0,255,0))
        printgLarge(f"Your Score: {p.score}", sWidth // 4 - 20, sHeight // 2 + 100, (255,255,255))
        clock.tick(60)
        pygame.display.update()
        pygame.display.flip() # forgot


g = Game()
p = Player()
e = pygame.sprite.Group()

while True:
    g.state_machine()
    clock.tick(60) # note: even outside of game class, we should have the clock.tick() method being called.