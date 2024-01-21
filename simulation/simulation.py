import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from communication_infrastructure.infrastructure import CommunicationInfrastructure
from devices.v2f_offboard import V2Foffboard
from devices.v2f_onboard import V2Fonboard
from devices.vhc import VHC
from devices.gate import Gate

# 1 Gate, 1 VHC
def simulation1():
    infra = CommunicationInfrastructure()

    gateId = 1
    gateLocation = 5

    vhcId = 2

    gateList = [(gateId, gateLocation, False)] ## (id, location, defaultState)

    gate = Gate(id=gateId, location=gateLocation)
    vhc = VHC(id=vhcId, location=0, payload=3, gatelist=gateList)

    v2f_offboard = V2Foffboard(gate, infra, gateId) 
    v2f_onboard = V2Fonboard(vhc, infra, vhcId) 

    infra.add_defined_user(gateId, v2f_offboard)
    infra.add_defined_user(vhcId, v2f_onboard)
    
    v2f_offboard.start()
    v2f_onboard.start()

## 2 Gates, 2 VHCs
def simulation2():
    infra = CommunicationInfrastructure()

    gate1 = Gate(1, 10)
    gate2 = Gate(2, 15)

    vehicle1 = VHC(3, 6, 3, [(1, 10, False), (2, 15, False)])
    v2f_onboard1 = V2Fonboard(vehicle1, infra, 3) ## ID 3
    vehicle1.set_onboard_module(v2f_onboard1)

    vehicle2 = VHC(4, 0, 3, [(1, 10, False), (2, 15, False)])
    v2f_onboard2 = V2Fonboard(vehicle2, infra, 4) ## ID 4
    vehicle2.set_onboard_module(v2f_onboard2)

    v2f_offboard1 = V2Foffboard(gate1, infra, 1) ## ID 1
    v2f_offboard2 = V2Foffboard(gate2, infra, 2) ## ID 2

    infra.add_defined_user(1, v2f_offboard1)
    infra.add_defined_user(2, v2f_offboard2)
    infra.add_defined_user(3, v2f_onboard1)
    infra.add_defined_user(4, v2f_onboard2)

    v2f_onboard1.start()
    v2f_onboard2.start()
    v2f_offboard1.start()
    v2f_offboard2.start()

def main():
    simulation1()


if __name__ == "__main__":
    main()