import sys
sys.path.insert(1, '../src')

import pygame
from scene import Scene
from window.window import Window
from window.topBarWindow import TopBarWindow
from element.element import Element
from element.button import ButtonElement
from game import GameManager

pygame.init()

SCENE = Scene(width=600, height=480, caption="pg-win")

dragWindow1 = TopBarWindow(0, 0, 300, 200, zAxis=1, caption='Window 0')
dragElement1 = ButtonElement(10, 50, 100, 30, caption='Button 0').setAction(onClick=lambda: print("pressed 0!"))
dragWindow1.addElement(dragElement1)

dragWindow2 = TopBarWindow(20, 20, 300, 200, zAxis=1, caption='Window 1')
dragElement2 = ButtonElement(10, 50, 100, 30, caption='Button 1').setAction(onClick=lambda: print("pressed 1!"))
dragWindow2.addElement(dragElement2)

centerWindow = Window(150, 120, 300, 240)
centerElement1 = ButtonElement(10, 10, 100, 30, caption='Win 0').setAction(onClick=lambda: dragWindow1.validate().focus())
centerElement2 = ButtonElement(160, 10, 100, 30, caption='Win 1').setAction(onClick=lambda: dragWindow2.validate().focus())
centerWindow.addElement(centerElement1)
centerWindow.addElement(centerElement2)

SCENE.addWindow(centerWindow)
SCENE.addWindow(dragWindow1)
SCENE.addWindow(dragWindow2)

GAME = GameManager(width=600, height=480, caption='pg-win')
GAME.addScene(SCENE, 'start')
GAME.setStartScene('start')
GAME.start()