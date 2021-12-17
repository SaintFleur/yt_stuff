import pygame


def add(a,b):
    return a + b

def sub(a,b):
    return a-b

def multiply(a,b):
    return a*b

def divide(a,b):
    return a/b

class App:
     def __init__(self):
         self._running = True
         self.window = None
         self.window_size = self.width, self.height = 500, 1000
         self.clock = pygame.time.Clock()

     def on_init(self):
         pygame.init()
         pygame.display.set_caption("Calculator")
         self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
         self._running = True

     def on_event(self, event):
         if event.type == pygame.QUIT:
             self.running = False

     def on_loop(self):
         pass

     def on_render(self):
         pass

     def on_cleanup(self):
         pygame.quit()

     def on_execute(self):
         if self.on_init() == False:
             self._running = False

         background_color = (255,255,255)

         while self._running:
             self.window.fill(background_color)

             events = pygame.event.get()
             for event in events:
                 self.on_event(event)

             self.on_loop()
             self.on_render()
             pygame.display.update()


         self.on_cleanup()




if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
