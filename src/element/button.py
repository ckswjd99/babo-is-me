import pygame
from enum import Enum, auto

from config import MOUSE_EVENTS, KEY_EVENTS
from .element import Element

class ButtonState(Enum):
  COMMON  = auto()
  HOVER   = auto()
  PRESSED = auto()

class ButtonElement(Element):
  def __init__(self, x, y, w, h, caption='Button'):
    super().__init__(x, y, w, h)
    
    # Caption
    self.caption = caption

    # Self state
    self.state = ButtonState.COMMON
    self._mousePos = (0, 0)
    self._mouseRel = (0, 0)

    # Styles
    self.style = {
      'image'                   : None,
      'imageCommon'             : None,
      'imageHover'              : None,
      'imagePressed'            : None,
      'backgroundColor'         : None,
      'backgroundColorCommon'   : (127, 223, 127),
      'backgroundColorHover'    : (200, 223, 200),
      'backgroundColorPressed'  : ( 63, 189,  63),
      'borderColor'             : None,
      'borderColorCommon'       : (127, 200, 127),
      'borderColorHover'        : (127, 200, 127),
      'borderColorPressed'      : (127, 200, 127),
      'textColor'               : (  0,   0,   0),
      'textColorCommon'         : (  0,   0,   0),
      'textColorHover'          : (  0,   0,   0),
      'textColorPressed'        : (  0,   0,   0),
      'borderWidth'             : 1,
      'borderRadius'            : 3,
      'fontName'                : 'arial',
      'fontSize'                : 14,
      'bold'                    : False,
      'italic'                  : False,
      'textAlign'               : 'center',
    }

    # Actions
    self.action = {
      'onHover'   : None,
      'onClick'   : None,
      'onRelease' : None,
    }
    
  def setAction(self, **kwargs):
    for key, val in kwargs.items():
      if key in self.action:
        self.action[key] = val
    return self

  def takeEvent(self, event):
    if event.type in MOUSE_EVENTS and self.contains(*self.getLocalPosition(*event.pos)):
      self.events.append(event)
      return True
    
    return False
  
  def update_self(self):
    # Calculate next state
    nextState = self.state
    dragged = False
    for event in self.events:
      if event.type in MOUSE_EVENTS:
        if event.type == pygame.MOUSEBUTTONDOWN:
          nextState = ButtonState.PRESSED
        elif event.type == pygame.MOUSEBUTTONUP:
          nextState = ButtonState.HOVER
        elif event.type == pygame.MOUSEMOTION and self.state == ButtonState.PRESSED:
          nextState = ButtonState.PRESSED
          dragged = True
        elif event.type == pygame.MOUSEMOTION and self.state != ButtonState.PRESSED:
          nextState = ButtonState.HOVER
    
    # Mouse Tracking
    if not self.contains(*self.getLocalPosition(*pygame.mouse.get_pos())):
      nextState = ButtonState.COMMON
    
    # Actions
    if self.state == ButtonState.COMMON and nextState == ButtonState.HOVER:
      self.action['onHover']() if self.action['onHover'] else None
    elif self.state != ButtonState.PRESSED and nextState == ButtonState.PRESSED:
      self.action['onClick']() if self.action['onClick'] else None
    elif self.state == ButtonState.PRESSED and nextState != ButtonState.PRESSED:
      self.action['onRelease']() if self.action['onRelease'] else None

    # Update state
    self.state = nextState

    pass
  
  def render_self(self, surface):
    renderImage = None
    backgroundColor = None
    borderColor = None

    # Defaults
    if self.style['image']:
      renderImage = self.style['image']
    elif self.style['backgroundColor'] and self.style['borderColor']:
      backgroundColor = self.style['backgroundColor']
      borderColor = self.style['borderColor']

    # COMMON state
    elif self.state == ButtonState.COMMON:
      if self.style['imageCommon']:
        renderImage = self.style['backgroundColorCommon']
      else:
        backgroundColor = self.style['backgroundColorCommon']
        borderColor = self.style['borderColorCommon']

    # HOVER state
    elif self.state == ButtonState.HOVER:
      if self.style['imageHover']:
        renderImage = self.style['imageHover']
      else:
        backgroundColor = self.style['backgroundColorHover']
        borderColor = self.style['borderColorHover']

    # PRESSED state
    elif self.state == ButtonState.PRESSED:
      if self.style['imagePressed']:
        renderImage = self.style['imagePressed']
      else:
        backgroundColor = self.style['backgroundColorPressed']
        borderColor = self.style['borderColorPressed']

    # Render button
    if renderImage:
      surface.blit(renderImage, (self.x, self.y))
    else:
      pygame.draw.rect(
        surface=surface,
        color=backgroundColor, 
        rect=self.getBoundingBox(),
        width=0,
        border_radius=self.style['borderRadius']
      )
      pygame.draw.rect(
        surface=surface, 
        color=borderColor, 
        rect=self.getBoundingBox(),
        width=self.style['borderWidth'],
        border_radius=self.style['borderRadius']
      )

