import pygame
import math

class Robot:
    def __init__(self, startpos, robotimg,path, width):
        self.m2p = 3779.52  # from meters to pixels

        self.path=path
        self.waypoint=len(path)-1

        self.x, self.y = startpos
        self.theta = 0
        self.trail_set = []
        self.a = 20
        self.w = width
        self.u = 30  # pix/sec
        self.W = 0  # rad/sec

        self.img = pygame.image.load(robotimg)  # skin img path provided in the arguments
        self.rotated = self.img
        self.rect = self.rotated.get_rect(center=(self.x, self.y))

    def move(self,dt, event=None):
        self.x += (self.u * math.cos(self.theta) - self.a * math.sin(self.theta) * self.W) * dt
        self.y += (self.u * math.sin(self.theta) + self.a * math.cos(self.theta) * self.W) * dt
        self.theta += self.W * dt
        self.rotated = pygame.transform.rotozoom(self.img, math.degrees(-self.theta), 1)
        self.rect = self.rotated.get_rect(center=(self.x, self.y))
        self.follow_path()

    def follow_path(self):
        target = self.path[self.waypoint]
        delta_x = target[0] - self.x
        delta_y = target[1] - self.y
        self.u = delta_x * math.cos(self.theta) + delta_y * math.sin(self.theta)
        self.W = (-1 / self.a) * math.sin(self.theta) * delta_x + (1 / self.a) * math.cos(self.theta) * delta_y
        if self.dist((self.x,self.y),self.path[self.waypoint]) <= 35:
            self.waypoint-=1
        if self.waypoint <= 0:
            self.waypoint=0






    def dist(self, point1, point2):
        (x1, y1) = point1
        (x2, y2) = point2
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)
        # calculation
        px = (x1 - x2) ** (2)
        py = (y1 - y2) ** (2)
        distance = (px + py) ** (0.5)
        return distance

    def draw(self, map):
        map.blit(self.rotated, self.rect)

    def trail(self, pos, map, color):

        for i in range(0, len(self.trail_set) - 1):
            pygame.draw.line(map, color, (self.trail_set[i][0], self.trail_set[i][1]),
                             (self.trail_set[i + 1][0], self.trail_set[i + 1][1]))
        if self.trail_set.__sizeof__() > 2000:
            self.trail_set.pop(0)
        self.trail_set.append(pos)

    def robot_simulate(self,Robot,environment,dt, event=None):
        Robot.move(dt, event=event)
        Robot.draw(environment.map)
        Robot.trail((Robot.x, Robot.y), environment.map, environment.yel)

class Envir:
    def __init__(self, dimentions,map):
        # COLORS
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.yel = (255, 255, 0)
        # MAP DIMS
        self.height, self.width = dimentions
        # window settings
        pygame.display.set_caption("diff drive")
        self.map = map

    def write_info(self):
        pass

    def robot_frame(self):
        pass


