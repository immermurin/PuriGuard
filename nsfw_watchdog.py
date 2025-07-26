import os
import shutil
import time
import threading
import uuid
import cv2
from nsfw_detector import predict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ------------------------
# CONFIGURATION
# ------------------------

WATCHED_FOLDERS = [
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Videos"),
    os.path.expanduser("~/Desktop")
]

SUPPORTED_EXTS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp',
                  '.mp4', '.mkv', '.avi', '.mov', '.wmv']

#PRANK_SCRIPT = "prank.py"

NSFW_THRESHOLD = 0.3
FRAME_INTERVAL = 5  # seconds
NSFW_MODEL_PATH = "nsfw_mobilenet2.224x224"  # Ensure this exists

SUSPICIOUS_KEYWORDS = [
    "xxx", "porn", "hentai", "onlyfans", "nsfw", "nude", "casino", "bet", "18+", "adult"
]

# ------------------------
# LOAD NSFW MODEL
# ------------------------

print("Loading NSFW model...")
model = predict.load_model(NSFW_MODEL_PATH)
print("Model loaded successfully.")

# ------------------------
# IMAGE DETECTION
# ------------------------

def is_image_nsfw(image_path):
    result = predict.classify(model, image_path)
    probs = result[image_path]
    return probs['porn'] + probs['sexy'] > 0.7

# ------------------------
# VIDEO DETECTION
# ------------------------

def is_video_nsfw(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_gap = int(fps * FRAME_INTERVAL)
        total_frames = 0
        nsfw_hits = 0
        i = 0

        while cap.isOpened():
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                break

            temp_path = f"temp_frame_{uuid.uuid4().hex}.jpg"
            cv2.imwrite(temp_path, frame)

            if is_image_nsfw(temp_path):
                nsfw_hits += 1

            total_frames += 1
            i += frame_gap

            if os.path.exists(temp_path):
                os.remove(temp_path)

        cap.release()

        nsfw_ratio = nsfw_hits / max(total_frames, 1)
        print(f"[Video Scan] {video_path}: NSFW ratio = {nsfw_ratio:.2f}")
        return nsfw_ratio > NSFW_THRESHOLD

    except Exception as e:
        print(f"[Error] Video scan failed: {e}")
        return False

# ------------------------
# TRIGGER PRANK
# ------------------------

def trigger_prank():
    print("[PRANK] Triggering BSOD prank...")
    #os.system(f'python {PRANK_SCRIPT}')
    os.system("bsod.exe")

# ------------------------
# EVENT HANDLER
# ------------------------

class NSFWFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        filepath = event.src_path
        filename = os.path.basename(filepath).lower()
        _, ext = os.path.splitext(filepath)
        ext = ext.lower()

        if ext not in SUPPORTED_EXTS:
            return

        time.sleep(2)  # Allow file to finish writing

        print(f"[Detected] New file: {filepath}")

        try:
            # Check suspicious keywords
            if any(keyword in filename for keyword in SUSPICIOUS_KEYWORDS):
                print(f"[Keyword Match] Suspicious file name: {filename}")
                os.remove(filepath)
                trigger_prank()
                return

            # Run NSFW scan
            if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']:
                if is_image_nsfw(filepath):
                    print(f"[NSFW Detected] Deleting image: {filepath}")
                    os.remove(filepath)
                    trigger_prank()

            elif ext in ['.mp4', '.mkv', '.avi', '.mov', '.wmv']:
                if is_video_nsfw(filepath):
                    print(f"[NSFW Detected] Deleting video: {filepath}")
                    os.remove(filepath)
                    trigger_prank()

        except Exception as e:
            print(f"[Error] Problem processing file: {e}")

# ------------------------
# START WATCHDOG
# ------------------------

def start_monitoring():
    observer = Observer()
    handler = NSFWFileHandler()

    for folder in WATCHED_FOLDERS:
        if os.path.exists(folder):
            observer.schedule(handler, folder, recursive=True)
            print(f"[Watching] {folder}")

    observer.start()
    print("[Monitoring Started]")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# ------------------------
# ENTRY POINT
# ------------------------

if __name__ == "__main__":
    start_monitoring()
