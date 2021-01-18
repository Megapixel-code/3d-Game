import math
import pygame

map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ]
game = True
window = pygame.display.set_mode((1000, 1000))
mousePos = (None, None)


class Ray:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.xAdd = math.cos(math.radians((90 + angle) - 180))
        self.yAdd = math.cos(math.radians(angle))


def display(mapList):
    for x in range(10):
        for y in range(10):
            if mapList[y][x] == 1:
                pygame.draw.rect(window, (200, 200, 200), (x * 100, y * 100, 100, 100))


def inWall(mapList, posX, posY):
    for x in range(10):
        for y in range(10):
            if mapList[y][x] == 1 and x * 100 <= posX < x * 100 + 100 and y * 100 <= posY < y * 100 + 100:
                return True
    return False


def Dist(ray, mapList):
    x = ray.x
    y = ray.y
    while not inWall(mapList, x, y):
        x += ray.xAdd * 20
        y += ray.yAdd * 20
    while inWall(mapList, x, y):
        x -= ray.xAdd
        y -= ray.yAdd
    return int(x), int(y)


while game:
    window.fill((100, 100, 100))
    display(map)
    if mousePos != (None, None):
        allRays = []
        for i in range(360):
            allRays.append(Ray(mousePos[0], mousePos[1], i))

        for i in range(len(allRays)):
            nexpPos = Dist(allRays[i], map)
            pygame.draw.line(window, (255, 255, 255), (allRays[i].x, allRays[i].y),
                             nexpPos)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            game = False
        if event.type == pygame.MOUSEBUTTONUP:
            mousePos = pygame.mouse.get_pos()
            print(mousePos)
