import tkinter as tk
import threading
import time
import pyautogui
import qrcode
from PIL import Image, ImageTk
from PIL.Image import Resampling
import os
import platform
import subprocess

ENABLE_PRANK = True
ENABLE_FAKE_RESTART = True
QR_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def restart_pc():
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.Popen(["shutdown", "/r", "/t", "0"])
        elif system == "Linux" or system == "Darwin":
            subprocess.Popen(["sudo", "shutdown", "-r", "now"])
        else:
            print("Unsupported OS for restart command")
    except Exception as e:
        print(f"Failed to restart PC: {e}")


def generate_qr_code(url, filename="rickroll_qr.png"):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="white", back_color="#0078D7")
    img.save(filename)

def fake_bsod():
    qr_path = "rickroll_qr.png"
    if not os.path.exists(qr_path):
        generate_qr_code(QR_URL, qr_path)

    root = tk.Tk()
    root.title("Fake BSOD")
    root.attributes("-fullscreen", True)
    root.configure(bg="#0078D7")
    root.attributes("-topmost", True)
    root.overrideredirect(True)

    stop_event = threading.Event()  # Event to signal window close

    def on_close():
        stop_event.set()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)  # Handle window close button if any
    root.bind("<Escape>", lambda e: on_close())  # Escape key also closes

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Main frame for center alignment
    center_frame = tk.Frame(root, bg="#0078D7")
    center_frame.place(relx=0.05, rely=0.10, anchor="nw")

    # Sad face
    sad_face = tk.Label(center_frame, text=":(", font=("Segoe UI", 160),
                        fg="white", bg="#0078D7", anchor="w")
    sad_face.pack(anchor="w")

    # Main BSOD text
    static_text = (
        "\nYour PC ran into a problem and needs to restart. We're\n"
        "just collecting some error info, and then we'll restart for\n"
        "you.\n"
    )
    static_label = tk.Label(center_frame, text=static_text, font=("Segoe UI", 26),
                            fg="white", bg="#0078D7", justify="left", anchor="w")
    static_label.pack(anchor="w")

    # Progress bar text
    progress_var = tk.StringVar(value="1% complete")
    progress_label = tk.Label(center_frame, textvariable=progress_var, font=("Segoe UI", 26),
                              fg="white", bg="#0078D7", justify="left", anchor="w")
    progress_label.pack(anchor="w", pady=(0, 30))

    # QR Code and info
    qr_img = Image.open(qr_path)
    qr_img = qr_img.resize((140, 140), Resampling.LANCZOS)
    qr_photo = ImageTk.PhotoImage(qr_img)

    qr_info_frame = tk.Frame(center_frame, bg="#0078D7")
    qr_info_frame.pack(anchor="w")

    qr_label = tk.Label(qr_info_frame, image=qr_photo, bg="#0078D7")
    qr_label.image = qr_photo
    qr_label.pack(side="left")

    right_text = (
        "For more information about this issue and possible fixes, visit\n"
        "https://www.windows.com/stopcode\n\n"
        "If you call a support person, give them this info:\n"
        "Stop code: CRITICAL_PROCESS_DIED"
    )
    right_label = tk.Label(qr_info_frame, text=right_text, font=("Segoe UI", 14),
                           fg="white", bg="#0078D7", justify="left", anchor="nw")
    right_label.pack(side="left", padx=20)


    # Progress animation thread
    def animate_progress():
        for i in range(1, 101):
            if stop_event.is_set():
                return  # Exit if window was closed
            progress_var.set(f"{i}% complete")
            time.sleep(5)
        if not stop_event.is_set():
            if ENABLE_FAKE_RESTART:
                threading.Thread(target=fake_restart_screen, daemon=True).start()
            restart_pc()

    threading.Thread(target=animate_progress, daemon=True).start()
    root.mainloop()

def fake_restart_screen():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")
    root.attributes("-topmost", True)
    root.overrideredirect(True)

    label = tk.Label(root, text="Restarting...", font=("Segoe UI", 20),
                     fg="white", bg="black")
    label.pack(expand=True)

    def end():
        time.sleep(3)
        root.destroy()

    threading.Thread(target=end).start()
    root.mainloop()

def mess_with_mouse():
    while True:
        x, y = pyautogui.position()
        pyautogui.moveTo(x, y, duration=0.5)
        time.sleep(0.1)

if ENABLE_PRANK:
    threading.Thread(target=mess_with_mouse, daemon=True).start()
    fake_bsod()
