import math

from panda3d.core import *


class Grid:
  def __init__(self, parent, spacing, extents):
    self.lines = LineSegs('grid')
    self.lines.setColor(0.529, 0.529, 0.529, 1.0)
    self.lines.setThickness(1.0)

    x = math.trunc(extents[0] / spacing) * spacing
    while x <= extents[1]:
      self.lines.moveTo(x, extents[2], 0.0)
      self.lines.drawTo(x, extents[2], 0.0)
      self.lines.drawTo(x, extents[3], 0.0)
      x += spacing

    y = math.trunc(extents[2] / spacing) * spacing
    while y <= extents[3]:
      self.lines.moveTo(extents[0], y, 0.0)
      self.lines.drawTo(extents[0], y, 0.0)
      self.lines.drawTo(extents[1], y, 0.0)
      y += spacing

    parent.attachNewNode(self.lines.create())
