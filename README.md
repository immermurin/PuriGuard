# PuriGuard
PuriGuard is an AI-powered content scanner that detects NSFW (Not Safe for Work) material from URLs, text, and images. Built with TensorFlow and Flask, it optionally triggers a prank (like a fake BSOD) when explicit content is detected. Designed for content filtering, monitoring, or creative deterrence.


# PuriGuard 🚫🛡️  
**AI-powered NSFW content scanner with prank-triggering capabilities**

PuriGuard is a content moderation and prank utility built with Python, TensorFlow, and Flask. It detects NSFW material in URLs, text, and image frames using a MobileNet-based deep learning model — and if NSFW content is detected, it can trigger a hilarious prank (like a fake BSOD or system restart screen) as a deterrent.

---

## 🔍 Features

- 🔗 **URL Scanner** – Extracts text and images from a web page to scan for explicit content.
- 📝 **Text Filter** – Checks input text for blocked keywords (e.g., "porn", "xxx", "casino").
- 🖼️ **Image Frame Detection** – Uses a pretrained NSFW model (MobileNet) to detect inappropriate image content.
- 🎭 **Prank Trigger** – Launches a prank GUI (e.g., fake BSOD) when NSFW content is found.
- 🐶 **Watchdog Integration** – Monitors file activity (optional `nsfw_watchdog` integration).

---

## 🧰 Technologies Used

- Python 3.8+
- Flask (API)
- TensorFlow / Keras
- TensorFlow Hub
- Pillow, BeautifulSoup
- PyAutoGUI & Tkinter (for pranks)

---

## 🚀 Installation

````bash
git clone https://github.com/yourusername/PuriGuard.git
cd PuriGuard
pip install -r requirements.txt


⚠️ Ensure you have prank.py or bsod.exe and the NSFW model (nsfw_mobilenet2.224x224.h5) in the root folder.

🧠 NSFW Model
PuriGuard uses nsfw_mobilenet2.224x224.h5 trained to detect:
- neutral, drawings, hentai, porn, sexy
Download and place it in the project directory.

🖥️ Usage
python nsfw_api.py
This will start the Flask server on port 6969.

You can now send POST requests to:
- /scan-url
POST /scan-url
{
  "url": "https://example.com"
}

- /scan-text
POST /scan-text
{
  "text": "casino and xxx links here"
}

- /scan-frame
POST /scan-frame
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA..."
}

- /trigger-prank
POST /trigger-prank
Triggers either prank.py or bsod.exe (configurable).

📁 Project Structure
PuriGuard/
├── nsfw_api.py                  # Main Flask API server
├── prank.py                     # Fake BSOD prank script
├── bsod.exe                     # Optional prank executable
├── nsfw_mobilenet2.224x224.h5   # NSFW detection model
├── nsfw_watchdog.py             # Optional file monitor
├── requirements.txt
└── README.md


🔐 License
MIT License — use it responsibly and ethically.
This tool is for educational and preventive purposes only.

🙋 Author
Built by John Emmanuel Sevilla
If you enjoyed this, give it a ⭐ and Rickroll responsibly.
---

Would you like me to generate the `requirements.txt` based on your current code?
