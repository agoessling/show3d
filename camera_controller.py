from direct.showbase.DirectObject import DirectObject
from panda3d.core import *


class FreeCameraController(DirectObject):
  _ROTATION_SCALING = 50.0
  _ZOOM_SCALING = 0.1
  _MIN_ZOOM_DISTANCE = 0.5
  _ZOOM_MOVE_SCALING = 0.3

  def __init__(self):
    base.disableMouse()

    base.camLens.setNear(0.1)

    self.accept('mouse1', self.mouse_click, ['left', 'down'])
    self.accept('mouse1-up', self.mouse_click, ['left', 'up'])
    self.accept('mouse3', self.mouse_click, ['right', 'down'])
    self.accept('mouse3-up', self.mouse_click, ['right', 'up'])
    self.accept('wheel_up', self.wheel, ['up'])
    self.accept('wheel_down', self.wheel, ['down'])

    taskMgr.add(self.on_frame, "Camera On Frame")

    self.camera_anchor = render.attachNewNode('camera_anchor')
    base.camera.reparentTo(self.camera_anchor)
    base.camera.setPos(0, -10, 0)
    base.camera.lookAt(self.camera_anchor)

    self.collision_handler = CollisionHandlerQueue()
    self.collision_traverser = CollisionTraverser('camera_traverser')

    click_node = CollisionNode('mouse_ray')
    click_nodepath = base.camera.attachNewNode(click_node)
    click_node.setFromCollideMask(GeomNode.getDefaultCollideMask())
    self.click_ray = CollisionRay()
    click_node.addSolid(self.click_ray)
    self.collision_traverser.addCollider(click_nodepath, self.collision_handler)

    self.background_plane = Plane(LVector3(0, 0, 1), Point3(0, 0, 0))

    self.mouse_down = None
    self.click_point_3d = None
    self.translate_plane = None
    self.prev_camera_xform = None
    self.prev_camera_anchor_pos = None
    self.prev_mouse_pos = None
    self.prev_camera_anchor_xform = None

  def get_3d_from_2d(self, pos, background_plane=None):
    self.click_ray.setFromLens(base.camNode, pos.x, pos.y)
    self.collision_traverser.traverse(render)

    if self.collision_handler.getNumEntries() > 0:
      self.collision_handler.sortEntries()
      entry = self.collision_handler.getEntry(0)
      return entry.getSurfacePoint(render)

    if background_plane:
      pos_3d = Point3()
      near_point = Point3()
      far_point = Point3()
      base.camLens.extrude(pos, near_point, far_point)
      background_plane.intersectsLine(pos_3d, render.getRelativePoint(base.camera, near_point),
          render.getRelativePoint(base.camera, far_point))
      return pos_3d

    return None

  def on_frame(self, task):
    if self.mouse_down:
      mouse_pos = Point2(base.mouseWatcherNode.getMouse())

    if self.mouse_down == 'left':
      near_point = Point3()
      far_point = Point3()
      base.camLens.extrude(mouse_pos, near_point, far_point)
      xform_matrix = self.prev_camera_xform.getMat()
      near_point = xform_matrix.xformPoint(near_point)
      far_point = xform_matrix.xformPoint(far_point)

      new_point = Point3()
      self.translate_plane.intersectsLine(new_point, near_point, far_point)
      delta = self.click_point_3d - new_point

      self.camera_anchor.setPos(self.prev_camera_anchor_pos + delta)

    elif self.mouse_down == 'right':
      mouse_delta = mouse_pos - self.prev_mouse_pos
      new_h = self.prev_camera_anchor_xform.getHpr().x - self._ROTATION_SCALING * mouse_delta.x
      new_p = self.prev_camera_anchor_xform.getHpr().y + self._ROTATION_SCALING * mouse_delta.y

      if new_p > 90.0:
        new_p = 90.0
      elif new_p < -90.0:
        new_p = -90.0

      self.camera_anchor.setH(new_h)
      self.camera_anchor.setP(new_p)

    return task.cont

  def wheel(self, direction):
    mouse_pos = Point2(base.mouseWatcherNode.getMouse())

    click_point_3d = self.get_3d_from_2d(mouse_pos)

    if click_point_3d:
      scale = 1.0 + self._ZOOM_SCALING if direction == 'up' else 1.0 - self._ZOOM_SCALING

      self.transparent_anchor_move(click_point_3d)

      new_pos = base.camera.getPos() * scale
      if new_pos.length() > 2.0 * base.camLens.getNear() or direction == 'up':
        base.camera.setPos(new_pos)

    else:
      scale = -self._ZOOM_MOVE_SCALING if direction == 'up' else self._ZOOM_MOVE_SCALING

      far_point = Point3()
      base.camLens.extrude(mouse_pos, Point3(), far_point)

      move_delta = far_point.normalized() * scale * base.camera.getPos().length()
      move_delta = render.getRelativeVector(base.camera, move_delta)

      self.camera_anchor.setPos(self.camera_anchor.getPos() + move_delta)

  def mouse_click(self, button, direction):
    if direction == 'down':
      mouse_pos = Point2(base.mouseWatcherNode.getMouse())

      # Ignore clicks if other buttons are already down.
      if self.mouse_down:
        return
      self.mouse_down = button

      if button == 'left':
        self.click_point_3d = self.get_3d_from_2d(mouse_pos, self.background_plane)
        self.translate_plane = Plane(render.getRelativeVector(base.camera, LVector3(0, 1, 0)),
            self.click_point_3d)
        self.prev_camera_xform = base.camera.getNetTransform()
        self.prev_camera_anchor_pos = self.camera_anchor.getPos()

      elif button == 'right':
        click_point_3d = self.get_3d_from_2d(mouse_pos)
        if click_point_3d:
          self.transparent_anchor_move(click_point_3d)
        else:
          new_anchor_pos = render.getRelativePoint(base.camera,
              Point3(0, base.camera.getPos().length(), 0))
          self.transparent_anchor_move(new_anchor_pos)

        self.prev_mouse_pos = mouse_pos
        self.prev_camera_anchor_xform = self.camera_anchor.getTransform()


    else:
      # Ignore releases unless it matches the currently active button.
      if self.mouse_down == button:
        self.mouse_down = None

  def transparent_anchor_move(self, pos):
    base.camera.wrtReparentTo(render)
    self.camera_anchor.setPos(pos)
    base.camera.wrtReparentTo(self.camera_anchor)

