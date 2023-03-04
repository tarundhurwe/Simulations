import pygame
import math
import numpy as np


class NoseHoover:
    def __init__(self, x, y, z, a, axis="y"):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.points = []
        self.axis = axis
        self.dt = 0.01
        self.angle = 0

    def calculate_new_points(self):
        dx = self.y * self.dt
        dy = (-self.x + self.y * self.z) * self.dt
        dz = (self.a - pow(self.y, 2)) * self.dt
        self.x += dx
        self.y += dy
        self.z += dz
        self.points.append(np.matrix([self.x, self.y, self.z]))
        self.angle += 0.01

    def rotation_matrix(self):
        rotation_x = [
            [1, 0, 0],
            [0, math.cos(self.angle), -math.sin(self.angle)],
            [0, math.sin(self.angle), math.cos(self.angle)],
        ]

        rotation_y = [
            [math.cos(self.angle), 0, -math.sin(self.angle)],
            [0, 1, 0],
            [math.sin(self.angle), 0, math.cos(self.angle)],
        ]

        rotation_z = [
            [math.cos(self.angle), -math.sin(self.angle), 0],
            [math.sin(self.angle), math.cos(self.angle), 0],
            [0, 0, 1],
        ]
        axis_dictionary = {"x": rotation_x, "y": rotation_y, "z": rotation_z}
        return axis_dictionary.get(self.axis)


class MainScreen:
    def __init__(self, attractor: NoseHoover):
        pygame.init()
        self.attractor = attractor
        self.height = pygame.display.get_desktop_sizes()[0][1]
        self.width = pygame.display.get_desktop_sizes()[0][0]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.run = True
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.scale = 10
        self.projection_matrix = np.matrix(
            [
                [self.height // 2, 0, self.width // 2],
                [0, self.height // 2, self.height // 2],
            ]
        )

    def stop_animation(self):
        self.run = False

    def start_screen(self):
        while self.run:
            self.screen.fill(self.black)
            self.attractor.calculate_new_points()
            for idx, point in enumerate(self.attractor.points):
                projection_2d = (
                    self.projection_matrix
                    * self.attractor.rotation_matrix()
                    * point.reshape((3, 1))
                )
                pygame.draw.circle(
                    self.screen,
                    self.white,
                    (
                        int(projection_2d[0][0] / self.scale) + self.width // 2,
                        int(projection_2d[1][0] / self.scale) + self.height // 2,
                    ),
                    1,
                )
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_animation()

    def quit_screen(self):
        pygame.quit()


if __name__ == "__main__":
    a = 1.5
    x = 2
    y = 4
    z = 3.5
    attractor = NoseHoover(x, y, z, a, "y")
    screen = MainScreen(attractor)
    screen.start_screen()
    screen.quit_screen()
