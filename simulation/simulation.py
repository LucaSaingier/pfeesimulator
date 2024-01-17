import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from communication_infrastructure.infrastructure import CommunicationInfrastructure
from communication_infrastructure.infrastructure import UserList
from communication_infrastructure.user import User
from devices.v2f_offboard import V2Foffboard
from devices.v2f_onboard import V2Fonboard
from devices.vhc import VHC
from devices.gate import Gate

# 1 Gate, 1 VHC
def simulation1():
    infra = CommunicationInfrastructure()
    
    gate = Gate(1, 5)
    vhc = VHC(2, 0, 5, [(1, 5, False)])
    v2f_offboard = V2Foffboard(gate, infra, 1) ## ID 1
    v2f_onboard = V2Fonboard(vhc, infra, 2) ## ID 2

    vhc.set_onboard_module(v2f_onboard)

    infra.add_defined_user(1, v2f_offboard)
    infra.add_defined_user(2, v2f_onboard)





def main():
    simulation1()
    print("Main thread started...")


if __name__ == "__main__":
    main()