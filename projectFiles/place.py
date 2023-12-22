from projectFiles.place_iterator import PlaceIterator
from projectFiles.booking_data_access import BookingDataAccess
from projectFiles.file_booking_data_access import FileBookingDataAccess
from projectFiles.requirements_booking_data_access import RequirementsBookingDataAccess
from projectFiles.number_booking_data_access import NumberBookingDataAccess


class Place:
    def __init__(self):
        self.booking_data_access = FileBookingDataAccess()
        self.number = NumberBookingDataAccess()
        self.requirements = RequirementsBookingDataAccess()

    def place_details(self):
        place_iterator = PlaceIterator(self.booking_data_access.read_from_txt())
        return place_iterator.iterate_places()

    def availability(self):
        place_iterator = PlaceIterator(self.booking_data_access.read_from_txt())
        if not place_iterator.iterate_available_places():
            return "There is no available places"
        return place_iterator.iterate_available_places()

    def book_place_random(self, booking_details):
        return self.number.write_to_txt(booking_details)

    def book_place(self, booking_details):
        return self.requirements.write_to_txt(booking_details)

    def cancel_booking(self, booking_details):
        return self.booking_data_access.cancel_to_txt(booking_details)

    def own_bookings(self, username):
        place_iterator = PlaceIterator(self.booking_data_access.find_from_txt(username))
        if not place_iterator.places:
            return "You have no bookings"
        return place_iterator.iterate_places()
