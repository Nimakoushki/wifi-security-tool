import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import os

class SettingsTab:
    def __init__(self, parent, exit_handler):
        self.parent = parent
        self.exit_handler = exit_handler
        self.settings_file = "settings.json"
        self.settings = self.load_settings()
        self.frame = ctk.CTkFrame(parent)
        self.setup_ui()
        self.load_to_ui()

    def load_settings(self):
        default = {
            "default_interface": "wlan0",
            "default_wordlist": "wifi_wordlist.txt",
            "save_logs": True,
            "logs_folder": "logs",
            "deauth_delay": 3,
            "max_bruteforce_length": 6,
            "theme": "dark",
            "auto_save_results": True
        }
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    saved = json.load(f)
                    default.update(saved)
            except:
                pass
        return default

    def save_settings(self):
        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=2)
            return True
        except:
            return False

    def load_to_ui(self):
        self.interface_var.set(self.settings.get("default_interface", "wlan0"))
        self.wordlist_var.set(self.settings.get("default_wordlist", "wifi_wordlist.txt"))
        self.save_logs_var.set(self.settings.get("save_logs", True))
        self.logs_folder_var.set(self.settings.get("logs_folder", "logs"))
        self.deauth_delay_var.set(str(self.settings.get("deauth_delay", 3)))
        self.max_length_var.set(str(self.settings.get("max_bruteforce_length", 6)))
        self.auto_save_var.set(self.settings.get("auto_save_results", True))

    def save_from_ui(self):
        self.settings["default_interface"] = self.interface_var.get()
        self.settings["default_wordlist"] = self.wordlist_var.get()
        self.settings["save_logs"] = self.save_logs_var.get()
        self.settings["logs_folder"] = self.logs_folder_var.get()
        self.settings["deauth_delay"] = int(self.deauth_delay_var.get())
        self.settings["max_bruteforce_length"] = int(self.max_length_var.get())
        self.settings["auto_save_results"] = self.auto_save_var.get()
        if self.save_settings():
            messagebox.showinfo("Success", "Settings saved")
        else:
            messagebox.showerror("Error", "Could not save settings")

    def setup_ui(self):
        gen_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        gen_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(gen_frame, text="General Settings", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        row = ctk.CTkFrame(gen_frame)
        row.pack(fill="x")
        ctk.CTkLabel(row, text="Default Interface:").pack(side="left", padx=5)
        self.interface_var = ctk.StringVar()
        ctk.CTkEntry(row, textvariable=self.interface_var, width=150).pack(side="left", padx=5)

        row2 = ctk.CTkFrame(gen_frame)
        row2.pack(fill="x")
        ctk.CTkLabel(row2, text="Default Wordlist:").pack(side="left", padx=5)
        self.wordlist_var = ctk.StringVar()
        ctk.CTkEntry(row2, textvariable=self.wordlist_var, width=300).pack(side="left", padx=5)
        ctk.CTkButton(row2, text="Browse", command=self.browse_wordlist).pack(side="left", padx=5)

        row3 = ctk.CTkFrame(gen_frame)
        row3.pack(fill="x")
        ctk.CTkLabel(row3, text="Logs Folder:").pack(side="left", padx=5)
        self.logs_folder_var = ctk.StringVar()
        ctk.CTkEntry(row3, textvariable=self.logs_folder_var, width=300).pack(side="left", padx=5)
        ctk.CTkButton(row3, text="Browse", command=self.browse_logs).pack(side="left", padx=5)

        self.save_logs_var = ctk.BooleanVar()
        ctk.CTkCheckBox(gen_frame, text="Save logs to file", variable=self.save_logs_var).pack(anchor="w", padx=5)

        att_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        att_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(att_frame, text="Attack Settings", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        row4 = ctk.CTkFrame(att_frame)
        row4.pack(fill="x")
        ctk.CTkLabel(row4, text="Deauth Delay (sec):").pack(side="left", padx=5)
        self.deauth_delay_var = ctk.StringVar()
        ctk.CTkEntry(row4, textvariable=self.deauth_delay_var, width=60).pack(side="left", padx=5)
        ctk.CTkLabel(row4, text="Max Brute Force Length:").pack(side="left", padx=5)
        self.max_length_var = ctk.StringVar()
        ctk.CTkEntry(row4, textvariable=self.max_length_var, width=60).pack(side="left", padx=5)

        self.auto_save_var = ctk.BooleanVar()
        ctk.CTkCheckBox(att_frame, text="Auto-save results", variable=self.auto_save_var).pack(anchor="w", padx=5)

        btn_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        btn_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="Save Settings", command=self.save_from_ui).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Reset to Default", command=self.reset_settings).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Open Logs Folder", command=self.open_logs).pack(side="left", padx=5)

    def browse_wordlist(self):
        f = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if f:
            self.wordlist_var.set(f)

    def browse_logs(self):
        d = filedialog.askdirectory()
        if d:
            self.logs_folder_var.set(d)

    def open_logs(self):
        folder = self.logs_folder_var.get()
        if not os.path.exists(folder):
            os.makedirs(folder)
        os.startfile(folder)

    def reset_settings(self):
        if messagebox.askyesno("Reset", "Reset all settings to default?"):
            self.settings = {
                "default_interface": "wlan0",
                "default_wordlist": "wifi_wordlist.txt",
                "save_logs": True,
                "logs_folder": "logs",
                "deauth_delay": 3,
                "max_bruteforce_length": 6,
                "theme": "dark",
                "auto_save_results": True
            }
            self.load_to_ui()
            self.save_settings()
            messagebox.showinfo("Success", "Settings reset")

    def get_frame(self):
        return self.frame