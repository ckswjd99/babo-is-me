from screen import Screen
from window.window import Window
from window.topBarWindow import TopBarWindow
from element.element import Element
from element.button import ButtonElement

SCREEN = Screen(width=600, height=480, caption="pg-win")

centerWindow = Window(150, 120, 300, 240)
centerElement1 = ButtonElement(10, 10, 100, 30).setAction(onClick=lambda: print("pressed 1!"))
centerElement2 = ButtonElement(160, 10, 100, 30).setAction(onClick=lambda: print("pressed 2!"))
centerWindow.addElement(centerElement1)
centerWindow.addElement(centerElement2)

dragWindow1 = TopBarWindow(0, 0, 300, 200, zAxis=1)
dragElement1 = ButtonElement(10, 50, 100, 30).setAction(onClick=lambda: print("pressed 0-0!"))
dragWindow1.addElement(dragElement1)

dragWindow2 = TopBarWindow(20, 20, 300, 200, zAxis=1)
dragElement2 = ButtonElement(10, 50, 100, 30).setAction(onClick=lambda: print("pressed 0-1!"))
dragWindow2.addElement(dragElement2)


SCREEN.addWindow(centerWindow)
SCREEN.addWindow(dragWindow1)
SCREEN.addWindow(dragWindow2)
SCREEN.start()
