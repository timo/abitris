# -*- coding: utf8 -*-
from OpenGL.GL import *
import pygame
from pygame.locals import *
from font import Text, bigfont, hugefont
import time 

import field
import random
from math import sin, cos

# don't initialise sound stuff plzkthxbai
pygame.mixer = None

screensize = (1024, 768)

ctime = 0

class Texture:
  def __init__(self, texturename):
    self.name = texturename
    try:
      self.Surface = pygame.image.load('../data/%s.png' % texturename)
    except:
      self.Surface = pygame.image.load('data/%s.png' % texturename)

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

  t = (ctime / 100) % 1 
  z = 0.05

  glTranslatef(x, y, 0)
  glBegin(GL_QUADS)

  glTexCoord2f(x * z + 0.1, y * z + t)
  glVertex2i(0, 0)

  glTexCoord2f(x * z + 0.1, y * z + z + t)
  glVertex2i(0, 1)

  glTexCoord2f(x * z + z + 0.1, y * z + z + t)
  glVertex2i(1, 1)

  glTexCoord2f(x * z + z + 0.1, y * z + t)
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
  global ctime
  init()
  ctime = time.time()

  

  gf = field.GameField()
  gf.colors = [(1, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1), (0, 1, 0), (0, 0, 1), (1, 0.7, 0)]
  gf.newPiece()
  gf.newPiece()

  try:
    fragen = random.shuffle([a.split(":") for a in open("../data/questions.txt").readlines()])
  except:
    fragen = random.shuffle([a.split(":") for a in open("data/questions.txt").readlines()])
  nextquestion = time.time() + 60

  piecetex = Texture("bg")

  lastdrop = ctime
  dropdelay = 0.6

  lastspeedincrease = ctime

  nextpiece = Text(u"Nächstes Teil")

  scoredisplay = Text("0 Punkte")
  linesdisplay = Text("0 Zeilen")
  bonusdisplay = Text("Spielbeginn!", bigfont)
  bonuspos = 10
  bonuszeit = ctime

  gameends = time.time() + 5 * 60
  timedisplay = Text("5:00")

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
    glTranslate(gf.sx + 1, 1, 0)
    glScalef(1 / 32., 1 / 32., 1 / 32.)
    nextpiece.draw()
    glTranslate(0, 7 * 32, 0)
    scoredisplay.draw()
    glTranslate(0, 32, 0)
    linesdisplay.draw()
    glTranslate(0, 64, 0)
    glScalef(2, 2, 1)
    timedisplay.draw()
    glPopMatrix()

    # render next piece
    glPushMatrix()
    piecetex.bind()
    glTranslatef(gf.sx + 1, 2, 0)
    drawField([map( lambda foo: [0, gf.npc][foo], bar) for bar in gf.npiece[gf.npaf]])

    glDisable(GL_TEXTURE_2D)

    glBegin(GL_LINE_LOOP)
    glVertex3i(0, 0, 1)
    glVertex3i(len(gf.npiece[gf.npaf]), 0, 1)
    glVertex3i(len(gf.npiece[gf.npaf]), len(gf.npiece[gf.npaf][0]), 1)
    glVertex3i(0, len(gf.npiece[gf.npaf][0]), 1)
    glEnd()

    glPopMatrix()

    if ctime < bonuszeit + 3:
      glPushMatrix()
      glTranslatef(0.5 + gf.sx / 2 - bonusdisplay.w / 32, bonuspos - (ctime - bonuszeit), 2)
      bonusdisplay.rgba = [1, 1, 1, 1. - ((ctime - bonuszeit) / 3.) ** 2]
      glScalef(1/16., 1/16., 1)
      bonusdisplay.draw()
      glPopMatrix()

  inputsys = {K_a:     [gf.rotate, [-1],    ctime],
              K_d:     [gf.rotate, [ 1],    ctime],
              K_LEFT:  [gf.move,   [-1, 0], ctime],
              K_RIGHT: [gf.move,   [ 1, 0], ctime],
              K_DOWN:  [gf.move,   [ 0, 1], ctime]}
  inputdelay = 0.15

  running = True
  while running:
    try:
      ctime = time.time()
      for event in pygame.event.get():
        if event.type == QUIT:
          running = False

      for thekey in inputsys.keys():
        if pygame.key.get_pressed()[thekey] and ctime > inputsys[thekey][2] + inputdelay:
          inputsys[thekey][0](*inputsys[thekey][1])
          inputsys[thekey][2] = ctime

      timedisplay.renderText("%i:%i" % ((gameends - time.time()) / 60, (gameends - time.time()) % 60))
      if time.time() > gameends:
        raise field.GameOver

      if ctime > lastdrop + dropdelay:
        lastdrop = ctime

        if not gf.move(0, 1):
          oldfield = gf.combinedField()
          altepunkte = gf.playerscore
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

            bonuspos = deletedlines[len(deletedlines) / 2]
            bonuszeit = ctime
            bonusdisplay.renderText("%s%i" % (["", "+"][gf.playerscore - altepunkte > 0], gf.playerscore - altepunkte))

            lastdrop = ctime

          scoredisplay.renderText("%i Punkte" % gf.playerscore)
          linesdisplay.renderText("%i Zeilen" % gf.linescleared)

      drawStuff(gf.combinedField( map(lambda col: col * (sin(ctime * 3) + 1.25), gf.pc )))
      pygame.display.flip()

      time.sleep(0.01)
      
      if ctime > lastspeedincrease + 60:
        dropdelay *= 0.8
        lastspeedincrease = ctime
        bonuspos = gf.sy / 2
        bonuszeit = ctime
        bonusdisplay.renderText("Schneller!")

    except field.GameOver:

      gf = field.GameField()
      gf.colors = [(1, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1), (0, 1, 0), (0, 0, 1), (1, 0.7, 0)]
      gf.newPiece()
      gf.newPiece()

      inputsys = {K_a:     [gf.rotate, [-1],    ctime],
                  K_d:     [gf.rotate, [ 1],    ctime],
                  K_LEFT:  [gf.move,   [-1, 0], ctime],
                  K_RIGHT: [gf.move,   [ 1, 0], ctime],
                  K_DOWN:  [gf.move,   [ 0, 1], ctime]}
  
      displaying = True
      gameover = Text("Game Over!", hugefont)
      gameover.rgba = (1, 0, 0, 1)
      overscore = Text("%i Punkte" % gf.playerscore, hugefont)
    
      while displaying:
        ctime = time.time()
    
        for event in pygame.event.get():
          if event.type == QUIT:
            displaying = False
            running = False
          elif event.type == KEYDOWN:
            displaying = False
    
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
    
        glPushMatrix()
        glTranslatef(16 + cos(ctime * 2), 9 - sin(ctime * 3), 1)
        glRotatef(sin(cos(ctime * 4)) * 33, 0, 0, 1)
        glTranslatef(-gameover.w / 64, -gameover.h / 64, 0)
        glScalef((1 + sin(ctime) * 0.2)/32., (1 + cos(ctime) * 0.2)/32., 1)
        gameover.rgba = (1, 0, 0, sin(ctime) * 0.3 + 0.7)
        gameover.draw()
        glPopMatrix()
    
        glPushMatrix()
        glTranslatef(16 - overscore.w / 64, 14 - overscore.h / 64, 2)
        glScalef(1/32., 1/32., 1)
        overscore.draw()
        glPopMatrix()
    
        pygame.display.flip()
        time.sleep(0.01)

  pygame.quit

rungame()
