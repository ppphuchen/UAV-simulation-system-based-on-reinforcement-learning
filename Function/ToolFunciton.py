import numpy as np
import scipy.spatial as ssp
import scipy.stats as sst

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