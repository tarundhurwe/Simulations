import pygame
import math
import numpy as np


class LorenzAttractor:
    def __init__(self, x, y, z, axis="y") -> None:
        self.x = x
        self.y = y
        self.z = z
        self.r = 250
        self.g = 209
        self.b = 60
        self.dt = 0.01
        self.rho = 28
        self.sigma = 10
        self.beta = 8 / 3
        self.points = []
        self.axis = axis
        self.color = [[self.r, self.g, self.b]]
        self.angle = 0

    def calculate_new_point(self):
        dx = (self.sigma * (self.y - self.x)) * self.dt
        dy = (self.x * (self.rho - self.z) - self.y) * self.dt
        dz = (self.x * self.y - self.beta * self.z) * self.dt
        self.x += dx
        self.y += dy
        self.z += dz
        self.angle += 0.01
        self.points.append(np.matrix([self.x, self.y, self.z]))
        # self.color.append(
        #     [
        #         (self.color[-1][0] + 1) % 255,
        #         (self.color[-1][1] + 1) % 255,
        #         (self.color[-1][2] + 1) % 255,
        #     ]
        # )

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
    def __init__(self, attractor: LorenzAttractor) -> None:
        pygame.init()
        self.attractor = attractor
        self.height = pygame.display.get_desktop_sizes()[0][1]
        self.width = pygame.display.get_desktop_sizes()[0][0]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.run = True
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.scale = 80
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
            self.attractor.calculate_new_point()
            for idx, point in enumerate(self.attractor.points):
                projection_2d = (
                    self.projection_matrix
                    * self.attractor.rotation_matrix()
                    * point.reshape((3, 1))
                )
                # (color[idx][0], color[idx][1], color[idx][2])
                pygame.draw.circle(
                    self.screen,
                    (
                        self.attractor.r,
                        self.attractor.g,
                        self.attractor.b,
                    ),
                    (
                        int(projection_2d[0][0] // self.scale) + self.width // 2,
                        int(projection_2d[1][0] // self.scale) + self.height // 2,
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
    x, y, z = 0.1, 1.0, 1.05
    lorenz_attractor = LorenzAttractor(x, y, z, "y")
    pygame_screen = MainScreen(lorenz_attractor)
    pygame_screen.start_screen()
    pygame_screen.quit_screen()
