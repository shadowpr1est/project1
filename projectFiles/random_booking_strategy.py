from projectFiles.booking_strategy import BookingStrategy
from projectFiles.place import Place


class RandomBookingStrategy(BookingStrategy):
    def __init__(self):
        self.place = Place()

    def get_place(self):
        return self.place

    def execute_strategy(self, booking_details):
        s = Place.availability(Place())

        for i in s:
            lst = i.split()
            if lst[1] != 'occupied':
                booking_details.set_id(lst[0])
                return self.place.book_place_random(booking_details)
