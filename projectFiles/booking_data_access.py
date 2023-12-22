from abc import ABC, abstractmethod


class BookingDataAccess(ABC):
    @abstractmethod
    def read_from_txt(self):
        pass

    @abstractmethod
    def write_to_txt(self, booking_details):
        pass

    @abstractmethod
    def cancel_to_txt(self, booking_details):
        pass

    @abstractmethod
    def find_from_txt(self, username):
        pass
