

class PlaceFlyweightFactory:
    def __init__(self):
        self.map = {}

    def get_place_flyweight(self, booking_details, make_booking):
        is_socket = str(booking_details.get_socket())
        is_wide = str(booking_details.get_wide())
        key = is_socket + is_wide

        if make_booking and key not in self.map:
            from projectFiles.place_flyweight import PlaceFlyweight
            self.map[key] = PlaceFlyweight(is_socket,is_wide)

        return self.map.get(key, None)
