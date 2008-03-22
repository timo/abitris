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
      li = 0
      for l in p[1:rows + 1]:
        afi = 0
        for afl in l.split(" "):
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

    # access to the field is field[x][y]
    # the field content is a color or maybe a color index of a palette or something
    self.field = [[0 for i in range(self.sy)] for j in range(self.sx)]

  def collides(self, newx, newy):
    """checks the position of the piece against the field boundaries and content."""
    pass # TODO: implement 