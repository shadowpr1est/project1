from projectFiles.observer import Observer
class ConcreteObserver(Observer):
    def __init__(self, full_name):
        self.full_name = full_name

    def specific_action(self):
        print(f"{self.full_name} is performing a specific action.")

    def update(self, message):
        print(f"{self.full_name} received message '{message}'")
