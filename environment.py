from datetime import datetime

# Define the Environment class for handling environment-related operations
class Environment:
    @staticmethod
    def get_curr_time():
        # Get the current date and time
        now = datetime.now()
        return now

    @staticmethod
    def get_curr_hour():
        # Get the current hour from the current time
        return Environment.get_curr_time().hour

if __name__ == "__main__":
    pass
