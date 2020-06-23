## import libraries
from pygame import *
from random import *
from datetime import *

## notes
"""------------------------------------------------------------
Some tutorials will show these imports as:
import pygame
import os
import random.

It's often simpler to do it as "from `library` import *" because then you don't
have to write thee library name every time you want to use it.

For example to set the window captionfrom pygame, if you import it using "import
pygame" you would have to write pygame.display.set_caption("MyGame"), but if you
write "from pygame import *" you only have to write display.set_caption("MyGame")

This doesn't sound like a lot, but when you're writing a game you need to refer
to pygame classes a LOT, so it saves a lot of time. If you use another library
that also has a class called `display`, then python  won't know which one you
want, so that's when you have to do it as "import pygame"
-------------------------------------------------------------"""

##import local libraries
from settings import *
from sprites import *

## ------------------ FUNCTIONS ---------------------
## initialise variables
def init(run_main = True):
    
    global game, player, all_sprites, do_tutorial
    for sprite in all_sprites:
        sprite.kill()
    bg_music()
    if game:
        print("got game")
        game = Game(True)
    else:
        print("ain't got game")
        game = Game(False)
        
    player = Player()
    bg_squares = BG_SQUARE_START
    while bg_squares > 0:
        new_bg_square = BG_Square()
        bg_sprites.add(new_bg_square)
        bg_squares -= 1
    if run_main:
        main()
    game.msg = ""
    game_over = False
    #print ("init end")

## bg music
def bg_music():
    BG_MUSIC_CH.set_volume(40)
    BG_MUSIC_CH.play(BG_MUSIC,-1)
    

## update sprites
def update(update_game_sprites):
    if update_game_sprites:
        all_sprites.update(keys)
    else:
        bg_sprites.update(keys)
## display
def text_objects(text, font, font_color):
    #print("text_objects start",text, foinitnt)
    #pygame.font
    textSurface = font.render(text, True, font_color)
    #print("text_objects end")
    return textSurface, textSurface.get_rect()

def message_display(text, font, center = (CENTER, MIDDLE), font_color = TXT_COLOR):
    #print("message_display start", text, font, center)
    TextSurf, TextRect = text_objects(text, font, font_color)
    TextRect.center = (center)
    SCREEN.blit(TextSurf, TextRect)
    #print("message_display end")

def refresh_screen(draw_sprites = True):
    #print("refresh_screen end",draw_sprites)
    SCREEN.fill(BG_COLOR)
    bg_sprites.draw(SCREEN)
    if draw_sprites:
        all_sprites.draw(SCREEN)
    SCREEN.blit(TITLE_BAR, TITLE_BAR_COORDS)
    message_display(TITLE, TITLE_FONT, TITLE_POS)
    message_display(game.top_msg, INFO_FONT, (CENTER, (TOP + 10)), MSG_COLOR)
    message_display(game.msg, MSG_FONT, (CENTER, MIDDLE), MSG_COLOR)
    message_display("score: " + str(player.score), INFO_FONT, (RIGHT - 60, TITLE_FONT_SIZE - int(INFO_FONT_SIZE / 2)))
    message_display("lives: " + str(player.lives), INFO_FONT, (LEFT + 60, TITLE_FONT_SIZE - int(INFO_FONT_SIZE / 2)))
    display.flip()
      #print("refresh_screen end")

## countdown
def countdown(num = 3):
#    global game
    if not game.tutorial_running:
        now = datetime.now()
        if not game.countdown_start:
            game.countdown_start = now
        start = game.countdown_start
        diff = (now - start).seconds
        if int(diff) <= num:
            game.msg = str(num - int(diff))
            game.paused_for_countdown = True
        else:
            game.msg = ""
            game.paused_for_countdown = False
            game.countdown = False
            game.countdown_start = None

def game_over(keys):
    global game, player
    now = datetime.now()
    if not game.countdown_start:
        game.countdown_start = now
    start = game.countdown_start
    diff = (now - start).seconds
    game.game_over = True
    if diff <= 2:
        game.msg = "Game Over"
    elif diff < 6:
        game.msg = "Score: " + str(player.score)
    else:
        game.msg = "Play Again (Y/N)?"
    
        if keys[K_y]:
            game.running = False
            init()

        if keys[K_n]:
            game.running = False
            do_quit()

def confirm_quit(keys):
    global game
    game.msg = "Really Quit(Y/N)?"
    if keys[K_y]:
        do_quit()
    elif keys[K_n]:
        game.running = False
        game.msg = ""
        game.confirm_quit = False
        

def do_quit():
    global game
    game.confirm_quit = False
    game.quit = True
    game.msg = "Thanks for playing!"
    now = datetime.now()
    if not game.countdown_start:
        game.countdown_start = now
    start = game.countdown_start
    diff = (now - start).seconds
    if diff > 3:
        quit()


def tutorial(keys):
    #print("tutorial",game.tutorial_step)
    global steps, do_tutorial
    if not do_tutorial:
        return
    if game.tutorial_step == (0,0) and keys[K_n]:    
        game.tutorial = False
        game.tutorial_running = False
        do_tutorial = False
        return
    elif game.tutorial_step == (0,0) and keys[K_y]:
        game.tutorial_step = (0,1)
        game.tutorial_start = False

    if game.tutorial_running:
        tut_stg = game.tutorial_step[0]
        tut_step = game.tutorial_step[1]
        if keys[K_x]:
            game.tutorial_step = (game.tutorial_step[0],0)
            game.tutorial_running = False
            game.msg = ""
            game.top_msg = ""
            return
        else:
            msg = steps[tut_stg][tut_step]["msg"]
            game.top_msg = "X to exit tutorial"
        now = datetime.now()
        if not game.tutorial_start:
            game.tutorial_start = now
        start = game.tutorial_start
        diff = (now - game.tutorial_start).seconds
        if diff <= steps[tut_stg][tut_step]["timer"]:
            game.msg = steps[tut_stg][tut_step]["msg"]
        else:
            game.tutorial_start = False
            game.tutorial_step = (game.tutorial_step[0],(game.tutorial_step[1] + 1))
            if game.tutorial_step[1] >= len(steps[game.tutorial_step[0]]):
                game.tutorial_step = (game.tutorial_step[0] + 1,0)
                game.top_msg = ""
                game.countdown = True
                game.tutorial_running = False
        
def main():
    #print("main start")
    global game, player, blob, keys, balls, blobs, all_sprites
    global pause_delay, first_balleater
    include_game_sprites = None
    while game.running:
        ## get window events
        #pygame.event
        for evt in event.get():
            #pygame.QUIT
            if evt == QUIT:
               game.confirm_quit = True

        ## get key presses
        #pygame.key
        keys = key.get_pressed()

        if player.tutorial_running:
            player.tutorial_running = False
            game.tutorial_running = True

        if game.first_time and game.tutorial_step == (0,0) and do_tutorial:
            #print(game.first_time, game.tutorial_step, do_tutorial)
            game.tutorial_running = True

        if game.tutorial_running:
            print("tutorial running")
            tutorial(keys)
            

        if first_balleater and do_tutorial and len(collectables) >= 1:
            game.tutorial_running = True
            game.tutorial_step = (3,0)
            first_balleater = False
            print("first be")
            tutorial(keys)

        if keys[K_x]:
            game.do_tutorial = False
            game.tutorial_running = False
        
        if player.game_over:
            game_over(keys)

        if game.quit:
            do_quit()
        
#        if game.new_ball or player.new_ball or len(balls) <= 0:
        #print("new ball",game.new_ball)
        if game.new_ball or player.new_ball:
            #print(player.extra_ball, player.score, do_tutorial)
            if player.extra_ball == 499 and player.score >= 500 and do_tutorial:
                game.tutorial_running = True
                game.tutorial_step = (2,0)
                tutorial(keys)
            new_ball = Ball()
            balls.add(new_ball)
            all_sprites.add(new_ball)
            player.score_increment += 1
            player.extra_ball += 1000
            player.new_ball = False
            game.new_ball = False

        #print("new blob",game.new_blob)
        #print(player.extra_ball, player.extra_blob, player.score)
        if game.new_blob or player.new_blob:
            if player.extra_blob == 1000 and player.score >= 1000 and do_tutorial:
                game.tutorial_running = True
                game.tutorial_step = (1,0)
                tutorial(keys)
            new_blob = Blob()
            blobs.add(new_blob)
            all_sprites.add(new_blob)
            player.extra_blob += 1000
            player.new_blob = False
            game.new_blob = False

        if game.countdown:
            #print("countdown")
            countdown()

        ## pause
        if keys[K_p] and game.pause_delay <= 0:
            #print("pause")
            game.toggle_pause()
        game.pause_delay -= 1


        ## quit
        #pygame.K_q
        if keys[K_q]:
            game.confirm_quit = True

        if game.confirm_quit:
            confirm_quit(keys)

        ## do not output sprites if game paused or quit
        if not (game.paused or \
                game.tutorial_running or \
                game.confirm_quit or \
                game.quit or \
                game.paused_for_countdown or\
                game.game_over):
            ## collsions

            #collectable collision
            #pygame.sprite
            collisions = sprite.groupcollide(blobs, collectables, False, True)
            for blob in collisions:
                for collectable in collisions[blob]:
                    if collectable.type == "BallEater":
                        blob.collected = "BallEater"
                        blob.invincable = True
                        blob.collected_at = datetime.now()

            #ball collisions
            #pygame.sprite
            if player.score >= 50 or not do_tutorial:
                collisions = sprite.groupcollide(blobs, balls, False, False)
                for blob in collisions:
                    if blob.invincable:
                        for ball in collisions[blob]:
                            ball.kill()
                            player.score += 1000
                            if len(balls) <= 0:
                                game.new_ball = True
                    else:
                        blob.kill()
                        if len(blobs) == 0:
                            player.lose_life()
                            for ball in balls:
                                ball.kill()
                            game.new_ball = True
                            game.new_blob = True
                            player.score_increment = 1
                            if player.lives > 0:
                                game.countdown = True
                
            if randint(0,9) == randint(0,9):
                new_bg_square = BG_Square()
                bg_sprites.add(new_bg_square)
            bg_sprites.update(keys)
            player.update()
            include_game_sprites = True
            if len(collectables) == 0:
                if randint(0,255) == 0 and ((do_tutorial and player.score >= 1500)\
                        or (not do_tutorial and player.score >= 250)):
                    new_balleater = Collectable("BallEater")
                    collectables.add(new_balleater)
                    all_sprites.add(new_balleater)
                    generate_balleater = False
                    if first_balleater:
                        game.tutorial_step = (3,0)
                        tutorial(keys)
        else:
            if randint(0,9) == randint(0,9):
                new_bg_square = BG_Square()
                bg_sprites.add(new_bg_square)
            include_game_sprites = False
        update(include_game_sprites)

        refresh_screen(include_game_sprites)
        CLOCK.tick(FPS)
#        CLOCK.tick(1)

if game:
    if not game.quit:
        init()
else:
    init()
