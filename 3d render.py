import math
import pygame
import time
import random

game = True
window = pygame.display.set_mode((990, 990))
carPos = (150, 150)
carAngle = 0


class Ray:
    def __init__(self, x, y, ray_angle):
        self.x = x
        self.y = y
        self.xAdd = math.cos(math.radians((90 + ray_angle) - 180))
        self.yAdd = math.cos(math.radians(ray_angle))


def create_map():
    mymap = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ]
    for y in range(8):
        for x in range(10):
            if mymap[y + 1][x] == 0 and random.randint(0, 1) == 0:
                mymap[y + 1][x] = 1
    mymap[1][1] = 0
    satisfied = False
    return mymap


def display(ray, n, mapList):
    wall_pos = Dist(ray, mapList)
    my_dist = math.sqrt((wall_pos[0] - int(carPos[0])) ** 2 + (wall_pos[1] - int(carPos[1])) ** 2)
    col = my_dist / 8
    if col > 100:
        col = 100
    taille = ((990 / (my_dist + 1)) * 100 - math.sin(math.radians(n * (180 / 200))) * 20)
    pygame.draw.rect(window, (225 - col, 216 - col, 159 - col / 1.05),
                     (n * 5 - 2.5, (990 - (taille)) / 2, 5, taille))


def inWall(mapList, posX, posY):
    x = int(posX / 100)
    y = int(posY / 100)
    if mapList[y][x] == 1:
        return True
    return False


def Dist(ray, mapList):
    x = ray.x
    y = ray.y
    while not inWall(mapList, int(x), int(y)):
        x += ray.xAdd * 10
        y += ray.yAdd * 10
    while inWall(mapList, int(x), int(y)):
        x -= ray.xAdd
        y -= ray.yAdd
    return int(x), int(y)


map = create_map()
while game:
    actualTime = time.process_time_ns()
    window.fill((55, 64, 69))
    pygame.draw.rect(window, (14, 32, 43), (0, 0, 1000, 500))

    allRays = []
    for j in range(200):
        angle = carAngle + j / 4 - 25
        if angle < 0:
            angle += 360
        elif angle >= 360:
            angle -= 360
        allRays.append(Ray(int(carPos[0]), int(carPos[1]), angle))
    for j in range(len(allRays)):
        display(allRays[j], j, map)

    if time.process_time_ns() < actualTime + 30000000:
        time.sleep(0.01)
    pygame.display.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        carAngle -= 1.5
        if carAngle < 0:
            carAngle += 360
    if keys[pygame.K_RIGHT]:
        carAngle += 1.5
        if carAngle >= 360:
            carAngle -= 360

    if keys[pygame.K_z]:
        newPos = ((carPos[0] + math.cos(math.radians((90 + carAngle) - 180)) * 2),
                  (carPos[1] + math.cos(math.radians(carAngle)) * 2))
        if not inWall(map, newPos[0], newPos[1]):
            carPos = newPos
    if keys[pygame.K_s]:
        newPos = ((carPos[0] - math.cos(math.radians((90 + carAngle) - 180)) * 2),
                  (carPos[1] - math.cos(math.radians(carAngle)) * 2))
        if not inWall(map, newPos[0], newPos[1]):
            carPos = newPos
    if keys[pygame.K_d]:
        newPos = ((carPos[0] + math.cos(math.radians((90 + carAngle + 90) - 180)) * 2),
                  (carPos[1] + math.cos(math.radians(carAngle + 90)) * 2))
        if not inWall(map, newPos[0], newPos[1]):
            carPos = newPos
    if keys[pygame.K_q]:
        newPos = ((carPos[0] - math.cos(math.radians((90 + carAngle + 90) - 180)) * 2),
                  (carPos[1] - math.cos(math.radians(carAngle + 90)) * 2))
        if not inWall(map, newPos[0], newPos[1]):
            carPos = newPos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            game = False
