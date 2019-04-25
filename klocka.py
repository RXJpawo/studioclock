# Original code (tick) written by:
# Al Sweigart al@inventwithpython.com
# Modified by Erik Linder sm0rvv@gmail.com

import sys, pygame, time, math
from pygame.locals import *

# set up a bunch of constants
BRIGHTBLUE = (  0,  50, 255)
WHITE      = (255, 255, 255)
DARKRED    = (128,   0,   0)
RED        = (255,   0,   0)
YELLOW     = (255, 255,   0)
GREEN      = (0,   255,   0)
BLACK      = (  0,   0,   0)

LEDMARKCOLOR = RED
LEDSECONDCOLOR = GREEN
TEXTCOLOR = RED
BGCOLOR = BLACK

WINDOWWIDTH = 800 # width of the program's window, in pixels
WINDOWHEIGHT =  600 # height in pixels
WIN_CENTERX = int(WINDOWWIDTH / 2)
WIN_CENTERY = int(WINDOWHEIGHT / 2)

LEDSIZE = int(WINDOWHEIGHT / 70) # size of the clock number's boxes
CLOCKSIZE = int(WINDOWHEIGHT / 2.4) # general size of the clock
FONTSIZE = int(WINDOWHEIGHT / 5)


# This function retrieves the x, y coordinates based on a "tick" mark, which ranges between 0 and 60
# A "tick" of 0 is at the top of the circle, 30 is at the bottom, 45 is at the "9 o'clock" position, etc.
# The "stretch" is how far from the origin the x, y return values will be
# "originx" and "originy" will be where the center of the circle is (almost always the center of the window)
def getTickPosition(tick, stretch=1.0, originx=WIN_CENTERX, originy=WIN_CENTERY):

    # The cos() and sin(), rotate ourselves 15 ticks (90 degrees) back to reach 0
    tick -= 15

    # ensure that tick is between 0 and 60
    tick = tick % 60

    tick = 60 - tick

    # the argument to sin() or cos() needs to range between 0 and 2 * math.pi
    # Since tick is always between 0 and 60, (tick / 60.0) will always be between 0.0 and 1.0
    # The (tick / 60.0) lets us break up the range between 0 and 2 * math.pi into 60 increments.
    x =      math.cos(2 * math.pi * (tick / 60.0))
    y = -1 * math.sin(2 * math.pi * (tick / 60.0)) # "-1 *" because in Pygame, the y coordinates increase going down (the opposite of how they normally go in mathematics)

    # sin() and cos() return a number between -1.0 and 1.0, so multiply to stretch it out.
    x *= stretch
    y *= stretch

    # Then do the translation (i.e. sliding) of the x and y points.
    # NOTE: Always do the translation addition AFTER doing the stretch.
    x += originx
    y += originy

    return x, y


# standard pygame setup code
pygame.init()
#DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN)
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Studio Clock')
fontObj = pygame.font.Font('/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf', FONTSIZE)
# fill the screen to draw from a blank state
DISPLAYSURF.fill(BGCOLOR)


while True: # main application loop
    facecolor = RED
    # event handling loop for quit events
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    # Reduce CPU load
    pygame.time.wait(100)

    # get the current time
    now = time.localtime()
    now_hour = now[3]
    now_minute = now[4]
    now_second = now[5]


    # Here is the settings for yellow-blinking minute
    if now_hour == 9 and now_minute == 28 and now_second%2 == 0:
        facecolor = YELLOW
    if now_hour == 13 and now_minute == 35 and now_second%2 == 0:
        facecolor = YELLOW

    # Blank screen
    if now_second == 0:
        DISPLAYSURF.fill(BGCOLOR)

    # Draw the four markers
    for marker in range(0, 60, 5):
        x, y = getTickPosition(marker, CLOCKSIZE * 1.1)
        pygame.draw.circle(DISPLAYSURF, facecolor, [int(x),int(y)], LEDSIZE)

    # draw the second LED's
    x, y = getTickPosition(now_second, CLOCKSIZE * 1)
    pygame.draw.circle(DISPLAYSURF, facecolor, [int(x), int(y)], LEDSIZE)

    # Type time
    # Change the factor values if the time is placed off center
    timetext = fontObj.render(str(now_hour).rjust(2, '0')+":"+str(now_minute).rjust(2, '0'), True, facecolor)
    DISPLAYSURF.blit(timetext, (WIN_CENTERX - FONTSIZE * 1.85, WIN_CENTERY - FONTSIZE / 1.15))
    
    pygame.display.update()
 
