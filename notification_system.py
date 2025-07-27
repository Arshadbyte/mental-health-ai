
import datetime
import time
import threading

def set_reminder(message, remind_time):
    """
    Sets a reminder to display a message at a specific time.
    Args:
        message (str): The reminder message.
        remind_time (datetime.datetime): The datetime object when the reminder should trigger.
    """
    now = datetime.datetime.now()
    delay = (remind_time - now).total_seconds()

    if delay <= 0:
        print("Reminder time is in the past or present. Displaying immediately.")
        print(f"REMINDER: {message}")
        return

    print(f"Setting reminder for {remind_time} (in {delay:.0f} seconds).")
    timer = threading.Timer(delay, display_reminder, args=[message])
    timer.start()

def display_reminder(message):
    """
    Function to be called when the reminder triggers.
    Args:
        message (str): The reminder message.
    """
    print(f"\n!!! REMINDER: {message} !!!\n")

if __name__ == "__main__":
    # Example Usage:
    print("Testing reminder system...")
    # Set a reminder for 10 seconds from now
    future_time = datetime.datetime.now() + datetime.timedelta(seconds=10)
    set_reminder("Take a deep breath!", future_time)

    # Set a reminder for 5 seconds from now
    future_time_2 = datetime.datetime.now() + datetime.timedelta(seconds=5)
    set_reminder("Drink some water!", future_time_2)

    print("Main program continues...")
    # Keep the main thread alive for a bit to allow reminders to trigger
    time.sleep(15)
    print("Main program finished.")


