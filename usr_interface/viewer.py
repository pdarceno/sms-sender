import tkinter as tk
from tkinter import ttk, messagebox
from .scheduler import get_all_scheduled_sms, delete_scheduled_sms

class ScheduledSMSViewer(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Scheduled SMS Viewer")
        self.geometry("700x400")
        self.tree = ttk.Treeview(self, columns=("id", "destination", "message", "scheduled_time", "status", "created_at"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self._populate()
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=5)
        del_btn = tk.Button(btn_frame, text="Delete Selected", command=self._delete_selected)
        del_btn.pack(side=tk.LEFT, padx=10)
        refresh_btn = tk.Button(btn_frame, text="Refresh", command=self._populate)
        refresh_btn.pack(side=tk.LEFT)

    def _populate(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for sms in get_all_scheduled_sms():
            self.tree.insert("", tk.END, values=sms)

    def _delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("No selection", "Please select an SMS to delete.")
            return
        for item in selected:
            sms_id = self.tree.item(item, "values")[0]
            delete_scheduled_sms(sms_id)
        self._populate()
