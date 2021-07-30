import numpy as np
import scipy.spatial as ssp
import scipy.stats as sst
import math
def get_euclid_distances(matrix):
    """
    :param matrix: (array)第一列为UAV智能体组以及PoI的横坐标，第二列为UAV智能体以及PoI的纵坐标
    :return: temp_matrix: (array) temp_matrix[i]表示该PoI距离第i个UAV的距离
    """
    temp_matrix = []
    rows = matrix.shape(0)
    temp_poi_x = matrix[rows][0]
    temp_poi_y = matrix[rows][1]
    for i in (rows-1):
        temp_matrix[i] = ((matrix[i][0] - temp_poi_x)**2 + (matrix[i][1] - temp_poi_y)**2)**0.5
    return temp_matrix

def get_normalized_distance(matrix):
    """
    :param matrix: (array) 第一列为UAV智能体的横坐标，第二列为UAV智能体的纵坐标
    :return: temp_matrix: (array) temp_matrix[i]表示第i个UAV的归一化距离
    """
    temp_euler_distance = []
    temp_matrix = []
    temp_max = 0.0
    rows = matrix.shape(0)
    for i in range(rows):
        temp_euler_distance[i] = (matrix[i][0]**2 + matrix[i][1]**2)**0.5
        if temp_euler_distance[i] > temp_max:
            temp_max = temp_euler_distance[i]
    for i in range(rows):
        temp_matrix[i] = temp_euler_distance[i]/temp_max

    return temp_matrix

def get_uav_angle(matrix):
    """
    :param matrix: (array) 第一列为UAV智能体的横坐标，第二列为UAV智能体的纵坐标
    :return: temp_matrix: (array) temp_matrix[i]表示第i个UAV的角度(弧度制)
    """
    rows = matrix.shape(0)
    temp_matrix = []
    for i in range(rows):
        temp_matrix[i] = math.atan2(matrix[i][1], matrix[i][0])
    return temp_matrix

