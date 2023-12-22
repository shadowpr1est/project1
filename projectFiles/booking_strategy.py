from abc import ABC, abstractmethod

class BookingStrategy(ABC):
    @abstractmethod
    def execute_strategy(self, booking_details):
        pass
