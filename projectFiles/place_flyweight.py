from projectFiles.place_flyweight_factory import PlaceFlyweightFactory
from projectFiles.booking_details import BookingDetails


class PlaceFlyweight:
    def __init__(self, is_socket, is_wide):
        self.is_socket = is_socket
        self.is_wide = is_wide
        self.place_flyweight_factory = PlaceFlyweightFactory()

    def book_place(self, booking_details):
        econom = self.place_flyweight_factory.get_place_flyweight(booking_details, True)
        return BookingDetails(
            booking_details.get_id(),
            booking_details.get_full_name(),
            econom.is_socket,
            econom.is_wide,
            booking_details.get_start_time(),
            booking_details.get_end_time()
        )

    def cancel_booking(self, booking_details):
        econom = self.place_flyweight_factory.get_place_flyweight(booking_details, False)
        return BookingDetails(
            booking_details.get_id(),
            booking_details.get_full_name(),
            econom.is_socket,
            econom.is_wide,
            booking_details.get_start_time(),
            booking_details.get_end_time()
        )
