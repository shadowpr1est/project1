from booking_details import BookingDetails
from booking import Booking
from booking_system import BookingSystem
from random_booking_strategy import RandomBookingStrategy
from choose_place_strategy import ChoosePlaceStrategy
from concrete_observer import ConcreteObserver


def main():
    bd = BookingDetails(29, "12312312", True, False, "22:00", "23:00")  # only for ChooseStrategy
    bd1 = BookingDetails(25, "123123", "21:00", "23:00")
    booking = Booking(RandomBookingStrategy())

    booking_system = BookingSystem()


    booking_system.make_booking(bd1)
    booking_system.cancel_booking(bd1)

    booking_system.place_available()

    # booking_system.make_booking()


if __name__ == "__main__":
    main()
