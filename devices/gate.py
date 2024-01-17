import time

class Gate:
    def __init__(self, id = None, location = None, default_state=False):
        self.id = id
        self.default_state = default_state
        self.state = default_state
        self.location = location

    def set_state(self, state): 
        if state:   
            print(f"Gate {self.id} is opening...")
        else:
            print(f"Gate {self.id} is closing...")

        time.sleep(3)
        self.state = state

        if state:
            print(f"Gate {self.id} is opened")
        else:
            print(f"Gate {self.id} is closed")

        return self.state

    def get_state(self):
        return self.state
    
    def get_default_state(self):
        return self.default_state