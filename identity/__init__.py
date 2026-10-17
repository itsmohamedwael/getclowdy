"""
identity package
Handles user profiles, license validation, and account credentials vault.
"""

from .user_profile import (
    load_profile,
    save_profile,
    is_first_run,
    is_known_ip,
    get_user_name,
    get_security_pin,
    register_current_ip,
    complete_setup,
    verify_pin,
)
from .license_validator import (
    verify_license_interactive,
    validate_stored_license,
)
from .account_vault import (
    load_vault,
    save_vault,
    save_contacts,
    get_default_email,
    get_default_phone,
    list_account_summaries,
    get_account,
    save_account,
    update_password,
    remove_email,
    remove_phone,
    remove_account,
    prepare_signup,
)

__all__ = [
    "load_profile",
    "save_profile",
    "is_first_run",
    "is_known_ip",
    "get_user_name",
    "get_security_pin",
    "register_current_ip",
    "complete_setup",
    "verify_pin",
    "verify_license_interactive",
    "validate_stored_license",
    "load_vault",
    "save_vault",
    "save_contacts",
    "get_default_email",
    "get_default_phone",
    "list_account_summaries",
    "get_account",
    "save_account",
    "update_password",
    "remove_email",
    "remove_phone",
    "remove_account",
    "prepare_signup",
]
