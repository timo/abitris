# -*- coding: utf8 -*-
from OpenGL.GL import *
import pygame
from pygame.locals import *
from font import Text
import time 

import field
import random
import math

# don't initialise sound stuff plzkthxbai
pygame.mixer = None

screensize = (1024, 768)

class Texture:
  def __init__(self, texturename):
    self.name = texturename
    self.Surface = pygame.image.load('../data/%s.png' % texturename)

    (self.w, self.h) = self.Surface.get_rect()[2:]

    self.glID = glGenTextures(1)
    self.bind()

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,     GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,     GL_REPEAT)

    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                 self.w, self.h,
                 0, GL_RGBA, GL_UNSIGNED_BYTE,
                 pygame.image.tostring(self.Surface, "RGBA", 0))

  def bind(self):
    glBindTexture(GL_TEXTURE_2D, self.glID)


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
  glEnable(GL_TEXTURE_2D)
  glClearColor(0.0,0.0,0.0,1.0)

def quad(x, y):
  glPushMatrix()

  glEnable(GL_TEXTURE_2D)

  t = (time.time() / 100) % 1 
  z = 0.09

  glTranslatef(x, y, 0)
  glBegin(GL_QUADS)

  glTexCoord2f(x * z, y * z + t)
  glVertex2i(0, 0)

  glTexCoord2f(x * z, y * z + z + t)
  glVertex2i(0, 1)

  glTexCoord2f(x * z + z, y * z + z + t)
  glVertex2i(1, 1)

  glTexCoord2f(x * z + z, y * z + t)
  glVertex2i(1, 0)

  glEnd()

  glDisable(GL_TEXTURE_2D)

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
  gf.newPiece()

  piecetex = Texture("bg")

  lastdrop = time.time()
  dropdelay = 0.3

  textthing = Text(u"Nächstes Teil")


  def drawStuff(tf):
    def drawField(thefield):
      for y in range(len(thefield)):
        for x in range(len(thefield[y])):
          if thefield[y][x] != 0:
            glColor(*thefield[y][x])
            glEnable(GL_TEXTURE_2D)
            quad(x, y)
            glDisable(GL_TEXTURE_2D)
            glColor(1, 1, 1)
            if x < len(thefield[y]) - 1 and thefield[y][x + 1] != thefield[y][x]:
              line(x + 1, y, x + 1, y + 1)

            if y < len(thefield) - 1 and thefield[y + 1][x] != thefield[y][x]:
              line(x, y + 1, x + 1, y + 1)

          else:
            glColor(1, 1, 1)
            if x < len(thefield[y]) - 1 and thefield[y][x + 1] != 0:
              line(x + 1, y, x + 1, y + 1)

            if y < len(thefield) - 1 and thefield[y + 1][x] != 0:
              line(x, y + 1, x + 1, y + 1)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glPushMatrix()
    glTranslatef(0.5, 0.5, 0)
    piecetex.bind()

    drawField(tf)

    glColor3f(1, 1, 1)

    glBegin(GL_LINE_LOOP)
    glVertex3i(0, 0, 1)
    glVertex3i(gf.sx, 0, 1)
    glVertex3i(gf.sx, gf.sy, 1)
    glVertex3i(0, gf.sy, 1)
    glEnd()

    glPopMatrix()

    # render GUI
    glPushMatrix()
    glTranslatef(12, 0, 0)
    glScalef(1 / 32., 1 / 32., 1 / 32.)
    textthing.draw()
    glPopMatrix()

    # render next piece
    glPushMatrix()
    piecetex.bind()
    glTranslatef(12, 1, 0)
    drawField([map( lambda foo: [0, gf.npc][foo], bar) for bar in gf.npiece[gf.npaf]])

    glDisable(GL_TEXTURE_2D)

    glBegin(GL_LINE_LOOP)
    glVertex3i(0, 0, 1)
    glVertex3i(len(gf.npiece[gf.npaf]), 0, 1)
    glVertex3i(len(gf.npiece[gf.npaf]), len(gf.npiece[gf.npaf][0]), 1)
    glVertex3i(0, len(gf.npiece[gf.npaf][0]), 1)
    glEnd()

    
    glPopMatrix()

  inputsys = {K_LEFT:  [gf.move,   [-1, 0], time.time()],
              K_RIGHT: [gf.move,   [ 1, 0], time.time()],
              K_DOWN:  [gf.move,   [ 0, 1], time.time()],
              K_a:     [gf.rotate, [-1],    time.time()],
              K_d:     [gf.rotate, [ 1],    time.time()]}
  inputdelay = 0.15

  try:
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == QUIT:
          running = False

      for thekey in inputsys.keys():
        if pygame.key.get_pressed()[thekey] and time.time() > inputsys[thekey][2] + inputdelay:
          inputsys[thekey][0](*inputsys[thekey][1])
          inputsys[thekey][2] = time.time()

      if time.time() > lastdrop + dropdelay:
        lastdrop = time.time()
        if not gf.move(0, 1):
          oldfield = gf.combinedField()
          deletedlines = gf.dropPiece()

          if deletedlines:
            fl = min(deletedlines)
            for x in range(gf.sx * 3):
              for l in deletedlines:
                for zx in range(max(0, min(x - l + fl, gf.sx))):
                  oldfield[l][zx] = map(lambda a: int(max(0, min(a*0.75, a - 0.1)) * 100) / 100., oldfield[l][zx])
                  if oldfield[l][zx] == (0, 0, 0):
                    oldfield[l][zx] = [0]

              drawStuff(oldfield)
              pygame.display.flip()
              time.sleep(0.025)

      drawStuff(gf.combinedField( map(lambda col: col * (math.sin(time.time() * 3) + 1.25), gf.pc )))
      pygame.display.flip()

      time.sleep(0.01)

  except field.GameOver:
    pass # TODO: implement some game-over stuff

  pygame.quit

rungame()
