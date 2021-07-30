from Agent.Agent import Agent
import numpy as np
from Function import ToolFunciton
from Arguments.FaEArgs import arglists

class PoI(Agent):
    """
    创建PoI
    """

    def __init__(self, arguments):
        """
        初始化PoI

        :param boundary_radius: (int) PoI的边界范围
        :param world_size: (int) 地图的边界范围
        :param poi_exploited_flag: (bool) 用于标记PoI是否被探索，值为0表示该PoI未被探索，值为1表示该PoI已被探索
        :param covered_time: (int) PoI的被覆盖时间
        :param can_comm: (bool) 表示PoI目前能否正常通信，为0表示不能，为1表示能
        """
        super(PoI, self).__init__()
        # 继承Agent的属性
        self.boundary_radius = arguments.boundary_radius
        self.world_size = arguments.world_size
        self.poi_exploited_flag = arguments.poi_exploited_flag
        # 初始PoI未被覆盖,赋值为0
        self.covered_time = arguments.covered_time
        self.exploiters = []
        # 存储覆盖该PoI的实例,初始为空
        self.temp_exploiters = []
        self.can_comm = arguments.can_comm
        # 暂存覆盖该PoI的实例,初始为空
    def reset(self, state, arguments):
        """
        重置PoI的位置，被覆盖时间，被覆盖的UAV列表

        :param state: (array) PoI的位置信息，state[0]为PoI的x轴坐标，state[1]为PoI的y轴坐标
        """
        self.state.poi_pos = state[0:2]
        #该PoI的位置
        self.covered_time = arguments.poi_exploited_flag
        self.poi_exploited_flag = arguments.poi
        self.can_comm = arguments.can_comm
        self.exploiters = []
        self.temp_exploiters = []
    def exploit_init(self, uav_agents):
        """
        计算所有UAV距离该PoI的距离，

        :param uav_agents: (array)UAV智能体的实例组
        :param uav_agents.pos: (array)UAV组的位置信息，其中uav_agents.pos[:, 0]表示UAV智能体组的所有横坐标，uav_agents.pos[:, 1]表示UAV智能体组的所有纵坐标
        """
        temp_dist_matrix = np.vstack([uav_agents.pos[:, 0:2], self.state.poi_pos])
        # 构成一个n行2列的矩阵，第一列为UAV智能体组以及PoI的横坐标，第二列为UAV智能体以及PoI的纵坐标

        distances = ToolFunciton.get_euclid_distances(temp_dist_matrix)
        #计算PoI与每个UAV智能体组中每个UAV的欧式距离，distance[i]为PoI距离第i个UAV的欧式距离 (float)
        dist_to_uavs = distances

        self.temp_exploiters = list(np.where(dist_to_uavs < self.boundary_radius)[0])
        # 更新poi范围内的所有UAV实体

        if len(self.temp_exploiters) > 0:
            self.poi_exploited_flag = 1
        #PoI范围内存在UAV，就把被探索标志设为1

    def step(self,uav_agents):
        """
        PoI进行一次action

        :param uav_agents:
        :return:
        """
        self.exploiters = []
        temp_dist_matrix = np.vstack([uav_agents.pos[:, 0:2], self.state.poi_pos])
        # 构成一个n行2列的矩阵，第一列为UAV智能体组以及PoI的横坐标，第二列为UAV智能体以及PoI的纵坐标

        distances = ToolFunciton.get_euclid_distances(temp_dist_matrix)
        # 计算PoI与每个UAV智能体组中每个UAV的欧式距离，distance[i]为PoI距离第i个UAV的欧式距离 (float)

        dist_to_uavs = distances
        self.temp_exploiters = list(np.where(dist_to_uavs < self.boundary_radius)[0])
        # 更新poi范围内的所有UAV实体

        uav_have_energy = False
        #用来标记PoI范围内是否有具有电量的UAV

        if len(self.temp_exploiters) > 0:
            for i in self.temp_exploiters:
                if uav_agents.energy[i] > 0:
                    uav_have_energy = True
        #寻找PoI范围内具有电量的UAV

            if self.poi_exploited_flag == 1:
                self.poi_exploited_flag = 0
                self.exploiters = self.temp_exploiters
        #存储探索该PoI的实例
        if uav_have_energy:
            self.can_comm = 1
        else:
            self.can_comm = 0
        #判断该PoI此时能否通信
if __name__ == "__main__":
   args = arglists()
   new_PoI = PoI(args)
   print(new_PoI.boundary_radius)

