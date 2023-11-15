from datetime import datetime

class Environment:
    @staticmethod
    def get_curr_time():
        now = datetime.now()
        return now

    @staticmethod
    def get_curr_hour():
        return Environment.get_curr_time().hour

if __name__ == "__main__":
    pass
