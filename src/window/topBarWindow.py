import pygame
from enum import Enum, auto

from element.button import ButtonElement
from .window import Window, WindowCondition

class TopBarWindow(Window):
  def __init__(
    self, x, y, w, h,
    isValid=True, isResizable=True, zAxis=0,
    getMouseEventOn=WindowCondition.FOCUSED, getKeyEventOn=WindowCondition.FOCUSED
  ):
    super().__init__(x, y, w, h, isValid, isResizable, zAxis, getMouseEventOn, getKeyEventOn)

    # Init attributes
    self.dragging = False
    self.dragStartGlobalPos = None
    self.dragStartLocalPos = None

    # Set TopBar
    topbar = ButtonElement(0, 0, self.w, 30, 'TopBar').setStyle(
      backgroundColor=(127, 127, 127), borderColor=(95, 95, 95), borderRadius=0, borderWidth=2
    ).setAction(
      onClick=self.startDrag, onRelease=self.finishDrag
    )
    self.addElement(topbar)

    # Set BarButton
    invalidateButton = ButtonElement(self.w-25, 5, 20, 20).setStyle(
      backgroundColor=(220, 100, 100), borderColor=(150, 75, 75), borderRadius=1, borderWidth=1
    ).setAction(onClick=self.invalidate)
    self.addElement(invalidateButton)

  def startDrag(self):
    self.dragging = True
    self.dragStartGlobalPos = pygame.mouse.get_pos()
    self.dragStartLocalPos = (self.dragStartGlobalPos[0] - self.x, self.dragStartGlobalPos[1] - self.y)
  
  def finishDrag(self):
    self.dragging = False
  
  def update_self(self):
    if self.dragging:
      currentMouseGlobalPos = pygame.mouse.get_pos()
      self.x = currentMouseGlobalPos[0] - self.dragStartLocalPos[0]
      self.y = currentMouseGlobalPos[1] - self.dragStartLocalPos[1]
