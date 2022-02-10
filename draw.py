from panda3d.core import *

def make_arrow(start, end, color=(1, 0, 0, 1), thickness=3, text=None):
  anchor = NodePath('arrow')

  line = LineSegs('line')
  line.setColor(color)
  line.setThickness(thickness)
  line.moveTo(start)
  line.drawTo(end)
  anchor.attachNewNode(line.create())

  scale = (Point3(end) - Point3(start)).length()

  line = LineSegs('head')
  line.setColor(color)
  line.setThickness(thickness)
  line.moveTo((-0.05, 0, -0.15))
  line.drawTo((0, 0, 0))
  line.drawTo((0.05, 0, -0.15))

  head_node = anchor.attachNewNode('head')
  # Set billboard and lines on child node so that the arrow head is still "up".
  head_node.attachNewNode(line.create()).setBillboardAxis()
  head_node.setScale(0.7 * scale)
  head_node.setPos(end)
  head_node.lookAt(start)
  head_node.setP(head_node, 90)

  if text:
    t = TextNode('label')
    t.setText(text)
    t.setTextColor(color)
    t_node = anchor.attachNewNode(t)
    t_node.setScale(0.15 * scale)
    t_node.setPos(end)
    t_node.setBillboardPointEye()

  return anchor


def draw_arrow(*args, **kwargs):
  return render.attachNewNode(make_arrow(*args, **kwargs).node())


def make_axis(position=(0, 0, 0), quat=LQuaternion.identQuat()):
  anchor = NodePath('axis');

  anchor.attachNewNode(make_arrow((0, 0, 0), (1, 0, 0), color=(1, 0, 0, 1), text='x').node())
  anchor.attachNewNode(make_arrow((0, 0, 0), (0, 1, 0), color=(0, 1, 0, 1), text='y').node())
  anchor.attachNewNode(make_arrow((0, 0, 0), (0, 0, 1), color=(0, 0, 1, 1), text='z').node())

  anchor.setPos(position)
  anchor.setQuat(quat)

  return anchor


def draw_axis(*args, **kwargs):
  return render.attachNewNode(make_axis(*args, **kwargs).node())
