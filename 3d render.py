import math
import pygame
import time
import random

game = True
carPos = (150.5, 150.5)
carAngle = 180

# ====================================================== TEXTURES ======================================================

# good website for colors : https://coolors.co/
gray1 = (162, 162, 162)
gray2 = (127, 127, 127)
gray3 = (51, 51, 51)
noir = (0, 0, 0)
orange1 = (232, 92, 0)
orange2 = (255, 127, 39)

wall_1 = [[gray1, gray1, gray1, gray1, gray1, gray1, gray1, gray1, gray1, gray1],
          [gray2, gray2, gray2, gray2, gray2, gray2, gray2, gray2, gray2, gray2],
          [gray2, gray2, gray3, gray3, gray3, gray3, gray3, gray3, gray2, gray2],
          [noir, noir, noir, gray2, gray2, gray2, gray2, noir, noir, noir],
          [gray2, gray2, gray2, gray2, gray2, gray2, gray2, gray2, gray2, gray2],
          [orange2, noir, noir, gray3, orange1, orange2, noir, noir, gray3, orange1],
          [orange1, orange2, noir, noir, gray3, orange1, orange2, noir, noir, gray3],
          [gray2, gray2, gray2, gray2, gray2, gray2, gray2, gray2, gray2, gray2],
          [gray2, gray2, gray2, gray2, gray2, gray2, gray2, gray2, gray2, gray2],
          [noir, noir, noir, noir, noir, noir, noir, noir, noir, noir]]

mob1 = [[gray1, gray1, gray1, gray1],
        [gray1, noir, gray1, gray1],
        [gray1, gray1, gray1, gray1],
        [gray1, gray1, gray1, gray1],
        [gray1, gray1, gray1, gray1],
        [gray1, gray1, gray1, gray1],
        [gray1, gray1, gray1, gray1],
        [gray1, noir, gray1, gray1]]

all_mobs = [mob1]
all_walls = [wall_1]
del gray1, gray2, gray3, noir, orange1, orange2
del wall_1, mob1


# ====================================================== TEXTURES ======================================================


class Ray:
    def __init__(self, x, y, ray_angle):
        self.x = x
        self.y = y
        self.angle = ray_angle
        self.xAdd = math.sin(math.radians(ray_angle))
        self.yAdd = - math.cos(math.radians(ray_angle))


class Mob:
    def __init__(self, lvl):
        self.health = lvl * 2
        self.lvl = lvl
        finished = False
        while not finished:
            finished = True
            self.x = random.randint(0, 1000)
            self.y = random.randint(0, 1000)
            for i in range(4):
                if in_wall(world_map, self.x, self.y, Ray(self.x, self.y, i * 90)):
                    finished = False

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

    def give_dist(self, pos):
        return math.sqrt((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2)


# ______________ TWEAKING TEXTURES ______________


def normalize_textures(my_list):
    all_textures = []
    for e in my_list:
        temp = []
        for i in range(len(e[0])):
            temp_2 = []
            for j in range(len(e)):
                temp_2.append(e[j][-(i + 1)])
            temp.append(temp_2)
        all_textures.append(temp)
    return all_textures

# ______________ OTHERS ______________


def rest(number):
    if number >= 0:
        return number - int(number / 360) * 360
    return number - int(number / 360) * 360 + 360


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


def display(ray, n, mapList, mobs_angle, mobs_distance, sizes):
    wall_pos = dist(ray, mapList)
    relative_pos = relative_dist(wall_pos)
    my_dist = math.sqrt((wall_pos[0] - int(carPos[0])) ** 2 + (wall_pos[1] - int(carPos[1])) ** 2)
    height = ((1000 / (my_dist + 1)) * 100 - math.sin(math.radians(n * (180 / 200))) * 20)

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

    mobs_start_positions = []
    for i in range(len(mobs)):
        mobs_start_positions.append(mobs_angle[i] - (sizes[i] * 0.25) / 2)
    for j in range(len(mobs)):
        mob_color_cor = mobs_distance[j] / 200
        if mob_color_cor < 1:
            mob_color_cor = 1

        if mobs_angle[j] - sizes[j] * 0.25 / 2 < ray.angle <= mobs_angle[j] + sizes[j] * 0.25 / 2 and mobs_distance[j] \
                <= my_dist or mobs_angle[j] - 360 - sizes[j] * 0.25 / 2 < ray.angle <= mobs_angle[j] - 360 + sizes[j] *\
                0.25 / 2 and mobs_distance[j] <= my_dist or mobs_angle[j] + 360 - sizes[j] * 0.25 / 2 < ray.angle <= \
                mobs_angle[j] + 360 + sizes[j] * 0.25 / 2 and mobs_distance[j] <= my_dist:
            mob_height = ((1000 / (mobs_distance[j] + 1)) * 100 - math.sin(math.radians(n * (180 / 200))) * 20) * 0.7
            col = mobs_textures[mobs[j].lvl][int(rest((ray.angle - mobs_angle[j]) + (sizes[j] * 0.25) / 2)/(sizes[j] /
                                                                                                            16))]
            for k in range(8):
                pygame.draw.rect(window, [int(col[k][0] / mob_color_cor), int(col[k][1] / mob_color_cor), int(col[k][2] / mob_color_cor)], [n * 5 - 2.5, ((3999 - mob_height / 0.7) / 8) + k * ((mob_height + 1) / 8), 5, (mob_height + 1) / 8 + 1])


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


def sort_mobs():
    distances = []
    for m in mobs:
        distances.append(m.give_dist(carPos))
    sorted_distances = distances.copy()
    sorted_distances.sort()
    sorted_distances.reverse()
    while distances != sorted_distances:
        for i in range(len(mobs) - 1):
            if distances[i] < distances[i + 1]:
                distances[i], distances[i + 1] = distances[i + 1], distances[i]
                mobs[i], mobs[i + 1] = mobs[i + 1], mobs[i]


def render():
    all_rays = []
    for j in range(200):
        angle = carAngle + j / 4 - 24.75
        if angle < 0:
            angle += 360
        elif angle >= 360:
            angle -= 360
        all_rays.append(Ray(int(carPos[0]), int(carPos[1]), angle))

    sort_mobs()
    m_angles = []
    m_distances = []
    m_sizes = []
    for m in mobs:
        m_angles.append(m.give_angle())
        m_distances.append(m.give_dist(carPos))
        m_sizes.append(int(1000 / (m.give_dist(carPos) + 1) * 5))
    j = 0
    for r in all_rays:
        display(r, j, world_map, m_angles, m_distances, m_sizes)
        j += 1


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
mobs_textures = normalize_textures(all_mobs)
del all_walls, all_mobs
right = 0
left = 0
world_map = create_map()
window = pygame.display.set_mode((995, 995))
mobs = []
for _ in range(5):
    mobs.append(Mob(0))
while game:
    # ===================================== INITIALIZATION OF VARIABLE AND SCREEN =====================================

    actualTime = time.time()
    window.fill((119, 98, 88))
    pygame.draw.rect(window, (19, 111, 99), (0, 0, 1000, 500))

    # ============================================ RENDERING ALL THE WINDOW ============================================

    render()

    # =================================== WAITING FOR THE END OF THE FRAME (~60 FPS) ===================================

    while time.time() < actualTime + 1 / 60:
        time.sleep(0.00001)

    # ===================================== ADDING CURSOR AND UPDATING THE SCREEN =====================================

    pygame.draw.circle(window, (255, 255, 255), [500, 500], 5, 3)
    pygame.draw.circle(window, (0, 0, 0), [500, 500], 4, 1)
    pygame.display.update()

    # ========================================== KEYS DETECTIONS AND MOVEMENT ==========================================

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        left += 1
        if left >= 30:
            carAngle -= 3
        elif left >= 10:
            carAngle -= 2
        else:
            carAngle -= 1
        if carAngle < 0:
            carAngle += 360
    else:
        left = 0
    if keys[pygame.K_RIGHT]:
        right += 1
        if right >= 30:
            carAngle += 3
        elif right >= 10:
            carAngle += 2
        else:
            carAngle += 1
        if carAngle >= 360:
            carAngle -= 360
    else:
        right = 0

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
