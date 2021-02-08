import math
import pygame
import time
import random

game = True
carPos = (150, 150)
carAngle = 180

# ====================================================== TEXTURES ======================================================

gray = (49, 47, 47)
white = (246, 232, 234)

wall_1 = [[gray, gray, gray, gray, gray, gray, gray, gray, gray, gray],
        [gray, gray, white, white, white, white, white, white, gray, gray],
        [gray, white, gray, white, white, white, white, gray, white, gray],
        [gray, white, white, gray, white, white, gray, white, white, gray],
        [gray, white, white, white, gray, gray, white, white, white, gray],
        [gray, white, white, white, gray, gray, white, white, white, gray],
        [gray, white, white, gray, white, white, gray, white, white, gray],
        [gray, white, gray, white, white, white, white, gray, white, gray],
        [gray, gray, white, white, white, white, white, white, gray, gray],
        [gray, gray, gray, gray, gray, gray, gray, gray, gray, gray]]

wall_2 = [[gray, gray, gray, gray, gray, gray, gray, gray, gray, gray],
          [gray, white, gray, white, gray, gray, white, gray, white, gray],
          [gray, white, gray, white, gray, gray, white, gray, white, gray],
          [gray, white, gray, white, gray, gray, white, gray, white, gray],
          [gray, white, gray, white, gray, gray, white, gray, white, gray],
          [gray, white, gray, white, gray, gray, white, gray, white, gray],
          [gray, white, gray, white, gray, gray, white, gray, white, gray],
          [gray, white, gray, white, gray, gray, white, gray, white, gray],
          [gray, white, gray, white, gray, gray, white, gray, white, gray],
          [gray, gray, gray, gray, gray, gray, gray, gray, gray, gray]]

all_walls = [wall_1, wall_2]
del gray, white
del wall_1, wall_2


# ====================================================== TEXTURES ======================================================


class Ray:
    def __init__(self, x, y, ray_angle):
        self.x = x
        self.y = y
        self.angle = ray_angle
        self.xAdd = math.sin(math.radians(ray_angle))
        self.yAdd = - math.cos(math.radians(ray_angle))


class Mob:
    def __init__(self, x, y, lvl):
        self.health = lvl
        self.x = x
        self.y = y
        self.lvl = lvl

    def move(self):
        pass

    def give_angle(self):
        relative_x = self.x - carPos[0]
        relative_y = self.y - carPos[1]
        if relative_y == 0 and relative_x > 0:
            return 90
        if relative_y == 0 and relative_x < 0:
            return 270
        if relative_y == 0:
            return None
        mob_angle = math.degrees(math.atan(relative_x / relative_y))
        mob_angle = -mob_angle
        if relative_x >= 0 and relative_y <= 0:
            return mob_angle
        if relative_y > 0:
            return mob_angle + 180
        if relative_x <= 0 and relative_y <= 0:
            return mob_angle + 360


# ______________ TWEAKING TEXTURES ______________


def normalize_textures(my_list):
    all_textures = []
    for e in my_list:
        temp = []
        for i in range(10):
            temp_2 = []
            for j in range(10):
                temp_2.append(e[j][-(i + 1)])
            temp.append(temp_2)
        all_textures.append(temp)
    return all_textures


# ______________ MAP MODIFICATIONS ______________


def validate_map(new_list):
    new_list[1][1] = -1
    modified = True
    while modified:
        modified = False
        for x in range(len(new_list) - 2):
            for y in range(len(new_list) - 2):
                if new_list[y + 1][x + 1] == 0 and (new_list[y][x + 1] == -1 or new_list[y + 1][x] == -1 or
                                                    new_list[y + 2][x + 1] == -1 or new_list[y + 1][x + 2] == -1):
                    new_list[y + 1][x + 1] = -1
                    modified = True
        if not modified:
            for i in range(len(new_list)):
                for k in range(len(new_list)):
                    if new_list[i][k] == 0:
                        return False
            for i in range(len(new_list) - 2):
                for k in range(len(new_list) - 2):
                    if new_list[i + 1][k + 1] != -1 and new_list[i + 2][k + 2] != -1 and \
                            new_list[i + 2][k + 1] == -1 and new_list[i + 1][k + 2] == -1:
                        return False
                    if new_list[i + 1][k + 1] == -1 and new_list[i + 2][k + 2] == -1 and \
                            new_list[i + 2][k + 1] != -1 and new_list[i + 1][k + 2] != -1:
                        return False

    for x in range(len(new_list)):
        for y in range(len(new_list)):
            if new_list[x][y] == -1:
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
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        for y in range(8):
            for x in range(10):
                if my_map[y + 1][x] == 0 and random.randint(0, 1) == 0:
                    my_map[y + 1][x] = random.randint(1, len(textures))
        my_map[1][1] = 0
        cont = validate_map(my_map.copy())
    return my_map


# ______________ RENDERING ______________


def relative_dist(pos):
    x = pos[0] + 1
    y = pos[1] + 1
    x -= int(x / 100) * 100
    y -= int(y / 100) * 100
    if x > y:
        return x, True
    else:
        return y, False


def give_wall(pos, mapList):
    for i in range(3):
        for j in range(3):
            x = mapList[int((pos[1] + (i - 1)) / 100)][int((pos[0] + (j - 1)) / 100)]
            if x != 0:
                return x


def display(ray, n, mapList):
    wall_pos = dist(ray, mapList)
    relative_pos = relative_dist(wall_pos)
    my_dist = math.sqrt((wall_pos[0] - int(carPos[0])) ** 2 + (wall_pos[1] - int(carPos[1])) ** 2)
    height = ((990 / (my_dist + 1)) * 100 - math.sin(math.radians(n * (180 / 200))) * 20)

    color_cor = my_dist / 200
    if color_cor < 1:
        color_cor = 1

    my_wall = textures[give_wall(wall_pos, mapList) - 1]

    if 90 > ray.angle or ray.angle > 270 and relative_pos[1]:
        for i in range(10):
            col = my_wall[-(int(relative_pos[0] / 10) + 1)][i]
            pygame.draw.rect(window, [int(col[0] / color_cor), int(col[1] / color_cor), int(col[2] / color_cor)],
                             [n * 5 - 2.5, (1000 - height) / 2 + height / 10 * i, 5, height / 10 + 1])
    elif 0 < ray.angle < 180 and relative_pos[1] is False:
        for i in range(10):
            col = my_wall[-(int(relative_pos[0] / 10) + 1)][i]
            pygame.draw.rect(window, [int(col[0] / color_cor), int(col[1] / color_cor), int(col[2] / color_cor)],
                             [n * 5 - 2.5, (1000 - height) / 2 + height / 10 * i, 5, height / 10 + 1])
    else:
        for i in range(10):
            col = my_wall[int(relative_pos[0] / 10)][i]
            pygame.draw.rect(window, [int(col[0] / color_cor), int(col[1] / color_cor), int(col[2] / color_cor)],
                             [n * 5 - 2.5, (1000 - height) / 2 + height / 10 * i, 5, height / 10 + 1])


def in_wall(mapList, posX, posY, ray):
    if posX < 0 or posY < 0 or posX >= 1000 or posY >= 1000:
        return False
    x = int(posX / 100)
    y = int(posY / 100)
    if mapList[y][x] != 0:
        return True
    x = int((posX + ray.xAdd) / 100)
    y = int((posY + ray.yAdd) / 100)
    if mapList[y][x] != 0:
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


def render():
    all_rays = []
    for j in range(200):
        angle = carAngle + j / 4 - 25
        if angle < 0:
            angle += 360
        elif angle >= 360:
            angle -= 360
        all_rays.append(Ray(int(carPos[0]), int(carPos[1]), angle))
    for j in range(len(all_rays)):
        display(all_rays[j], j, world_map)


# ______________ MOVEMENT ______________


def walk(my_angle):
    global carPos

    if my_angle > 360:
        my_angle -= 360
    elif my_angle < 0:
        my_angle += 360

    new_pos = ((carPos[0] - math.sin(math.radians(-my_angle)) * 2),
               (carPos[1] - math.cos(math.radians(-my_angle)) * 2))
    if not in_wall(world_map, new_pos[0], new_pos[1], Ray(carPos[0], carPos[1], my_angle)):
        carPos = new_pos
        return

    new_pos = ((carPos[0] - math.sin(math.radians(-my_angle)) * 2), carPos[1])
    if not in_wall(world_map, new_pos[0], new_pos[1], Ray(carPos[0], carPos[1], my_angle)):
        carPos = new_pos
        return

    new_pos = (carPos[0], (carPos[1] - math.cos(math.radians(-my_angle)) * 2))
    if not in_wall(world_map, new_pos[0], new_pos[1], Ray(carPos[0], carPos[1], my_angle)):
        carPos = new_pos
        return


textures = normalize_textures(all_walls)
del all_walls
world_map = create_map()
window = pygame.display.set_mode((990, 990))
while game:
    # ===================================== INITIALIZATION OF VARIABLE AND SCREEN =====================================

    actualTime = time.process_time_ns()
    window.fill((119, 98, 88))
    pygame.draw.rect(window, (19, 111, 99), (0, 0, 1000, 500))

    # ============================================ RENDERING ALL THE WINDOW ============================================

    render()

    # =================================== WAITING FOR THE END OF THE FRAME (~30 FPS) ===================================

    if time.process_time_ns() < actualTime + 30000000:
        time.sleep(0.01)
    pygame.display.update()

    # ========================================== KEYS DETECTIONS AND MOVEMENT ==========================================

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
        walk(carAngle)
    if keys[pygame.K_s]:
        walk(carAngle + 180)
    if keys[pygame.K_d]:
        walk(carAngle + 90)
    if keys[pygame.K_q]:
        walk(carAngle + 270)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            game = False
