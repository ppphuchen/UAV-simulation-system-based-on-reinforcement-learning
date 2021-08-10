from Agent import Agent
from Agent.User.PoI import PoI
from Agent.Worker.UAV import UAV
import numpy as np
import random
from Arguments.FaEArgs import arglists

def test_PoI():
    """
    对PoI文档进行测试
    :return:
    """
    args = arglists()
    new_PoI = PoI(args)
    state = np.zeros(2)
    new_PoI.poi_position_reset(state, args)

    uav_agents_pos = np.zeros(100,2)
    #生成一个100行 2列的uav_pos矩阵 第一列为uav的横坐标，第二列为uav的纵坐标
    uav_agents_energy = np.zeros(100)
    #生成一个100个uav的数组，每个uav的能量初始为0
    new_PoI.exploit_init(uav_agents_pos)
    new_PoI.step(uav_agents_pos, uav_agents_energy)
def test_UAV():
    """
    对UAV文档进行测试
    :return:
    """
    args = arglists()
    new_UAV = UAV(args)
    state = np.zeros(1,3)
    #生成一个1行3列的state矩阵，第一列为uav的横坐标，第二列为uav的纵坐标，第三列为uav的角度
    new_UAV.reset(state, args)
    distance_from_poi = np.zeros(1,100)
    #生成一个1行100列的矩阵，每一列表示第i个poi距离该uav的距离
    new_UAV.get_observation(distance_from_poi,timestep=100)
def test_Env():
    """
    对Env文档进行测试
    :return: 
    """
    args = arglists()
    new_Env = UAV(args)
    new_Env.reset(args)
    new_Env.agents_reset()
    new_Env.position_reset()
    action = np.zeros(100,2)
    #第一列为当前uav的横坐标，第二列为当前uav的纵坐标
    new_state = new_Env.step(action)
if __name__ == "__main__":
    test_Env()
    test_PoI()
    test_UAV()
