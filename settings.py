##--------------- CONSTANTS -------------------
from os import *
from pygame import *


## local files
HOME_FOLDER = path.dirname(__file__)
IMG_FOLDER = path.join(HOME_FOLDER,"img")
MP3_FOLDER = path.join(HOME_FOLDER,"mp3")
BG_MUSIC_FOLDER = path.join(MP3_FOLDER,"bg_music")
SFX_FOLDER = path.join(MP3_FOLDER,"sfx")

## images
def load_img(img_fn):
    return image.load(path.join(IMG_FOLDER,img_fn))
ICON_IMG = load_img("blob.png")
BLOB_IMG = load_img("blob.png")
BLOB_LRG_IMG = load_img("blob_lrg.png")
BLOB_LRG_ALT_IMG = load_img("blob_lrg_alt.png")
BALL_IMG = load_img("ball.png")
BG_SQUARE_IMG = load_img("square.png")

## title
TITLE = "Blob Dodger"

## -------------- SCREEN ---------------------
## dimensions
HEIGHT = 720
WIDTH = 1200
SCREEN_SIZE = (WIDTH, HEIGHT)


TOP_MARGIN = int(HEIGHT / 10)
""" Having a TOP_MARGIN is good if you need space at the top """
MARGIN = int(HEIGHT / 30)
LEFT = MARGIN
CENTER = int(WIDTH / 2)
RIGHT = WIDTH - MARGIN
TOP = TOP_MARGIN
MIDDLE = int(HEIGHT / 2)
BOTTOM = HEIGHT - MARGIN

## window
SCREEN = display.set_mode(SCREEN_SIZE)

#pygame.display
display.set_caption(TITLE)
display.set_icon(ICON_IMG)

FPS = 60

## colours (for more colours: w3schools.com/colors/colors_picker.asp)
WHITE = (0, 0, 0)
BLACK = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (127, 127, 127)
BG_COLOR = (201, 230, 242, 30)
TXT_COLOR = (150, 206, 180)
BALL_COLOR = (194, 68, 81)
BLOB_COLOR = (82, 187, 107)
TITLE_BAR_COLOR = (45, 49, 75)
MSG_COLOR = TITLE_BAR_COLOR

## title bar
TITLE_BAR_HEIGHT = TOP_MARGIN
TITLE_BAR_WIDTH = WIDTH
TITLE_BAR_DIMS = (TITLE_BAR_WIDTH, TITLE_BAR_HEIGHT)
TITLE_BAR_COORDS = (0, 0)
TITLE_BAR = Surface(TITLE_BAR_DIMS)
TITLE_BAR.fill(TITLE_BAR_COLOR)


## lifetimes
""" I use these for when we are asking the player a question, but if they don't
respond, after a while we move on anyway. Usally for quitting/game over """
GAME_OVER_LIFETIME = 400

## delays
""" I use delays when it would be bad if the player accidentally held a key
down and produced two key presses instead of one. If you use p to pause and
unpause"""
PAUSE_DELAY = 15

## sizes
BALL_SIZE = 25
BLOB_SIZE = 25

## speed/time
BALL_SPEED = 8
BLOB_SPEED = 12
CLOCK = time.Clock()

##fonts
font.init()

INFO_FONT_SIZE = int(HEIGHT / 40)
TITLE_FONT_SIZE = 2 * INFO_FONT_SIZE
COUNTDOWN_FONT_SIZE = int(HEIGHT / 1.5)
MSG_FONT_SIZE = int(HEIGHT / 15)

MAIN_FONT = "couriernew"

INFO_FONT = font.SysFont(MAIN_FONT,INFO_FONT_SIZE)
TITLE_FONT = font.SysFont(MAIN_FONT,TITLE_FONT_SIZE)
COUNTDOWN_FONT = font.SysFont(MAIN_FONT,COUNTDOWN_FONT_SIZE)
MSG_FONT =  font.SysFont(MAIN_FONT,MSG_FONT_SIZE)

TITLE_X = CENTER
TITLE_Y = int(TOP_MARGIN / 2.3)
TITLE_POS = (TITLE_X, TITLE_Y)

## ------------ AUDIO ---------------
# init
mixer.init()
SUPERDRUMS = path.join(BG_MUSIC_FOLDER,"superdrumloop.wav")
NEW_BLOB_SFX = path.join(SFX_FOLDER,"new_blob.wav")
NEW_BALL_SFX = path.join(SFX_FOLDER,"new_ball.wav")
BALLEATER_ACTIVE_SFX = path.join(SFX_FOLDER,"balleater_active.wav")
LOSE_LIFE_SFX = path.join(SFX_FOLDER,"lose_life.wav")
BALL_EATEN_SFX = path.join(SFX_FOLDER,"ball_eaten.wav")
BLOB_EATEN_SFX = path.join(SFX_FOLDER,"blob_eaten.wav")
NEW_BALLEATER_SFX = path.join(SFX_FOLDER,"new_balleater.wav")

BG_MUSIC = mixer.Sound(SUPERDRUMS)
NEW_BLOB = mixer.Sound(NEW_BLOB_SFX)
NEW_BALL = mixer.Sound(NEW_BALL_SFX)
BALLEATER_ACTIVE = mixer.Sound(BALLEATER_ACTIVE_SFX)
LOSE_LIFE = mixer.Sound(LOSE_LIFE_SFX)
BALL_EATEN = mixer.Sound(BALL_EATEN_SFX)
BLOB_EATEN = mixer.Sound(BLOB_EATEN_SFX)
NEW_BALLEATER = mixer.Sound(NEW_BALLEATER_SFX)


BG_MUSIC_CH = mixer.Channel(0)
SFX_CH = mixer.Channel(1)
COLLECTABLE_ACTIVE_CH = mixer.Channel(2)


## ----------- QUANTITIES ----------
BG_SQUARE_START = 50

## ---------------- SPECIAL -----------
"""These are probably unique to your game"""
MODES = ["Standard","Multiball","Impossiball", "ImpossiMultiball"]
DIRECTIONS = [("left","down"),("right","down"),("left","up"),("right","up"), ("left",""),("right",""),("","up"),("","down")]
LEVEL_UP = [100, 200, 400, 800, 1600, 3200, 6400, 10000]
LEVEL_MAX_HP = [120, 140, 160, 180, 200, 250, 300, 500]

## ------------ GLOBAL VARIABLES -----------------
player = None
game = None
keys = None
first_game = True
first_balleater = True
generate_balleater = None
do_tutorial = True
steps = [
    [
        {
            "timer":10,
            "msg":"Want a tutorial (Y/N)?"
        },{
            "timer":1.5,
            "msg":"This is Blob Dodger"
        },{
            "timer":1.5,
            "msg":"You are a blob"
        },{
            "timer":1.5,
            "msg":"Dodge the balls"
        },{
           "timer":1.5,
            "msg":"And blast through walls"
        },{
           "timer":1.5,
            "msg":"Survive longer to earn more points"
        },{
           "timer":1.5,
            "msg":"Sounds easy, right?"
        },{
           "timer":1.5,
            "msg":"Controls"
        },{
           "timer":1.5,
            "msg":"Arrow keys or WSAD to move"
        },{
           "timer":1.5,
            "msg":"P to pause/unpause"
        },{
           "timer":1.5,
            "msg":"Q to quit"
        },{
            "timer":1.5,
            "msg":"Ok, go!"
        }
    ],[
        {
           "timer":1.5,
            "msg":"You got an extra blob"
        },{
           "timer":1.5,
            "msg":"All blobs move in parallel"
        },{
           "timer":1.5,
            "msg":"New ball every 1,000 points"
        },{
           "timer":1.5,
            "msg":"Points go up quicker each time"
        },{
            "timer":1.5,
            "msg":"Ok, go!"
        }
    ],[
        {
           "timer":1.5,
            "msg":"Uh-oh, now there's another ball"
        },{
           "timer":1.5,
            "msg":"Starting to get tricky!"
        },{
           "timer":1.5,
            "msg":"New ball every 1,000 points"
        },{
           "timer":1.5,
            "msg":"Ready to get dodging?"
        },{
            "timer":1.5,
            "msg":"Ok,let's go!"
        }
    ],[
        {
           "timer":1.5,
            "msg":"Cool, that's a Ball Eater"
        },{
           "timer":1.5,
            "msg":"Collect it and become invincable!"
        },{
           "timer":1.5,
            "msg":"Plus get 1,000 points for eating a ball"
        },{
           "timer":1.5,
            "msg":"Be careful though"
        },{
            "timer": 1.5,
            "msg":"Remember what happens every 1,000 points!"
        },{
            "timer":1.5,
            "msg":"Ok, it's dodging time!"
        }
    ]
]


