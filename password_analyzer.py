import math
import getpass
import re
import random
from common_words import COMMON_WORDS
from fun_facts_list import  FUN_FACTS


def has_lower(s):
    for c in s:
        if 'a' <= c <= 'z':
            return True
    return False

def has_upper(s):
    for c in s:
        if 'A' <= c <= 'Z':
            return True
    return False

def has_digit(s):
    for c in s:
        if '0' <= c <= '9':
            return True
    return False

def has_symbol(s):
    for c in s:
        if not c.isalnum():
            return True
    return False


def charset_size(pw):
    size = 0

    if has_lower(pw): size += 26
    if has_upper(pw): size += 26
    if has_digit(pw): size += 10
    if has_symbol(pw): size += 33
    return max(size, 1)

def entropy_bits(pw):
    if not pw:
        return 0.0
    return len(pw) * math.log2(charset_size(pw))

def crack_time(seconds):
    if seconds < 1:
        return "instantly"
    
    minutes = 60
    hour = 60 * minutes
    day = 24 * hour
    year = 365 * day

    if seconds >= year:
        return f"{seconds / year:.1f} years"
    if seconds >= day:
        return f"{seconds / day:.1f} days"
    if seconds >= hour:
        return f"{seconds / hour:.1f} hours"
    if seconds >= minutes:
        return f"{seconds / minutes:.1f} minutes"
    return f"{seconds:.1f} seconds"


def time_to_crack(bits, guesses_per_sec=1e9):
    if bits <= 0:
        return 0.0
    expected_guesses = 2**(bits - 1)
    return expected_guesses / max(guesses_per_sec, 1.0)

def time_to_crack_seconds(bits, guesses_per_sec):
    return time_to_crack(bits, guesses_per_sec)

def human_time(seconds):
    return crack_time(seconds)

# anything above 120 is already very good so cap it at 120
def strength_score(bits):
    if bits <= 0:
        return 0
    capped = min(bits, 120.0)
    return int(round((capped / 120.0) * 100))

def strength_label(score):
    if score < 20:
        return "Very Weak"
    if score < 40:
        return "Weak"
    if score < 60:
        return "Fair"
    if score < 75:
        return "Good"
    if score < 90:
        return "Strong"
    return "Very Strong"

# --------------------
# simple pattern check
# --------------------

def only_letters(pw: str) -> bool:
    return pw.isalpha()

def only_digits(pw: str) -> bool:
    return pw.isdigit()

def only_symbols(pw: str) -> bool:
    return len(pw) > 0 and all((not c.isalnum()) for c in pw)

def has_repeat_3(pw: str) -> bool:
    # any same character 3+ times in a row
    for i in range(len(pw) - 2):
        if pw[i] == pw[i+1] == pw[i+2]:
            return True
    return False

def has_alpha_sequence(pw: str) -> bool:
    # looks for 'abcd', 'bcde', etc. (case-insensitive)
    seq = "abcdefghijklmnopqrstuvwxyz"
    low = pw.lower()
    for i in range(len(seq) - 3):
        if seq[i:i+4] in low:
            return True
    return False

def has_numeric_sequence(pw: str) -> bool:
    # simple checks for common runs or repeats
    if "0000" in pw or "1111" in pw:
        return True
    asc = ["0123","1234","2345","3456","4567","5678","6789"]
    desc = ["9876","8765","7654","6543","5432","4321","3210"]
    return any(r in pw for r in asc + desc)

def has_year_like(pw: str) -> bool:
    # 1900–2099 anywhere
    return re.search(r"(19|20)\d{2}", pw) is not None

def contains_common_word(pw):
    low = pw.lower()
    for word in COMMON_WORDS:
        if word in low:
            return True
    return False


# nist style functions to check for password security

def below_min_length(pw: str) -> bool:
    # NIST minimum: 8. (We’ll still *recommend* 12–16 later.)
    return len(pw) < 8

def above_reasonable_length(pw: str) -> bool:
    # Services should allow up to 64+; flag only as an FYI.
    return len(pw) > 64

def contains_username(pw: str, username: str) -> bool:
    return bool(username) and username.lower() in pw.lower()

def contains_context_info(pw: str, first_name: str = "", last_name: str = "") -> bool:
    low = pw.lower()
    return (first_name and first_name.lower() in low) or (last_name and last_name.lower() in low)

def contains_common_word(pw: str) -> bool:
    COMMON_WORDS = {"password","qwerty","admin","letmein","welcome","iloveyou"}
    low = pw.lower()
    return any(w in low for w in COMMON_WORDS)


# tips section

def password_tips(pw: str, username: str = "", first_name: str = "", last_name: str = "") -> list[str]:
    tips: list[str] = []

    # NIST-style guidance
    if below_min_length(pw):
        tips.append("NIST: allow at least 8 characters — aim for 12–16 for stronger security.")
    if above_reasonable_length(pw):
        tips.append("Very long password — allowed per NIST; ensure it's memorable or stored in a manager.")
    if contains_username(pw, username):
        tips.append("Avoid using your username inside the password.")
    if contains_context_info(pw, first_name=first_name, last_name=last_name):
        tips.append("Avoid personal info like your name in the password.")
    if contains_common_word(pw):
        tips.append("Avoid passwords found in common/breached lists (e.g., 'password', 'qwerty').")

    # Composition
    if len(pw) < 12:
        tips.append("Use at least 12–16 characters (longer = more entropy).")
    if not has_upper(pw):
        tips.append("Add uppercase letters to expand the character set.")
    if not has_lower(pw):
        tips.append("Add lowercase letters to expand the character set.")
    if not has_digit(pw):
        tips.append("Include digits to increase combinations.")
    if not has_symbol(pw):
        tips.append("Include symbols to enlarge the search space.")

    # Structural patterns
    if only_letters(pw):
        tips.append("Avoid letter-only passwords — mix digits and symbols too.")
    if only_digits(pw):
        tips.append("Avoid number-only passwords — very weak to brute-force.")
    if only_symbols(pw):
        tips.append("Avoid symbol-only passwords — include letters and digits.")
    if has_repeat_3(pw):
        tips.append("Avoid repeating the same character 3+ times (e.g., 'aaa').")
    if has_alpha_sequence(pw):
        tips.append("Avoid alphabet sequences like 'abcd'.")
    if has_numeric_sequence(pw):
        tips.append("Avoid numeric sequences like 1234/0000.")
    if has_year_like(pw):
        tips.append("Avoid years or dates — attackers try those first.")

    # Construction guidance
    if len(pw) < 16 or has_alpha_sequence(pw) or has_numeric_sequence(pw):
        tips.append("Consider a 4–5 word passphrase (e.g., 'orbit-lemon-stereo-train').")

    # Deduplicate while preserving order (optional nice touch)
    seen = set()
    unique = []
    for t in tips:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique


# -----------------------------
# Main analysis function
# -----------------------------

def analyze_password(pw, username="", first_name="", last_name=""):
    """
    Returns a plain dict so it's easy to show in Streamlit.
    """
    bits = entropy_bits(pw)
    score = strength_score(bits)
    label = strength_label(score)

    # a few simple attacker profiles
    profiles = {
        "online (10/sec)": 10.0,
        "online (1k/sec)": 1000.0,
        "offline (1e9/sec)": 1_000_000_000.0
    }
    crack_times = {}
    for name, rate in profiles.items():
        secs = time_to_crack_seconds(bits, rate)
        crack_times[name] = human_time(secs)

    flags = {
        "has_lower": has_lower(pw),
        "has_upper": has_upper(pw),
        "has_digit": has_digit(pw),
        "has_symbol": has_symbol(pw),
        "only_letters": only_letters(pw),
        "only_digits": only_digits(pw),
        "only_symbols": only_symbols(pw),
        "repeat_3": has_repeat_3(pw),
        "alpha_sequence": has_alpha_sequence(pw),
        "numeric_sequence": has_numeric_sequence(pw),
        "year_like": has_year_like(pw),
        "common_word": contains_common_word(pw),
    }

    return {
        "length": len(pw),
        "charset": charset_size(pw),
        "entropy_bits": bits,
        "score": score,
        "label": label,
        "crack_times": crack_times,
        "flags": flags,
        "tips": password_tips(pw, username, first_name, last_name),
    }

def get_fun_facts(n=6, seed=None):
    """
    Return up to n random (title, text) facts from FUN_FACTS.
    """
    if seed is not None:
        random.seed(seed)
    n = max(1, min(n, len(FUN_FACTS)))
    return random.sample(FUN_FACTS, n)

