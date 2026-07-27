import customtkinter as ctk
from tkinter import messagebox
import threading
import subprocess
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.wifi_scanner import WiFiScanner

class ScanTab:
    def __init__(self, parent, exit_handler):
        self.parent = parent
        self.exit_handler = exit_handler
        self.scanning = False
        self.selected_network = None
        self.frame = ctk.CTkFrame(parent)
        self.setup_controls()
        self.setup_networks_table()
        self.setup_log_area()
        self.setup_target_section()

    def setup_controls(self):
        control_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        control_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(control_frame, text="Interface:").pack(side="left", padx=5)
        self.interface_var = ctk.StringVar(value="WiFi")
        self.interface_combo = ctk.CTkComboBox(control_frame, values=["WiFi", "wlan0", "wlan0mon"],
                                               variable=self.interface_var, width=120)
        self.interface_combo.pack(side="left", padx=5)

        self.scan_btn = ctk.CTkButton(control_frame, text="🔍 Start Scan", command=self.start_scan)
        self.scan_btn.pack(side="left", padx=20)

        self.stop_btn = ctk.CTkButton(control_frame, text="⏹ Stop", command=self.stop_scan, state="disabled")
        self.stop_btn.pack(side="left", padx=5)

        self.status_label = ctk.CTkLabel(control_frame, text="⚪ Ready", text_color="blue")
        self.status_label.pack(side="right", padx=10)

    def setup_networks_table(self):
        table_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        from tkinter import ttk
        columns = ("#", "SSID", "BSSID", "CH", "Signal", "Security")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.column("#", width=40, anchor="center")
        self.tree.column("SSID", width=200)
        self.tree.column("BSSID", width=150)
        self.tree.column("CH", width=60, anchor="center")
        self.tree.column("Signal", width=120)
        self.tree.column("Security", width=100)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind('<<TreeviewSelect>>', self.on_network_select)

    def on_network_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            if values:
                self.selected_network = {
                    'ssid': values[1], 'bssid': values[2], 'channel': values[3],
                    'signal': values[4], 'security': values[5]
                }
                self.target_label.configure(text=f"🎯 Target: {self.selected_network['ssid']}")
                self.target_select_btn.configure(state="normal")

    def setup_log_area(self):
        log_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        from tkinter import scrolledtext
        self.log_area = scrolledtext.ScrolledText(log_frame, height=8, state="disabled", wrap="word")
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)

    def setup_target_section(self):
        target_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        target_frame.pack(fill="x", padx=10, pady=5)
        self.target_label = ctk.CTkLabel(target_frame, text="No target selected")
        self.target_label.pack(side="left", padx=5)
        self.target_select_btn = ctk.CTkButton(target_frame, text="Select as Target", command=self.confirm_target, state="disabled")
        self.target_select_btn.pack(side="right", padx=5)

    def confirm_target(self):
        if self.selected_network:
            msg = f"Target: {self.selected_network['ssid']}\nBSSID: {self.selected_network['bssid']}\nContinue?"
            if messagebox.askyesno("Confirm Target", msg):
                self.add_log(f"Target set: {self.selected_network['ssid']}", "success")
                return True
        return False

    def add_log(self, message, tag="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.configure(state="normal")
        self.log_area.insert("end", f"[{timestamp}] {message}\n", tag)
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def start_scan(self):
        if self.scanning:
            return
        self.scanning = True
        self.scan_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_label.configure(text="🟡 Scanning...", text_color="orange")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.add_log("Starting scan...", "info")
        thread = threading.Thread(target=self.scan_networks, daemon=True)
        thread.start()

    def scan_networks(self):
        networks = WiFiScanner.scan_all_networks()
        if not networks:
            networks = WiFiScanner.get_test_networks()
            self.parent.after(0, self.add_log, "Using test data (no networks found)", "warning")
        for i, net in enumerate(networks, 1):
            signal_bar = "█" * (int(net.get('signal',50))//10) + "░" * (10 - int(net.get('signal',50))//10)
            self.parent.after(0, self.add_network_to_table,
                i, net.get('ssid','?'), net.get('bssid','?'), net.get('channel','?'),
                f"{net.get('signal',50)}% {signal_bar}", net.get('security','?'))
        self.parent.after(0, self.scan_complete, len(networks))

    def add_network_to_table(self, idx, ssid, bssid, ch, sig, sec):
        self.tree.insert("", "end", values=(idx, ssid, bssid, ch, sig, sec))

    def scan_complete(self, count):
        self.scanning = False
        self.scan_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text=f"✅ Scan Complete - {count} networks", text_color="green")
        self.add_log(f"Scan finished. {count} networks found.", "success")

    def stop_scan(self):
        self.scanning = False
        self.add_log("Scan stopped by user", "warning")
        self.scan_complete(0)

    def get_frame(self):
        return self.frame