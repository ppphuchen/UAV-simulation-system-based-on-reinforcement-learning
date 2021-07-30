import Agent
import numpy as np
import random
from Arguments.FaEArgs import arglists

class UAV(Agent):
    """
    创建UAV
    """

    def __init__(self, arguments):
        """
        初始化UAV

        :param comm_radius: (float) UAV的通信范围
        :param boundary_radius: (float) PoI的覆盖范围
        :param energy: (int) UAV目前的能量
    #    :param uav_obs_pos: (array) UAV的当前位置，array[0]表示横坐标，array[1]表示纵坐标
    #    :param uav_over: (array) array[i]=0表示第i个UAV没有越过边界,array[i]=1表示第i个UAV越过了边界
        :param uav_now_num: (int)  当前UAV的数量
        :param poi_now_num: (int) 当前poi的数量
        :param world_size: (int) 此时Env的边界范围
        :param is_wall: (int) 判断UAV飞行途中是否撞墙,为0表示没有撞墙,为1表示撞墙
        :param delta_energy: (int) UAV消耗的能量
        :param n_step: (int) Env中目前全局的时隙数
        :param max_line_v: (int)  UAV飞行的最大线速度50
        :param max_angle_v: (int) UAV飞行的最大角速度2π
        """
        super(UAV, self).__init__()
        # 继承父类的属性
        self.energy = arguments.energy
        # 3
        self.comm_radius = arguments.comm_radius
        self.boundary_radius= arguments.boundary_radius
        self.energy = arguments.energy
        self.uav_now_num = arguments.uav_now_num
        self.poi_now_num = arguments.poi_now_num
        self.world_size = arguments.world_size
        self.is_wall = arguments.is_wall
        self.delta_energy = arguments.delta_energy
        # 0
        self.n_step = arguments.n_step
        self.max_line_v = arguments.max_line_v
        # 50 cm/s
        self.max_angle_v = arguments.max_angle_v
        # 2π
        

    def reset(self, state, arguments):
        """
        利用随机化算法重新设置UAV的位置

        :param state: (array)state[0]表示UAV的横坐标，state[1]表示UAV的纵坐标，state[2]表示UAV目前的方向
        :param init_line_v: (float) UAV的初始线速度为0
        :param init_angle_v: (float) UAV的初始角速度为0
        """
        self.state.uav_pos = state[0:2]
        self.state.uav_pos[0] = random.randint(0, 100)
        self.state.uav_pos[1] = random.randint(0, 100)
        # 将uav的横纵坐标在0~100里随机选取
        self.state.uav_orientation = state[2]
        self.state.line_v = arguments.init_line_v
        self.state.angle_v = arguments.init_angle_v
        # uav飞行线速度和角速度设置为0
        self.energy = arguments.energy
        self.delta_energy = arguments.delta_energy
        # 重置UAV的能量和消耗的能量

    def get_observation(self, distance_from_poi, timestep):
        """
        计算与环境中所有PoI的距离，并判断此时UAV是否撞墙

        :param distance_from_poi: (array) distance_from_poi[i]表示第i个poi与UAV的距离
        :param timestep: (int) UAV已经使用的时间步数
        """

        dist_to_pois = distance_from_poi[-self.n_evaders:]
        # 所有poi距离该UAV的距离

        local_obs = np.zeros(2)
        if self.torus is False:
            if np.any(self.state.uav_pos <= 1) or np.any(self.state.uav_pos >= 999):
                self.wall = 1
            else:
                self.wall = 0
            local_obs[0] = self.wall
        local_obs[1] = float(timestep) / self.n_step
        # local_obs[0]表示UAV是否撞墙，local_obs[1]存UAV已使用的时间步数的归一化值

        for i in range(self.poi_now_num):
            normal_dist_to_pois = dist_to_pois[i] / self.obs_radius
        # 计算每个Poi距离UAV的归一化距离

if __name__ == "__main__":
   args = arglists()
   new_UAV = UAV(args)
   print(new_UAV.energy)




















