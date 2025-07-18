
import tkinter as tk
from usr_interface.notepad import Notepad

def main() -> None:
    root = tk.Tk()
    _ = Notepad(root)
    root.mainloop()

if __name__ == "__main__":
    main()