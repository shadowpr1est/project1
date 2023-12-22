class BookingDetails:
    id = None
    full_name = None
    is_socket = None
    is_wide = None
    start_time = None
    end_time = None
    # def __init__(self, id , full_name, is_socket, is_wide, start_time, end_time):
    #     self.id = id
    #     self.full_name = full_name
    #     self.is_socket = is_socket
    #     self.is_wide = is_wide
    #     self.start_time = start_time
    #     self.end_time = end_time

    def __init__(self,*args):
        l = []
        for i in args:
            l.append(i)

        if len(l) == 3: # Random
            self.full_name = l[0]
            self.start_time = l[1]
            self.end_time = l[2]
        elif len(l) == 6: # Requirements
            self.id = l[0]
            self.full_name = l[1]
            self.is_socket = l[2]
            self.is_wide = l[3]
            self.start_time = l[4]
            self.end_time = l[5]
        elif len(l) == 4: # Number
            self.id = l[0]
            self.full_name = l[1]
            self.start_time = l[2]
            self.end_time = l[3]
        else: # Remove
            self.id = l[0]
            self.full_name = l[1]




    def set_full_name(self, name):
        self.full_name = name

    def set_start_time(self, time):
        self.start_time = time

    def set_end_time(self, time):
        self.end_time = time

    def set_id(self,id):
        self.id = id

    def set_is_socket(self,socket):
        self.is_socket = socket

    def set_is_wide(self,wide):
        self.is_wide = wide
    def get_socket(self):
        return self.is_socket

    def get_wide(self):
        return self.is_wide

    def get_id(self):
        return self.id

    def get_full_name(self):
        return self.full_name

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def __str__(self):
        return (f"BookingDetails(id={self.id}, "
                f"full_name='{self.full_name}', "
                f"is_socket={self.is_socket}, "
                f"is_wide={self.is_wide}, "
                f"start_time='{self.start_time}', "
                f"end_time='{self.end_time}')")