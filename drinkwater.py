import customtkinter as ctk
import schedule
import time
import threading
import pyttsx3
from win10toast import ToastNotifier
import pystray
from PIL import Image, ImageDraw
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Notifier and TTS
toaster = ToastNotifier()
tts = pyttsx3.init()

# State
do_not_disturb = False
running = True
hour_vars = {}  # hour -> BooleanVar

# Volume helpers (Windows)
def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def is_muted():
    return bool(get_volume_interface().GetMute())

def set_mute(mute: bool):
    get_volume_interface().SetMute(1 if mute else 0, None)

# Popup UI, must run on main thread
def show_popup(msg):
    popup = ctk.CTkToplevel(app)
    popup.title("Drink Water")
    popup.geometry("360x160")
    popup.attributes("-topmost", True)
    popup.grab_set()  # keep focus
    lbl = ctk.CTkLabel(popup, text=msg, font=("", 20))
    lbl.pack(expand=True, pady=(10, 5))
    btn = ctk.CTkButton(popup, text="Dismiss", width=120, command=popup.destroy)
    btn.pack(pady=(0, 12))
    popup.after(8000, lambda: (popup.winfo_exists() and popup.destroy()))

# Reminder job
def remind(hour):
    global do_not_disturb
    if do_not_disturb:
        return

    label = f"{hour % 12 or 12}:00 {'AM' if hour < 12 else 'PM'}"
    msg = f"Time to drink water - {label}"

    # Handle mute
    was_muted = is_muted()
    if was_muted:
        set_mute(False)

    # Toast and voice
    toaster.show_toast("Water Reminder", msg, duration=5, threaded=True)
    try:
        tts.say("Time to drink water")
        tts.runAndWait()
    except Exception:
        pass

    if was_muted:
        set_mute(True)

    # Popup on main thread
    app.after(0, lambda: show_popup("💧 Drink water now"))

# Scheduler loop
def scheduler_loop():
    while running:
        schedule.run_pending()
        time.sleep(1)

# Setup schedule based on checked hours
def refresh_schedule():
    schedule.clear()
    for h, var in hour_vars.items():
        if var.get():
            schedule.every().day.at(f"{h:02d}:00").do(lambda h=h: remind(h))

# Tray icon helpers
def create_icon_image():
    img = Image.new("RGB", (64, 64), (0, 120, 215))
    d = ImageDraw.Draw(img)
    d.ellipse((14, 14, 50, 50), fill="white")
    return img

tray_icon = None

def on_show(icon, item):
    icon.stop()
    app.after(0, app.deiconify)

def on_toggle_dnd(icon, item):
    global do_not_disturb
    do_not_disturb = not do_not_disturb
    app.after(0, lambda: dnd_btn.configure(text=f"DND: {'ON' if do_not_disturb else 'OFF'}"))

def on_quit(icon, item):
    icon.stop()
    app.after(0, stop_and_exit())

def minimize_to_tray():
    global tray_icon
    app.withdraw()

    def _on_show(icon, item):
        icon.stop()
        app.after(0, app.deiconify)

    def _on_toggle(icon, item):
        global do_not_disturb
        do_not_disturb = not do_not_disturb
        app.after(0, lambda: dnd_btn.configure(text=f"DND: {'ON' if do_not_disturb else 'OFF'}"))

    def _on_quit(icon, item):
        icon.stop()
        app.after(0, stop_and_exit())

    image = create_icon_image()
    tray_icon = pystray.Icon(
        "WaterReminder",
        image,
        "Water Reminder",
        menu=pystray.Menu(
            pystray.MenuItem("Show", _on_show),
            pystray.MenuItem("Toggle DND", _on_toggle),
            pystray.MenuItem("Quit", _on_quit),
        ),
    )
    threading.Thread(target=tray_icon.run, daemon=True).start()

# Clean exit
def stop_and_exit():
    global running
    running = False
    schedule.clear()
    try:
        app.destroy()
    except Exception:
        pass

# UI
app = ctk.CTk()
app.title("Water Reminder")
app.geometry("420x520")

header = ctk.CTkLabel(app, text="Water Reminder", font=("", 22))
header.pack(pady=(18, 6))

sub = ctk.CTkLabel(app, text="Select hours to notify", font=("", 12))
sub.pack(pady=(0, 6))

frame = ctk.CTkScrollableFrame(app, width=380, height=320)
frame.pack(pady=6)

# Create checkboxes for 10 AM - 7 PM
for h in range(10, 20):
    label = f"{h % 12 or 12}:00 {'AM' if h < 12 else 'PM'}"
    var = ctk.BooleanVar(value=True)
    cb = ctk.CTkCheckBox(frame, text=label, variable=var)
    cb.pack(anchor="w", pady=4, padx=8)
    hour_vars[h] = var

# Controls
btn_frame = ctk.CTkFrame(app)
btn_frame.pack(pady=12, fill="x", padx=20)

dnd_btn = ctk.CTkButton(btn_frame, text=f"DND: {'ON' if do_not_disturb else 'OFF'}",
                       command=lambda: toggle_dnd())
dnd_btn.pack(side="left", padx=(10, 8), pady=10)

min_btn = ctk.CTkButton(btn_frame, text="Minimize to Tray", command=minimize_to_tray)
min_btn.pack(side="left", padx=8, pady=10)

stop_btn = ctk.CTkButton(btn_frame, text="Stop Reminders", command=stop_and_exit)
stop_btn.pack(side="right", padx=(8, 10), pady=10)

def toggle_dnd():
    global do_not_disturb
    do_not_disturb = not do_not_disturb
    dnd_btn.configure(text=f"DND: {'ON' if do_not_disturb else 'OFF'}")

# Start scheduling and thread
refresh_schedule()
t = threading.Thread(target=scheduler_loop, daemon=True)
t.start()

# Minimize on close
app.protocol("WM_DELETE_WINDOW", minimize_to_tray)

app.mainloop()
