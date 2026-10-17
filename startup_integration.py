"""
startup_integration.py
Register / unregister CLOWDY in the Windows current-user Run key so it
starts automatically when the user logs in.
"""

import sys
import winreg
from pathlib import Path

from branding import ASSISTANT_NAME, LEGACY_STARTUP_APP_NAMES, STARTUP_APP_NAME

APP_NAME = STARTUP_APP_NAME
_RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


def _exe_cmd() -> str:
    """
    Returns the shell command that should be stored in the registry.
    - Frozen (PyInstaller) build  → path to the .exe
    - Running as .py script       → pythonw.exe "<main.py path>"  (no console window)
    """
    if getattr(sys, "frozen", False):
        return f'"{sys.executable}"'
    python_exe = Path(sys.executable)
    pythonw = python_exe.parent / "pythonw.exe"
    if not pythonw.exists():
        pythonw = python_exe
    main_py = Path(__file__).resolve().parent / "main.py"
    return f'"{pythonw}" "{main_py}"'


def _delete_value_if_exists(key, value_name: str) -> bool:
    try:
        winreg.DeleteValue(key, value_name)
        return True
    except FileNotFoundError:
        return False


def register_startup() -> str:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _RUN_KEY, 0, winreg.KEY_SET_VALUE)
        for legacy_name in LEGACY_STARTUP_APP_NAMES:
            if legacy_name != APP_NAME:
                _delete_value_if_exists(key, legacy_name)
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, _exe_cmd())
        winreg.CloseKey(key)
        return f"✅  {ASSISTANT_NAME} will now start automatically when you log in."
    except Exception as exc:
        return f"⚠  Could not register startup entry: {exc}"


def unregister_startup() -> str:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _RUN_KEY, 0, winreg.KEY_SET_VALUE)
        removed = _delete_value_if_exists(key, APP_NAME)
        for legacy_name in LEGACY_STARTUP_APP_NAMES:
            if _delete_value_if_exists(key, legacy_name):
                removed = True
        winreg.CloseKey(key)
        if removed:
            return f"✅  {ASSISTANT_NAME} removed from Windows startup."
        return f"{ASSISTANT_NAME} was not registered for auto-start."
    except FileNotFoundError:
        return f"{ASSISTANT_NAME} was not registered for auto-start."
    except Exception as exc:
        return f"⚠  Could not remove startup entry: {exc}"


def is_registered() -> bool:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _RUN_KEY, 0, winreg.KEY_READ)
        try:
            for value_name in [APP_NAME] + list(LEGACY_STARTUP_APP_NAMES):
                try:
                    winreg.QueryValueEx(key, value_name)
                    winreg.CloseKey(key)
                    return True
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
            return False
        except Exception:
            winreg.CloseKey(key)
            return False
    except (FileNotFoundError, Exception):
        return False


def manage_startup(parameters: dict, player=None) -> str:
    """Tool entry-point called by ClowdyLive._execute_tool."""
    action = (parameters.get("action") or "status").lower()
    if action in ("register", "enable", "add", "on"):
        return register_startup()
    if action in ("unregister", "disable", "remove", "off"):
        return unregister_startup()
    if is_registered():
        return f"✅  {ASSISTANT_NAME} is currently registered to start with Windows."
    return f"{ASSISTANT_NAME} is NOT set to start automatically with Windows."
