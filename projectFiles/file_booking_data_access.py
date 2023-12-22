from datetime import datetime

from projectFiles.booking_data_access import BookingDataAccess
import os


class FileBookingDataAccess(BookingDataAccess):
    def __init__(self):
        self.file_path = "C:/Users/alish/pyProject/untitled1/projectFiles/bookings.txt"

    def read_from_txt(self):
        with open(self.file_path, 'r') as file:
            places = [line.strip() for line in file]
        for i in range(len(places)):
            lst = places[i].split()
            if len(lst) > 4 and datetime.strptime(lst[-2], "%H:%M").time() < datetime.now().time():
                places[i] = f"{places[0]} available {places[2]} {places[3]}"

        return places

    def write_to_txt(self, booking_details):
        pass

    def cancel_to_txt(self, booking_details):
        temp_file_path = "C:/Users/alish/pyProject/untitled1/projectFiles/tempFile.txt"
        id = str(booking_details.get_id())
        removed = False
        with open(temp_file_path, 'w') as temp_file, open(self.file_path, 'r') as file:
            for line in file:
                current_line = line.split()
                if current_line[0] == id and current_line[-1].strip() == booking_details.get_full_name():
                    temp_file.write(f"{id} available {current_line[2]} {current_line[3]}")
                    removed = True
                else:
                    temp_file.write(line.strip())

                temp_file.write("\n")

        os.remove(self.file_path)
        os.rename(temp_file_path, self.file_path)
        if removed:
            return "Deleted successfully ✅"
        else:
            return "Failed to delete ❌"

    def find_from_txt(self, username):
        matching_places = []
        with open(self.file_path, 'r') as file:
            for line in file:
                if username in line:
                    matching_places.append(line.strip())
        return matching_places
