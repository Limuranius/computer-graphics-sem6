import Objects
from Colors import Color
import Drawer
import Borders
from Primitives import PolarPoint
from BaseObjects import BaseDrawable
import pygame

Drawer.init()


class Engine:
    objects: list[BaseDrawable] = []
    running: bool = False

    def init_objects(self):
        benis = Objects.Polygon(
            [(227, 272), (221, 284), (204, 292), (184, 285), (173, 266), (171, 244), (186, 233), (205, 231), (206, 220),
             (209, 201), (212, 186), (215, 167), (221, 152), (226, 145), (240, 146), (249, 154), (254, 167), (255, 178),
             (255, 194), (257, 209), (256, 224), (263, 231), (277, 239), (284, 257), (287, 269), (286, 281), (277, 291),
             (258, 292), (246, 286), (236, 272)],
            rotation_axis=(227, 292),
        )
        self.objects += [
            benis
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
        # self.objects[0].rotation_angle += 0.5
        for edge in self.objects[0].edges:
            edge.p0.x += (random.random() - 0.5) * 20
            edge.p1.x += (random.random() - 0.5) * 20
            edge.p0.y += (random.random() - 0.5) * 20
            edge.p1.y += (random.random() - 0.5) * 20
        self.objects[0].draw_triangles()

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
