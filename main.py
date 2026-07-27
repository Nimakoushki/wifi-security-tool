import customtkinter as ctk
from tkinter import messagebox
from utils.exit_handler import ExitHandler
from gui.scan_tab import ScanTab
from gui.handshake_tab import HandshakeTab
from gui.crack_tab import CrackTab
from gui.settings_tab import SettingsTab
from gui.about_tab import AboutTab

# تنظیمات تم
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class WiFiSecurityApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("✦ WiFi Security Tool Pro ✦")
        self.root.geometry("1200x900")
        self.root.minsize(1000, 750)

        self.exit_handler = ExitHandler()
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.setup_tabs()
        self.setup_statusbar()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_tabs(self):
        self.tabview = ctk.CTkTabview(
            self.main_frame,
            segmented_button_selected_color="#00CED1",
            segmented_button_selected_hover_color="#20B2AA"
        )
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # تب‌ها با آیکون‌های جدید
        self.tabview.add("📶 Scan")
        self.tabview.add("📡 Handshake")
        self.tabview.add("🔑 Crack")
        self.tabview.add("🎭 Rogue AP")
        self.tabview.add("⚙️ Settings")
        self.tabview.add("💡 About")

        self.scan_tab = ScanTab(self.tabview.tab("📶 Scan"), self.exit_handler)
        self.scan_tab.get_frame().pack(fill="both", expand=True)

        self.handshake_tab = HandshakeTab(self.tabview.tab("📡 Handshake"), self.exit_handler)
        self.handshake_tab.get_frame().pack(fill="both", expand=True)

        self.crack_tab = CrackTab(self.tabview.tab("🔑 Crack"), self.exit_handler)
        self.crack_tab.get_frame().pack(fill="both", expand=True)

        self.setup_rogue_tab(self.tabview.tab("🎭 Rogue AP"))

        self.settings_tab = SettingsTab(self.tabview.tab("⚙️ Settings"), self.exit_handler)
        self.settings_tab.get_frame().pack(fill="both", expand=True)

        self.about_tab = AboutTab(self.tabview.tab("💡 About"))
        self.about_tab.get_frame().pack(fill="both", expand=True)

    def setup_rogue_tab(self, parent):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="both", expand=True)
        label = ctk.CTkLabel(
            frame,
            text="🎭 Rogue AP Farm\n\nUnder Development...",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold", slant="italic"),
            text_color="gray"
        )
        label.pack(expand=True)

    def setup_statusbar(self):
        self.statusbar = ctk.CTkFrame(self.root, height=40, corner_radius=0, fg_color="#2b2b2b")
        self.statusbar.pack(side="bottom", fill="x")

        self.status_label = ctk.CTkLabel(
            self.statusbar,
            text="✅ Ready",
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=12, slant="italic")
        )
        self.status_label.pack(side="left", padx=10)

        self.version_label = ctk.CTkLabel(
            self.statusbar,
            text="v2.0 - Professional Edition",
            anchor="e",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold", slant="italic")
        )
        self.version_label.pack(side="right", padx=10)

        self.theme_btn = ctk.CTkButton(
            self.statusbar,
            text="🌓",
            width=40,
            command=self.toggle_theme,
            font=ctk.CTkFont(size=14)
        )
        self.theme_btn.pack(side="right", padx=5)

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")

    def on_closing(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.exit_handler.save_state({"last_session": "closed"})
            self.root.destroy()
            self.exit_handler.cleanup()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WiFiSecurityApp()
    app.run()