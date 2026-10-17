"""
identity/user_profile.py
User profile management: first-run detection, IP tracking, onboarding, and
device-verification (PIN check when launching from an unknown IP/location).
"""

import json
import re
import socket
import sys
import urllib.request
from pathlib import Path
from threading import Lock

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

def _base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


BASE_DIR     = _base_dir()
PROFILE_PATH = BASE_DIR / "config" / "user_profile.json"
_lock        = Lock()

# ---------------------------------------------------------------------------
# Default profile
# ---------------------------------------------------------------------------

def _empty_profile() -> dict:
    return {
        "name":           "",
        "nickname":       "",
        "age":            "",
        "city":           "",
        "language":       "en",
        "last_ip":        "",
        "known_ips":      [],
        "setup_complete": False,
        "security_pin":   "",
    }

# ---------------------------------------------------------------------------
# Load / save
# ---------------------------------------------------------------------------

def load_profile() -> dict:
    if not PROFILE_PATH.exists():
        return _empty_profile()
    with _lock:
        try:
            data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else _empty_profile()
        except Exception:
            return _empty_profile()


def save_profile(profile: dict) -> None:
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        PROFILE_PATH.write_text(
            json.dumps(profile, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

# ---------------------------------------------------------------------------
# Networking helpers
# ---------------------------------------------------------------------------

def get_local_ip() -> str:
    """Returns the machine's LAN IP (used for device fingerprinting)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# ---------------------------------------------------------------------------
# Profile queries
# ---------------------------------------------------------------------------

def is_first_run() -> bool:
    profile = load_profile()
    if profile.get("setup_complete", False):
        return False

    try:
        base_dir = _base_dir()
        license_file = base_dir / "config" / "license_key.json"
        if license_file.exists():
            with open(license_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("license_key") == "CLOWDY-OWNER-INFINITE-TEST-KEY-999":
                    complete_setup(
                        name="Admin",
                        nickname="Admin",
                        age="20",
                        city="Cairo",
                        language="en"
                    )
                    return False
    except Exception:
        pass

    return True


def is_known_ip() -> bool:
    profile    = load_profile()
    current_ip = get_local_ip()
    return current_ip in profile.get("known_ips", [])


def get_user_name() -> str:
    """Returns the preferred display name (nickname or full name or 'sir')."""
    profile = load_profile()
    return (profile.get("nickname") or profile.get("name") or "").strip() or "sir"


def get_security_pin() -> str:
    return load_profile().get("security_pin", "")

# ---------------------------------------------------------------------------
# Mutating helpers
# ---------------------------------------------------------------------------

def register_current_ip() -> None:
    """Add the current LAN IP to the list of trusted IPs."""
    profile    = load_profile()
    current_ip = get_local_ip()
    known      = profile.get("known_ips", [])
    if current_ip not in known:
        known.append(current_ip)
    profile["known_ips"] = known
    profile["last_ip"]   = current_ip
    save_profile(profile)


def complete_setup(
    name:         str,
    nickname:     str = "",
    age:          str = "",
    city:         str = "",
    language:     str = "en",
    security_pin: str = "",
) -> None:
    """
    Persist a newly-completed onboarding session.
    Also writes the name into the long-term memory so CLOWDY refers to the
    user by name immediately.
    """
    profile                    = load_profile()
    profile["name"]            = name.strip()
    profile["nickname"]        = (nickname.strip() or name.strip())
    profile["age"]             = age.strip()
    profile["city"]            = city.strip()
    profile["language"]        = language.strip() or "en"
    profile["security_pin"]    = security_pin.strip()
    profile["setup_complete"]  = True
    profile["last_ip"]         = get_local_ip()

    known = profile.get("known_ips", [])
    ip    = get_local_ip()
    if ip not in known:
        known.append(ip)
    profile["known_ips"] = known
    save_profile(profile)

    # Mirror identity into the CLOWDY memory system
    try:
        from memory.memory_manager import update_memory
        payload: dict = {"identity": {}}
        if profile["name"]:
            payload["identity"]["name"] = {"value": profile["name"]}
        if profile["city"]:
            payload["identity"]["city"] = {"value": profile["city"]}
        if profile["age"]:
            payload["identity"]["age"] = {"value": profile["age"]}
        if payload["identity"]:
            update_memory(payload)
    except Exception:
        pass


def verify_pin(entered: str) -> bool:
    """Returns True if the entered PIN matches the stored one."""
    stored = get_security_pin()
    if not stored:
        return True          # no PIN set → allow
    return entered.strip() == stored.strip()
