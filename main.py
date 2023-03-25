from Colors import Color
import Drawer
import pygame
from ThreeD.Objects import FrameObject, Camera

Drawer.init()


class FPSCounter:
    TICKS_RANGE = 100  # От скольки тиков берётся среднее
    ticks: int  # Счётчик тиков
    range_sum: float
    ticks_stack: list[float]

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.ticks = 0
        self.font = pygame.font.SysFont("Verdana", 20)
        self.range_sum = self.clock.tick()
        self.ticks_stack = [self.range_sum]

    def render(self, surface: pygame.Surface):
        text = self.font.render("{:.1f}".format(self.get_fps()), True, (255, 255, 255))
        surface.blit(text, (0, 0))

    def get_fps(self) -> float:
        self.ticks += 1
        tick = self.clock.tick()
        self.ticks_stack.append(tick)
        self.range_sum += tick
        if self.ticks >= self.TICKS_RANGE:
            top_tick = self.ticks_stack.pop(0)
            self.range_sum -= top_tick
        avg_ticks = self.range_sum / self.TICKS_RANGE
        return 1000 / avg_ticks


class Engine:
    objects = []
    running: bool = False
    fps = FPSCounter()
    camera = Camera()

    def init_objects(self):
        self.objects += [
            # FrameObject("ThreeD/Objects/Х.txt", x=-100, y=0, z=400),
            # FrameObject("ThreeD/Objects/У.txt", x=0, y=0, z=400),
            # FrameObject("ThreeD/Objects/И.txt", x=100, y=0, z=400)
        ]

    def fill_background(self):
        Drawer.fill_background(Color.BLACK)

    def draw_objects(self):
        for obj in self.objects:
            obj.draw(self.camera)

    def check_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False

    def main_loop(self):
        # self.camera.fov += 0.1
        for obj in self.objects:
            obj.z_angle += 0.1
            obj.x_angle += 0.1
            obj.y_angle += 0.1

    def run(self):
        self.init_objects()
        self.running = True
        while self.running:
            self.check_events()
            self.fill_background()

            self.main_loop()
            self.draw_objects()
            self.fps.render(Drawer.screen)

            Drawer.update()


if __name__ == "__main__":
    e = Engine()
    e.run()
    pygame.quit()
