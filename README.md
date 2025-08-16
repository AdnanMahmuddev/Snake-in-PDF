# 🐍 Snake in a PDF

Yes, you read that right — this is a fully playable **Snake game embedded inside a PDF**.  
It works in Chrome’s built-in PDF viewer (and some other PDF readers that support JavaScript + forms).  
No external tools or plugins are required — just open the PDF and play!

---

## 🎮 Demo
![Snake in PDF Demo](demo.gif)  
*(If GIF doesn’t load, check the repository screenshots.)*

---

## ✨ Features
- ✅ Play **Snake directly inside a PDF** file  
- ✅ Uses **only raw PDF structure, JavaScript, and form fields**  
- ✅ Works in **Chrome’s PDF viewer** (tested in Chrome 139)  
- ✅ **No plugins, no Flash, no hacks** — just PDF magic  
- ✅ Generated using **Python**, so it’s fully reproducible  

---

## ⚙️ How It Works
This project uses a very unconventional approach:
1. A **Python script** (`snake_pdf.py`) generates the PDF.  
2. The PDF contains **form fields** (hidden buttons/inputs) that act as the "grid" for the Snake game.  
3. Embedded **JavaScript** handles:
   - Snake movement  
   - Collision detection  
   - Food spawning  
   - Score counting  
4. When you press arrow keys (↑ ↓ ← →), the Snake moves inside the PDF like a normal game.  

In short: PDF + JavaScript + forms = a playable game.

---

## 📥 Installation & Usage
1. Clone this repo:
   ```bash
   git clone https://github.com/your-username/snake-in-pdf.git
   cd snake-in-pdf
