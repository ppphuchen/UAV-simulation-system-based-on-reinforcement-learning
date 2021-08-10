from Agent.User.PoI import PoI
from Agent.Worker.UAV import UAV
from Function.ToolFunciton import get_normalized_distance
from Function.ToolFunciton import get_uav_angle
from Function.CommFuction import get_uav_state
import numpy as np
class Env(object):
    """
    创造一个Env环境
    """

    def __init__(self, arguments):
        """
        初始化Env环境
        :param torus: (int) 判断Env是否是循环地图，为1表示Env是循环，为0表示Env不是循环的
        :param world_size: (int) Env中的边界大小
        :param uav_max_num: (int) Env中可以容纳UAV的最大数量
        :param timestep_limit: (int) Env中的最大时隙数
        :param n_steo: (int) Env中表示全局目前的时隙数
        :param now_step: (int) Env中当前的时隙数
        :param comm_radius: (float) UAV的通信范围
        :param boundary_radius: (float) PoI的覆盖范围
        :param uav_now_num: (int)  当前UAV的数量
        :param poi_now_num: (int) 当前poi的数量
        """
        self.torus = arguments.torus
        self.world_size = arguments.world_size
        self.uav_max_num = arguments.uav_max_num
        self.poi_max_num = arguments.poi_max_num
        self.n_step = arguments.n_step
        self.now_step = arguments.now_step
        self.uav_now_num = arguments.uav_now_num
        self.poi_now_num = arguments.poi_now_num
        self.agents = [UAV(self) for i in range(self.uav_now_num)]
        [self.agents.append(PoI(self)) for _ in range(self.poi_now_num)]
        #创建一个agents列表，前uav_now_num个元素是当前的UAV，后poi_now_num个元素是当前的PoI
    def env_reset(self, arguments):
        self.torus = arguments.torus
        self.world_size = arguments.world_size
        self.uav_max_num = arguments.uav_max_num
        self.poi_max_num = arguments.poi_max_num
        self.n_step = arguments.n_step
        self.now_step = arguments.now_step
        self.uav_now_num = arguments.uav_now_num
        self.poi_now_num = arguments.poi_now_num
    def agents_reset(self):
        """初始化agents"""
        self.agents = [UAV(self) for i in range(self.uav_now_num)]
        [self.agents.append(PoI(self)) for _ in range(self.poi_now_num)]

    def position_reset(self):
        """重置Env中的UAV，PoI的位置信息"""
        uav_pos = np.zeros((self.uav_now_num, 2))
        poi_pos = np.zeros((100, 2))
        for i in range(10):
              for j in range(10):
                   poi_pos[int(i * 10 + j)][0] = 50 + i * 100
                   poi_pos[int(i * 10 + j)][1] = 50 + j * 100
        #重置poi的位置，100个poi均匀分布在1000*1000的地图里
        self.uav_pos = uav_pos
        self.poi_pos = poi_pos
        #存入重置后的位置

    def step(self, action=None):
        """
        更新经过action选择后的状态和奖励

        :param action: (arry) action的第一列为当前UAV的横坐标，UAV的第二列为当前UAV的纵坐标
        """
        self.now_step += 1
        uav_normal_distance = []
        uav_normal_distance = get_normalized_distance(action[:, 0:2])
        #计算每个UAV的归一化距离
        uav_new_angle = get_uav_angle(action[:, 0:2])
        #计算每个UAV的角度
        next_state = get_uav_state(uav_normal_distance, uav_new_angle, self.agents[0:self.uav_now_num], self.now_step)
        #更新经过这一步后的状态
        return next_state

if __name__ == "__main__":
    new_Env = Env()
