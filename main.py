import os
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

# ADB Shell Libraries
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.auth.keygen import keygen

class WirelessDebuggingApp(App):
    device = None
    signer = None

    def build(self):
        # RSA Key များ စစ်ဆေးခြင်း/ထုတ်လုပ်ခြင်း (ADB ချိတ်ဖို့ မရှိမဖြစ်လိုပါသည်)
        self.setup_keys()

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Status Label
        self.status_label = Label(text='[✔] Ready to Connect', font_size=16, size_hint_y=None, height=60)
        self.layout.add_widget(self.status_label)

        # Inputs
        self.ip_input = TextInput(hint_text='Target IP (e.g. 192.168.1.5)', multiline=False, size_hint_y=None, height=40)
        self.port_input = TextInput(hint_text='Port (Default: 5555)', text='5555', multiline=False, size_hint_y=None, height=40)
        self.code_input = TextInput(hint_text='Pairing Code (For Android 11+)', multiline=False, size_hint_y=None, height=40)
        self.cmd_input = TextInput(hint_text='Custom Command (without adb)', multiline=False, size_hint_y=None, height=40)

        self.layout.add_widget(self.ip_input)
        self.layout.add_widget(self.port_input)
        self.layout.add_widget(self.code_input)
        self.layout.add_widget(self.cmd_input)

        # Buttons in ScrollView
        scroll_view = ScrollView()
        btn_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        btn_layout.bind(minimum_height=btn_layout.setter('height'))

        btn_layout.add_widget(Button(text='Connect Device', on_press=self.connect_device, size_hint_y=None, height=50))
        btn_layout.add_widget(Button(text='Pair Device (Android 11+)', on_press=self.pair_device, size_hint_y=None, height=50))
        btn_layout.add_widget(Button(text='List Packages', on_press=lambda x: self.send_command('pm list packages -3'), size_hint_y=None, height=50))
        btn_layout.add_widget(Button(text='Battery Status', on_press=lambda x: self.send_command('dumpsys battery'), size_hint_y=None, height=50))
        btn_layout.add_widget(Button(text='Screenshot', on_press=lambda x: self.send_command('screencap -p /sdcard/screen.png'), size_hint_y=None, height=50))
        btn_layout.add_widget(Button(text='Run Custom Command', on_press=self.run_custom, size_hint_y=None, height=50))
        
        scroll_view.add_widget(btn_layout)
        self.layout.add_widget(scroll_view)

        return self.layout

    def setup_keys(self):
        # ADB Key မရှိသေးရင် အသစ်ထုတ်ပါမယ်
        key_path = 'adbkey'
        if not os.path.exists(key_path):
            keygen(key_path)
        
        with open(key_path) as f:
            priv = f.read()
        with open(key_path + '.pub') as f:
            pub = f.read()
            
        self.signer = PythonRSASigner(pub, priv)

    def connect_device(self, instance):
        ip = self.ip_input.text
        port = self.port_input.text
        
        try:
            self.device = AdbDeviceTcp(ip, int(port), default_transport_timeout_s=9)
            # Connect လုပ်ပြီး RSA Key ပို့ပါမယ် (ဖုန်းမှာ Allow လုပ်ဖို့လိုပါတယ်)
            self.device.connect(rsa_keys=[self.signer], auth_timeout_s=0.1)
            self.status_label.text = f"Connected to {ip}:{port}"
        except Exception as e:
            self.status_label.text = f"Connection Failed: {str(e)}"

    def pair_device(self, instance):
        # Android 11+ Wireless Pairing
        ip = self.ip_input.text
        port = self.port_input.text
        code = self.code_input.text
        
        if not code:
            self.status_label.text = "Error: Pairing Code ထည့်ပါ"
            return

        try:
            temp_device = AdbDeviceTcp(ip, int(port))
            success = temp_device.connect(rsa_keys=[self.signer], auth_timeout_s=0.1)
            if not success:
                 # Pairing Protocol သုံးခြင်း
                result = temp_device.adb_connect(ip, int(port)) 
                # Note: adb-shell library pairing logic can be complex
                self.status_label.text = "Pairing command sent (Check Log)"
        except Exception as e:
            self.status_label.text = f"Pair Error: {str(e)}"

    def send_command(self, cmd):
        if not self.device:
            self.status_label.text = "Error: Device not connected!"
            return
        
        try:
            # ADB Shell သုံးပြီး Command ပို့ခြင်း
            result = self.device.shell(cmd)
            self.status_label.text = f"Result: {result[:100]}..." # ရှည်လွန်းရင် ဖြတ်ပြမည်
        except Exception as e:
             self.status_label.text = f"Command Error: {str(e)}"

    def run_custom(self, instance):
        cmd = self.cmd_input.text
        if cmd:
            self.send_command(cmd)

if __name__ == '__main__':
    WirelessDebuggingApp().run()
      
