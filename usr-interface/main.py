import tkinter as tk
from tkinter import filedialog, messagebox

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filepath:
        with open(filepath, "r", encoding="utf-8") as file:
            text.delete("1.0", tk.END)
            text.insert(tk.END, file.read())
        root.title(f"Notepad - {filepath}")

def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])
    if filepath:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(text.get("1.0", tk.END))
        root.title(f"Notepad - {filepath}")

def clear_text():
    if messagebox.askyesno("Clear", "Clear all text?"):
        text.delete("1.0", tk.END)

def main():
    # Set up window
    global root, text  # Declare as global to access in open_file, save_file, clear_text
    root = tk.Tk()
    root.title("Notepad")
    root.geometry("800x600")

    # Create text area with scrollbar
    text = tk.Text(root, wrap="word", font=("Consolas", 12))
    scrollbar = tk.Scrollbar(root, command=text.yview)
    text.configure(yscrollcommand=scrollbar.set)

    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create menu bar
    menu = tk.Menu(root)
    file_menu = tk.Menu(menu, tearoff=0)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Clear", command=clear_text)
    file_menu.add_command(label="Exit", command=root.quit)
    menu.add_cascade(label="File", menu=file_menu)

    root.config(menu=menu)

    # Run the app
    root.mainloop()

if __name__ == "__main__":
    main()
