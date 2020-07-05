import numpy as np
import matplotlib.pyplot as plt


coordinates = np.array([[565.0,575.0],[25.0,185.0],[345.0,750.0],[945.0,685.0],[845.0,655.0],
                        [880.0,660.0],[25.0,230.0],[525.0,1000.0],[580.0,1175.0],[650.0,1130.0],
                        [1605.0,620.0],[1220.0,580.0],[1465.0,200.0],[1530.0,5.0],[845.0,680.0],
                        [725.0,370.0],[145.0,665.0],[415.0,635.0],[510.0,875.0],[560.0,365.0]])


Nc_max = 300         # 迭代次数
ants_num = 20       # 蚁群数量
cities_num = len(coordinates)

alpha = 1   # 信息启发式因子
beta = 3    # 期望启发式因子
rho = 0.1   # 信息挥发因子
Q = 1


# 生成邻接矩阵
def get_adjacency_matrix(coordinates):
    cities_num = len(coordinates)
    adjacency_matrix = np.zeros((cities_num, cities_num))
    for i in np.arange(cities_num):
        for j in np.arange(i, cities_num):
            adjacency_matrix[i][j] = adjacency_matrix[j][i] = np.linalg.norm(coordinates[i]-coordinates[j])
        adjacency_matrix[i][i] = np.finfo(float).eps
    return adjacency_matrix


adjacency_matrix = get_adjacency_matrix(coordinates)                # 邻接矩阵
pheromone_table = np.ones((cities_num, cities_num))                 # 信息素矩阵
path_table = np.zeros((ants_num, len(coordinates))).astype(int)     # 路径记录表
eta = 1.0/adjacency_matrix                                          # 启发矩阵
best_path_length = np.zeros(Nc_max)                                 # 最短路程
path_ave_length = np.zeros(Nc_max)                                  # 每次迭代的路程平均值
best_path = np.zeros((Nc_max, cities_num)).astype(int)              # 最佳路径


for Nc in np.arange(Nc_max):
    path_table[:, 0] = np.random.permutation(np.arange(0, cities_num))[:ants_num]
    length = np.zeros(ants_num)
    for i in np.arange(ants_num):
        visiting = path_table[i][0]
        unvisited = list(np.arange(cities_num))
        unvisited.remove(visiting)
        for j in np.arange(1, cities_num):
            probability = np.zeros(len(unvisited))
            for k in np.arange(len(probability)):
                probability[k] = np.power(pheromone_table[visiting][unvisited[k]], alpha) * np.power(eta[visiting][unvisited[k]], alpha)
            cumsum_probability = (probability / sum(probability)).cumsum()
            cumsum_probability -= np.random.rand()

            next_city = 0
            for k in np.arange(len(cumsum_probability)):
                if cumsum_probability[k] > 0:
                    next_city = unvisited[k]
                    break

            path_table[i, j] = next_city
            unvisited.remove(next_city)
            length[i] += adjacency_matrix[visiting][next_city]
            visiting = next_city

        length[i] += adjacency_matrix[visiting][path_table[i][0]]

    path_ave_length[Nc] = length.mean()

    # 获取每次迭代过程中的最小路经长度和具体方案
    if Nc == 0:
        best_path_length[Nc] = length.min()
        best_path[Nc] = path_table[length.argmin()].copy()
    else:
        if length.min() > best_path_length[Nc-1]:
            best_path_length[Nc] = best_path_length[Nc-1]
            best_path[Nc] = best_path[Nc-1].copy()
        else:
            best_path_length[Nc] = length.min()
            best_path[Nc] = path_table[length.argmin()].copy()

    # 更新信息素
    delt_pheromone_table = np.zeros((cities_num, cities_num))
    for i in np.arange(ants_num):
        for j in np.arange(cities_num - 1):
            delt_pheromone_table[path_table[i, j]][path_table[i, j+1]] += Q/adjacency_matrix[path_table[i, j]][path_table[i, j+1]]

            delt_pheromone_table[path_table[i, j + 1]][path_table[i, 0]] += Q/adjacency_matrix[path_table[i, j+1]][path_table[i, 0]]
    pheromone_table = (1-rho) * pheromone_table + delt_pheromone_table


result_path = best_path[-1]

plt.subplot(211)
for each in coordinates:
    plt.scatter(each[0], each[1])

for i in range(cities_num-1):
    m, n = best_path[-1][i], best_path[-1][i+1]
    plt.plot([coordinates[m][0], coordinates[n][0]], [coordinates[m][1],coordinates[n][1]])

plt.subplot(212)
plt.plot(np.arange(len(best_path_length)), best_path_length)
plt.xlabel('times')
plt.ylabel('Path length')

plt.show()