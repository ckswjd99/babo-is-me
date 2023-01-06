import pygame

class Scene:
  def __init__(self, width=600, height=480, caption="pygame-window"):
    # Initialize - Display
    self.width = width
    self.height = height
    self.caption = caption
    self.backgroundColor = (0, 0, 0)    # Black

    # Initialize - Hierarchy
    self.parentGame = None
    self.windows = []
    
  def addWindow(self, window):
    self.windows.insert(0, window)
    window.parentScreen = self

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

  def render(self, screen):
    ## Windows render function ##

    # Render self
    screen.fill(self.backgroundColor)

    # Render windows in reverse order
    for window in reversed(self.windows):
      if window.isValid:
        window.render(screen)
  
