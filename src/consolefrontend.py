# this is a very simple frontend to the tetris field, allowing the code to be
# tested.

import field
import sys
from select import select
import time

gf = field.GameField()

def printGameField():
  for lin in gf.combinedField():
    print "".join(str(x) for x in lin)

running = True
while running:
  print
  print
  print
  printGameField()

#===============================================================================
#  (inp, null, null2) = select((sys.stdin), (), (), 0.1)
#  print inp
#  if len(inp) > 0:
#    key = sys.stdin.read()
#    
#    if key == "a":
#      gf.move(-1, 0)
#    elif key == "s":
#      gf.move(0, 1)
#    elif key == "d":
#      gf.move(1, 0)
#===============================================================================

  if not gf.move(0, 1):
    gf.dropPiece()

  time.sleep(1)