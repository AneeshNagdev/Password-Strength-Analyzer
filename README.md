# 🔐 Password Analyzer with Fun Facts

A simple yet educational web application that allows users to **check the strength of their passwords** and learn **cybersecurity fun facts** in the process.  
Built using **Python (Flask)** for the backend and **HTML, CSS, and JavaScript** for the frontend.

---

## 📸 Screenshots

### Landing Page
![Landing Page](screenshots/landing.png)

### Password Analysis
![Password Analysis](screenshots/analysis.png)

---

## ✨ Features

- **Password Strength Analysis**: Checks length, complexity, common words, and more.
- **Estimated Crack Time**: Shows how long it might take to crack the password.
- **Improvement Tips**: Gives personalized suggestions to make passwords stronger.
- **Fun Facts Section**: Displays random cybersecurity facts every 4 seconds.
- **Eye Button**: Toggle password visibility when typing.
- **Privacy Notice**: Passwords are never stored — analysis happens in your session only.

---


---

## 🛠️ Tech Stack

**Frontend:**
- HTML, CSS, JavaScript

**Backend:**
- Python 3(Flask Framework)

**Other:**
- Vercel for deployment
- `requirements.txt` for dependency management

---

## 📂 Project Structure

password-analyzer/
│
├── screenshots/ # Project screenshots
| ├── landing.png
| └── analysis.png
|
├── static/
│ ├── style.css # Frontend styles
│ └── script.js # Frontend JavaScript
│
├── templates/
│ └── index.html # Landing page
│
├── app.py # Flask backend
├── common_words_list.py # Common words for password check
├── fun_facts_list.py # List of fun facts
├── password_analyzer.py # Password analysis logic
├── requirements.txt # Python dependencies
├── vercel.json # Vercel deployment configuration

---

## ⚡ Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/password-analyzer.git
cd password-analyzer
```
