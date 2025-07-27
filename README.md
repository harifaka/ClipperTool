# 🧹 ClipperTool — The Clipboard Cleanup Commander!

Welcome to **ClipperTool**, your new best friend in the wild west of clipboard chaos.  
Whether you're a productivity ninja, a code samurai, or just someone who copies way too much junk, ClipperTool is here to save your sanity.

---

## What is ClipperTool? 🤔

ClipperTool is a slick, modern clipboard manager with a twist:  
It **automatically cleans your clipboard text** by removing or keeping only lines containing your secret list of forbidden (or beloved) words.

- **Remove mode** — Kick out the bad lines like a bouncer at a club.  
- **Keep mode** — Keep only the VIP lines, everything else gets the boot.

No more annoying copy-paste clutter. Just clean, laser-focused clipboard content every time.

---

## Features 💥

- **🔍 Clipboard monitoring** — Runs quietly in the background, waiting for your clipboard to get messy.
- **⚙️ Configurable filters** — Edit simple text files to control exactly what you want removed or kept.
- **🔄 Multiple filter sets** — Switch between configs like changing hats.
- **✨ Modern GUI** — A sleek, sexy interface powered by ttkbootstrap (because ugly UI is so 2000s).
- **🎛️ Two modes** — Remove or keep lines, toggled with a single click.
- **📂 Portable configs** — Store your filter lists in `Documents/ClipperTool/Configs/`, so no surprises when updating. 
- **⚡ Lightweight and fast** — Like a ninja, but for your clipboard.

---

## Quick Start 🚀

1. **Download** the latest release or clone this repo
2. **Drop** your `.txt` filter files in `Documents/ClipperTool/Configs/`
3. **Launch** `ClipperTool.exe` (or run `python clipper_app.py`)
4. **Pick** your filter set from the dropdown menu
5. **Toggle** between **Remove** or **Keep** mode from the menu
6. **Click** the big button to start the magic ✨
7. **Copy** some text — watch the clutter vanish or only the VIP lines stay!

---

## Example Filter Files 📝

Create `.txt` files in your configs folder:

**spam_filter.txt** (Remove mode):
```
advertisement
promotion
spam
unsubscribe
```

**code_keywords.txt** (Keep mode):
```
function
class
import
def
```

---

## Build It Yourself 🏗️

Want to tweak or improve the tool? Here's how:

```bash
# Setup
git clone https://github.com/harifaka/ClipperTool
cd ClipperTool
python -m venv venv
.\venv\Scripts\activate          # Windows
source venv/bin/activate         # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run from source
python clipper_app.py

# Build executable
.\build.bat                      # Windows
# or manually:
pyinstaller clipper_app.spec
```

**Requirements:**
- Python 3.8+
- ttkbootstrap
- pyperclip

---

## Project Structure 🏛️

```
ClipperTool/
├── .github/
│ └── workflows/
│ └── release.yml
├── src/
│ ├── config/
│ │ ├── init.py
│ │ └── config_manager.py
│ ├── core/
│ │ ├── init.py
│ │ └── clipboard_processor.py
│ ├── ui/
│ │ ├── init.py
│ │ ├── constants.py
│ │ ├── main_window.py
│ │ ├── popups.py
│ │ └── widgets.py
│ ├── utils/
│ │ ├── init.py
│ │ └── resources.py
│ ├── favicon.ico
│ └── main.py
├── tests/
├── .gitignore
├── LICENSE
└── README.md
```

---

## Why ClipperTool? 🤷‍♂️

Because life is too short for messy clipboards. Plus, you get to say you use a *pro-level, funky, clipboard cleaning wizard* — and honestly, that sounds pretty cool at parties.

**Perfect for:**
- 💻 Developers cleaning code snippets
- 📊 Data analysts filtering CSV content  
- 📝 Writers removing unwanted formatting
- 🔍 Researchers cleaning scraped text
- 🤖 Anyone who copy-pastes like it's their job

---

## Contributing 🤝

ClipperTool is open source and ready for your magic touch!

- 🐛 **Found a bug?** Open an issue
- 💡 **Have an idea?** Start a discussion  
- 🛠️ **Want to contribute?** Fork and submit a PR
- ⭐ **Like the project?** Give it a star!

---

## 📄 License

This project is open source and licensed under the **[Eclipse Public License 2.0](https://www.eclipse.org/legal/epl-2.0/)**.  
Feel free to use, modify, and share it under the terms of the EPL.