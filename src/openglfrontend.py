from OpenGL.GL import *
import pygame
from pygame.locals import *
from font import Text
from time import sleep

# don't initialise sound stuff plzkthxbai
pygame.mixer = None

screensize = (1024, 768)

def setres((width, height)):
  """res = tuple
sets the resolution and sets up the projection matrix"""
  if height==0:
    height=1
  glViewport(0, 0, width, height)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  glOrtho(0, width / 32, height / 32, 0, -10, 10)
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()

def init():
  # initialize everything
  pygame.init()
  screen = pygame.display.set_mode(screensize, OPENGL|DOUBLEBUF)
  setres(screensize)

  # some OpenGL magic!
  glEnable(GL_BLEND)
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
  glEnable(GL_LINE_SMOOTH)
  glEnable(GL_TEXTURE_2D)
  glClearColor(0.8,0.9,1.0,1.0)

def rungame():
  init()
  
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == QUIT:
        running = False
    # handle events
    # handle game
    # render gamefield
    # render GUI
    sleep(0.1)
  
  pygame.quit