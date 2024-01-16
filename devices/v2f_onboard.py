import time
from communication_infrastructure.user import User


MAX_VALID_REQUEST_TIME = 5

class V2Fonboard(User):
    def __init__(self, _vhc, infrastructure, user_id):
        super().__init__(infrastructure, user_id)
        self.vhc = _vhc
        self.last_request_state = None
        self.last_request_time = None
        self.last_request_gate_id = None
        self.waiting_for_ack = False
        

    def request_state(self, id, state):
        self.waiting_for_ack = True
        self.last_request_gate_id = id
        self.last_request_state = state

        if (self.last_request_time == None) or (time.time() - self.last_request_time > MAX_VALID_REQUEST_TIME):
            statebody = ""
            if state != True:
                statebody = "TRUE"
            else:
                statebody = "FALSE"
            self.infra.send_message(self.user_id, id, f"REQ-LOCK-{statebody}")
            self.last_request_time = time.time()
            

    def crossed(self, id = None):
        if (id is not None):
            self.infra.send_message(self.user_id, id, "REQ-CROS")
        elif (id is None and self.last_request_time is not None):
            self.infra.send_message(self.user_id, self.last_request_gate_id, "REQ-CROS")
        self.last_request_gate_id = None

    def location(self, location, payload):
        self.infra.send_broadcast(self.user_id, f"LOC-{location}-{payload}")

    def onboard_treat_message(self, sender_id, message):
        if message.split("-")[0] == "ACK" and self.last_request_gate_id == sender_id:
            self.waiting_for_ack = False
            self.vhc.set_location(self.vhc.get_location() + 1)
        elif message.split("-")[0] == "LOC":
            self.vhc.add_vehicle(sender_id, message.split("-")[1], message.split("-")[2])


    def run(self):
        while self.active:

            (sender_id, message) = self.get_message()
            if message:
                self.treat_message(sender_id, message)

            if (self.waiting_for_ack):
                self.request_state(self.last_request_gate_id, self.last_request_state)
            else:
                driving = self.vhc.drive()

            if (driving == True):
                self.location(self.vhc.get_location(), self.vhc.get_payload())

            time.sleep(1)  # Prevent busy waiting
            


#Types de messages:
            # REQ: demande de lock ou crossed, à destination des portes
            # ACK: acquittement de la porte
            # LOC: localisation pour les autres véhicules ajouter localisation et payload
            # ERR: erreur 