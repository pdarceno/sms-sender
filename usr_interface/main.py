NOTEPAD_TITLE: str = "Notepad"
NOTEPAD_GEOMETRY: str = "800x600"
FILE_MENU_LABEL: str = "File"
OPEN_LABEL: str = "Open"
SAVE_LABEL: str = "Save"
CLEAR_LABEL: str = "Clear"
EXIT_LABEL: str = "Exit"
CLEAR_CONFIRM_TITLE: str = "Clear"
CLEAR_CONFIRM_MESSAGE: str = "Clear all text?"
TEXT_FILE_TYPE: tuple[str, str] = ("Text files", "*.txt")

import tkinter as tk
from tkinter import filedialog, messagebox
from sms_send.main import SMSSender
import pandas as pd
from db_read.main import populate_excel
from constants import SMSGLOBAL_API_KEY, SMSGLOBAL_API_SECRET, SMSGLOBAL_API_URL

# Import Notepad from notepad.py
from usr_interface.notepad import Notepad

def main() -> None:
    root = tk.Tk()
    _ = Notepad(root)
    root.mainloop()

if __name__ == "__main__":
    main()
def main() -> None:
    root = tk.Tk()
    _ = Notepad(root)
    root.mainloop()

if __name__ == "__main__":
    main()
