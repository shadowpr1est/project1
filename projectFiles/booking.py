from projectFiles.place import Place


class Booking:
    def __init__(self, strategy):
        self.strategy = strategy
        self.place = Place()

    def book_place(self, booking_details):
        return self.strategy.execute_strategy(booking_details)

    def get_strategy(self):
        return self.strategy

    def cancel_booking(self, booking_details):
        return self.place.cancel_booking(booking_details)
