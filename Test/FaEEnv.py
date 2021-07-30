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
    new_PoI.reset(state)
    new_PoI.exploit_init(uav_agents)
    new_PoI.step(uav_agents)
def test_UAV():
    """
    对UAV文档进行测试
    :return:
    """
    args = arglist()
    new_UAV = UAV(args)
    new_UAV.reset(state)
    new_UAV.get_observation(distance_from_poi,timestep=100)

if __name__ == "__main__"
    test_PoI()
    test_UAV()