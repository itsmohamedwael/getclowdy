# ☁️ Clowdy — Next-Gen Real-time Desktop AI Companion

[![GitHub](https://img.shields.io/badge/GitHub-getclowdy-blue?logo=github)](https://github.com/itsmohamedwael/getclowdy)
[![Gemini](https://img.shields.io/badge/Gemini-3.6%20Flash-orange?logo=google)](https://ai.google.dev/)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011-0078D6?logo=windows)](https://microsoft.com)

**Clowdy** is an ultra-fast, expressive real-time desktop AI companion with full system automation, screen & camera vision, customizable voice presets, and authentic Egyptian Arabic & English conversational intelligence.

---

## ✨ Key Features

- 🎙️ **Real-Time Live Voice**: Powered by Google Gemini 3.6 Flash live bidirectional streaming audio for ultra-low latency conversations.
- 🇪🇬 **Authentic Egyptian Personality & Dialect**: Speaks natural, fluent Egyptian Arabic (العامية المصرية) and English, complete with humour, emotion, internet culture, and melodic singing capability.
- 👁️ **Multimodal Computer Vision**: Real-time screen analysis, desktop tracking, and webcam vision with zero lag.
- 💻 **Complete Windows Automation**:
  - Launch and control applications
  - Manage files, folders, and desktop workspaces
  - Run terminal / CMD commands via natural language
  - Adjust volume, brightness, display settings, and media
- 🔐 **Secure Licensing & Identity**: Built-in cryptographic license validation, user profiles, and Windows DPAPI credential vault.
- 🚀 **Windows Startup Integration**: Seamless background launch with Windows startup management.
- 🧠 **Persistent Context & Memory**: Remembers preferences, names, and interaction context across sessions.

---

## ⚡ Quick Start

### 1. Prerequisites
- **Windows 10 / 11 (64-bit)**
- **Python 3.10+** (Python 3.12 or 3.14 recommended)
- Microphone and Speaker / Headphones
- Gemini API Key ([Google AI Studio](https://aistudio.google.com/))

### 2. Installation

```bash
git clone https://github.com/itsmohamedwael/getclowdy.git
cd getclowdy
python -m pip install -r requirements.txt
```

### 3. Run Clowdy

```bash
python main.py
```

On first launch, enter your Gemini API key and license credentials.

---

## 📁 Repository Structure

```
getclowdy/
├── actions/                  # System automation & tool modules
│   ├── browser_control.py
│   ├── cmd_control.py
│   ├── code_helper.py
│   ├── computer_control.py
│   ├── computer_settings.py
│   ├── desktop.py
│   ├── dev_agent.py
│   ├── file_controller.py
│   ├── flight_finder.py
│   ├── open_app.py
│   ├── reminder.py
│   ├── screen_processor.py   # Live screen & camera processor
│   ├── send_message.py
│   ├── weather_report.py
│   ├── web_search.py
│   └── youtube_video.py
├── agent/                    # Task planner, executor, and error recovery
├── config/                   # Configuration & license management
├── core/                     # Personality prompts & core system instructions
│   └── prompt.txt
├── identity/                 # User onboarding, vault & license verification
│   ├── account_vault.py
│   ├── license_validator.py
│   └── user_profile.py
├── memory/                   # Contextual memory management
├── branding.py               # Assistant branding & normalization
├── startup_integration.py    # Windows CurrentVersion\Run integration
├── ui.py                     # Animated desktop UI & HUD interface
├── voice_settings.py         # Voice personality presets & audio config
├── main.py                   # Main live async orchestration engine
└── requirements.txt          # Python dependencies
```

---

## 🔒 Security Notice

This repository contains the client application source only. Sensitive secrets, API keys, and local credentials (`config/api_keys.json`, `config/license_key.json`, `.env`) are excluded via `.gitignore`.
