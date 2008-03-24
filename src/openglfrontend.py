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
  glEnable(GL_DEPTH_TEST)
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

def line(x1, y1, x2, y2):
  glBegin(GL_LINES)

  glVertex3i(x1, y1, 1)
  glVertex3i(x2, y2, 1)  

  glEnd()

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

      tf = gf.combinedField()
      for y in range(gf.sy):
        for x in range(gf.sx):
          if tf[y][x] != 0:
            glColor(*tf[y][x])
            quad(x, y)
            glColor(0, 0, 0)
            if x < gf.sx - 1 and tf[y][x + 1] != tf[y][x]:
              line(x + 1, y, x + 1, y + 1)
            if y < gf.sy - 1 and tf[y+1][x] != tf[y][x]:
              line(x, y + 1, x + 1, y + 1)
          else:
            glColor(0, 0, 0)
            if x < gf.sx - 1 and tf[y][x + 1] != 0:
              line(x + 1, y, x + 1, y + 1)
            if y < gf.sy - 1 and tf[y+1][x] != 0:
              line(x, y + 1, x + 1, y + 1)
      

      glColor3f(0, 0, 0)
      glBegin(GL_LINE_LOOP)

      glVertex3i(0, 0, 1)
      glVertex3i(gf.sx, 0, 1)
      glVertex3i(gf.sx, gf.sy, 1)
      glVertex3i(0, gf.sy, 1)

      glEnd()

      glPopMatrix()

      # render GUI


      pygame.display.flip()

      time.sleep(0.05)

  except field.GameOver:
    pass # TODO: implement some game-over stuff

  pygame.quit

rungame()
