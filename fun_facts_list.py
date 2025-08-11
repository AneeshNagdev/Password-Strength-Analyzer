import random

FUN_FACTS = [
    ("Hashing (what & why)",
     "Websites should never store your raw password. They store a hash — the output of a one-way function. "
     "At login your input is hashed again and compared. If a database leaks, attackers still don't see the originals."),

    ("Salting (unique per user)",
     "A salt is a random string stored with your hash. It makes identical passwords produce different hashes, "
     "which breaks rainbow tables and prevents attackers from cracking many accounts at once with precomputed lists."),

    ("Pepper (extra secret)",
     "A pepper is a secret value added before hashing but kept outside the database (like in app config). "
     "Even if the DB leaks, guesses still fail without the pepper."),

    ("Slow hashes beat fast hashes",
     "Fast hashes like MD5/SHA-1 help attackers try billions of guesses per second. "
     "Password hashes (bcrypt, scrypt, Argon2) are designed to be slow and memory-hard to reduce cracking speed."),

    ("Rate limiting & lockouts",
     "Online services can slow or block repeated login attempts. This disrupts online brute force. "
     "It doesn't help against offline cracking of a stolen hash dump — that's why slow hashing still matters."),

    ("Passphrases are practical",
     "Four or five random words (e.g., 'orbit-lemon-stereo-train') can be easier to remember and very strong. "
     "Length typically helps more than fancy character substitutions on short words."),

    ("Password managers",
     "Managers create long, unique passwords and remember them for you. "
     "They reduce reuse — a major cause of account takeovers after breaches."),

    ("MFA (second step)",
     "Multi-Factor Authentication adds another proof, like an app code or a hardware key. "
     "That way, a stolen password alone isn't enough to log in."),

    ("Reused passwords = chain reaction",
     "Reusing the same password on multiple sites is dangerous. If one site is breached, "
     "attackers try the same combo elsewhere (credential stuffing)."),

    ("Rainbow tables, briefly",
     "Rainbow tables are giant precomputed lists of hashes. Salts make them useless, "
     "because the same password with different salts doesn't match the precomputed values."),

    ("Key stretching",
     "Key stretching runs the hash many times to slow down guessing. PBKDF2, bcrypt, scrypt, and Argon2 all support a tunable cost parameter."),

    ("Security questions caveat",
     "Answers like pet names or birth city are often public. If a site requires them, "
     "use random answers and store them in your manager."),
]


