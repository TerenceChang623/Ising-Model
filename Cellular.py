import numpy as np
import matplotlib.pyplot as plt
import random
import time
import gc

# cells表示整个场所在某个时刻的状态, shape为(length, Width), cells为中为0的点表示空缺的点,为1的点表示被人占据的点

people_num = 250                # 游客数量
length = 30                     # 场所宽度
width = 30                      # 场所长度
exits = [[0, 0]]                # 出口坐标


class EachPerson(object):
    def __init__(self, length, width):
        self.coordinate = np.array((np.random.randint(width), np.random.randint(length))).astype(int)
        # self.speed = 233

    def move(self, direction):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if direction == 4 + 3 * i + j:
                    self.coordinate[0] = self.coordinate[0] + i
                    self.coordinate[1] = self.coordinate[1] + j


class CellularSpace(object):
    def __init__(self, center_coordinate, exits, cells):
        self.center_coordinate = center_coordinate
        self.cells_coordinates = np.zeros((9, 2)).astype(int)
        self.possibilities = np.ones(9)
        self.exits = exits
        self.cells = cells
        self.get_cells_coordinates()
        self.get_possibilities()

    def get_cells_coordinates(self):
        for i in range(-1, 2):
            for j in range(-1, 2):
                self.cells_coordinates[4 + 3 * i + j][0] = self.center_coordinate[0] + i
                self.cells_coordinates[4 + 3 * i + j][1] = self.center_coordinate[1] + j

    def get_possibilities(self):
        min_distances = dict()
        for i in range(9):
            # 9个cell分别距最近出口的距离,key为cell索引值, value为最小距离值
            distances_to_exits = np.zeros(len(self.exits))
            for j in range(len(self.exits)):
                distance = np.linalg.norm(self.exits[j] - self.cells_coordinates[i])
                distances_to_exits[j] = distance
            min_distances[i] = distances_to_exits.min()

            # 如果超出范围,possibility置0
            if (self.cells_coordinates[i][0] >= 0) and (self.cells_coordinates[i][0] < len(cells)) \
                    and (self.cells_coordinates[i][1] >= 0) and (self.cells_coordinates[i][1] < len(cells[0])):
                # 如果cell已被占据,possibility置0,由于对象可以保持不动,中心点不置0
                if (self.cells[self.cells_coordinates[i][0], self.cells_coordinates[i][1]] != 0) and i != 4:
                    self.possibilities[i] = 0
            else:
                self.possibilities[i] = 0

        # 删除不可能的cell
        for i in range(9):
            if self.possibilities[i] == 0:
                min_distances.pop(i)

        # 从可能的cell中再次寻找最小值
        min_distance = min(min_distances.values())

        # 让距离值最小的cell的possibility为0.8,非最小的但可能的cell为0.2
        for key in min_distances:
            if min_distances[key] == min_distance:
                self.possibilities[key] = 0.9
            else:
                self.possibilities[key] = 0.1

        # 概率归一化
        possibilities_sum = self.possibilities.sum()
        self.possibilities /= possibilities_sum


# 随机生成一定的人数,保证初始坐标不重复
def create_people(num):
    people = list()
    while len(people) < num:
        person = EachPerson(length, width)
        if cells[person.coordinate[0], person.coordinate[1]] == 0:
            cells[person.coordinate[0], person.coordinate[1]] = 1
            people.append(person)
    return people


# 获取运动方向
def get_direction(possibilities):
    judgement = possibilities.cumsum()-np.random.random()
    direction = 0
    for i in range(9):
        if judgement[i] > 0:
            direction = i
            break
    return direction


# 建立初始状态
cells = np.zeros((width, length)).astype(int)

# cells[45] = -np.ones(100)

random_people = create_people(people_num)
plt.ion()
count = 0
while True:
    plt.title('time:' + str(count) + '\n' + 'The number of people:'+str(len(random_people)))

    for exit in exits:
        cells[exit[0], exit[1]] = 0
    
    plt.imshow(cells)
    plt.pause(0.1)
    plt.clf()
    # plt.show()
    

    # 全部人疏散时,停止计数
    if len(random_people) == 0:
        break

    # 打乱操作每个人的顺序
    random.shuffle(random_people)
    for each in random_people:

        cellular_space = CellularSpace(each.coordinate, exits, cells)
        direction = get_direction(cellular_space.possibilities)

        # 原来占据的cell清零
        cells[each.coordinate[0], each.coordinate[1]] = 0

        # 移动至下一个cell
        each.move(direction)

        # 移动后占据的cell置1
        cells[each.coordinate[0], each.coordinate[1]] = 1

        # cells[each.coordinate[0], each.coordinate[1]] = 0

        # 如果有人到了出口处, 逃离成功并删除此对象, 出口处置0
        if list((each.coordinate[0], each.coordinate[1])) in exits:

            random_people.remove(each)

        # 释放对象内存, 内存实在受不了了QAQ
        del cellular_space
        gc.collect()

    count += 1
    # time.sleep(0.5)
print(count)