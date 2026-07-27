import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.wifi_password_finder import WiFiPasswordFinder

class CrackTab:
    def __init__(self, parent, exit_handler):
        self.parent = parent
        self.exit_handler = exit_handler
        self.finder = WiFiPasswordFinder()
        self.finder.set_callback(self.update_status)
        self.wordlist_file = None
        self.target_ssid = None
        self.frame = ctk.CTkFrame(parent)
        self.setup_target_section()
        self.setup_files_section()
        self.setup_controls()
        self.setup_progress_section()
        self.setup_log_area()
        self.setup_results_section()

    def setup_target_section(self):
        target_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        target_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(target_frame, text="🎯 Target WiFi SSID:").pack(side="left", padx=5)
        self.target_var = ctk.StringVar()
        self.target_entry = ctk.CTkEntry(target_frame, textvariable=self.target_var, width=200)
        self.target_entry.pack(side="left", padx=5)
        self.current_btn = ctk.CTkButton(target_frame, text="Use Current Network", command=self.get_current_wifi)
        self.current_btn.pack(side="left", padx=5)
        self.saved_btn = ctk.CTkButton(target_frame, text="Find from Windows Memory", command=self.find_from_saved)
        self.saved_btn.pack(side="left", padx=5)

    def setup_files_section(self):
        file_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        file_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(file_frame, text="Wordlist File:").pack(side="left", padx=5)
        self.wordlist_var = ctk.StringVar(value="No file selected")
        self.wordlist_label = ctk.CTkLabel(file_frame, textvariable=self.wordlist_var, text_color="gray")
        self.wordlist_label.pack(side="left", padx=5)
        self.browse_btn = ctk.CTkButton(file_frame, text="Browse", command=self.browse_wordlist)
        self.browse_btn.pack(side="left", padx=5)
        self.create_btn = ctk.CTkButton(file_frame, text="Create Sample Wordlist", command=self.create_sample_wordlist)
        self.create_btn.pack(side="left", padx=5)

    def setup_controls(self):
        control_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        control_frame.pack(fill="x", padx=10, pady=5)
        self.start_btn = ctk.CTkButton(control_frame, text="▶ Start Dictionary Attack", command=self.start_attack)
        self.start_btn.pack(side="left", padx=5)
        self.stop_btn = ctk.CTkButton(control_frame, text="⏹ Stop", command=self.stop_attack, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        self.status_label = ctk.CTkLabel(control_frame, text="⚪ Ready", text_color="blue")
        self.status_label.pack(side="right", padx=10)

    def setup_progress_section(self):
        progress_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        progress_frame.pack(fill="x", padx=10, pady=5)
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=500)
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)
        self.progress_label = ctk.CTkLabel(progress_frame, text="Ready")
        self.progress_label.pack()

    def setup_log_area(self):
        log_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        from tkinter import scrolledtext
        self.log_area = scrolledtext.ScrolledText(log_frame, height=10, state="disabled")
        self.log_area.pack(fill="both", expand=True)

    def setup_results_section(self):
        results_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        results_frame.pack(fill="x", padx=10, pady=5)
        self.results_text = ctk.CTkTextbox(results_frame, height=80)
        self.results_text.pack(fill="x", padx=5, pady=5)
        self.save_btn = ctk.CTkButton(results_frame, text="Save Password", command=self.save_result, state="disabled")
        self.save_btn.pack(side="left", padx=5)
        self.copy_btn = ctk.CTkButton(results_frame, text="Copy to Clipboard", command=self.copy_password, state="disabled")
        self.copy_btn.pack(side="left", padx=5)

    def update_status(self, message, level="info", current=None, total=None, current_word=""):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.configure(state="normal")
        self.log_area.insert("end", f"[{timestamp}] {message}\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")
        if current and total:
            percent = current / total
            self.progress_bar.set(percent)
            self.progress_label.configure(text=f"Progress: {percent*100:.1f}% ({current}/{total}) - Testing: {current_word[:15]}")
        if "found" in message.lower():
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", f"✅✅✅ PASSWORD FOUND: {self.finder.password_found}\n\nUse it to connect.")
            self.save_btn.configure(state="normal")
            self.copy_btn.configure(state="normal")

    def get_current_wifi(self):
        current = self.finder.get_current_wifi()
        if current:
            self.target_var.set(current)
            self.update_status(f"Current network: {current}", "success")

    def find_from_saved(self):
        ssid = self.target_var.get().strip()
        if not ssid:
            messagebox.showwarning("Error", "Enter SSID first")
            return
        pwd = self.finder.find_saved_password(ssid)
        if pwd:
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", f"✅ Password from Windows memory: {pwd}")
            self.save_btn.configure(state="normal")
            self.copy_btn.configure(state="normal")
        else:
            self.update_status("Password not found in Windows memory.", "error")

    def browse_wordlist(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.wordlist_file = filename
            self.wordlist_var.set(os.path.basename(filename))
            self.update_status(f"Wordlist loaded: {filename}", "success")

    def create_sample_wordlist(self):
        filename = "sample_wordlist.txt"
        passwords = ["12345678","password","123456789","qwerty123","admin123"]
        with open(filename, "w") as f:
            f.write("\n".join(passwords))
        self.wordlist_file = filename
        self.wordlist_var.set(filename)
        self.update_status(f"Created sample wordlist with {len(passwords)} passwords", "success")

    def start_attack(self):
        ssid = self.target_var.get().strip()
        if not ssid:
            messagebox.showwarning("Error", "Enter target SSID")
            return
        if not self.wordlist_file or not os.path.exists(self.wordlist_file):
            messagebox.showwarning("Error", "Select a valid wordlist")
            return
        self.target_ssid = ssid
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", "Attack in progress...")
        thread = threading.Thread(target=self._run_attack, daemon=True)
        thread.start()

    def _run_attack(self):
        self.finder.find_password_from_wordlist(self.target_ssid, self.wordlist_file)
        self.parent.after(0, self.attack_finished)

    def attack_finished(self):
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        if not self.finder.password_found:
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", "❌ Password not found in wordlist.\nTry a larger dictionary.")

    def stop_attack(self):
        self.finder.stop_finding()
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

    def save_result(self):
        if self.finder.password_found:
            filename = filedialog.asksaveasfilename(defaultextension=".txt")
            if filename:
                with open(filename, "w") as f:
                    f.write(f"SSID: {self.target_ssid}\nPassword: {self.finder.password_found}")
                self.update_status("Password saved.", "success")

    def copy_password(self):
        if self.finder.password_found:
            self.parent.clipboard_clear()
            self.parent.clipboard_append(self.finder.password_found)
            self.update_status("Password copied to clipboard.", "success")

    def get_frame(self):
        return self.frame