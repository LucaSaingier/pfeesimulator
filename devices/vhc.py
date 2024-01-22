LIMIT_DISTANCE = 15

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

    def request_state(self, id, state):
        return self.onboard_module.lock_state(id, state)
    
    def crossed_gate(self, id=None):
        return self.onboard_module.crossed(id)
    
    def add_vehicle(self, id, location, payload):
        if (id, location, payload) not in self.vhc_list:
            self.vhc_list.append((id, location, payload))
        else:
            self.vhc_list.remove((id, location, payload))
            self.vhc_list.append((id, location, payload))
    
    def drive(self):
        for vhc in self.vhc_list:
            if vhc[1] + vhc[2] == self.location + 1: # Potential Collision
                print(f"V - VHC {self.id} stopped because of VHC {vhc[0]} in front. [Location: {self.location}]")
                return False 
            
        for gate in self.gatelist:
            if gate[1] == self.location + 1: # Gate is in front
                self.request_state(gate[0], gate[2])
                print(f"V - VHC {self.id} stopped because of Gate {gate[0]} in front. [Location: {self.location}]\n   Waiting for ACK...")
                return False
            
            if gate[1] == self.location - self.payload - 1: # Gate is behind
                self.crossed_gate(gate[0])
                print(f"V - VHC {self.id} crossed Gate {gate[0]}. [Location: {self.location}]\n   Sended CROS...")
            
            if (self.location >= LIMIT_DISTANCE):
                print(f"V - VHC {self.id} exited the simulation.")
                self.onboard_module.stop()
                return False
        
        self.location += 1
        print(f"V - VHC {self.id} is driving... [Location: {self.location}]")
        
        return True