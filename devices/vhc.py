# gatelist = [(door_id, door_location, opengate), (door_id, door_location, opengate), ...]
#gatelist = [(1, 2, True), (5, 4, True)]
# vhc_list = [(vhc_id, location ,payload), (vhc_id, location, payload), ...]
#vhc_list = []

class VHC:
    def __init__(self, id = None,location = None, payload = 5, gatelist = [], vhc_list = []):
        self.onboard_module = None
        self.location = location
        self.payload = payload
        self.id = id

        # Simu
        self.gatelist = gatelist
        self.vhc_list = vhc_list


    def set_onboard_module(self, onboard_module):
        self.onboard_module = onboard_module

    def get_location(self):
        return self.location
    
    def get_payload(self):
        return self.payload
    
    def set_location(self, location):
        self.location = location

    def notify_state(self, id, state):
        return self.onboard_module.request_state(id, state)
    
    def crossed_gate(self, id=None):
        return self.onboard_module.crossed(id)
    
    def add_vehicle(self, id, location, payload):
        self.vhc_list.append((id, location, payload))
    

    # Simu
    def drive(self):
        print(f"VHC {self.id} is driving... Location: {self.location}")

        for vhc in self.vhc_list:
            if vhc[1] + vhc[2] == self.location + 1: # Potential Collision
                return False 
            
        for gate in self.gatelist:
            if gate[1] == self.location + 1: # Gate is in front
                self.notify_state(gate[0], gate[2])
                return False
            
            if gate[1] == self.location - 1: # Gate is behind
                self.crossed_gate(gate[0])
        
        self.location += 1
        
        return True