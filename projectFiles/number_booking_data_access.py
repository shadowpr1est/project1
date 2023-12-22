import os
from datetime import datetime

from projectFiles.file_booking_data_access import FileBookingDataAccess
class NumberBookingDataAccess(FileBookingDataAccess):
    def write_to_txt(self, booking_details):
        temp_file_path = "C:/Users/alish/pyProject/untitled1/projectFiles/tempFile.txt"
        id = str(booking_details.get_id())
        start_time = datetime.strptime(booking_details.get_start_time(), '%H:%M').time()
        end_time = datetime.strptime(booking_details.get_end_time(), '%H:%M').time()
        written = False
        with open(temp_file_path, 'w') as temp_file, open(self.file_path, 'r') as file:
            for line in file:
                current_line = line.split()
                if current_line[0] == id and current_line[1] == "available":
                    temp_file.write(f"{id} occupied {current_line[2]} {current_line[3]} {start_time.strftime('%H:%M')} "
                                    f"{end_time.strftime('%H:%M')} {booking_details.get_full_name()}")
                    written = True
                else:
                    temp_file.write(line.strip())
                temp_file.write("\n")
        os.remove(self.file_path)
        os.rename(temp_file_path, self.file_path)
        if written:
            return "Booking successful ✅"
        else:
            return "This place is occupied by someone 🚫"