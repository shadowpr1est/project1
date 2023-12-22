from projectFiles.place import Place
class ChoosePlaceStrategy:
    def __init__(self):
        self.place = Place()

    def get_place(self):
        return self.place

    def execute_strategy(self, booking_details):
        return self.place.book_place(booking_details)

