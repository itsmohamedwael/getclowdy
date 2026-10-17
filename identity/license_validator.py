import os
import sys
import uuid
import socket
import json
import shutil
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent

def self_destruct():
    # Show user-friendly expiration warning
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning(
            "Trial Expired",
            "Your 7-day trial of Clowdy has expired.\nThe application will now automatically deactivate and remove its executable from your PC."
        )
        root.destroy()
    except Exception:
        pass

    # Windows self-deletion batch script
    exe_path = sys.executable if getattr(sys, "frozen", False) else __file__
    bat_path = Path(os.environ.get("TEMP", "")) / "clowdy_cleanup.bat"
    
    bat_content = f"""@echo off
:loop
tasklist | find /i "{Path(exe_path).name}" >nul
if not errorlevel 1 (
    timeout /t 1 >nul
    goto loop
)
del /f /q "{exe_path}"
del "%~f0"
"""
    try:
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write(bat_content)
        # Execute batch file detached and silently
        subprocess.Popen(["cmd.exe", "/c", str(bat_path)], creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception:
        pass

def verify_license_interactive() -> bool:
    base_dir = get_base_dir()
    license_file = base_dir / "config" / "license_key.json"
    
    # Generate unique HWID
    try:
        import uuid
        hwid = str(uuid.getnode())
    except Exception:
        hwid = socket.gethostname()
        
    license_key = None
    if license_file.exists():
        try:
            with open(license_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                license_key = data.get("license_key")
        except Exception:
            pass

    if license_key:
        # Validate silently against server first
        url = "https://www.getclowdynow.xyz/api/license/validate"
        payload = {
            "licenseKey": license_key.strip(),
            "hwid": hwid,
            "deviceName": socket.gethostname()
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Clowdy Desktop App"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=4) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                if res_data.get("success"):
                    return True # Valid! Start the app immediately
        except Exception:
            pass

    # Show advanced UI for activation since no key is stored or validation failed
    import tkinter as tk
    import ctypes
    
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

    dialog = tk.Tk()
    dialog.title("Clowdy License Activation")
    
    W = 480
    H = 360
    sw = dialog.winfo_screenwidth()
    sh = dialog.winfo_screenheight()
    dialog.geometry(f"{W}x{H}+{(sw-W)//2}+{(sh-H)//2}")
    dialog.resizable(False, False)
    
    C_BG     = "#0E0E11"
    C_PRI    = "#6366F1"
    C_DIM    = "#18181B"
    C_MID    = "#27272A"
    C_TEXT   = "#F4F4F6"
    C_MUTED  = "#8E9196"
    C_RED    = "#EF4444"
    C_GREEN  = "#10B981"
    FONT_FAMILY = "Segoe UI"
    
    dialog.configure(bg=C_BG)
    
    activated = [False]
    
    # Title / Branding
    logo_label = tk.Label(
        dialog, text="CLOWDY.", fg=C_PRI, bg=C_BG,
        font=(FONT_FAMILY, 24, "bold")
    )
    logo_label.pack(pady=(28, 4))
    
    subtitle_label = tk.Label(
        dialog, text="EXPRESSIVE DESKTOP INTELLIGENCE", fg=C_MUTED, bg=C_BG,
        font=(FONT_FAMILY, 8, "bold")
    )
    subtitle_label.pack(pady=(0, 20))
    
    inst_label = tk.Label(
        dialog, text="Please enter your Clowdy License Key to activate systems:",
        fg=C_TEXT, bg=C_BG, font=(FONT_FAMILY, 10), wraplength=400
    )
    inst_label.pack(pady=(0, 10))
    
    # Input Frame
    input_frame = tk.Frame(dialog, bg=C_BG)
    input_frame.pack(fill="x", padx=40)
    
    entry_var = tk.StringVar()
    entry = tk.Entry(
        input_frame, textvariable=entry_var, fg=C_TEXT, bg=C_DIM,
        insertbackground=C_TEXT, font=(FONT_FAMILY, 11), borderwidth=1,
        relief="solid", highlightthickness=0, justify="center"
    )
    entry.configure(highlightbackground=C_MID, highlightcolor=C_PRI)
    entry.pack(fill="x", ipady=8)
    
    # Status / Error Label
    status_label = tk.Label(
        dialog, text="", fg=C_RED, bg=C_BG, font=(FONT_FAMILY, 9), wraplength=400
    )
    status_label.pack(pady=(8, 8))
    
    # Website Link
    link_label = tk.Label(
        dialog, text="Don't have a license? Register on the Clowdy website",
        fg=C_PRI, bg=C_BG, font=(FONT_FAMILY, 9, "underline"), cursor="hand2"
    )
    link_label.pack(pady=(0, 14))
    
    import webbrowser
    def open_web(e):
        webbrowser.open("https://clowdy-website-ci9q48304-mwintelleginces-projects.vercel.app/signup")
        
    link_label.bind("<Button-1>", open_web)
    
    def on_activate():
        key = entry_var.get().strip()
        if not key:
            status_label.config(text="Please enter a license key.", fg=C_RED)
            return
            
        status_label.config(text="Verifying license key...", fg=C_MUTED)
        dialog.update()
        
        # Validate against server
        url = "https://www.getclowdynow.xyz/api/license/validate"
        payload = {
            "licenseKey": key,
            "hwid": hwid,
            "deviceName": socket.gethostname()
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Clowdy Desktop App"},
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=6) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                if res_data.get("success"):
                    license_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(license_file, "w", encoding="utf-8") as f:
                        json.dump({"license_key": key}, f, indent=2)
                    
                    status_label.config(text="License activated successfully!", fg=C_GREEN)
                    activated[0] = True
                    dialog.update()
                    dialog.after(1000, dialog.destroy)
                else:
                    err_msg = res_data.get("error", "Activation failed.")
                    status_label.config(text=err_msg, fg=C_RED)
        except urllib.error.HTTPError as e:
            try:
                err_data = json.loads(e.read().decode("utf-8"))
                err_msg = err_data.get("error", "Invalid or expired key.")
            except Exception:
                err_msg = "Invalid or expired license key."
            status_label.config(text=err_msg, fg=C_RED)
        except Exception:
            status_label.config(text="Connection error. Could not reach activation server.", fg=C_RED)
            
    btn_frame = tk.Frame(dialog, bg=C_BG)
    btn_frame.pack(fill="x", padx=40, pady=2)
    
    activate_btn = tk.Button(
        btn_frame, text="ACTIVATE CLOWDY", command=on_activate,
        bg=C_PRI, fg=C_TEXT, activebackground=C_PRI, activeforeground=C_TEXT,
        font=(FONT_FAMILY, 10, "bold"), borderwidth=0, cursor="hand2", pady=8
    )
    activate_btn.pack(fill="x")
    
    entry.bind("<Return>", lambda e: on_activate())
    entry.focus_set()
    
    dialog.mainloop()
    return activated[0]

def check_license_and_self_destruct():
    base_dir = get_base_dir()
    license_file = base_dir / "config" / "license_key.json"
    
    # Generate unique HWID
    try:
        import uuid
        hwid = str(uuid.getnode())
    except Exception:
        hwid = socket.gethostname()
 
    license_key = None
    if license_file.exists():
        try:
            with open(license_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                license_key = data.get("license_key")
        except Exception:
            pass
 
    if not license_key:
        sys.exit(0)
 
    # Validate against server
    url = "https://www.getclowdynow.xyz/api/license/validate"
    payload = {
        "licenseKey": license_key.strip(),
        "hwid": hwid,
        "deviceName": socket.gethostname()
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "Clowdy Desktop App"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            if res_data.get("success"):
                return
            else:
                if res_data.get("deleteSelf") or res_data.get("expired"):
                    self_destruct()
                    sys.exit(0)
                raise Exception("Activation failed.")
    except urllib.error.HTTPError as e:
        try:
            err_data = json.loads(e.read().decode("utf-8"))
            if err_data.get("deleteSelf") or err_data.get("expired"):
                self_destruct()
                sys.exit(0)
        except Exception:
            pass
        sys.exit(0)
    except Exception as e:
        sys.exit(0)
