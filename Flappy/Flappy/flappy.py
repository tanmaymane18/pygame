import pygame
import random
import os

img_dir = os.path.join(os.path.dirname(__file__), 'img')
snd_dir = os.path.join(os.path.dirname(__file__), 'sound')

# CONSTANTS 
width = 288
height = 512
fps = 60
frame_count = 0
gap = 100
score = 0
font_name = pygame.font.match_font('arial')
base_height = int(height - height*(3/4))
# CLOCK
clock = pygame.time.Clock()
# COLOURS 
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
# INITIALISING PYGAME
pygame.init()
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")
# FUNCTIONS

def score_count(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, white)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surf.blit(text_surface, text_rect)

def newbar(length):
        upper = upper_bar(length)
        all_sprites.add(upper)
        bars.add(upper)
        lower = lower_bar(length)
        all_sprites.add(lower)
        bars.add(lower)
# CLASSES OF SPRITES
class bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bird_img, (30,30))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = (35, height/2)
        self.gravity = 0
        self.speedy = 0
        self.lift = -7

    def update(self):
        self.speedy += self.gravity
        self.rect.y += self.speedy
        # CHECKING IF BIRD HITS BOTTOM
        if self.rect.bottom > height-60 :
            self.rect.bottom = height-60
            self.speedy = 0

    def up(self):
        # GRAVITY EXISTS AFTER THE FIRST 'SPACE'
        self.gravity = 0.3
        # LIFTS TH BIRD WHENEVER 'SPACE'
        self.speedy += self.lift
        self.rect.y += self.speedy
        
class upper_bar(pygame.sprite.Sprite):
    def __init__(self, length):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(bar_img, 180)
        self.image = pygame.transform.scale(self.image, (40, length))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = width+500
        
    def update(self):
        self.rect.x -= 2
        if self.rect.right < 0 :
                self.kill()
        if self.rect.right == 20 :
                global score
                score += 1
class lower_bar(pygame.sprite.Sprite):
    def __init__(self, length_upper):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bar_img, (40, height - base_height-(length_upper+gap)))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.bottom = height - base_height
        self.rect.left = width+500

    def update(self):
        self.rect.x -= 2


class base(pygame.sprite.Sprite):
        def __init__(self, prev_right):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.transform.scale(base_img, (10*width, base_height))
                self.rect = self.image.get_rect()
                self.rect.bottom = height
                self.rect.left = prev_right

        def update(self):
                self.rect.x -= 2
                if self.rect.right < 0:
                       self.rect.left = 10*width
        

# LOAD ALL GRAPHICS
background_1 = pygame.image.load(os.path.join(img_dir, "background-day.png")).convert()
background_2 = pygame.image.load(os.path.join(img_dir, "background-night.png")).convert()
background_rect = background_1.get_rect()
background_list = [background_1, background_2]
background = random.choice(background_list)
bird_img_1 = pygame.image.load(os.path.join(img_dir, "bluebird-midflap.png")).convert()
bird_img_2 = pygame.image.load(os.path.join(img_dir, "redbird-midflap.png")).convert()
bird_img_3 = pygame.image.load(os.path.join(img_dir, "yellowbird-midflap.png")).convert()
bird_list = [bird_img_1, bird_img_2, bird_img_3]
bird_img = random.choice(bird_list)
bar_img_red = pygame.image.load(os.path.join(img_dir, "pipe-red.png")).convert()
bar_img_green = pygame.image.load(os.path.join(img_dir, "pipe-green.png")).convert()
bar_list = [bar_img_red, bar_img_green]
bar_img = random.choice(bar_list)
base_img = pygame.image.load(os.path.join(img_dir, "base.png")).convert()
# SPRITES
all_sprites = pygame.sprite.Group()
bars = pygame.sprite.Group()
Bird = bird()
all_sprites.add(Bird)
Base_1 = base(0)
Base_2 = base(width)
all_sprites.add(Base_1)
all_sprites.add(Base_2)
# LEGTH OF THE UPPER BAR
length = random.randrange(10, base_height)
newbar(length)
# GAME LOOP
running = True

while running :
    clock.tick(fps)
    frame_count += 1
    # EVENT HANDLING
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE:
                Bird.up()
    # CREATING NEW BARS 
    if frame_count % 70 == 0 and frame_count > 0  :
        length = random.randrange(10, base_height)
        newbar(length)
    # CHECKING IF BIRD HITS THE BARS
    hits = pygame.sprite.spritecollide(Bird, bars, False)
    for hit in hits:
        running = False
    # UPDATE
    all_sprites.update()
    pygame.display.update()
    # DRAW
    gameDisplay.blit(background, background_rect)
    all_sprites.draw(gameDisplay)
    score_count(gameDisplay, str(score), 20, width/2, 10)
    
pygame.quit()

