from usr_interface.main import main as notepad_main
from sms_send.main import main as sms_main

sms_main()
notepad_main()

if __name__ == "__main__":
    print("Running the main script...")