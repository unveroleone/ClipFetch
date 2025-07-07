# iOS Video & Audio Downloader API

This repository provides a minimal Flask-based API for downloading videos or audio from platforms like YouTube and TikTok. It is designed to work seamlessly with iOS Shortcuts and is especially well-suited for home server setups.

---

## 📌 Overview

This tool allows users to send a POST request from iOS Shortcuts to a local or remote server. The server processes the request using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp), downloads the desired media in the requested format, and returns a temporary download URL.

---
### 🔗 iOS Shortcut Link

Use the following link to integrate with your iOS Shortcuts:

[IPhone-Shortcut](https://www.icloud.com/shortcuts/71162fb38fda4f02963de61d52aae969)

---

## 🏠 Recommended: Home Server Setup

Running this project on a home server (e.g., Raspberry Pi, macOS, or Windows machine) is highly recommended:

- No need for cookies
- No IP bans from YouTube
- Private, local access from iOS devices
- Compatible with tools like DuckDNS or ZeroTier for remote access

---

## ⚠️ VPS Limitations

If deployed on a public VPS, you may experience issues such as:

- YouTube blocking public IPs
- CAPTCHA requirements
- Frequent expiration of cookies

To mitigate this, use a `cookies.txt` file extracted from a logged-in browser session. However, note that cookies often become invalid after a few requests when using public IPs.

---

## Installation

### Requirements

- Python 3.7+
- `yt-dlp`
- `ffmpeg` 
- Optional: `cookies.txt` for VPS use

### Steps

```bash
git clone https://github.com/unveroleone/ClipFetch.git
cd ClipFetch
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To run the server:

```bash
python server.py
```

The API will be available at:
```
http://<your-ip>:5000/download
```

---


## Project Structure

```
ClipFetch/
├── server.py           # Main Flask app
├── requirements.txt    # Python dependencies
├── cookies.txt         # Optional: YouTube login cookies for VPS
└── yt-downloads/       # Temporary storage for downloaded files
```

---

## Security Note

This project does not implement authentication. If exposed to the internet, it is strongly recommended to:

- Restrict access via firewall or IP whitelisting
- Use it behind a VPN or within a private network
- Avoid exposing it to unknown users

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements or encounter any issues, feel free to:

1. Fork the repository and submit a pull request.
2. Create an issue on GitHub to report bugs or suggest features.

Your feedback helps make this project better for everyone!  