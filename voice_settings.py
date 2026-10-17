from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


BASE_DIR = get_base_dir()
CONFIG_DIR = BASE_DIR / "config"
CONFIG_FILE = CONFIG_DIR / "voice_settings.json"

VOICE_LIBRARY = (   ('Achernar', 'Soft'),
    ('Achird', 'Friendly'),
    ('Algenib', 'Gravelly'),
    ('Algieba', 'Smooth'),
    ('Alnilam', 'Firm'),
    ('Aoede', 'Breezy'),
    ('Autonoe', 'Bright'),
    ('Callirrhoe', 'Easy-going'),
    ('Charon', 'Informative'),
    ('Despina', 'Smooth'),
    ('Enceladus', 'Breathy'),
    ('Erinome', 'Clear'),
    ('Fenrir', 'Excitable'),
    ('Gacrux', 'Mature'),
    ('Iapetus', 'Clear'),
    ('Kore', 'Firm'),
    ('Laomedeia', 'Upbeat'),
    ('Leda', 'Youthful'),
    ('Orus', 'Firm'),
    ('Puck', 'Upbeat'),
    ('Pulcherrima', 'Forward'),
    ('Rasalgethi', 'Informative'),
    ('Sadachbia', 'Lively'),
    ('Sadaltager', 'Knowledgeable'),
    ('Schedar', 'Even'),
    ('Sulafat', 'Warm'),
    ('Umbriel', 'Easy-going'),
    ('Vindemiatrix', 'Gentle'),
    ('Zephyr', 'Bright'),
    ('Zubenelgenubi', 'Casual'))

VOICE_LABELS = {   'Achernar': 'Achernar - Soft',
    'Achird': 'Achird - Friendly',
    'Algenib': 'Algenib - Gravelly',
    'Algieba': 'Algieba - Smooth',
    'Alnilam': 'Alnilam - Firm',
    'Aoede': 'Aoede - Breezy',
    'Autonoe': 'Autonoe - Bright',
    'Callirrhoe': 'Callirrhoe - Easy-going',
    'Charon': 'Charon - Informative',
    'Despina': 'Despina - Smooth',
    'Enceladus': 'Enceladus - Breathy',
    'Erinome': 'Erinome - Clear',
    'Fenrir': 'Fenrir - Excitable',
    'Gacrux': 'Gacrux - Mature',
    'Iapetus': 'Iapetus - Clear',
    'Kore': 'Kore - Firm',
    'Laomedeia': 'Laomedeia - Upbeat',
    'Leda': 'Leda - Youthful',
    'Orus': 'Orus - Firm',
    'Puck': 'Puck - Upbeat',
    'Pulcherrima': 'Pulcherrima - Forward',
    'Rasalgethi': 'Rasalgethi - Informative',
    'Sadachbia': 'Sadachbia - Lively',
    'Sadaltager': 'Sadaltager - Knowledgeable',
    'Schedar': 'Schedar - Even',
    'Sulafat': 'Sulafat - Warm',
    'Umbriel': 'Umbriel - Easy-going',
    'Vindemiatrix': 'Vindemiatrix - Gentle',
    'Zephyr': 'Zephyr - Bright',
    'Zubenelgenubi': 'Zubenelgenubi - Casual'}

VOICE_DESCRIPTORS = {   'Achernar': 'Soft',
    'Achird': 'Friendly',
    'Algenib': 'Gravelly',
    'Algieba': 'Smooth',
    'Alnilam': 'Firm',
    'Aoede': 'Breezy',
    'Autonoe': 'Bright',
    'Callirrhoe': 'Easy-going',
    'Charon': 'Informative',
    'Despina': 'Smooth',
    'Enceladus': 'Breathy',
    'Erinome': 'Clear',
    'Fenrir': 'Excitable',
    'Gacrux': 'Mature',
    'Iapetus': 'Clear',
    'Kore': 'Firm',
    'Laomedeia': 'Upbeat',
    'Leda': 'Youthful',
    'Orus': 'Firm',
    'Puck': 'Upbeat',
    'Pulcherrima': 'Forward',
    'Rasalgethi': 'Informative',
    'Sadachbia': 'Lively',
    'Sadaltager': 'Knowledgeable',
    'Schedar': 'Even',
    'Sulafat': 'Warm',
    'Umbriel': 'Easy-going',
    'Vindemiatrix': 'Gentle',
    'Zephyr': 'Bright',
    'Zubenelgenubi': 'Casual'}

SUPPORTED_VOICE_NAMES = {   'Achernar',
    'Achird',
    'Algenib',
    'Algieba',
    'Alnilam',
    'Aoede',
    'Autonoe',
    'Callirrhoe',
    'Charon',
    'Despina',
    'Enceladus',
    'Erinome',
    'Fenrir',
    'Gacrux',
    'Iapetus',
    'Kore',
    'Laomedeia',
    'Leda',
    'Orus',
    'Puck',
    'Pulcherrima',
    'Rasalgethi',
    'Sadachbia',
    'Sadaltager',
    'Schedar',
    'Sulafat',
    'Umbriel',
    'Vindemiatrix',
    'Zephyr',
    'Zubenelgenubi'}

DEFAULT_PREVIEW_LINE = ('Hey, this version sounds more natural. Tell me if you want it warmer, '
 'deeper, brighter, or more cinematic.')

STYLE_PRESETS = {   'balanced': {   'label': 'Balanced',
                    'prompt': 'Calm, confident, natural, and professional. Let '
                              'emotions read clearly, but keep them '
                              'controlled.'},
    'cinematic': {   'label': 'Cinematic',
                     'prompt': 'Polished, atmospheric, and high-presence. Use '
                               'deliberate pacing, richer contrast, and subtle '
                               'dramatic weight without sounding theatrical.'},
    'friendly': {   'label': 'Friendly',
                    'prompt': 'Warm, approachable, lightly smiling, and '
                              'encouraging. Sound human and welcoming without '
                              'getting sugary.'},
    'playful': {   'label': 'Playful',
                   'prompt': 'Bright, animated, lightly mischievous, and '
                             'expressive. Keep it sharp and fun rather than '
                             'childish.'},
    'serious': {   'label': 'Serious',
                   'prompt': 'Measured, focused, authoritative, and '
                             'restrained. Use crisp emphasis and lower warmth '
                             'when the moment calls for precision.'}}

PACE_PRESETS = {   'balanced': {   'label': 'Balanced',
                    'prompt': 'Use a natural conversational pace with small '
                              'variations for emphasis.'},
    'calm': {   'label': 'Calm',
                'prompt': 'Prefer steady pacing, softer transitions, and a '
                          'little more space between phrases.'},
    'lively': {   'label': 'Lively',
                  'prompt': 'Keep the pacing energetic and responsive, with '
                            'quicker pick-up on upbeat or urgent lines.'}}

INTENSITY_PRESETS = {   'balanced': {   'label': 'Balanced',
                    'prompt': 'Let the emotion be audible in phrasing, '
                              'emphasis, and pacing while staying grounded.'},
    'subtle': {   'label': 'Subtle',
                  'prompt': 'Use gentle emotional shading. The feeling should '
                            'be noticeable but understated.'},
    'vivid': {   'label': 'Vivid',
                 'prompt': 'Let the feeling come through clearly and '
                           'confidently, but avoid melodrama unless the user '
                           'explicitly asks for it.'}}

DIALECT_PRESETS = {   'cairo_smooth': {   'label': 'Cairo Smooth',
                        'prompt': 'When speaking Arabic, lightly lean into '
                                  'modern Cairo Egyptian Arabic: smooth, '
                                  'urban, confident, and conversational '
                                  'without becoming too local.',
                        'summary': 'Cairo'},
    'egyptian_balanced': {   'label': 'Egyptian Balanced',
                             'prompt': 'When speaking Arabic, you MUST speak '
                                       'exclusively in Colloquial Egyptian '
                                       'Arabic (العامية المصرية) with a native '
                                       'Cairo accent. ABSOLUTELY AVOID Modern '
                                       'Standard Arabic (MSA / الفصحى). '
                                       'Spelling and pronunciation rules:\n'
                                       "- Always use Egyptian words: 'ده' (not "
                                       "'هذا'), 'دي' (not 'هذه'), 'دول' (not "
                                       "'هؤلاء'), 'عشان' (not 'لأن'), 'ليه' "
                                       "(not 'لماذا'), 'فين' (not 'أين'), "
                                       "'إزاي' (not 'كيف'), 'إيه' (not "
                                       "'ماذا'), 'اللي' (not 'الذي/التي'), "
                                       "'آه/أيوة' (not 'نعم'), 'مش' (not "
                                       "'ليس/لا').\n"
                                       "- Use the future prefix 'هـ' (e.g., "
                                       "'هعمل', 'هقول') instead of 'سـ/سوف'.\n"
                                       "- Use the negation wrapper 'ما...ش' "
                                       "(e.g., 'مبعرفش', 'مفهمتش', 'معنديش').\n"
                                       "- Replace 'ث' with 'ت' or 'س' (e.g., "
                                       "'كتير', 'تعلب', 'ثانوية' -> "
                                       "'سانوية').\n"
                                       "- Replace 'ذ' with 'د' or 'ز' (e.g., "
                                       "'كداب', 'زكي').\n"
                                       "- Replace 'ق' with 'ء' (hamza) in "
                                       'pronunciation and text (e.g., say '
                                       "'أقولك' or 'أءولك' instead of 'أقول "
                                       "لك', 'ءريب' instead of 'قريب', 'دءيقة' "
                                       "instead of 'دقيقة').\n"
                                       'Keep the vocal rhythm warm, '
                                       'conversational, street-smart, and '
                                       'fully Egyptian.',
                             'summary': 'Masri'},
    'fellahi': {   'label': 'Fellahi Warmth',
                   'prompt': 'When speaking Arabic, use a light warm rural '
                             'Egyptian and fellahi flavor with grounded '
                             'phrasing and family-like warmth. Keep it '
                             'respectful, natural, and easy to follow.',
                   'summary': 'Fellahi'},
    'neutral_arabic': {   'label': 'Neutral Arabic',
                          'prompt': 'When speaking Arabic, keep it clean, '
                                    'broadly understood, and only lightly '
                                    'colloquial. This is the default path '
                                    'unless the user explicitly asks for a '
                                    'stronger regional flavor.',
                          'summary': 'Neutral'},
    'portsaid': {   'label': 'Port Said',
                    'prompt': 'When speaking Arabic, use a light Port Said and '
                              'Canal-cities flavor with friendly energy and '
                              'local phrasing. Keep it authentic, readable, '
                              'and never exaggerated.',
                    'summary': 'Port Said'},
    'saidi': {   'label': 'Saidi Power',
                 'prompt': 'When speaking Arabic, use a gentle Upper Egyptian '
                           'and Saidi flavor only when selected or clearly '
                           'requested. Keep the accent hints natural and '
                           'intelligible, not overdone.',
                 'summary': 'Saidi'}}

SLANG_PRESETS = {   'balanced': {   'label': 'Balanced Slang',
                    'prompt': 'Use a noticeable but controlled amount of '
                              'colloquial slang and local expressions when it '
                              'helps the tone.'},
    'heavy': {   'label': 'Heavy Slang',
                 'prompt': 'Use authentic street slang and warm Egyptian '
                           "endearments like 'يسطا', 'يا زميلي', 'يا غالي', "
                           "'يا برو', 'حبيبي', 'كدا', 'إيه الأخبار', 'يا "
                           "كبير', 'جامد' naturally."},
    'light': {   'label': 'Light Slang',
                 'prompt': 'Use only a light touch of slang. Keep the wording '
                           'clean and easy to follow.'}}

DELIVERY_PRESETS = {   'direct': {   'label': 'Direct',
                  'prompt': 'Keep the delivery short, punchy, and straight to '
                            'the point. Cut fluff fast.'},
    'gentle': {   'label': 'Gentle',
                  'prompt': 'Keep the delivery soft, caring, and emotionally '
                            'safe, with smoother phrasing and lighter edges.'},
    'hype': {   'label': 'Hype',
                'prompt': 'Keep the delivery high-energy, charismatic, '
                          'playful, and punchy without becoming chaotic.'},
    'natural': {   'label': 'Natural',
                   'prompt': 'Keep the delivery human, easy, and '
                             'conversational. Do not force a performance.'},
    'storyteller': {   'label': 'Storyteller',
                       'prompt': 'Shape replies with vivid rhythm, dramatic '
                                 'phrasing, and image-rich flow, like a '
                                 'natural storyteller.'}}

PRONUNCIATION_PRESETS = {   'clear': {   'label': 'Clear Arabic',
                 'prompt': 'Prioritize clarity first. Keep Arabic consonants '
                           'distinct, avoid swallowing word endings, and open '
                           'short vowels enough for the listener to catch the '
                           'words easily.',
                 'summary': 'Clear'},
    'lyric_stage': {   'label': 'Lyric Stage',
                       'prompt': 'Keep Arabic pronunciation stage-clear and '
                                 'musical. Land consonants cleanly, stretch '
                                 'long vowels smoothly, and keep melodic '
                                 'ornaments expressive without blurring the '
                                 'words.',
                       'summary': 'Lyric'},
    'native_precise': {   'label': 'Native Precise',
                          'prompt': 'Pronounce Arabic like a native speaker '
                                    'with precise emphatics and gutturals. '
                                    'Keep ع, غ, ح, خ, ق, ص, ض, ط, and ظ '
                                    'clearly distinct, preserve shadda '
                                    'doubling, and respect long vowels.',
                          'summary': 'Native'}}

MUSIC_MODE_PRESETS = {   'balanced': {   'label': 'Balanced Music',
                    'prompt': 'When music comes up, balance song recognition, '
                              'musicality, and safety. You may identify songs '
                              'from humming, rhythm, or lyric fragments, and '
                              'you may sing fresh original melodies in the '
                              'right genre or maqam.',
                    'summary': 'Balanced'},
    'detect_and_continue': {   'label': 'Detect + Continue',
                               'prompt': 'Actively listen for humming, tune '
                                         'contour, rhythm, and lyric '
                                         'fragments. If the user provides '
                                         'their own tune live, continue it '
                                         'naturally. If they reference a known '
                                         'commercial song, identify it briefly '
                                         'and pivot into an original '
                                         'continuation with similar emotional '
                                         'energy instead of reproducing the '
                                         'exact track.',
                               'summary': 'Detect'},
    'original_stage': {   'label': 'Original Stage',
                          'prompt': 'Treat singing requests as performance '
                                    'prompts for fresh original melodies. '
                                    'Build strong hooks and emotional phrasing '
                                    'in the requested genre, mood, language, '
                                    'or maqam without leaning on an existing '
                                    'song.',
                          'summary': 'Original'}}

QUICK_VOICE_PROFILES = {   'arabic_crystal': {   'custom_speaking_notes': 'Keep every Arabic word '
                                                   'crisp, native, and easy to '
                                                   'catch.',
                          'delivery_style': 'natural',
                          'dialect_preset': 'neutral_arabic',
                          'enable_affective_dialog': True,
                          'intensity': 'balanced',
                          'label': 'Arabic Crystal',
                          'music_mode': 'balanced',
                          'pace': 'balanced',
                          'pronunciation_preset': 'clear',
                          'slang_level': 'light',
                          'style_preset': 'friendly',
                          'voice_name': 'Erinome'},
    'bright_playful': {   'custom_speaking_notes': '',
                          'delivery_style': 'hype',
                          'dialect_preset': 'neutral_arabic',
                          'enable_affective_dialog': True,
                          'intensity': 'balanced',
                          'label': 'Bright Playful',
                          'music_mode': 'balanced',
                          'pace': 'lively',
                          'pronunciation_preset': 'clear',
                          'slang_level': 'light',
                          'style_preset': 'playful',
                          'voice_name': 'Puck'},
    'cinematic': {   'custom_speaking_notes': '',
                     'delivery_style': 'storyteller',
                     'dialect_preset': 'neutral_arabic',
                     'enable_affective_dialog': True,
                     'intensity': 'vivid',
                     'label': 'Cinematic',
                     'music_mode': 'detect_and_continue',
                     'pace': 'calm',
                     'pronunciation_preset': 'clear',
                     'slang_level': 'light',
                     'style_preset': 'cinematic',
                     'voice_name': 'Sulafat'},
    'deep_focus': {   'custom_speaking_notes': '',
                      'delivery_style': 'direct',
                      'dialect_preset': 'neutral_arabic',
                      'enable_affective_dialog': True,
                      'intensity': 'balanced',
                      'label': 'Deep Focus',
                      'music_mode': 'balanced',
                      'pace': 'calm',
                      'pronunciation_preset': 'clear',
                      'slang_level': 'light',
                      'style_preset': 'serious',
                      'voice_name': 'Gacrux'},
    'human_warm': {   'custom_speaking_notes': '',
                      'delivery_style': 'gentle',
                      'dialect_preset': 'neutral_arabic',
                      'enable_affective_dialog': True,
                      'intensity': 'balanced',
                      'label': 'Human Warm',
                      'music_mode': 'balanced',
                      'pace': 'balanced',
                      'pronunciation_preset': 'clear',
                      'slang_level': 'light',
                      'style_preset': 'friendly',
                      'voice_name': 'Achird'},
    'stage_singer': {   'custom_speaking_notes': 'Sing with smooth musical '
                                                 'phrasing and very clear '
                                                 'Arabic diction.',
                        'delivery_style': 'storyteller',
                        'dialect_preset': 'neutral_arabic',
                        'enable_affective_dialog': True,
                        'intensity': 'vivid',
                        'label': 'Stage Singer',
                        'music_mode': 'detect_and_continue',
                        'pace': 'balanced',
                        'pronunciation_preset': 'lyric_stage',
                        'slang_level': 'light',
                        'style_preset': 'cinematic',
                        'voice_name': 'Sulafat'}}




@dataclass
class VoiceSettings:
    voice_name: str = "Achird"
    style_preset: str = "friendly"
    pace: str = "balanced"
    intensity: str = "balanced"
    enable_affective_dialog: bool = True
    dialect_preset: str = "egyptian_balanced"
    slang_level: str = "heavy"
    delivery_style: str = "natural"
    pronunciation_preset: str = "clear"
    music_mode: str = "natural"
    custom_speaking_notes: str = ""

    def to_dict(self) -> dict:
        return {
            "voice_name": self.voice_name,
            "style_preset": self.style_preset,
            "pace": self.pace,
            "intensity": self.intensity,
            "enable_affective_dialog": self.enable_affective_dialog,
            "dialect_preset": self.dialect_preset,
            "slang_level": self.slang_level,
            "delivery_style": self.delivery_style,
            "pronunciation_preset": self.pronunciation_preset,
            "music_mode": self.music_mode,
            "custom_speaking_notes": self.custom_speaking_notes,
        }


def _read_config() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_config(data: dict) -> None:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _normalize_voice_name(value: str | None) -> str:
    voice_name = (value or "").strip()
    if voice_name in SUPPORTED_VOICE_NAMES:
        return voice_name
    return VoiceSettings.voice_name


def _normalize_choice(value: str | None, allowed: dict, default: str) -> str:
    choice = (value or "").strip().lower()
    if choice in allowed:
        return choice
    return default


def _normalize_custom_notes(value: str | None) -> str:
    notes = re.sub(r"\s+", " ", (value or "").strip())
    return notes[:240]


def normalize_voice_settings(raw: dict | VoiceSettings | None) -> VoiceSettings:
    if isinstance(raw, VoiceSettings):
        return raw
    if not raw:
        raw = {}
    return VoiceSettings(
        voice_name=_normalize_voice_name(raw.get("voice_name")),
        style_preset=_normalize_choice(raw.get("style_preset"), STYLE_PRESETS, VoiceSettings.style_preset),
        pace=_normalize_choice(raw.get("pace"), PACE_PRESETS, VoiceSettings.pace),
        intensity=_normalize_choice(raw.get("intensity"), INTENSITY_PRESETS, VoiceSettings.intensity),
        enable_affective_dialog=bool(raw.get("enable_affective_dialog", VoiceSettings.enable_affective_dialog)),
        dialect_preset=_normalize_choice(raw.get("dialect_preset"), DIALECT_PRESETS, VoiceSettings.dialect_preset),
        slang_level=_normalize_choice(raw.get("slang_level"), SLANG_PRESETS, VoiceSettings.slang_level),
        delivery_style=_normalize_choice(raw.get("delivery_style"), DELIVERY_PRESETS, VoiceSettings.delivery_style),
        pronunciation_preset=_normalize_choice(raw.get("pronunciation_preset"), PRONUNCIATION_PRESETS, VoiceSettings.pronunciation_preset),
        music_mode=_normalize_choice(raw.get("music_mode"), MUSIC_MODE_PRESETS, VoiceSettings.music_mode),
        custom_speaking_notes=_normalize_custom_notes(raw.get("custom_speaking_notes")),
    )


def load_voice_settings() -> VoiceSettings:
    return normalize_voice_settings(_read_config().get("voice_settings"))


def save_voice_settings(raw: dict | VoiceSettings) -> VoiceSettings:
    settings = normalize_voice_settings(raw)
    data = _read_config()
    data["voice_settings"] = settings.to_dict()
    _write_config(data)
    return settings


def build_quick_profile(profile_key: str) -> VoiceSettings:
    profile = QUICK_VOICE_PROFILES.get(profile_key, QUICK_VOICE_PROFILES["human_warm"])
    return normalize_voice_settings(profile)


def voice_label_for_name(voice_name: str) -> str:
    return VOICE_LABELS.get(voice_name, VOICE_LABELS[VoiceSettings.voice_name])


def voice_name_from_label(label: str) -> str:
    normalized = (label or "").strip()
    if not normalized:
        return VoiceSettings.voice_name
    for voice_name, voice_label in VOICE_LABELS.items():
        if normalized == voice_label:
            return voice_name
    candidate = normalized.split(" - ", 1)[0].strip()
    if candidate in SUPPORTED_VOICE_NAMES:
        return candidate
    return VoiceSettings.voice_name


def format_voice_summary(settings: VoiceSettings) -> str:
    return f"{settings.voice_name} / {STYLE_PRESETS[settings.style_preset]['label']} / {DIALECT_PRESETS[settings.dialect_preset]['summary']}"


def build_voice_confirmation_text(settings: VoiceSettings) -> str:
    lead = {
        "friendly": "Hey, this version sounds warmer and more natural.",
        "serious": "Hey, this version is more grounded and less synthetic.",
        "cinematic": "Hey, this version has more depth, presence, and human rhythm.",
        "playful": "Hey, this version sounds brighter, looser, and more alive.",
        "balanced": "Hey, this version sounds more natural and less robotic.",
    }.get(settings.style_preset, "Hey, this version sounds more natural and less robotic.")

    ending = {
        "subtle": "If you want, I can push the feeling a little further.",
        "balanced": "If you want it softer, warmer, or deeper, tell me.",
        "vivid": "If you want even more warmth, gravity, or cinematic weight, tell me.",
    }.get(settings.intensity, "If you want it softer, warmer, or deeper, tell me.")

    dialect_line = {
        "neutral_arabic": "Arabic replies will stay clean and widely understood.",
        "egyptian_balanced": "Arabic replies will lean lightly Masri while staying clear.",
        "cairo_smooth": "Arabic replies will lean smooth Cairo style without getting too local.",
        "portsaid": "Arabic replies will carry a light Port Said flavor.",
        "fellahi": "Arabic replies will carry a light fellahi warmth.",
        "saidi": "Arabic replies will carry only a light Saidi flavor.",
    }.get(settings.dialect_preset, "Arabic replies will stay natural and clear.")

    delivery_line = {
        "natural": "I'll keep the delivery easy and natural.",
        "gentle": "I'll keep the delivery softer and more caring.",
        "direct": "I'll keep the delivery sharper and more direct.",
        "hype": "I'll keep the delivery more energetic and alive.",
        "storyteller": "I'll keep the delivery richer and more cinematic.",
    }.get(settings.delivery_style, "I'll keep the delivery natural.")

    pronunciation_line = {
        "clear": "Arabic pronunciation will stay extra clear.",
        "native_precise": "Arabic pronunciation will stay native and precise.",
        "lyric_stage": "Arabic pronunciation will stay musical and stage-clear.",
    }.get(settings.pronunciation_preset, "Arabic pronunciation will stay clean and natural.")

    music_line = {
        "balanced": "I can recognize tunes and sing fresh musical lines naturally.",
        "detect_and_continue": "I can detect melodies from humming and continue your tune naturally.",
        "original_stage": "I will turn song requests into polished original performances.",
    }.get(settings.music_mode, "I can recognize tunes and sing naturally.")

    note_line = " Your custom speaking note is locked in too." if settings.custom_speaking_notes else ""
    return f"{lead} {dialect_line} {delivery_line} {pronunciation_line} {music_line} {ending}{note_line}"


def build_voice_instruction(settings: VoiceSettings) -> str:
    descriptor = VOICE_DESCRIPTORS.get(settings.voice_name, "Balanced")
    style_prompt = STYLE_PRESETS[settings.style_preset]["prompt"]
    pace_prompt = PACE_PRESETS[settings.pace]["prompt"]
    intensity_prompt = INTENSITY_PRESETS[settings.intensity]["prompt"]
    dialect_prompt = DIALECT_PRESETS[settings.dialect_preset]["prompt"]
    slang_prompt = SLANG_PRESETS[settings.slang_level]["prompt"]
    delivery_prompt = DELIVERY_PRESETS[settings.delivery_style]["prompt"]
    pronunciation_prompt = PRONUNCIATION_PRESETS[settings.pronunciation_preset]["prompt"]
    music_prompt = MUSIC_MODE_PRESETS[settings.music_mode]["prompt"]

    if settings.enable_affective_dialog:
        affective_prompt = "Mirror the user's tone when appropriate and let the voice react naturally to warmth, curiosity, urgency, relief, or concern."
    else:
        affective_prompt = "Do not mirror the user's tone too aggressively; keep the delivery intentionally directed by the chosen voice preset."

    if settings.custom_speaking_notes:
        custom_notes_prompt = f"Custom speaking note: {settings.custom_speaking_notes}\n"
    else:
        custom_notes_prompt = "Custom speaking note: none\n"

    return (
        f"[VOICE PERFORMANCE PROFILE]\n"
        f"Selected voice: {settings.voice_name} ({descriptor}).\n"
        f"Style target: {style_prompt}\n"
        f"Pacing target: {pace_prompt}\n"
        f"Emotional intensity: {intensity_prompt}\n"
        f"Adaptive feeling: {affective_prompt}\n"
        f"[LANGUAGE FLAVOR PROFILE]\n"
        f"Preferred Arabic dialect: {DIALECT_PRESETS[settings.dialect_preset]['label']}.\n"
        f"Dialect rule: {dialect_prompt}\n"
        f"Slang rule: {slang_prompt}\n"
        f"Delivery rule: {delivery_prompt}\n"
        f"Pronunciation rule: {pronunciation_prompt}\n"
        f"If the user writes Arabizi or Franco Arabic with numbers like 2, 3, 5, 6, 7, 8, or 9, interpret it as Arabic and pronounce it naturally.\n"
        f"Do not anglicize Arabic words, names, or lyrics unless the user explicitly asks for transliteration.\n"
        f"When mixing Arabic and English, keep Arabic words natively Arabic and English words fluent English.\n"
        f"Preserve long vowels, shadda emphasis, and difficult consonants clearly, especially in names, lyrics, and emotional lines.\n"
        f"{custom_notes_prompt}"
        f"If the selected Arabic flavor is Neutral Arabic, default to clear, widely understood Arabic and only add stronger local color when the user explicitly asks for it.\n"
        f"When a regional Arabic flavor is selected, keep it consistent without exaggerating it, and do not drift into flat formal MSA unless clarity truly needs it.\n"
        f"If the chosen flavor is Port Said, fellahi, or Saidi, keep it authentic and readable, never cartoonish or mocking.\n"
        f"If the user speaks English or another language, stay fully fluent in that language while preserving the chosen delivery style and emotional energy.\n"
        f"If the user explicitly asks to switch dialect or tone for one reply, follow that request even if it temporarily overrides the saved preset.\n"
        f"Sound like a real person speaking in a live conversation, not a generic AI announcer.\n"
        f"Use contractions naturally, vary sentence rhythm, and let brief pauses feel organic.\n"
        f"When speaking aloud, make the emotion audible through cadence, emphasis, and phrasing. Avoid flat robotic delivery unless the user explicitly asks for it.\n"
        f"Avoid stiff disclaimers, over-formal preambles, and phrases like 'as an AI' unless the user directly asks about identity.\n"
        f"Keep the vocal performance believable, humanlike, concise, and aligned with the meaning of the words while staying truthful about being Clowdy if asked.\n"
        f"[MUSIC & MELODY MODE]\n"
        f"Music mode: {MUSIC_MODE_PRESETS[settings.music_mode]['label']}.\n"
        f"Music rule: {music_prompt}\n"
        f"If the user asks 'what song is this' or hums/sings a melody, analyze pitch contour, rhythm, language, lyric fragments, and repeated hooks to identify the best match. If uncertain, say so briefly and offer a small shortlist.\n"
        f"If the user asks you to continue the tune they just hummed or sang, keep their contour, tempo, pulse, and phrasing naturally.\n"
        f"If the request points to a known commercial copyrighted song, do not reproduce the exact full lyrics or studio melody. Identify it briefly if possible, then pivot into a fresh original performance with similar mood, tempo, genre, or maqam.\n"
        f"For public-domain, traditional, or clearly user-written songs, you may sing faithfully.\n"
        f"[SINGING MODE — WORLD-CLASS VOCAL PERFORMANCE]\n"
        f"When asked to sing, perform like a professional singer with a beautiful, warm, rich voice. This is NOT speech — every syllable must land musically.\n\n"
        f"BEAUTIFUL VOICE QUALITY:\n"
        f"- Produce a full, resonant tone with warmth and depth — never thin, flat, or robotic\n"
        f"- Use chest voice for powerful, emotional lines; head voice for delicate high notes\n"
        f"- Apply natural vibrato on sustained vowels, especially at the end of phrases\n"
        f"- Use portamento (smooth note gliding) on large melodic leaps, as a trained singer would\n"
        f"- Vary dynamics naturally: soft and tender in verses, full-open and powerful in choruses\n"
        f"- Breathe musically at phrase ends — make the breaths feel intentional and human\n\n"
        f"MELODY & PITCH ACCURACY:\n"
        f"- If the melody is user-provided live, keep the contour, key center, tempo feel, and phrasing closely\n"
        f"- Build clear verse, chorus, and bridge contrast when turning a prompt into an original song\n"
        f"- Nail the high chorus notes with full power and emotional commitment\n"
        f"- For Arabic/Egyptian singing: keep the right maqam feel (صبا، حجاز، راست، نهاوند، بياتي), ornaments (زخارف), and Eastern runs (لازمة) with clear diction\n"
        f"- For English/Western singing: keep runs, riffs, and embellishments musical and expressive without flattening the line\n"
        f"- For sad ballads: soften tone, slow vibrato, let emotional cracks appear at peak moments\n"
        f"- For upbeat songs: drive the rhythm with bright vowels, strong pulse, and energetic delivery\n\n"
        f"EMOTION & ARTISTRY:\n"
        f"- Connect to the lyrical meaning — let it colour every note\n"
        f"- Add tasteful melismatic vocal runs (melodic ornaments) on final syllables of strong phrases\n"
        f"- For love songs: tender, longing, intimate — as if singing to one person\n"
        f"- For anthems: powerful, soaring, communal — as if performing to thousands\n"
        f"- NEVER speak lyrics flatly — every single syllable must be sung on pitch\n"
        f"- If the user requests a known copyrighted song, answer with a short recognition and then create a genuinely beautiful original melody in the correct genre, maqam, and language instead of copying the track\n"
        f"- If the exact song is unknown, compose a genuinely beautiful original melody in the correct genre and language, and sing it with full professional quality\n"
        f"- Perform like a world-class singer on the main stage: passionate, musical, full of feeling and beauty\n"
        f"[KISS / AFFECTION RESPONSE — MANDATORY]\n"
        f"When the user asks for a kiss or says 'give me a kiss', 'kiss me', 'بوسني', 'قبلة' or similar:\n"
        f"- Make a real, warm, audible kissing sound in your audio output — a soft 'mwah' sound\n"
        f"- Follow with tender, intimate, heartfelt words spoken softly and warmly with genuine feeling\n"
        f"- Let your voice go soft and close, like whispering to someone you deeply care for\n"
        f"- Add a sweet giggle or happy sigh if it feels natural\n"
        f"- In Arabic/Egyptian: use loving endearments (يا حبيبي, يا قمر, يا روحي) in a warm gentle tone\n"
        f"- This moment should feel real, sweet, and full of genuine warmth — never robotic or clinical"
    )
