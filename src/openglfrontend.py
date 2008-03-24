from OpenGL.GL import *
import pygame
from pygame.locals import *
from font import Text
import time 

import field

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
  #glEnable(GL_LINE_SMOOTH)
  #glEnable(GL_TEXTURE_2D)
  glClearColor(0.8,0.9,1.0,1.0)

def quad(x, y):
  glPushMatrix()
  
  glTranslatef(x, y, 0)
  glBegin(GL_QUADS)

  glVertex2i(0, 0)
  glVertex2i(0, 1)
  glVertex2i(1, 1)
  glVertex2i(1, 0)

  glEnd()
  
  glPopMatrix()


def rungame():
  init()
  
  gf = field.GameField()
  gf.colors = [(1, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1), (0, 1, 0), (0, 0, 1)]
  gf.newPiece()

  lastdrop = time.time()
  dropdelay = 1

  try:
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == QUIT:
          running = False
        elif event.type == KEYDOWN:
          if event.key == K_LEFT:
            gf.move(-1, 0)
          elif event.key == K_RIGHT:
            gf.move(1, 0)
          elif event.key == K_DOWN:
            gf.move(0, 1)
          elif event.key == K_a:
            gf.rotate(-1)
          elif event.key == K_d:
            gf.rotate(1)

      if time.time() > lastdrop + dropdelay:
        lastdrop = time.time()
        if not gf.move(0, 1):
          gf.dropPiece()

      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      glLoadIdentity()

      glPushMatrix()

      glTranslatef(0.5, 0.5, 0)

      y = 0
      for r in gf.combinedField():
        x = 0
        for c in r:
          if c != 0:
            glColor(*c)
            quad(x, y)
          x += 1
        y += 1

      glColor3f(0, 0, 0)
      glBegin(GL_LINE_LOOP)
      
      glVertex2i(0, 0)
      glVertex2i(gf.sx, 0)
      glVertex2i(gf.sx, gf.sy)
      glVertex2i(0, gf.sy)

      glEnd()

      glPopMatrix()

      # render GUI


      pygame.display.flip()

      time.sleep(0.05)

  except field.GameOver:
    pass # TODO: implement some game-over stuff

  pygame.quit

rungame()
