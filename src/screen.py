import pygame
from threading import Thread
from time import sleep

class Screen(object):
  def __new__(cls, *args, **kwargs):
    # Singleton pattern
    if not hasattr(cls, "_instance"):
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self, width=600, height=480, caption="pygame-window"):
    # Singleton pattern
    cls = type(self)
    if hasattr(cls, "_init"):
      return
    cls._init = True
    
    # Initialize - Display
    self.width = width
    self.height = height
    self.screen = None
    self.caption = caption
    self.backgroundColor = (0, 0, 0)    # Black

    # Initialize - Windows
    self.windows = []

    # Initialize - Control
    
  def addWindow(self, window):
    self.windows.insert(0, window)
    window.parentScreen = self


  def start(self):
    # Create display
    self.screen = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption = self.caption

    # main loop
    running = True
    while running:
      running = self.update()
      self.render()

  def update(self):
    ## Windows update function ##

    # Forward events to windows
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return False
      
      for window in self.windows:
        if window.isValid and window.takeEvent(event):
          break
    
    # Update windows
    for window in self.windows:
      if window.isValid:
        window.update()

    # Update focus
    self.windows.sort(key=lambda x: x.zAxis, reverse=True)
    for window in self.windows:
      if window.isValid:
        window.isFocused = True
        break
    
    return True

  def render(self):
    ## Windows render function ##

    # Render self
    self.screen.fill(self.backgroundColor)

    # Render windows in reverse order
    for window in reversed(self.windows):
      if window.isValid:
        window.render(self.screen)
    
    # Render on display
    pygame.display.update()
  
