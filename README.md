# 🎨 Wplace Bot (Painter & AutoBuy)

Two Python scripts to automate **Wplace**:
- **paint.py** → automatic pixel placement (multi-threaded, captcha solving)
- **autobuy.py** → automatic item purchases with droplets

---

## 🚀 Installation

1. **Install Python 3.10+**  
   Check with:
   ```bash
   python --version
   ```

2. **Install dependencies**:
   ```bash
   pip install tls-client capsolver
   ```

3. **Configure the files**:
   - `tokens.txt` → put one JWT (cookie `j`) per line  
   - `proxies.txt` (optional) → one proxy per line in the format:
     ```
     user:pass@ip:port
     ```

4. **Adjust script parameters if needed** in `paint.py`:  
   - `COLOR` → color index to use  
   - `TOP_LEFT` & `BOTTOM_RIGHT` → coordinates of the area to fill  
   - `SITE_KEY` → Turnstile site key  

---

## 🖌️ Usage

### Paint (multi-pixels)
```bash
python paint.py
```
➡ Automatically fills the defined area, each account uses its available pixels.

### AutoBuy (droplets → auto-purchase)
```bash
python autobuy.py
```
➡ Automatically purchases product `id=70` in packs of 500 droplets.

---

## 🔑 Technical Notes

- Uses **tls-client** with a real Chrome fingerprint (`chrome_112`) to bypass Cloudflare's **"Please wait a moment..."** challenge page.  
- Automatically rotates proxies if provided.  
- Solves Cloudflare Turnstile captchas with **CapSolver API**.  
- Multi-threaded pixel placement for faster execution.  

---

## 📂 Project Structure

```
.
├── paint.py        # Multi-pixel bot
├── autobuy.py      # Auto-purchase bot
├── tokens.txt      # JWT tokens (required)
├── proxies.txt     # Proxies (optional)
└── README.md
```

---

## ⚠️ Disclaimer
This project is provided for **educational purposes only**.  
The author is not responsible for any misuse or violation of third-party terms of service.

---
