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

class Notepad:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(NOTEPAD_TITLE)
        self.root.geometry(NOTEPAD_GEOMETRY)

        self.text = tk.Text(self.root, wrap="word", font=("Consolas", 12))
        self.scrollbar = tk.Scrollbar(self.root, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._setup_menu()

    def _setup_menu(self) -> None:
        menu = tk.Menu(self.root)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label=OPEN_LABEL, command=self.open_file)
        file_menu.add_command(label=SAVE_LABEL, command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label=CLEAR_LABEL, command=self.clear_text)
        file_menu.add_command(label=EXIT_LABEL, command=self.root.quit)
        menu.add_cascade(label=FILE_MENU_LABEL, menu=file_menu)
        self.root.config(menu=menu)

    def open_file(self) -> None:
        filepath = filedialog.askopenfilename(filetypes=[TEXT_FILE_TYPE])
        if filepath:
            with open(filepath, "r", encoding="utf-8") as file:
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, file.read())
            self.root.title(f"{NOTEPAD_TITLE} - {filepath}")

    def save_file(self) -> None:
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[TEXT_FILE_TYPE])
        if filepath:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(self.text.get("1.0", tk.END))
            self.root.title(f"{NOTEPAD_TITLE} - {filepath}")

    def clear_text(self) -> None:
        if messagebox.askyesno(CLEAR_CONFIRM_TITLE, CLEAR_CONFIRM_MESSAGE):
            self.text.delete("1.0", tk.END)

def main() -> None:
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()

if __name__ == "__main__":
    main()
