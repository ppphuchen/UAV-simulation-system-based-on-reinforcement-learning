from Agent.User.PoI import PoI
from Agent.Worker.UAV import UAV
from Function.ToolFunciton import get_normalized_distance
from Function.ToolFunciton import get_uav_angle
from Function.CommFuction import get_uav_state
import numpy as np
import torch
import scipy.io
import random
import numpy as np
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
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
        :param is_terminal: (bool) 当前游戏是否终止，为1终止，为0不终止
        :param covered_flag:(bool) 表示该PoI目前是否被覆盖，为0表示未被覆盖，为1表示已经被覆盖
        """
        self.covered_flag = arguments.covered_flag
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
        self.dist_matrix = np.zeros((self.uav_now_num, self.poi_now_num))
        # 创建一个距离矩阵，横轴是PoI，纵轴是UAV
        self.uavs_angle = np.zeros(self.uav_now_num)
        # 创建一个弧度矩阵，第i列为第i个UAV的角度
        self.pois_angle = np.zeros(self.poi_now_num)
        # 创建一个弧度矩阵，第i列为第i个poi的角度
        self.uavs_energy = np.zeros(self.uav_now_num)
        # 创建一个能量矩阵，第i列为第i个UAV的能量
        self.pois_covered = np.zeros(self.poi_now_num)
        # 创建一个覆盖标记矩阵，第i列为第i个PoI是否被标记

    def env_reset(self, arguments):
        self.torus = arguments.torus
        self.world_size = arguments.world_size
        self.uav_max_num = arguments.uav_max_num
        self.poi_max_num = arguments.poi_max_num
        self.n_step = arguments.n_step
        self.now_step = arguments.now_step
        self.uav_now_num = arguments.uav_now_num
        self.poi_now_num = arguments.poi_now_num
        self.dist_matrix = np.zeros((self.uav_now_num, self.poi_now_num))
    def agents_reset(self):
        """初始化agents"""
        self.agents = [UAV(self) for i in range(self.uav_now_num)]
        [self.agents.append(PoI(self)) for _ in range(self.poi_now_num)]

    def position_reset(self):
        """重置Env中的UAV，PoI的位置信息"""
        uavs_pos = np.zeros((self.uav_now_num, 2))
        pois_pos = np.zeros((100, 2))
        for i in range(10):
              for j in range(10):
                   pois_pos[int(i * 10 + j)][0] = 50 + i * 100
                   pois_pos[int(i * 10 + j)][1] = 50 + j * 100
        #重置poi的位置，100个poi均匀分布在1000*1000的地图里
        self.uavs_pos = uavs_pos
        self.pois_pos = pois_pos
        #存入重置后的位置
    def update_uav_energy(self):
        """更新UAV的能量"""
        for i in self.uav_now_num:
            new_UAV = UAV(self)
            self.uavs_energy[i] = new_UAV.energy

    def update_dist(self):
        """计算并更新PoI组和UAV组之间的距离"""
        for i in self.uav_now_num:
            new_UAV = UAV(self)
            temp_dist = new_UAV.get_observation(self.uavs_pos[i,:], self.pois_pos ,self.now_step)
            self.dist_matrix[i,:] = temp_dist
    def update_uav_angle(self):
        """计算并更新Env里所有UAV的角度"""
        for i in self.uav_now_num:
            self.uavs_angle[i] = get_uav_angle(self.uavs_pos)

    def update_poi_angle(self):
        """计算并更新Env里所有poi的角度"""
        for i in self.poi_now_num:
            self.pois_angle[i] = get_uav_angle(self.pois_pos)
    def update_poi_cover(self):
        """更新poi的被覆盖情况"""
        for i in self.poi_now_num:
            new_PoI = PoI(self)
            new_PoI.step(self.uavs_pos, self.uavs_energy)
            if self.covered_flag == 1:
                self.pois_covered[i] = 1
            else:
                self.pois_covered[i] = 0

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
        dones = np.zeros(self.uav_now_num)
        dones[0] = self.is_terminal
        info = [{}]
        return next_state, dones, info

    def greedy(self):
        """
        对每个UAV更新角度并且，找到UAV范围内没有被覆盖的PoIs
        :param arguments:
        :return:
        """
        ac = np.zeros((self.uav_now_num, 2)) * 0.5
        for i in self.uav_now_num:
            temp_uav_to_pois = self.dist_matrix[i, :]
            index_dist_argsort = np.argsort(temp_uav_to_pois)
            #排序后根据距离从近到远找到第一个没有被覆盖的PoIs的下标,以及它的角度
            for j in index_dist_argsort:
                if self.pois_covered[index_dist_argsort[j]] == 0:
                    ac[i, 1] = self.pois_angle[index_dist_argsort[j]]
                    break
        actions = torch.FloatTensor([[a[0], a[1]] for a in ac])
        # action的第i行的第一列为0.5， 第二列为UAV距离最近的没有被访问过的PoI的角度

    def render(self, agent_pos0):
        """
        :param agent_pos0: (array) 第一列为UAV的横坐标，第二列为UAV的纵坐标
        :return: 
        """
        temp_x = agent_pos0[:, 0]
        temp_y = agent_pos0[:, 1]
        x0 = temp_x[0: self.uav_now_num]
        y0 = temp_y[0: self.uav_now_num]
        myparams = {
            'axes.labelsize': '20',
            'xtick.labelsize': '18',
            'ytick.labelsize': '18',
            'lines.linewidth': 1.3,
            'legend.fontsize': '18',
            'font.family': 'Times New Roman',
            'figure.figsize': '7, 7',  # 图片尺寸
            'grid.alpha': 0.1

        }
        plt.style.use("seaborn-deep")
        pylab.rcParams.update(myparams)
        '''
        params = {
        'axes.labelsize': '35',
        'xtick.labelsize': '27',
        'ytick.labelsize': '27',
        'lines.linewidth': 2,
        'legend.fontsize': '27',
        'figure.figsize': '12, 9'  # set figure size
        }

        pylab.rcParams.update(params)  # set figure parameter
        # line_styles=['ro-','b^-','gs-','ro--','b^--','gs--']  #set line style
        '''
        plt.plot(x0, y0, marker='^', markersize=6)
        #所有点形成轨迹
        plt.plot(x0[0], y0[0], marker='o', markersize=8)
        #标记初始点
        fig1 = plt.figure(1)
        ax_values = [0, 1000, 0, 1000]
        plt.axis(ax_values)
        plt.axhline()
        plt.axvline()
        # axes = plt.subplot(111)
        # axes = plt.gca()
        # axes.set_yticks([0, 50, 100, 150, 200, 250])
        # axes.set_xticks([0, 50, 100, 150, 200])
        # axes.grid(True)  # add grid

        plt.legend(loc="lower right")  # set legend location
        plt.ylabel('y_coordinate')  # set ystick label
        plt.xlabel('x_coordinate')  # set xstck label

        r = 150 
        center = (x0[0], y0[0])
        x = np.linspace(center[0] - r, center[0] + r, 5000)
        y1 = np.sqrt(r ** 2 - (x - center[0]) ** 2) + center[1]
        y2 = -np.sqrt(r ** 2 - (x - center[0]) ** 2) + center[1]
        plt.plot(x, y1, 'k--')
        plt.plot(x, y2, 'k--')
        x = center[0]
        y = center[1]
        # plt.plot(x, y, color="black", marker="o", markersize=4)
        
        for i in range(10):
            for j in range(10):
                x = 50 + i * 100
                y = 50 + j * 100
                plt.plot(x, y, color="black", marker="o", markersize=6, alpha=0.5)
        #为PoI作图
        plt.savefig('plot.pdf', bbox_inches='tight')
        plt.show()


if __name__ == "__main__":
    new_Env = Env()
