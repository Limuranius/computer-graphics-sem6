import Objects
from Colors import Color
import Drawer
import Borders
from Primitives import PolarPoint
from BaseObjects import BaseDrawable
import pygame
from OptimizedObjects import PolygonOptimized

Drawer.init()


class Engine:
    objects: list[BaseDrawable] = []
    running: bool = False

    def init_objects(self):
        self.objects += [
            PolygonOptimized("Polygons/N.txt", x=50, y=100, size=20),
            PolygonOptimized("Polygons/I.txt", x=100, y=100, size=20),
            PolygonOptimized("Polygons/G.txt", x=150, y=100, size=20),
            PolygonOptimized("Polygons/G.txt", x=200, y=100, size=20),
            PolygonOptimized("Polygons/E.txt", x=250, y=100, size=20),
            PolygonOptimized("Polygons/R.txt", x=300, y=100, size=20),
            PolygonOptimized("Polygons/S.txt", x=350, y=100, size=20),
        ]

    def fill_background(self):
        Drawer.fill_background(Color.BLACK)

    def draw_objects(self):
        for obj in self.objects:
            obj.draw()

    def check_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False

    def main_loop(self):
        import random
        self.objects[0].angle += 0.1
        self.objects[0].size += random.random() - 0.5

    def run(self):
        self.init_objects()
        self.running = True
        while self.running:
            self.check_events()
            self.fill_background()
            self.main_loop()
            self.draw_objects()
            Drawer.update()


if __name__ == "__main__":
    e = Engine()
    e.run()
    pygame.quit()
