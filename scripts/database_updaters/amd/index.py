import sys
sys.path.append("../../")
from interfaces.amd.index import *

interface = AMDInterface()
interface.auth()

cpu_list = list(interface.get_processors())
for cpu in cpu_list:

    print(cpu)

gpu_list = list(interface.get_gpus())
for gpu in gpu_list:

    print(gpu)