from utils.file_handler import load_json_file, save_json_file

FILE_PATH = "data/booking.json"

class BookingRepository:
    def get_all(self):
        return load_json_file(FILE_PATH)

    def save_all(self, data):
        save_json_file(FILE_PATH, data)