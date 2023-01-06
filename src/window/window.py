import pygame
from enum import Enum, auto

from element.element import Element

class WindowCondition(Enum):
  ALWAYS  = auto()
  FOCUSED = auto()
  NEVER   = auto()

class Window:
  def __init__(
    self, x, y, w, h, 
    isValid=True, isResizable=False, zAxis=0,
    getMouseEventOn=WindowCondition.FOCUSED, getKeyEventOn=WindowCondition.FOCUSED
  ):
    # Window location and size
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.surface = pygame.surface.Surface((self.w, self.h))

    # Window state
    self.isValid = isValid
    self.isResizable = isResizable
    self.zAxis = zAxis

    # Event process
    self.events = []
    self.getMouseEventOn = getMouseEventOn
    self.getKeyEventOn = getKeyEventOn

    # Visuals
    self.backgroundColor  = (255, 255, 255)   # White
    self.borderColor      = (63,  63,  63)    # Dimgray
    self.borderWidth      = 2
    self.borderRadius     = 0
    
    # Hierarchy
    self.parentScreen = None
    self.elements = []

  def focus(self):
    self.parentScreen.windows.remove(self)
    self.parentScreen.windows.insert(0, self)
  
  def validate(self):
    self.isValid = True

  def invalidate(self):
    self.isValid = False

  def destroy(self):
    self.parentScreen.windows.remove(self)
  
  def getPosition(self):
    return (self.x, self.y)
  
  def setPosition(self, x=None, y=None):
    self.x = x if x else self.x
    self.y = y if y else self.y
  
  def getSize(self):
    return (self.w, self.h)
  
  def setSize(self, w=None, h=None):
    self.w = w if w else self.w
    self.h = h if h else self.h
  
  def getBoundingBox(self):
    return self.surface.get_bounding_rect()

  def contains(self, tx, ty):
    return (
      self.x <= tx and 
      tx <= self.x + self.w and 
      self.y <= ty and 
      ty <= self.y + self.h
    )

  def pushEvent(self, event):
    self.events.append(event)
  
  def getEvents(self):
    result = self.events
    self.events = []
    return result

  def takeEvent(self, event):
    if (
      event.type == pygame.MOUSEMOTION or 
      event.type == pygame.MOUSEBUTTONDOWN or 
      event.type == pygame.MOUSEBUTTONUP or 
      event.type == pygame.MOUSEWHEEL
    ):  
    # Mouse event
      if not self.contains(*event.pos):
        return False
      else:
        self.events.append(event)
        return True

    elif (
      event.type == pygame.KEYDOWN or
      event.type == pygame.KEYUP
    ):
    # Key event
      if (
        self.getKeyEventOn == WindowCondition.ALWAYS or 
        (self.getKeyEventOn == WindowCondition.FOCUSED and self.isFocused)
      ):
        self.events.append(event)
        return True
    
    return False

  def addElement(self, element):
    element.parentWindow = self
    self.elements.insert(0, element)

  def update_focus(self):
    for event in self.events:
      if event.type == pygame.MOUSEBUTTONDOWN and self.contains(*event.pos):
        self.focus()
  
  def update_self(self):
    pass

  def update(self):
    # Update focus
    self.update_focus()

    # Update self
    self.update_self()

    # Forward events to elements
    for event in self.getEvents():
      for element in self.elements:
        if element.takeEvent(event):
          break

    # Update elements
    for element in self.elements:
      element.update()
        
  def render_self(self):
    # Render self
    self.surface.fill(self.backgroundColor)
    pygame.draw.rect(
      surface=self.surface, 
      color=self.borderColor, 
      rect=self.getBoundingBox(),
      width=self.borderWidth,
      border_radius=self.borderRadius
    )

  def render(self, screen):
    # Render self
    self.render_self()
    
    # Render elements
    for element in reversed(self.elements):
      element.render(self.surface)

    # Render on screen
    screen.blit(self.surface, (self.x, self.y))    
  