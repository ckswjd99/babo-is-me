import pygame
from enum import Enum, auto

class ElementCondition(Enum):
  ALWAYS  = auto()
  FOCUSED = auto()
  NEVER   = auto()

class Element:
  def __init__(self, x, y, w, h):
    # Parent window
    self.window = None

    # Element location and size at window
    self.x = x
    self.y = y
    self.w = w
    self.h = h

    # Event handlers
    self.events = []
    self.eventHandlers = {
      pygame.MOUSEMOTION: None,
      pygame.MOUSEBUTTONDOWN: None,
      pygame.MOUSEBUTTONUP: None,
      pygame.MOUSEWHEEL: None,
      pygame.KEYDOWN: None,
      pygame.KEYUP: None,
    }

    # Visuals
    self.style = {
      'image'                   : None,
      'backgroundColor'         : None,
      'borderColor'             : None,
      'textColor'               : (  0,   0,   0),
      'borderWidth'             : 1,
      'borderRadius'            : 3,
    }

    # Children
    self.children = []
  
  ## SETTERS ##
  def setStyle(self, **kwargs):
    for key, val in kwargs.items():
      if key in self.style:
        print(key, val)
        self.style[key] = val
    return self
  
  def setEventHandler(self, type, handler):
    self.eventHandlers[type] = handler
  
  def getBoundingBox(self):
    return pygame.Rect(self.x, self.y, self.w, self.h)

  def contains(self, tx, ty):
    return (
      self.x <= tx and 
      tx <= self.x + self.w and 
      self.y <= ty and 
      ty <= self.y + self.h
    )

  def getLocalPosition(self, tx, ty):
    wx, wy = self.parentWindow.x, self.parentWindow.y
    return (tx - wx, ty - wy)

  def getEvents(self):
    result = self.events
    self.events = []
    return result

  def takeEvent(self, event):
    # React to event
    if self.eventHandlers[event.type] is not None:
      self.events.append(event)
      return True
    
    return False
    
  def update_self(self):
    pass
      
  def update(self):
    # update self
    self.update_self()

    # check children existance
    if len(self.children) == 0:
      self.getEvents()
      return

    # forward events to children
    for event in self.getEvents():
      for child in self.children:
        if child.takeEvent(event):
          break

    # update children
    for child in self.children:
      child.update()

  def render_self(self, surface):
    # Render background
    surface.fill(self.style['backgroundColor'])
    pygame.draw.rect(
      surface=surface, 
      color=self.style['borderColor'], 
      rect=self.getBoundingBox(),
      width=self.style['borderWidth'],
      border_radius=self.style['borderRadius']
    )

  def render(self, surface):
    # render self
    self.render_self(surface)

    # render children
    for child in reversed(self.children):
      child.render(surface)
