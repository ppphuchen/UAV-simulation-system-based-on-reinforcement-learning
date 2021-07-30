from Agent.User.PoI import PoI
from Agent.Worker.UAV import UAV
import numpy as np
class Env(object):
    """
    创造一个Env环境
    """

    def __init__(self, arglist):
        """
        初始化Env环境

        :param torus: (int) 判断Env是否是循环地图，为1表示Env是循环，为0表示Env不是循环的
        :param world_size: (int) Env中的边界大小
        :param uav_max_num: (int) Env中可以容纳UAV的最大数量
        :param timestep_limit: (int) Env中的最大时隙数
        :param n_steo: (int) Env中表示全局目前的时隙数
        :param comm_radius: (float) UAV的通信范围
        :param boundary_radius: (float) PoI的覆盖范围
        :param uav_now_num: (int)  当前UAV的数量
        :param poi_now_num: (int) 当前poi的数量
        """
        self.torus = arglist.torus
        self.world_size = arglist.world_size
        self.uav_max_num = arglist.uav_max_num
        self.poi_max_num = arglist.poi_max_num
        self.n_step = arglist.n_step
        self.uav_now_num = arglist.uav_now_num
        self.poi_now_num = arglist.poi_now_num

        self.agents = [UAV(self) for i in range(self.uav_now_num)]
        [self.agents.append(PoI(self)) for _ in range(self.poi_now_num)]
        #创建一个agents列表，前uav_now_num个元素是当前的UAV，后poi_now_num个元素是当前的PoI

    def reset(self):
        """重置Env，UAV，PoI的位置信息"""
        self.agents = [UAV(self) for i in range(self.uav_now_num)]
        [self.agents.append(PoI(self)) for _ in range(self.poi_now_num)]
        uav_pos = np.zeros((self.uav_now_num, 2))
        poi_pos = np.zeros((100, 2))
        for i in range(10):
              for j in range(10):
                   poi_pos[int(i * 10 + j)][0] = 50 + i * 100
                   poi_pos[int(i * 10 + j)][1] = 50 + j * 100

        #重置poi的位置，100个poi均匀分布在1000*1000的地图里

    def step(self, action=None):
        """更新经过action选择后的状态和奖励"""
        pass
if __name__ == "__main__":
    new_Env = Env()