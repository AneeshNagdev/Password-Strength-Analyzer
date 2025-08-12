

document.addEventListener("DOMContentLoaded", function () {
  // ===== Password visibility toggle =====
  const togglePasswordBtn = document.getElementById("togglePassword");
  const passwordInput = document.getElementById("password");

  if (togglePasswordBtn && passwordInput) {
    togglePasswordBtn.addEventListener("click", function () {
      const isPassword = passwordInput.type === "password";
      passwordInput.type = isPassword ? "text" : "password";
      togglePasswordBtn.textContent = isPassword ? "🙈" : "👁";
    });
  }

  // ===== Analyzer wiring =====
  const form = document.getElementById("passwordForm");
  const result = document.getElementById("result");
  const scoreEl = document.getElementById("score");
  const labelEl = document.getElementById("label");
  const bitsEl = document.getElementById("bits");
  const barFill = document.getElementById("bar-fill");
  const tipsList = document.getElementById("tips-list");
  const crackBody = document.getElementById("crack-body");

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const pw = (passwordInput?.value || "").trim();

      if (!pw) {
        result.classList.remove("hidden");
        scoreEl.textContent = "—";
        labelEl.textContent = "Please enter a password.";
        bitsEl.textContent = "—";
        barFill.style.width = "0%";
        tipsList.innerHTML = "";
        if (crackBody) crackBody.innerHTML = "";
        return;
      }

      fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password: pw })
      })
        .then((r) => r.json())
        .then((data) => {
          result.classList.remove("hidden");

          const score = Number(data.score) || 0;
          const label = data.label || "—";
          const bits = Number(data.entropy_bits) || 0;

          scoreEl.textContent = `${score}/100`;
          labelEl.textContent = label;
          bitsEl.textContent = bits.toFixed(2);
          barFill.style.width = Math.min(100, Math.max(0, score)) + "%";

          // crack times table
          if (crackBody) {
            crackBody.innerHTML = "";
            const times = data.crack_times || {};
            // Keep the order readable if backend dict is unordered
            const preferredOrder = ["online (10/sec)", "online (1k/sec)", "offline (1e9/sec)"];
            const keys = Object.keys(times);
            const ordered = preferredOrder.filter(k => keys.includes(k)).concat(keys.filter(k => !preferredOrder.includes(k)));
            ordered.forEach((k) => {
              const tr = document.createElement("tr");
              const td1 = document.createElement("td"); td1.textContent = k;
              const td2 = document.createElement("td"); td2.textContent = times[k];
              tr.appendChild(td1); tr.appendChild(td2);
              crackBody.appendChild(tr);
            });
          }

          // tips
          const tips = Array.isArray(data.tips) ? data.tips : [];
          tipsList.innerHTML = "";
          if (tips.length === 0) {
            const li = document.createElement("li");
            li.textContent = "Looks good! Consider using a passphrase and enabling MFA for important accounts.";
            tipsList.appendChild(li);
          } else {
            tips.slice(0, 6).forEach((t) => {
              const li = document.createElement("li");
              li.textContent = t;
              tipsList.appendChild(li);
            });
          }
        })
        .catch((err) => {
          console.error(err);
          result.classList.remove("hidden");
          scoreEl.textContent = "—";
          labelEl.textContent = "Error analyzing password.";
          bitsEl.textContent = "—";
          barFill.style.width = "0%";
          tipsList.innerHTML = "";
          if (crackBody) crackBody.innerHTML = "";
        });
    });
  }

  // ===== Auto-rotating Fun Facts =====
  const cardEl = document.getElementById("fact-card");
  const titleEl = document.getElementById("fact-title");
  const textEl = document.getElementById("fact-text");
  const dotsEl = document.getElementById("dots");

  if (cardEl && titleEl && textEl && dotsEl) {
    const FACTS = [
      ["Hashing (what & why)",
       "Websites should never store your raw password. They store a hash — a one-way function. At login your input is hashed again and compared. Even if a database leaks, attackers don’t see the originals."],
      ["Salting (unique per user)",
       "A salt is a random string stored with your hash. It makes identical passwords produce different hashes, which breaks rainbow tables and stops mass cracking with precomputed lists."],
      ["Pepper (extra secret)",
       "A pepper is a secret value added before hashing but kept outside the database. Even if the DB leaks, guesses still fail without the pepper."],
      ["Slow hashes beat fast hashes",
       "Fast hashes like MD5/SHA-1 help attackers try billions of guesses per second. Password-specific algorithms (bcrypt, scrypt, Argon2) are slow and memory-hard to resist cracking."],
      ["Rate limiting & lockouts",
       "Sites can slow or block repeated login attempts. That disrupts online brute force, but slow hashing still matters for offline attacks on stolen hashes."],
      ["Passphrases are practical",
       "Four or five random words (e.g., “orbit-lemon-stereo-train”) can be easier to remember and very strong. Length usually helps more than fancy substitutions on short words."],
      ["Password managers",
       "Managers create long, unique passwords and remember them for you. They also prevent reuse — a major cause of account takeovers."],
      ["MFA (second step)",
       "Multi-Factor Authentication adds another proof, like an authenticator app code or a hardware key. A stolen password alone isn’t enough."],
      ["Reused passwords = chain reaction",
       "If one site with your reused password is breached, attackers try the same email/password everywhere (credential stuffing)."],
      ["Rainbow tables, briefly",
       "Rainbow tables are giant precomputed hash lists. Salts make them useless because the same password with different salts won’t match those values."],
      ["Key stretching",
       "Key stretching runs the hash many times to slow guessing. PBKDF2, bcrypt, scrypt, and Argon2 all have a tunable cost parameter."],
      ["Security questions caveat",
       "Answers like pet names or birth city are often public. If a site requires them, use random answers and store them in your manager."]
    ];

    function renderDots(count) {
      dotsEl.innerHTML = "";
      for (let i = 0; i < count; i++) {
        const span = document.createElement("span");
        span.textContent = "•";
        span.style.margin = "0 4px";
        span.className = i === 0 ? "active" : "";
        dotsEl.appendChild(span);
      }
    }
    renderDots(FACTS.length);

    let idx = 0;
    function showFact(i) {
      const [title, text] = FACTS[i];
      cardEl.style.opacity = 0;
      setTimeout(() => {
        titleEl.textContent = title;
        textEl.textContent = text;
        [...dotsEl.children].forEach((dot, k) => {
          dot.className = k === i ? "active" : "";
        });
        cardEl.style.opacity = 1;
      }, 200);
    }

    showFact(idx);
    setInterval(() => {
      idx = (idx + 1) % FACTS.length; // forward only
      showFact(idx);
    }, 4000);
  }

  // footer year
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
});
