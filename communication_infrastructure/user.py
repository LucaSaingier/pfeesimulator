import threading
import time

MAX_USERS = 20
MAX_MESSAGES = 10
MAX_MESSAGE_SIZE = 256

class User:
    def __init__(self, infrastructure, user_id):
        self.infra = infrastructure
        self.user_id = user_id
        self.messages = []
        self.message_count = 0
        self.lock = threading.Lock()
        self.active = False
        self.thread = threading.Thread(target=self.run)

    def add_message(self, message):
        with self.lock:
            if self.message_count >= MAX_MESSAGES:
                return -1  # Queue is full
            self.messages.append(message[:MAX_MESSAGE_SIZE])
            self.message_count += 1
            return 0  # Success

    def get_message(self):
        with self.lock:
            if self.message_count == 0:
                return None  # No messages
            self.message_count -= 1
            return self.messages.pop(0)
        
    def send_message(self, receiver_id, message):
        return self.infra.send_message(self.user_id, receiver_id, message)
    
    def send_broadcast(self, message):
        return self.infra.send_broadcast(self.user_id, message)

    def run(self):
        while self.active:
            print(f"User {self.user_id} is running...")
            (sender_id, message) = self.get_message()
            if message:
                print(f"User {self.user_id} received message: {message} (from {sender_id})")
            time.sleep(1)

    def stop(self):
        self.active = False
        self.thread.join()