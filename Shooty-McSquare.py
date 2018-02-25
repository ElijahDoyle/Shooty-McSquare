import pygame
import random

class Character:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.lives = 3
        self.invulnerable = False
        self.invulnerableStartTime = False
        self.color = (255,255,255)
        self.blinkStart = True
        self.blinkTime = None
        self.blinkRate = 100


    def display(self,surface):
        pygame.draw.rect(surface,self.color , pygame.Rect(self.x, self.y, self.height, self.width), 0)

    def blink(self,newColor):
        if self.blinkStart == True:
            if pygame.time.get_ticks() > self.blinkTime + self.blinkRate:
                self.color = newColor
                self.blinkStart = False
                self.blinkTime = pygame.time.get_ticks()
        elif self.blinkStart == False:
            if pygame.time.get_ticks() > self.blinkTime + self.blinkRate:
                self.color = (255, 255, 255)
                self.blinkStart = True
                self.blinkTime = pygame.time.get_ticks()

class Projectile:
    def __init__(self, x, y, direction, color):
        self.x = x
        self.y = y
        self.yVelocity = -25 * direction
        self.color = color

    def go(self):
        self.y += self.yVelocity

    def display(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, 20, 50), 0)

class EnemyShip:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xVelocity = 4
        self.yChange = 20
        self.timeShot = None

    def display(self, surface):
        pygame.draw.rect(surface, (70, 50, 50), pygame.Rect(self.x, self.y, 50, 50), 0 )

    def move(self):
        self.x += self.xVelocity
        if self.x <= 0 or self.x >= screenWidth - 50:
            self.xVelocity = -(self.xVelocity)
            self.y += self.yChange

        if self.y >= 220:
            self.yChange = -20
        elif self.y <= 0:
            self.yChange = 20

    def shoot(self):
        shoot(self.x/2 + 5, self.y + 50, projectileList, -1)

class Star:
    def __init__(self,x,y,radius):
        self.x = x
        self.y = y
        self.radius = radius

    def display(self, screen):
        pygame.draw.circle(screen, (150,150,150), ((self.x), (self.y)), (self.radius))

def shoot(x, y, PList, direction, color):
    newProjectile = Projectile(x, y, direction, color)
    PList.append(newProjectile)

def starryBackground(surface):
    starList = []
    for star in range(26):
        star = Star(random.randint(0,790), random.randint(0,690), random.randint(5,11))
        starList.append(star)
    return starList

def createEnemy(x,y, eList):
    newEnemy = EnemyShip(x,y)
    eList.append(newEnemy)

test = Character(400,400,75,75)

pygame.init()
clock = pygame.time.Clock()
screenHeight = 800
screenWidth = 800
screen = pygame.display.set_mode((screenWidth,screenHeight))
done = False
projectileList = []
enemyList = []
timeDestroyed = None
beamStarted = None
beamEnded = None
points = 0
lastHit = 0
pygame.display.set_caption("Shooty McSquare")
quit = False
fired = False

createEnemy(random.randint(0, 730), random.randint(0, 200), enemyList)
createEnemy(random.randint(0, 730), random.randint(0, 200), enemyList)
createEnemy(random.randint(0, 730), random.randint(0, 200), enemyList)

font = pygame.font.SysFont('times new roman', 75)

def displayText(displaySurface, text, x, y, textColor, screenColor):
    text = text + "                                             "
    message = font.render(text, True, textColor, screenColor)
    displaySurface.blit(message, (x, y))

while not quit:
    starList = starryBackground(screen)
    while not done:
        screen.fill((0, 0, 0))

        for star in starList:
            star.display(screen)
            star.y += 2
            if star.y > screenHeight - 100:
                star.y = -5
                star.x = random.randint(0,795)

        if test.invulnerable:
            test.blink((0,0,0))
            if pygame.time.get_ticks() > test.invulnerableStartTime + 2000:
                test.invulnerable = False
                test.color = (255,255,255)
                test.blinkStart = True
                test.blinkTime = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot(test.x + test.width / 2 - 10, test.y, projectileList, 1, (255,0,0))

        for enemy in enemyList:
            enemy.display(screen)
            enemy.move()
            shootCooldown = 2000
            if enemy.timeShot is None:
                enemy.timeShot = pygame.time.get_ticks()
                #shoot(enemy.x + 25, enemy.y + 50, projectileList, -1, (255,100,0))
                #enemy.timeShot = pygame.time.get_ticks()
            elif pygame.time.get_ticks() > enemy.timeShot + shootCooldown:
                shoot(enemy.x + 25, enemy.y + 50, projectileList, -1, (255,0,0))
                enemy.timeShot = pygame.time.get_ticks()
            if enemy.x >= test.x and enemy.x <= test.x + test.width and enemy.y >= test.y and enemy.y <= test.y + test.height and not test.invulnerable:
                test.lives -= 1
                test.invulnerableStartTime = pygame.time.get_ticks()
                test.blinkTime = pygame.time.get_ticks()
                test.invulnerable = True
                points += 1
                enemyList.remove(enemy)

        if len(enemyList) < 2:
            createEnemy(random.randint(0, 750), random.randint(0, 200), enemyList)


        for projectile in projectileList:
            projectile.go()
            projectile.display(screen)
            if projectile.y < -50 or projectile.y > screenHeight - 100:
                projectileList.remove(projectile)
            for enemy in enemyList:
                if projectile.x >= enemy.x and projectile.x <= enemy.x + 50 and projectile.y <= enemy.y + 50 and projectile.y >= enemy.y:
                    enemyList.remove(enemy)
                    projectileList.remove(projectile)
                    timeDestroyed = pygame.time.get_ticks()
                    cooldown = 500
                    points += 1
                if projectile.x >= test.x and projectile.x <= test.x + test.width and projectile.y >= test.y and projectile.y <= test.y + test.height and not test.invulnerable:
                    cooldown = 500
                    if pygame.time.get_ticks() > lastHit + cooldown:
                        test.lives -= 1
                        lastHit = pygame.time.get_ticks()
                        projectileList.remove(projectile)
                    test.invulnerable = True
                    test.invulnerableStartTime = pygame.time.get_ticks()
                    test.blinkTime = pygame.time.get_ticks()

        if timeDestroyed != None and pygame.time.get_ticks() > timeDestroyed + cooldown:
            createEnemy(random.randint(0, 730), random.randint(0, 200), enemyList)
            timeDestroyed = None
            timeShot = None

        if beamEnded != None:
            if pygame.time.get_ticks() >= beamEnded + 3000:
                beamStarted = None
                beamEnded = None
                fired = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            test.y -= 8
        if pressed[pygame.K_DOWN]:
            test.y += 8
        if pressed[pygame.K_LEFT]:
            test.x -= 8
        if pressed[pygame.K_RIGHT]:
            test.x += 8
        if pressed[pygame.K_1]:
            for projectile in projectileList:
                print(projectile)
        if (pressed[pygame.K_w] and beamEnded == None) or fired:
            fired = True
            if beamStarted == None:
                beamStarted = pygame.time.get_ticks()
            elif pygame.time.get_ticks() <= beamStarted + 500:
                shoot(test.x + test.width / 2 - 10, test.y, projectileList, 1, (0,20,225))
            elif pygame.time.get_ticks() > beamStarted + 500:
                beamEnded = pygame.time.get_ticks()
                fired = False

        if test.x < 0:
            test.x = 1
        elif test.x > screenWidth - test.width:
            test.x = screenWidth - test.width - 1
        if test.y < 0:
            test.y = 1
        elif test.y > (screenHeight - 100) - test.height:
            test.y = screenHeight - test.height - 101

        test.display(screen)
        color = (150,150,150)
        message = "Points: " + str(points)
        pygame.draw.rect(screen, color, pygame.Rect(0, screenHeight - 100, screenWidth, 100))
        displayText(screen, message, 0, screenHeight - 100, (0, 0, 255), color)

        if test.lives == 3:
            pygame.draw.rect(screen, (255,255,255),pygame.Rect(500, screenHeight - 75, 50,50))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(600, screenHeight - 75, 50, 50))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(700, screenHeight - 75, 50, 50))
        elif test.lives == 2:
            pygame.draw.rect(screen, (255,255,255),pygame.Rect(500, screenHeight - 75, 50,50))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(600, screenHeight - 75, 50, 50))
        elif test.lives == 1:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(500, screenHeight - 75, 50, 50))

        if beamEnded == None:
            pygame.draw.rect(screen, (0,0,255), pygame.Rect(350, screenHeight - 70, 75, 25), 0)
        elif beamEnded + 1000 > pygame.time.get_ticks() >= beamEnded + 500:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 70, 12, 25), 0)
        elif beamEnded + 1500 > pygame.time.get_ticks() >= beamEnded + 1000:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 70, 25, 25), 0)
        elif beamEnded + 2000 > pygame.time.get_ticks() >= beamEnded + 1500:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 70, 37, 25), 0)
        elif beamEnded + 2500 > pygame.time.get_ticks() >= beamEnded + 2000:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 70, 50, 25), 0)
        elif beamEnded + 3000 > pygame.time.get_ticks() >= beamEnded + 2500:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 70, 62, 25), 0)

        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(350, screenHeight - 70, 75, 25), 2)

        if test.lives == -1:
            for blinks in range(3):
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(test.x, test.y, test.height, test.width), 0)
                pygame.display.flip()
                pygame.time.delay(500)
                test.display(screen)
                pygame.display.flip()
                pygame.time.delay(500)
            done = True

        pygame.display.flip()
        clock.tick(60)

    screen.fill((0, 0, 0))
    reallyDone = False
    while not reallyDone:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quit = True
                reallyDone = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reallyDone = True
                    done = False
                    points = 0
                    test.x = 350
                    test.y = 650
                    test.lives = 3
                    test.invulnerable = True
                    test.invulnerableStartTime = pygame.time.get_ticks()

        displayText(screen, "Game Over", 225, screenHeight - 450, (255, 255, 255), (0, 0, 0))
        pygame.display.flip()
