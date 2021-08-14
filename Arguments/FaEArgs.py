import argparse
import numpy as np
def arglists():
    parser = argparse.ArgumentParser()
    #UAV的具有默认值的参数
    parser.add_argument("--energy", type=int, default=3, help="UAV默认初始能量", )
    parser.add_argument("--comm_radius", type=float , default=10.0, help="UAV默认通信范围",)
    parser.add_argument("--uav_now_num", type=int, default=10, help="UAV默认当前数量", )
    parser.add_argument("--is_wall", type=bool, default=0, help="默认UAV没有撞墙，正常飞行", )
    parser.add_argument("--delta_energy", type=int, default=0, help="默认UAV初始消耗的能量为0", )
    parser.add_argument("--max_line_v", type=float, default=50, help="UAV的最大线速度为50cm/s", )
    parser.add_argument("--max_angle_v", type=float, default=2*np.pi, help="UAV的最大角速度为2π", )
    parser.add_argument("--init_line_v", type=float, default=0, help="UAV的初始线速度")
    parser.add_argument("--init_angle_v", type=float, default=0, help="UAV的初始角速度")
    #UAVEnv的具有的默认参数值
    parser.add_argument("--world_size", type=int, default=1000, help="默认的边界范围", )
    parser.add_argument("--max_uav_num", type=int, default=100, help="默认的Env中UAV的最大数量")
    parser.add_argument("--max_poi_num", type=int, default=100, help="默认的Env中PoI的最大数量")
    parser.add_argument("--n_step", type=int, default=1024, help="默认UAV初始可以使用的时隙数", )
    parser.add_argument("--now_step", type=int, default=0, help="默认的当前的时隙数")
    parser.add_argument("--is_terminal", tpye=bool, default=0, help="默认值为0表示游戏正在继续")
    #PoI的具有默认值的参数
    parser.add_argument("--poi_exploited_flag", type=bool, default=0, help="标记PoI是否被覆盖，默认值为0未被覆盖", )
    parser.add_argument("--boundary_radius", type=float, default=20, help="PoI的边界范围", )
    parser.add_argument("--poi_now_num", type=int, default=10, help="PoI默认当前数量", )
    parser.add_argument("--covered_time", type=int, default=0, help="PoI的被覆盖时间，默认为0", )
    parser.add_argument("--can_comm", type=bool, default=0, help="标记PoI此时能否正常通信", )
    return parser.parse_args()
