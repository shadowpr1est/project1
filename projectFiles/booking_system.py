from projectFiles.booking_system_singleton import BookingSystemSingleton
from projectFiles.place import Place
from projectFiles.place_flyweight import PlaceFlyweight
from projectFiles.choose_place_strategy import ChoosePlaceStrategy


class BookingSystem:
    def __init__(self):
        self.observers = []
        self.system_singleton = BookingSystemSingleton.get_instance()
        self.booking = None
        self.place = Place()

    def set_booking(self, booking):
        self.booking = booking

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

    def make_booking(self, booking_details):
        if self.booking is None:
            raise Exception("You are not defined the strategy")

        if isinstance(self.booking.get_strategy(), ChoosePlaceStrategy):
            place_flyweight = PlaceFlyweight(booking_details.get_socket, booking_details.get_wide)
            return self.booking.book_place(place_flyweight.book_place(booking_details))
        else:
            return self.booking.book_place(booking_details)

    def cancel_booking(self, booking_details):
        return self.place.cancel_booking(booking_details)

    def place_available(self):
        return self.place.availability()

    def places(self):
        return self.place.place_details()

    def my_bookings(self, username):
        return self.place.own_bookings(username)
