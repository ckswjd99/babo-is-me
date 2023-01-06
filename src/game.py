import pygame

class GameManager(object):
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
    self.nowScene = None
    self.startScene = None
    self.scenes = {}
  
  def setStartScene(self, sceneName):
    self.startScene = sceneName

  def addScene(self, scene, sceneName):
    self.scenes[sceneName] = scene
    scene.parentGame = self

  def start(self):
    # Check start scene
    if not self.startScene in self.scenes:
      print('No start scene!')
      return
    
    self.nowScene = self.scenes[self.startScene]

    # Create display
    self.screen = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption = self.caption

    # main loop
    running = True
    while running:
      running = self.update()
      self.render()
  
  def update(self):
    # Update nowScene
    return self.nowScene.update()

  def render(self):
    # Render nowScene
    self.nowScene.render(self.screen)
    
    # Render on display
    pygame.display.update()