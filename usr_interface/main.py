import tkinter as tk
from tkinter import filedialog, messagebox

class Notepad:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Notepad")
        self.root.geometry("800x600")

        self.text = tk.Text(self.root, wrap="word", font=("Consolas", 12))
        self.scrollbar = tk.Scrollbar(self.root, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._setup_menu()

    def _setup_menu(self) -> None:
        menu = tk.Menu(self.root)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Clear", command=self.clear_text)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu)

    def open_file(self) -> None:
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "r", encoding="utf-8") as file:
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, file.read())
            self.root.title(f"Notepad - {filepath}")

    def save_file(self) -> None:
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(self.text.get("1.0", tk.END))
            self.root.title(f"Notepad - {filepath}")

    def clear_text(self) -> None:
        if messagebox.askyesno("Clear", "Clear all text?"):
            self.text.delete("1.0", tk.END)

def main() -> None:
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()

if __name__ == "__main__":
    main()
