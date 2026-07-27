import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import threading
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class HandshakeManagerSimple:
    def __init__(self, exit_handler):
        self.exit_handler = exit_handler
        self.capturing = False
    def start_capture(self, ssid, bssid, channel, interface):
        self.capturing = True
        return True
    def stop_capture(self):
        self.capturing = False
    def get_cap_file(self):
        return "handshake_demo.cap"

class HandshakeTab:
    def __init__(self, parent, exit_handler):
        self.parent = parent
        self.exit_handler = exit_handler
        self.target_network = None
        self.capture_manager = HandshakeManagerSimple(exit_handler)
        self.frame = ctk.CTkFrame(parent)
        self.setup_target_info()
        self.setup_settings()
        self.setup_controls()
        self.setup_log_area()
        self.setup_results_section()

    def setup_target_info(self):
        target_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        target_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(target_frame, text="🎯 Target Network", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.target_ssid_var = ctk.StringVar(value="Not selected")
        self.target_bssid_var = ctk.StringVar(value="-")
        self.target_channel_var = ctk.StringVar(value="-")
        ctk.CTkLabel(target_frame, textvariable=self.target_ssid_var).pack(anchor="w")
        ctk.CTkLabel(target_frame, textvariable=self.target_bssid_var).pack(anchor="w")
        ctk.CTkLabel(target_frame, textvariable=self.target_channel_var).pack(anchor="w")
        self.select_btn = ctk.CTkButton(target_frame, text="Select from Scan", command=self.select_from_scan)
        self.select_btn.pack(pady=5)

    def setup_settings(self):
        settings_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        settings_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(settings_frame, text="Interface:").pack(side="left", padx=5)
        self.interface_var = ctk.StringVar(value="wlan0mon")
        self.interface_combo = ctk.CTkComboBox(settings_frame, values=["wlan0mon", "wlan0", "WiFi"], variable=self.interface_var, width=120)
        self.interface_combo.pack(side="left", padx=5)

    def setup_controls(self):
        control_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        control_frame.pack(fill="x", padx=10, pady=5)
        self.start_btn = ctk.CTkButton(control_frame, text="▶ Start Capture", command=self.start_capture)
        self.start_btn.pack(side="left", padx=5)
        self.stop_btn = ctk.CTkButton(control_frame, text="⏹ Stop", command=self.stop_capture, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        self.status_label = ctk.CTkLabel(control_frame, text="⚪ Ready", text_color="blue")
        self.status_label.pack(side="right", padx=10)

    def setup_log_area(self):
        log_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_area = scrolledtext.ScrolledText(log_frame, height=10, state="disabled")
        self.log_area.pack(fill="both", expand=True)

    def setup_results_section(self):
        results_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        results_frame.pack(fill="x", padx=10, pady=5)
        self.results_text = ctk.CTkTextbox(results_frame, height=80)
        self.results_text.pack(fill="x", padx=5, pady=5)

    def update_status(self, message, level="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.configure(state="normal")
        self.log_area.insert("end", f"[{timestamp}] {message}\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def select_from_scan(self):
        dialog = ctk.CTkToplevel(self.frame)
        dialog.title("Select Target")
        dialog.geometry("300x200")
        ctk.CTkLabel(dialog, text="SSID:").pack(pady=5)
        ssid_entry = ctk.CTkEntry(dialog)
        ssid_entry.pack(pady=5)
        ctk.CTkLabel(dialog, text="BSSID:").pack(pady=5)
        bssid_entry = ctk.CTkEntry(dialog)
        bssid_entry.pack(pady=5)
        ctk.CTkLabel(dialog, text="Channel:").pack(pady=5)
        ch_entry = ctk.CTkEntry(dialog)
        ch_entry.pack(pady=5)
        def set_target():
            self.target_network = {"ssid": ssid_entry.get(), "bssid": bssid_entry.get(), "channel": ch_entry.get()}
            self.target_ssid_var.set(self.target_network["ssid"])
            self.target_bssid_var.set(self.target_network["bssid"])
            self.target_channel_var.set(self.target_network["channel"])
            dialog.destroy()
        ctk.CTkButton(dialog, text="OK", command=set_target).pack(pady=10)

    def start_capture(self):
        if not self.target_network:
            messagebox.showwarning("No Target", "Please select a target first")
            return
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.update_status(f"Starting capture on {self.target_network['ssid']}...")
        thread = threading.Thread(target=self._simulate_capture, daemon=True)
        thread.start()

    def _simulate_capture(self):
        import time
        for i in range(5):
            if not self.capture_manager.capturing:
                break
            time.sleep(1)
            self.update_status(f"Listening... {i+1}/5")
        self.capture_manager.capturing = False
        self.parent.after(0, self.capture_finished)

    def capture_finished(self):
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", "✅ Handshake captured!\nFile: handshake_demo.cap")
        self.update_status("Capture finished.", "success")

    def stop_capture(self):
        self.capture_manager.stop_capture()
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.update_status("Stopped by user.", "warning")

    def get_frame(self):
        return self.frame