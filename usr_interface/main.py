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
        self._add_floating_sms_button()

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

    def _add_floating_sms_button(self) -> None:
        self.sms_button = tk.Button(self.root, text="Send SMS", bg="#4CAF50", fg="white", command=self._show_sms_send_ui)
        self.sms_button.place(relx=0.01, rely=0.95, anchor="sw")

    def _show_sms_send_ui(self) -> None:
        self.sms_window = tk.Toplevel(self.root)
        self.sms_window.title("Send SMS")
        self.sms_window.geometry("300x200")
        self.sms_window.transient(self.root)
        self.sms_window.grab_set()

        tk.Label(self.sms_window, text="Send Type:").pack(pady=(10, 0))
        self.send_type = tk.StringVar(value="test")
        test_radio = tk.Radiobutton(self.sms_window, text="Testing Send", variable=self.send_type, value="test", command=self._update_sms_ui)
        live_radio = tk.Radiobutton(self.sms_window, text="Live Send", variable=self.send_type, value="live", command=self._update_sms_ui)
        test_radio.pack(anchor="w", padx=20)
        live_radio.pack(anchor="w", padx=20)

        self.input_frame = tk.Frame(self.sms_window)
        self.input_frame.pack(fill="x", pady=10)
        self._update_sms_ui()

        send_btn = tk.Button(self.sms_window, text="Send", command=self._handle_sms_send)
        send_btn.pack(pady=10)

    def _update_sms_ui(self) -> None:
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        if self.send_type.get() == "test":
            tk.Label(self.input_frame, text="Test Phone Number:").pack(anchor="w", padx=10)
            self.test_number_entry = tk.Entry(self.input_frame)
            self.test_number_entry.pack(fill="x", padx=10)
        else:
            # Live send: only file picker for Excel/CSV
            tk.Label(self.input_frame, text="Excel/CSV File:").pack(anchor="w", padx=10)
            self.file_path_var = tk.StringVar()
            file_frame = tk.Frame(self.input_frame)
            file_frame.pack(fill="x", padx=10)
            self.file_entry = tk.Entry(file_frame, textvariable=self.file_path_var)
            self.file_entry.pack(side="left", fill="x", expand=True)
            tk.Button(file_frame, text="Browse", command=self._browse_file).pack(side="left", padx=(5,0))

    def _browse_file(self):
        filetypes = [
            ("Excel files", "*.xlsx *.xls"),
            ("CSV files", "*.csv"),
        ]
        path = filedialog.askopenfilename(filetypes=filetypes)
        if path:
            self.file_path_var.set(path)

    @staticmethod
    def get_customer_phone(phone, phone2):
        import pandas as pd
        # Ensure any NaNs from pandas are converted to 'nan'
        phone = 'nan' if pd.isna(phone) else str(phone).strip().replace(" ", "").replace(".", "")
        phone2 = 'nan' if pd.isna(phone2) else str(phone2).strip().replace(" ", "").replace(".", "")
        # Choose the first phone if not 'nan', otherwise the second
        dest = phone if phone != 'nan' else phone2
        return dest

    def _handle_sms_send(self) -> None:
        template = self.text.get("1.0", tk.END).strip()
        sender = SMSSender(template)
        message = sender.replace_keywords("123456", "100.00", "John Doe")
        if self.send_type.get() == "test":
            number = self.test_number_entry.get()
            if not number:
                messagebox.showerror("Error", "Please enter a test phone number.")
                return
            # Actually send SMS to the test number
            success = sender.send_sms(number, SMSGLOBAL_API_KEY, SMSGLOBAL_API_SECRET, SMSGLOBAL_API_URL)
            if success:
                messagebox.showinfo("Test SMS", f"SMS sent to: {number}\nMessage: {message}")
            else:
                messagebox.showerror("Test SMS", f"Failed to send SMS to: {number}")
        else:
            file_path = self.file_path_var.get()
            if not file_path:
                messagebox.showerror("Error", "Please select an Excel or CSV file.")
                return
            # Update the Excel file with DB data before sending SMS
            try:
                populate_excel(file_path, test_flag=False)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update Excel from DB: {e}")
                return
            # Read Excel/CSV and send SMS to each Account No
            try:
                if file_path.lower().endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(file_path)
                elif file_path.lower().endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    messagebox.showerror("Error", "Unsupported file type. Please select an Excel or CSV file.")
                    return
                if 'Account No' not in df.columns:
                    messagebox.showerror("Error", "File must contain a column named 'Account No'.")
                    return
                failed = []
                for idx, row in df.iterrows():
                    account_no = str(row['Account No'])
                    # Try to get customer_name and ar_balance from the row, fallback to blank if missing
                    customer_name = str(row['Customer Name']) if 'Customer Name' in row and pd.notnull(row['Customer Name']) else ""
                    ar_balance = str(row['Arrears Balance']) if 'Arrears Balance' in row and pd.notnull(row['Arrears Balance']) else ""
                    phone = row['Phone'] if 'Phone' in row else None
                    phone2 = row['Phone2'] if 'Phone2' in row else None
                    destination = self.get_customer_phone(phone, phone2)
                    sms_message = sender.replace_keywords(account_no, ar_balance, customer_name)
                    sender.message_template = sms_message
                    success = sender.send_sms(destination, SMSGLOBAL_API_KEY, SMSGLOBAL_API_SECRET, SMSGLOBAL_API_URL)
                    if not success:
                        failed.append(account_no)
                if not failed:
                    messagebox.showinfo("Live SMS", "All SMS messages sent successfully.")
                else:
                    messagebox.showwarning("Live SMS", f"Failed to send SMS to: {', '.join(map(str, failed))}")
            except Exception as e:
                messagebox.showerror("Live SMS", f"Error sending SMS: {e}")
        self.sms_window.destroy()

def main() -> None:
    root = tk.Tk()
    _ = Notepad(root)
    root.mainloop()

if __name__ == "__main__":
    main()
