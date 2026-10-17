ASSISTANT_NAME = "Clowdy"
ASSISTANT_NAME_UPPER = "CLOWDY"
MODEL_BADGE = "MWAEL.DEV"
SYSTEM_SUBTITLE = "Expressive Desktop Intelligence"
BUILD_NAME = "Clowdy"
STARTUP_APP_NAME = "CLOWDY_MWAEL_DEV"
LEGACY_STARTUP_APP_NAMES = ("CLOWDY_MARK_XXX", "CLOWDY_MWAEL_DEV")
OWNER_WEBSITE = "https://itsmohamedwael.info"


def normalize_assistant_text(text):
    if not isinstance(text, str) or not text:
        return text

    normalized = text
    replacements = (
        ("J.A.R.V.I.S.", ASSISTANT_NAME_UPPER),
        ("J.A.R.V.I.S", ASSISTANT_NAME_UPPER),
        ("CLOWDY", ASSISTANT_NAME_UPPER),
        ("Clowdy", ASSISTANT_NAME),
        ("clowdy", ASSISTANT_NAME.lower()),
        ("Tony Stark's AI assistant", "an expressive desktop AI assistant"),
    )

    for old, new in replacements:
        normalized = normalized.replace(old, new)

    return normalized
