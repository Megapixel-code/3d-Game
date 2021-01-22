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
        self.angle = ray_angle
        self.xAdd = math.sin(math.radians(ray_angle))
        self.yAdd = - math.cos(math.radians(ray_angle))


def validate_map(new_list):
    new_list[1][1] = 2
    modified = True
    while modified:
        modified = False
        for x in range(len(new_list) - 2):
            for y in range(len(new_list) - 2):
                if new_list[y + 1][x + 1] == 0 and (new_list[y][x + 1] == 2 or new_list[y + 1][x] == 2 or
                                                    new_list[y + 2][x + 1] == 2 or new_list[y + 1][x + 2] == 2):
                    new_list[y + 1][x + 1] = 2
                    modified = True
        if not modified:
            for i in range(len(new_list)):
                for k in range(len(new_list)):
                    if new_list[i][k] == 0:
                        return False
            for i in range(len(new_list) - 2):
                for k in range(len(new_list) - 2):
                    if new_list[i + 1][k + 1] == 1 and new_list[i + 2][k + 2] == 1 and new_list[i + 2][k + 1] == 2 and \
                            new_list[i + 1][k + 2] == 2:
                        return False
                    if new_list[i + 1][k + 1] == 2 and new_list[i + 2][k + 2] == 2 and new_list[i + 2][k + 1] == 1 and \
                            new_list[i + 1][k + 2] == 1:
                        return False

    for x in range(len(new_list)):
        for y in range(len(new_list)):
            if new_list[x][y] == 2:
                new_list[x][y] = 0
    return True


def create_map():
    cont = False
    my_map = []
    while not cont:
        my_map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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
                if my_map[y + 1][x] == 0 and random.randint(0, 1) == 0:
                    my_map[y + 1][x] = 1
        my_map[1][1] = 0
        cont = validate_map(my_map.copy())
    return my_map


def relative_dist(pos):
    x = pos[0] + 1
    y = pos[1] + 1
    x -= int(x / 100) * 100
    y -= int(y / 100) * 100
    if x > y:
        return x
    else:
        return y


def display(ray, n, mapList):
    wall_pos = dist(ray, mapList)
    relative_pos = relative_dist(wall_pos)
    my_dist = math.sqrt((wall_pos[0] - int(carPos[0])) ** 2 + (wall_pos[1] - int(carPos[1])) ** 2)
    col = my_dist / 8
    if col > 100:
        col = 100
    height = ((990 / (my_dist + 1)) * 100 - math.sin(math.radians(n * (180 / 200))) * 20)

    if 0 <= relative_pos < 25 or 50 <= relative_pos < 75:
        col = int(col / 10)
        pygame.draw.rect(window, [14 - col, 32 - col, 43 - col / 1.05],
                         [n * 5 - 2.5, (990 - height) / 2, 5, height])
    if 25 <= relative_pos < 50 or 75 <= relative_pos < 100:
        pygame.draw.rect(window, [180 - col, 184 - col, 171 - col / 1.05],
                         [n * 5 - 2.5, (990 - height) / 2, 5, height])


def in_wall(mapList, posX, posY, ray):
    if posX < 0 or posY < 0 or posX >= 1000 or posY >= 1000:
        return False
    x = int(posX / 100)
    y = int(posY / 100)
    if mapList[y][x] == 1:
        return True
    x = int((posX + ray.xAdd) / 100)
    y = int((posY + ray.yAdd) / 100)
    if mapList[y][x] == 1:
        return True
    return False


def dist(ray, mapList):
    x = ray.x
    y = ray.y
    rel_x = []
    if ray.angle < 90 or ray.angle > 270:
        for i in range(int(y / 100) + 1):
            rel_x.append([math.tan(math.radians(ray.angle)) * (y - i * 100) + x, i * 100])
    else:
        for i in range(int((1000 - y) / 100) + 1):
            rel_x.append([math.tan(math.radians(180 - ray.angle)) * ((1000 - i * 100) - y) + x, (10 - i) * 100])
    rel_y = []
    if 0 < ray.angle < 180:
        for i in range(int((1000 - x) / 100) + 1):
            rel_y.append([(10 - i) * 100, math.tan(math.radians(ray.angle - 90)) * (((10 - i) * 100) - x) + y])

    else:
        for i in range(int(x / 100) + 1):
            rel_y.append([i * 100, math.tan(math.radians(270 - ray.angle)) * (x - i * 100) + y])

    best_x = None
    for i in range(len(rel_x)):
        if in_wall(mapList, rel_x[i][0], rel_x[i][1], ray):
            best_x = rel_x[i]

    best_y = None
    for i in range(len(rel_y)):
        if in_wall(mapList, rel_y[i][0], rel_y[i][1], ray):
            best_y = rel_y[i]

    if best_x is None:
        return best_y
    if best_y is None:
        return best_x

    dist_x = math.sqrt((best_x[0] - int(carPos[0])) ** 2 + (best_x[1] - int(carPos[1])) ** 2)
    dist_y = math.sqrt((best_y[0] - int(carPos[0])) ** 2 + (best_y[1] - int(carPos[1])) ** 2)

    if dist_x > dist_y:
        return best_y
    return best_x


world_map = create_map()
while game:
    actualTime = time.process_time_ns()
    window.fill((119, 98, 88))
    pygame.draw.rect(window, (19, 111, 99), (0, 0, 1000, 500))

    allRays = []
    for j in range(200):
        angle = carAngle + j / 4 - 25
        if angle < 0:
            angle += 360
        elif angle >= 360:
            angle -= 360
        allRays.append(Ray(int(carPos[0]), int(carPos[1]), angle))
    for j in range(len(allRays)):
        display(allRays[j], j, world_map)

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
        newPos = ((carPos[0] - math.sin(math.radians(-carAngle)) * 2),
                  (carPos[1] - math.cos(math.radians(-carAngle)) * 2))
        if not in_wall(world_map, newPos[0], newPos[1], Ray(carPos[0], carPos[1], carAngle)):
            carPos = newPos
    if keys[pygame.K_s]:
        newPos = ((carPos[0] + math.sin(math.radians(-carAngle)) * 2),
                  (carPos[1] + math.cos(math.radians(-carAngle)) * 2))
        if not in_wall(world_map, newPos[0], newPos[1], Ray(carPos[0], carPos[1], carAngle)):
            carPos = newPos
    if keys[pygame.K_d]:
        newPos = ((carPos[0] + math.sin(math.radians(-carAngle + 90)) * 2),
                  (carPos[1] + math.cos(math.radians(-carAngle + 90)) * 2))
        if not in_wall(world_map, newPos[0], newPos[1], Ray(carPos[0], carPos[1], carAngle)):
            carPos = newPos
    if keys[pygame.K_q]:
        newPos = ((carPos[0] + math.sin(math.radians(-carAngle + 270)) * 2),
                  (carPos[1] + math.cos(math.radians(-carAngle + 270)) * 2))
        if not in_wall(world_map, newPos[0], newPos[1], Ray(carPos[0], carPos[1], carAngle)):
            carPos = newPos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            game = False
