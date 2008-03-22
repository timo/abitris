# this is a very simple frontend to the tetris field, allowing the code to be
# tested.

import field
import sys
from select import select
import time

gf = field.GameField()

def printGameField():
  for lin in gf.combinedField():
    print "".join(str(y) for y in lin).replace("0", ".").replace("1", "O")

running = True
while running:
  print
  print
  print
  printGameField()

  key = sys.stdin.read(1)
    
  if key == "a":
    gf.move(-1, 0)
  elif key == "s":
    gf.move(0, 1)
  elif key == "d":
    gf.move(1, 0)
  elif key == "q":
    gf.rotate(-1)
  elif key == "e":
    gf.rotate(1)

  if not gf.move(0, 1):
    gf.dropPiece()

  time.sleep(0.1)
