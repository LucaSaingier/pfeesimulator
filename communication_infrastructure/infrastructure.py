import random
from communication_infrastructure.user import User

class UserList:
    def __init__(self, infrastructure):
        self.infra = infrastructure
        self.users = {}

    def generate_random_user_id(self):
        while True:
            user_id = random.randint(1, 10000)  # Arbitrary upper limit
            if user_id not in self.users:
                return user_id

    def connect_user(self):
        user_id = self.generate_random_user_id()
        self.users[user_id] = User(self.infra, user_id)
        return user_id

    def disconnect_user(self, user_id):
        if user_id in self.users:
            self.users[user_id].stop()
            del self.users[user_id]
            return 0  # Success
        return -1  # User not found

    def get_user(self, user_id):
        return self.users.get(user_id, None)
    

class CommunicationInfrastructure:
    def __init__(self):
        self.user_list = UserList(self)

    def send_message(self, sender_id, receiver_id, message):
        sender = self.user_list.get_user(sender_id)
        receiver = self.user_list.get_user(receiver_id)
        if not sender or not receiver:
            return -1  # User not found
        return receiver.add_message((sender_id, message))
    
    def send_broadcast(self, sender_id, message):
        sender = self.user_list.get_user(sender_id)
        if not sender:
            return -1
        for user_id in self.user_list.users:
            if user_id != sender_id:
                self.send_message(sender_id, user_id, message)
        return 0

    def receive_message(self, user_id):
        user = self.user_list.get_user(user_id)
        if not user:
            return None  # User not found
        return user.get_message()
    
    def add_user(self):
        return self.user_list.connect_user()
    
    def disconnect_user(self, user_id):
        return (self.user_list.disconnect_user(user_id) == 0)
    
    def disconnect_all_users(self):
        for user_id in list(self.user_list.users.keys()):
            self.disconnect_user(user_id)