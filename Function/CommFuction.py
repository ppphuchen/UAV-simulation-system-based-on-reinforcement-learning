import numpy as np
import math
def get_uav_state(matrix_distance, matrix_angle,matrix_agent,now_step):
    """
    更新UAV的状态

    :param matrix_distance:(array) matrix_distance[i]为第i个UAV的归一化距离
    :param matrix_angle:(array) matrix_angle[i]为第i个UAV的角度(弧度制)
    :param matrix_agent:(array) matrix_agent[i]为第i个UAV智能体实例
    :param now_step:(int) 当前的时隙数
    :return: new_state:(array) 更新后UAV智能体组的状态
    """

    new_state = [[], [], [], 0, ]
    new_state[:][0] = matrix_distance
    new_state[:][1] = matrix_angle
    new_state[:][2] = matrix_agent
    new_state[0][3] = now_step
    return  new_state
