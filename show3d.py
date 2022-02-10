from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *

import procedural3d

import camera_controller
import grid


class MyApp(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)

    box_maker = procedural3d.BoxMaker(
      center=(0., 0., 0.),
      width=2.,
      depth=2.,
      height=2.,
      segments={
        "width": 2,
        "depth": 4,
        "height": 3
      },
      open_sides=('left', 'back', 'top'),
      thickness=.45,
      inverted=False,
      vertex_color=None,
      has_uvs=True,
      tex_offset={
        "left": (.5, .5),
        "back": (.5, .5),
        "bottom": (.5, .5)
      },
      tex_scale={
        "left": (.5, .5),
        "right": (.5, .5),
        "back": (.5, .5),
        "front": (.5, .5),
        "bottom": (.5, .5),
        "top": (.5, .5)
      }
    )
    box = self.render.attach_new_node(box_maker.generate())
    box.set_render_mode_filled_wireframe((1., 0., 0., 1.))

    box_maker.center = (100, 100, 100)
    box = self.render.attach_new_node(box_maker.generate())
    box.set_render_mode_filled_wireframe((1., 0., 0., 1.))

    self.grid = grid.Grid(self.render, 7.3, (-100, 100, -100, 100))

    self.camera_controller = camera_controller.FreeCameraController()


if __name__ == '__main__':
  MyApp().run()
