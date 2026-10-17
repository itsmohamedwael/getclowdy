"""
identity/account_vault.py
Secure storage for user contacts, personal credentials, and accounts.
Sensitive password blobs are protected via Windows DPAPI (CryptProtectData).
"""

import base64
import json
import re
import sys
from pathlib import Path
from threading import Lock

try:
    import win32crypt
    _DPAPI = True
except ImportError:
    win32crypt = None
    _DPAPI = False


def _base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


BASE_DIR = _base_dir()
VAULT_PATH = BASE_DIR / "config" / "account_vault.json"
_LOCK = Lock()


def _empty_vault() -> dict:
    return {
        "emails": [],
        "phones": [],
        "defaults": {
            "email": "",
            "phone": "",
        },
        "accounts": [],
    }


def load_vault() -> dict:
    if not VAULT_PATH.exists():
        return _empty_vault()
    with _LOCK:
        try:
            data = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return _empty_vault()
            data.setdefault("emails", [])
            data.setdefault("phones", [])
            data.setdefault("defaults", {"email": "", "phone": ""})
            data.setdefault("accounts", [])
            return data
        except Exception:
            return _empty_vault()


def save_vault(vault: dict) -> None:
    VAULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _LOCK:
        VAULT_PATH.write_text(
            json.dumps(vault, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


def _normalize_email(value: str) -> str:
    return (value or "").strip().lower()


def _normalize_phone(value: str) -> str:
    return re.sub(r"\s+", "", (value or "").strip())


def _split_values(raw) -> list:
    if not raw:
        return []
    if isinstance(raw, list):
        parts = []
        for item in raw:
            parts.extend(_split_values(item))
        return parts
    return [p.strip() for p in re.split(r"[,;\n]+", str(raw)) if p.strip()]


def _protect_secret(secret: str) -> str:
    if not secret:
        return ""
    if not _DPAPI or win32crypt is None:
        raise RuntimeError("Windows secure encryption is unavailable on this machine.")
    encrypted = win32crypt.CryptProtectData(secret.encode("utf-8"), "CLOWDY", None, None, None, 0)
    if isinstance(encrypted, tuple):
        encrypted = encrypted[1]
    return base64.b64encode(encrypted).decode("ascii")


def _unprotect_secret(blob: str) -> str:
    if not blob:
        return ""
    if not _DPAPI or win32crypt is None:
        return ""
    try:
        decrypted = win32crypt.CryptUnprotectData(base64.b64decode(blob), None, None, None, 0)
        if isinstance(decrypted, tuple):
            decrypted = decrypted[1]
        return decrypted.decode("utf-8")
    except Exception:
        return ""


def _dedupe(values: list, normalizer=None) -> list:
    output = []
    seen = set()
    for value in values:
        norm = normalizer(value) if normalizer else value
        if norm and norm not in seen:
            seen.add(norm)
            output.append(norm)
    return output


def save_contacts(
    emails=None,
    phones=None,
    default_email: str = "",
    default_phone: str = "",
) -> dict:
    vault = load_vault()
    new_emails = _split_values(emails)
    new_phones = _split_values(phones)

    vault["emails"] = _dedupe(vault.get("emails", []) + [_normalize_email(e) for e in new_emails if e])
    vault["phones"] = _dedupe(vault.get("phones", []) + [_normalize_phone(p) for p in new_phones if p])

    defaults = vault.setdefault("defaults", {"email": "", "phone": ""})
    if default_email:
        defaults["email"] = _normalize_email(default_email)
    elif not defaults.get("email") and vault["emails"]:
        defaults["email"] = vault["emails"][0]

    if default_phone:
        defaults["phone"] = _normalize_phone(default_phone)
    elif not defaults.get("phone") and vault["phones"]:
        defaults["phone"] = vault["phones"][0]

    save_vault(vault)
    return vault


def get_default_email() -> str:
    vault = load_vault()
    defaults = vault.get("defaults", {})
    return defaults.get("email") or (vault.get("emails", [""])[0] if vault.get("emails") else "")


def get_default_phone() -> str:
    vault = load_vault()
    defaults = vault.get("defaults", {})
    return defaults.get("phone") or (vault.get("phones", [""])[0] if vault.get("phones") else "")


def _match_account(account: dict, service: str, username: str = "") -> bool:
    target_service = (service or "").strip().lower()
    if (account.get("service") or "").strip().lower() != target_service:
        return False
    if not username:
        return True
    target_user = username.strip().lower()
    options = [
        (account.get("username") or "").strip().lower(),
        (account.get("email") or "").strip().lower(),
        (account.get("label") or "").strip().lower(),
    ]
    return target_user in options


def list_account_summaries(service: str = "") -> list:
    vault = load_vault()
    summaries = []
    target = (service or "").strip().lower()
    for acc in vault.get("accounts", []):
        if target and (acc.get("service") or "").strip().lower() != target:
            continue
        summaries.append({
            "service": acc.get("service", ""),
            "username": acc.get("username", ""),
            "email": acc.get("email", ""),
            "phone": acc.get("phone", ""),
            "label": acc.get("label", ""),
            "notes": acc.get("notes", ""),
        })
    return summaries


def get_account(service: str, username: str = "", include_password: bool = False) -> dict:
    vault = load_vault()
    for acc in vault.get("accounts", []):
        if _match_account(acc, service, username):
            res = dict(acc)
            blob = res.pop("password_blob", "")
            if include_password and blob:
                res["password"] = _unprotect_secret(blob)
            return res
    return {}


def save_account(
    service: str,
    username: str = "",
    email: str = "",
    phone: str = "",
    password: str = "",
    label: str = "",
    notes: str = "",
) -> dict:
    service_name = (service or "").strip().lower()
    if not service_name:
        raise ValueError("service is required")

    username_val = (username or "").strip()
    email_val = _normalize_email(email)
    phone_val = _normalize_phone(phone)

    if not username_val and not email_val:
        raise ValueError("username or email is required")

    vault = load_vault()
    existing_index = -1
    for idx, acc in enumerate(vault.get("accounts", [])):
        if _match_account(acc, service_name, username_val or email_val):
            existing_index = idx
            break

    payload = {
        "service": service_name,
        "username": username_val,
        "email": email_val,
        "phone": phone_val,
        "label": (label or "").strip(),
        "notes": (notes or "").strip(),
    }
    if password:
        payload["password_blob"] = _protect_secret(password)

    if existing_index >= 0:
        current = vault["accounts"][existing_index]
        for k, v in payload.items():
            if v or k == "password_blob":
                current[k] = v
    else:
        vault.setdefault("accounts", []).append(payload)

    if email_val and email_val not in vault.get("emails", []):
        vault.setdefault("emails", []).append(email_val)
    if phone_val and phone_val not in vault.get("phones", []):
        vault.setdefault("phones", []).append(phone_val)

    save_vault(vault)
    return payload


def update_password(service: str, username: str, password: str) -> dict:
    if not password:
        raise ValueError("password is required")
    vault = load_vault()
    encrypted = _protect_secret(password)
    for acc in vault.get("accounts", []):
        if _match_account(acc, service, username):
            acc["password_blob"] = encrypted
            save_vault(vault)
            return acc
    raise ValueError("account not found")


def remove_email(email: str) -> bool:
    target = _normalize_email(email)
    vault = load_vault()
    orig = list(vault.get("emails", []))
    vault["emails"] = [e for e in orig if e != target]
    if vault.get("defaults", {}).get("email") == target:
        vault["defaults"]["email"] = vault["emails"][0] if vault["emails"] else ""
    changed = len(orig) != len(vault["emails"])
    if changed:
        save_vault(vault)
    return changed


def remove_phone(phone: str) -> bool:
    target = _normalize_phone(phone)
    vault = load_vault()
    orig = list(vault.get("phones", []))
    vault["phones"] = [p for p in orig if p != target]
    if vault.get("defaults", {}).get("phone") == target:
        vault["defaults"]["phone"] = vault["phones"][0] if vault["phones"] else ""
    changed = len(orig) != len(vault["phones"])
    if changed:
        save_vault(vault)
    return changed


def remove_account(service: str, username: str = "") -> bool:
    vault = load_vault()
    orig = list(vault.get("accounts", []))
    vault["accounts"] = [a for a in orig if not _match_account(a, service, username)]
    changed = len(orig) != len(vault["accounts"])
    if changed:
        save_vault(vault)
    return changed


def prepare_signup(service: str = "") -> dict:
    return {
        "service": (service or "").strip().lower(),
        "default_email": get_default_email(),
        "default_phone": get_default_phone(),
        "emails": load_vault().get("emails", []),
        "phones": load_vault().get("phones", []),
        "known_accounts": list_account_summaries(service),
    }
