# This file contains the classes used for the tetris field
# The Piece class contains all necessary stuff for pieces, like what fields are
# filles and what fields are not and colors and all the like.
# The GameField class contains the game logic needed for moving pieces about,
# snapping them to tge field and deleting lines.
# Drawing, animation and other gamefield related tasks are handled by a
# seperate class.

import random

class PieceList:
  def __init__(self):
    # the piecelist is a three-dimensional array, containing a list of 
    # two-dimensional semiboolean fields for the field itself, each
    # part of the list being one step in the rotation of the piece.
    self.piecelist = []
    pieces = open("pieces.txt", "r").read().split("\n\n")
    for p in (a.split("\n") for a in pieces):
      clr = [int(a) for a in p[0].split(" ")]
      if p[-1] != "":
        rows = len(p) - 1
      else:
        rows = len(p) - 2
      cols = len(p[1].split(" ")[0])
      animframes = len(p[1].split(" "))
      piece = [[ [ 0 for i in range(0, rows)] for j in range(0, cols)] for k in range(0, animframes)]
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

pl = PieceList()

class Piece:
  def __init__(self):
    self.geometry = random.choice(pl.piecelist)
    self.rotation = random.randint(len(self.geometry) - 1)

class GameField:
  def __init__(self):
    self.sx = 11
    self.sy = 20

    # this is the current piece, fetched from the piecelist and initialised
    # with a random color.
    self.piece = []
    
    # the X and Y coordinates of the piece.
    self.px = 0
    self.py = 0
    # the animation frame of the piece (rotation actually)
    self.paf = 0

    # access to the field is field[x][y].
    # the field content is a color or maybe a color index of a palette or something.
    self.field = [[0 for i in range(self.sy)] for j in range(self.sx)]

  def collides(self, newx, newy):
    """checks the position of the piece against the field boundaries and content."""
    # iterate all fields in the current piece
    # x coordinate in piece
    for xip in range(0, len(self.piece[self.paf])):
      # y coordinate in piece
      for yip in range(0, len(self.piece[self.paf][xip])):
        
        # x and y coordinates in field
        xif = self.px + xip
        yif = self.py + yip
        
        # no need to check for collisions on empty spaces!
        if self.piece[paf][xip][yip] == 0:
          continue
        
        # is the piece outside of the playing field?
        if xif < 0 or xif > self.sx or yif < 0 or yif > self.sy:
          return true
        
        if self.field[xif][yif] != 0:
          return true

    return false