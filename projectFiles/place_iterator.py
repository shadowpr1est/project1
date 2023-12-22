class PlaceIterator:
    def __init__(self, places):
        self.places = places
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.places):
            result = self.places[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

    def iterate_available_places(self):
        lst = []
        for temp in self.places:
            if "available" in temp:
                lst.append(temp)
        return lst

    def iterate_places(self):
        return self.places
