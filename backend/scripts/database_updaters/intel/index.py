import sys
sys.path.append("../../")
from interfaces.intel.index import *

interface = IntelInterface()
interface.auth()

cpu_list = list(interface.get_processors())
for cpu in cpu_list:

    insert = table.insert_one(cpu).inserted_id
    print('inserted ' + str(insert))