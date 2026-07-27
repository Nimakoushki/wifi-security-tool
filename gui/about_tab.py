import customtkinter as ctk
import webbrowser

class AboutTab:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)

        title = ctk.CTkLabel(
            self.frame,
            text="✦ About This Project ✦",
            font=ctk.CTkFont(family="Segoe UI", size=36, weight="bold", slant="italic"),
            text_color="#00CED1"
        )
        title.pack(pady=30)

        info_frame = ctk.CTkFrame(self.frame, corner_radius=15, fg_color="#1e1e1e")
        info_frame.pack(pady=20, padx=40, fill="x")

        info_text = """
        🔒 WiFi Security Tool Pro

        Version 2.0

        A professional tool for:
        • Scanning WiFi networks
        • Capturing Handshakes
        • Dictionary-based password cracking
        • Windows memory password recovery

        Designed for educational and ethical security testing.
        """
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(family="Segoe UI", size=16, slant="italic"),
            justify="center"
        )
        info_label.pack(pady=15, padx=20)

        github_frame = ctk.CTkFrame(self.frame, corner_radius=15)
        github_frame.pack(pady=10, padx=40, fill="x")

        github_btn = ctk.CTkButton(
            github_frame,
            text="🚀 Visit on GitHub",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold", slant="italic"),
            fg_color="#333333",
            hover_color="#555555",
            corner_radius=12,
            command=lambda: webbrowser.open("https://github.com/Nimakoushki")
        )
        github_btn.pack(pady=15, padx=20)

        ethical_frame = ctk.CTkFrame(self.frame, corner_radius=15, fg_color="#8B0000")
        ethical_frame.pack(pady=20, padx=40, fill="x")

        ethical_text = """
        ⚠️ Ethical Notice ⚠️
        This tool is intended for:
        • Testing your own network security
        • Educational purposes only
        • With explicit permission from the network owner

        Unauthorized use is strictly prohibited.
        """
        ethical_label = ctk.CTkLabel(
            ethical_frame,
            text=ethical_text,
            font=ctk.CTkFont(family="Segoe UI", size=13, slant="italic"),
            text_color="white",
            justify="center"
        )
        ethical_label.pack(pady=10, padx=20)

        footer = ctk.CTkLabel(
            self.frame,
            text="~ Made with ❤️ by Nima Koushki ~",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold", slant="italic"),
            text_color="#FFD700"
        )
        footer.pack(pady=15)

    def get_frame(self):
        return self.frame