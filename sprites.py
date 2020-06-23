""" You've probably come across sprites in Scratch. Sprites are a good way to
organise anything that moves, anything that could affect something that moves
and many other things. Most things that aren't variables (score) or constants
(screen height) could be sprites. Sprites are a special type of `class`.

First we have to set up some variables that will the settings of each sprite
will be held in """
from pygame import *
from settings import *
from random import *
from datetime import *

## groups
#pygame.sprite x 3
all_sprites = sprite.Group()
bg_sprites = sprite.Group()
balls = sprite.Group()
blobs = sprite.Group()
collectables = sprite.Group()

## sprites
"""this gets confusing now!"""

#pygame.sprite
class Ball(sprite.Sprite):
    """ The __init__ section sets up a new sprite for the first time """    
    def __init__(self, direction = DIRECTIONS[randint(0,3)]):
        #pygame.sprite - this is required for a pygame sprite
        sprite.Sprite.__init__(self)
        """ You can use an image in here, but this is just a rectangle """
##        self.image = Surface((BALL_SIZE, BALL_SIZE))
##        self.image.fill(BALL_COLOR)


        self.image = BALL_IMG
        self.rotation = float(randint(-359,0))
        self.image = transform.rotate(self.image,self.rotation)

        """ This sets up a few coordinates like top, left, center, bottom left""" 
        self.rect = self.image.get_rect()
        self.rect.center = (randint(LEFT,RIGHT),randint(TOP, BOTTOM))
        self.direction = direction
        self.speed = BALL_SPEED

        ## sfx
        mixer.Channel(1).play(NEW_BALL,1)
              
    """ The update section changes the sprite between frames. Useful for movements """
    def update(self,keys):
        """ This handles the multiball in Quad Pong """

        global player
        speed = int(self.speed)

        ## ------- x movement ---------
        if self.direction[0] == "right" and self.rect.right < RIGHT:
            self.rect.x += speed
        elif self.direction[0] == "right" and self.rect.right >= RIGHT:
            self.rect.x -= speed
            self.direction = ("left", self.direction[1])
            self.speed += 0.002
        elif self.direction[0] == "left" and self.rect.left > LEFT:
            self.rect.x -= speed
            self.speed += 0.002
        elif self.direction[0] == "left" and self.rect.left <= LEFT:
            self.rect.x += speed
            self.direction = ("right", self.direction[1])
            self.speed += 0.002

        ## ------- y movement ---------
        if self.direction[1] == "up" and self.rect.top > TOP:
            self.rect.y -= speed
        elif self.direction[1] == "up" and self.rect.top <= TOP:
            self.rect.y += speed
            self.direction = (self.direction[0], "down",)
            self.speed += 0.002
        elif self.direction[1] == "down" and self.rect.bottom < BOTTOM:
            self.rect.y += speed
            self.speed += 0.002
        elif self.direction[1] == "down" and self.rect.bottom >= BOTTOM:
            self.rect.y -= speed
            self.direction = (self.direction[0], "up",)
            self.speed += 0.002

    def draw(self):
        SCREEN.blit(self.image, self.rect)

##    def kill(self):
##        SFX_CH.play(BLOB_EATEN,1)

class BG_Square(sprite.Sprite):

    def __init__(self):
        sprite.Sprite.__init__(self)
        self.size = randint(5,100)
##        self.image = Surface((self.size, self.size))
##        self.image.fill((92, 205, 198))
        self.image = BG_SQUARE_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (randint(0,WIDTH),randint(0,HEIGHT))
        self.direction =  DIRECTIONS[randint(0,7)]
        self.size = randint(5,100)
        self.image = transform.scale(self.image, (self.size,self.size))
        self.speed = randint(1,4)

    def update(self,keys):
        x_dir = self.direction[0]
        y_dir = self.direction[1]

        if x_dir == "left":
            self.rect.x -= self.speed
        elif x_dir == "right":
            self.rect.x += self.speed
        if y_dir == "up":
            self.rect.y -= self.speed
        elif y_dir == "down":
            self.rect.y += self.speed

        if self.rect.right <= LEFT or self.rect.bottom <= TOP or self.rect.left >= RIGHT or self.rect.top >= BOTTOM:
            self.kill()

    def draw(self):
        SCREEN.blit(self.image, self.rect)

class Collectable (sprite.Sprite):

    def __init__(self, _type):
        sprite.Sprite.__init__(self)
        self.image = BLOB_LRG_ALT_IMG
##        self.image = Surface((2 * BLOB_SIZE, 2 * BLOB_SIZE))
##        self.image.fill((240, 140, 160))
        self.rect = self.image.get_rect()
        self.rect.center = (randint(MARGIN, RIGHT), randint(TOP_MARGIN, BOTTOM))
        self.type = _type

        ## sfx
        mixer.Channel(1).play(NEW_BALLEATER,1)

    def draw(self):
        SCREEN.blit(self.image, self.rect)

        
class Blob(sprite.Sprite):

    def __init__(self):
        sprite.Sprite.__init__(self)
##        self.image = Surface((BLOB_SIZE, BLOB_SIZE))
##        self.image.fill(BLOB_COLOR)
        self.image = BLOB_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (randint(LEFT,RIGHT),randint(TOP, BOTTOM))
        self.speed = BLOB_SPEED
        self.collectable_ready = False
        self.collected_at = None
        self.collected = None
        self.invincable = False

        ## sfx
        mixer.Channel(1).play(NEW_BLOB)

    def update(self,keys):
        global do_tutorial, generate_balleater, blobs
        if (keys[K_UP] or keys[K_w]) and self.rect.center[1] > TOP:
            #move up
            self.rect.y -= self.speed
        elif (keys[K_UP] or keys[K_w]) and self.rect.center[1] <= TOP:
            #wrap to bottom
            self.rect.y += HEIGHT - (TOP_MARGIN + MARGIN)
        
        if (keys[K_DOWN] or keys[K_s]) and self.rect.center[1] < BOTTOM:
            #move down
            self.rect.y += self.speed
        elif (keys[K_DOWN] or keys[K_s]) and self.rect.center[1] >= BOTTOM:
            #wrap to top
            self.rect.y -= HEIGHT - (TOP_MARGIN + MARGIN)
        
        if (keys[K_LEFT] or keys[K_a]) and self.rect.center[0] > LEFT:
            #move left
            self.rect.x -= self.speed
        elif (keys[K_LEFT] or keys[K_a]) and self.rect.center[0] <= LEFT:
            #wrap to right
            self.rect.x += WIDTH - (2 * MARGIN)
        
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.center[0] < RIGHT:
            #move right
            self.rect.x += self.speed
        elif (keys[K_RIGHT] or keys[K_d]) and self.rect.center[0] >= RIGHT:
            #wrap to bottom
            self.rect.x -= WIDTH - (2 * MARGIN)

        if self.collected:
            if self.collected == "BallEater":
                time_now = datetime.now()
                if (time_now.microsecond % 500) <= 200:
##                    self.image = Surface((2 * BLOB_SIZE, 2 * BLOB_SIZE))
##                    self.image.fill(BLOB_COLOR)
                    self.image = BLOB_LRG_IMG
                else:
##                    self.image = Surface((2 * BLOB_SIZE, 2 * BLOB_SIZE))
##                    self.image.fill((240, 140, 160))
                    self.image = BLOB_LRG_ALT_IMG
                diff = time_now - self.collected_at
                if diff.seconds >= 5:
                    self.collected = None
                    self.invincable = False
                    self.collected_at = None
##                    self.image = Surface((BLOB_SIZE, BLOB_SIZE))
##                    self.image.fill(BLOB_COLOR)
                    self.image = BLOB_IMG
                stop_sfx = True
                for blob in blobs:
                    if blob.collected == True:
                        stop_sfx = False
                if stop_sfx == True:
                    COLLECTABLE_ACTIVE_CH.fadeout(2)

    """ draw puts the sprite on the screen """
    def draw(self):
        SCREEN.blit(self.image, self.rect)

    def _kill(self):
        global run_timer
        self.kill()
        if player.lives > 0:
            new_ball = Ball()
            balls.add(new_ball)
            all_sprites.add(new_ball)
            run_timer = True
        else:
            game.game_over()

    def clean(self):
        self.kill()


## ------------------ OTHER CLASSES --------------------
""" Not every object needs to be a sprite, some can be simple classes,
like the player in Quad Pong. The player isn't on screen, so doesn't move
or interact with anything on screen, except using the keyboard. Player
may only need lives and score, but there might be coins, XP, levels etc """

class Player():

    def __init__(self):
        self.score = 0
        self.lives = 3
        self.hp = 100
        self.xp = 0
        self.level = 0
        self.max_hp = LEVEL_MAX_HP[0]
        self.score_increment = 1
        self.earn_points = False
        self.extra_blob = 0
        self.new_blob = False
        self.extra_ball = -501
        self.new_ball = False
        self.game_over = False
        self.tutorial_running = False
        self.tutorial_step = False

    def update(self):
        global blob, balls, game
        self.score += self.score_increment
        #print (self.score, self.extra_blob, self.extra_ball)
        if self.score >= self.extra_blob:
            print("new blob")
            self.new_blob = True
        if self.score > self.extra_ball:
            self.new_ball = True
    
    def lose_hp(self, hp = 10):
        self.hp -= hp
        if self.hp <= 0:
            self.lose_life()

    def lose_life(self):
        self.lives -= 1
        self.earn_points = False
        if self.lives == 0:
            self.game_over = True
            
    def gain_xp(self, xp):
        self.xp += xp
        if LEVEL_UP[(level + 1)] <= xp:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp = LEVEL_MAX_HP[self.level]

        
class Game():
    def __init__(self, do_tutorial):
        self.running = True
        self.paused = False
        self.countdown = True
        self.confirm_quit = False
        self.quit = False
        self.msg = "Welcome to " + TITLE
        self.new_ball = True
        self.new_blob = True
        self.countdown_start = None
        self.pause_delay = 0
        self.game_over = False
        self.game_over_countdown_start = None
        self.first_time = True
        self.do_tutorial = do_tutorial
        self.tutorial= False
        self.tutorial_start = None
        self.tutorial_balleater = False
        self.tutorial_step = (0,0)
        self.tutorial_running = do_tutorial
        self.top_msg = ""
        
        
    def toggle_pause(self):
        self.pause_delay = PAUSE_DELAY
        if self.paused:
            self.paused = False
            self.msg = ""
        else:
            self.paused = True
            self.msg = "Paused"

       
    def respond(self, letter):
        if self.confirm_quit == True and letter == "y":
            self.quit = True
        if self.confirm_quit == True and letter == "n":
            self.msg = ""
            self.confirm_quit = False
            self.countdown = True

