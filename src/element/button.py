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
      'padding'                 : 6,
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
    }

    # Font configs
    self.fontStyle = {
      'fontName'                : 'arial',
      'fontSize'                : 14,
      'bold'                    : False,
      'italic'                  : False,
      'verticalAlign'           : 'center',
      'horizontalAlign'         : 'center',
    }
    self.font = pygame.font.SysFont(
      self.fontStyle['fontName'], 
      self.fontStyle['fontSize'], 
      self.fontStyle['bold'], 
      self.fontStyle['italic']
    )

    # Actions
    self.action = {
      'onHover'   : None,
      'onClick'   : None,
      'onRelease' : None,
    }
    
  def setFontStyle(self, **kwargs):
    modified = False
    for key, val in kwargs.items():
      if key in self.fontStyle:
        self.fontStyle[key] = val

    if modified:
      self.font = pygame.font.SysFont(
        self.fontStyle['fontName'], 
        self.fontStyle['fontSize'], 
        self.fontStyle['bold'], 
        self.fontStyle['italic']
      )
    return self


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
    for event in self.events:
      if event.type in MOUSE_EVENTS:
        if event.type == pygame.MOUSEBUTTONDOWN:
          nextState = ButtonState.PRESSED
        elif event.type == pygame.MOUSEBUTTONUP:
          nextState = ButtonState.HOVER
        elif event.type == pygame.MOUSEMOTION and self.state == ButtonState.PRESSED:
          nextState = ButtonState.PRESSED
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

  
  def render_self(self, surface):
    renderImage = None
    backgroundColor = None
    borderColor = None
    captionColor = None

    # Defaults
    if self.style['image']:
      renderImage = self.style['image']
    elif self.style['backgroundColor'] and self.style['borderColor']:
      backgroundColor = self.style['backgroundColor']
      borderColor = self.style['borderColor']
      captionColor = self.style['textColor']

    # COMMON state
    elif self.state == ButtonState.COMMON:
      if self.style['imageCommon']:
        renderImage = self.style['backgroundColorCommon']
      else:
        backgroundColor = self.style['backgroundColorCommon']
        borderColor = self.style['borderColorCommon']
        captionColor = self.style['textColorCommon']

    # HOVER state
    elif self.state == ButtonState.HOVER:
      if self.style['imageHover']:
        renderImage = self.style['imageHover']
      else:
        backgroundColor = self.style['backgroundColorHover']
        borderColor = self.style['borderColorHover']
        captionColor = self.style['textColorHover']

    # PRESSED state
    elif self.state == ButtonState.PRESSED:
      if self.style['imagePressed']:
        renderImage = self.style['imagePressed']
      else:
        backgroundColor = self.style['backgroundColorPressed']
        borderColor = self.style['borderColorPressed']
        captionColor = self.style['textColorPressed']

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
    
    # Render caption
    if self.caption != '':
      renderedCaption = self.font.render(self.caption, True, captionColor)
      captionX = 0
      captionY = 0

      if self.fontStyle['horizontalAlign'] == 'center':
        captionX = self.x + self.w/2 - renderedCaption.get_width()/2
      elif self.fontStyle['horizontalAlign'] == 'right':
        captionX = self.x + self.w - self.style['padding'] - renderedCaption.get_width()
      else:
        captionX = self.x + self.style['padding']

      if self.fontStyle['verticalAlign'] == 'center':
        captionY = self.y + self.h/2 - renderedCaption.get_height()/2
      elif self.fontStyle['verticalAlign'] == 'bottom':
        captionY = self.y + self.h - self.style['padding'] - renderedCaption.get_height()
      else:
        captionY = self.y + self.style['padding']

      surface.blit(renderedCaption, (captionX, captionY))

