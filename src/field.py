# This file contains the classes used for the tetris field
# The Piece class contains all necessary stuff for pieces, like what fields are
# filles and what fields are not and colors and all the like.
# The GameField class contains the game logic needed for moving pieces about,
# snapping them to tge field and deleting lines.
# Drawing, animation and other gamefield related tasks are handled by a
# seperate class.

import random

class GameOver(Exception):
  pass

class PieceList:
  def __init__(self):
    # the piecelist is a three-dimensional array, containing a list of 
    # two-dimensional semiboolean fields for the field itself, each
    # part of the list being one step in the rotation of the piece.
    self.piecelist = []
    pieces = open("../data/pieces.txt", "r").read().split("\n\n")
    for p in (a.split("\n") for a in pieces):
      clr = [int(a) for a in p[0].split(" ")]
      if p[-1] != "":
        rows = len(p) - 1
      else:
        rows = len(p) - 2
      cols = len(p[1].split(" ")[0])
      animframes = len(p[1].split(" "))
      piece = [[ [ 0 for i in range(0, rows)]
                  for j in range(0, cols)]
                  for k in range(0, animframes)]
      li = 0 # line index
      for l in p[1:rows + 1]:
        afi = 0 # Animation Frame Index
        for afl in l.split(" "):
          # attention: the array is [y][x], not [x][y], but that's no problem,
          # as all piece arrays are squared anyway!
          piece[afi][li] = [".O".index(aflp) for aflp in afl]
          afi += 1
        li += 1

      self.piecelist.append(piece)

  def getPiece(self):
    return random.choice(self.piecelist)

pl = PieceList()

class GameField:
  def __init__(self):
    self.sx = 11
    self.sy = 20

    self.colors = [1]

    # fill the stack first
    self.npiece, self.npc, self.npaf, self.npx, self.npy = 0, 0, 0, 0, 0
    self.newPiece()
    # then put the piece onto the field.
    self.newPiece()

    # access to the field is field[y][x].
    # the field content is a color or maybe a color index of a palette
    # or something.
    self.field = [[0 for i in range(self.sx)] for j in range(self.sy)]

  def newPiece(self):
    """selects a new piece from the PieceList and drops it into
the game field"""
    # get the next piece.
    self.piece = self.npiece
    self.pc = self.npc
    self.paf = self.npaf
    self.px = self.npx
    self.py = self.npy

    # this is the current piece, fetched from the piecelist and initialised
    # with a random color.
    self.npiece = pl.getPiece()

    # piece color
    self.npc = random.choice(self.colors)

    # the animation frame of the piece (rotation actually)
    self.npaf = random.randrange(0, len(self.npiece))

    # the X and Y coordinates of the piece.
    self.npx = (self.sx - len(self.npiece[self.npaf][0])) / 2
    self.npy = 0

  def checkField(self):
    """checks for full lines and erases them"""
    erased = []
    i = self.sy - 1
    while i > 0:
      if False not in [0 != a for a in self.field[i]]:
        erased.append(i - len(erased))
        for j in range(i, 1, -1):
          self.field[j] = self.field[j - 1][:]
        self.field[0] = [0] * self.sx
      else:
        i -= 1
    
    return erased

  def collides(self, newx, newy, newpaf):
    """checks the position of the piece against the field boundaries and
content."""
    # iterate all fields in the current piece
    # x coordinate in piece
    for yip in range(0, len(self.piece[newpaf])):
      # y coordinate in piece
      for xip in range(0, len(self.piece[newpaf][yip])):

        # x and y coordinates in field
        xif = newx + xip
        yif = newy + yip

        # no need to check for collisions on empty spaces!
        if self.piece[newpaf][yip][xip] == 0:
          continue

        # is the piece outside of the playing field?
        if xif < 0 or xif > self.sx - 1 or yif < 0 or yif > self.sy - 1:
          return True

        if self.field[yif][xif] != 0:
          return True

    return False

  def move(self, dx, dy):
    """tries to move the piece by (dx|dy).
returns False, if the move couldn't be carried out"""
    if not self.collides(self.px + dx, self.py + dy, self.paf):
      self.px += dx
      self.py += dy
      return True
    else:
      return False

  def rotate(self, dir):
    """tries to rotate the piece. +1 means to the right, -1 means to the left.
returns False, if the rotation couldn't be carried out.""" 
    if not self.collides(self.px, self.py, (self.paf + dir) % len(self.piece)):
      self.paf = (self.paf + dir) % len(self.piece)
      return True
    else:
      return False

  def combinedField(self, color = None):
    """returns the field together with the floating piece."""
    a = [a[:] for a in self.field]

    # x coordinate in piece
    for yip in range(0, len(self.piece[self.paf])):
      # y coordinate in piece
      for xip in range(0, len(self.piece[self.paf][yip])):
        if self.piece[self.paf][yip][xip] != 0:
          a[self.py + yip][self.px + xip] = color or self.pc

    return a

  def dropPiece(self):
    """combines the floating piece with the field, checks for lines to be
erased, wether or not the game should be over, and finally generates a new
piece."""
    self.field = self.combinedField()
    res = self.checkField()
    if not res and self.py == 0:
      raise GameOver
    self.newPiece()
    return res
