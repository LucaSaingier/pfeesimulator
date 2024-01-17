import time
from communication_infrastructure.user import User


TIMEOUT_COUNTER = 100

class V2Foffboard(User):
    def __init__(self, _gate, infrastructure, user_id):
        self.gate = _gate
        self.counter = 0

        self.last_request_time = None
        self.last_changed_time = None
        self.request_ids = []

        super().__init__(infrastructure, user_id) 
        

    def lock_state(self, state):
        self.counter += 1
        current_state = self.gate.get_state()

        if current_state != state:
            self.gate.set_state(state)
            self.last_changed_time = time.time()

        return True

    def unlock_state(self):
        if self.counter > 0:
            self.counter -= 1
        if self.counter == 0:
            if self.gate.get_state() != self.gate.get_default_state():
                self.gate.set_state(self.gate.get_default_state())


    def counter_reset(self): # In case a crossed signal is lost
        self.counter = 0

    def get_counter(self):
        return self.counter
    
    def offboard_treat_message(self, sender_id, message):
        if message.split("-")[0] == "REQ":
            if message.split("-")[1] == "LOCK":
                self.last_request_time = time.time()
                if (sender_id not in self.request_ids):
                        self.request_ids.append(sender_id)
                else:
                    return

                if message.split("-")[2] == "TRUE":
                    self.lock_state(True)
                elif message.split("-")[2] == "FALSE":
                    self.lock_state(False)

                self.send_broadcast("ACK")
            elif message.split("-")[1] == "CROS":
                self.unlock_state()
                self.request_ids.remove(sender_id)

    def run(self):
        while self.active:
            message = self.get_message()
            if message:
                print(f"V2Foffboard {self.user_id} received message: {message[1]} (from {message[0]}) ")
                self.offboard_treat_message(message[0], message[1])

            if (self.last_request_time and (time.time() - self.last_request_time) > TIMEOUT_COUNTER):
                self.counter_reset()

            if self.counter == 0 and self.gate.get_state() != self.gate.get_default_state():
                self.gate.set_state(self.gate.get_default_state())

            time.sleep(1)  # Prevent busy waiting
    