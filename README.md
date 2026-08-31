
markdown
[🇬🇧 English](README.md) | [🇮🇷 فارسی](README.fa.md)

# 📁 AFAR Ultimate v7.0 – File Architecture & Reverse-engineering Tool

**AFAR (AI-Ready File Architecture & Reverse-engineering)** is a powerful cross‑platform desktop application that lets you build complex folder/file structures from a simple text list, reverse‑engineer any existing directory into a clean AI‑ready prompt, and manage your Git/GitHub repositories with a rich graphical interface.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Table of Contents
- [Key Features](#-key-features)
- [Installation & Requirements](#-installation--requirements)
- [How to Use](#-how-to-use)
- [Advanced Git Commands](#-advanced-git-commands)
- [Customization](#-customization)
- [Author & Credit](#-author--credit)
- [License](#-license)

---

## 🌟 Key Features

| Feature | Description |
|---------|-------------|
| **📥 Forward Engine** | Paste any tree, bullet, numbered, or emoji list, then instantly deploy the structure to your disk. |
| **📤 Reverse Engine** | Scan any folder and export its structure as Tree, JSON, XML, Markdown Checklist, or Flat List. |
| **🐙 Full GitHub Integration** | Login with your personal access token, list repos, create new repos, clone, commit, push, pull, and manage local repositories. |
| **📂 File Tree & Editor** | Browse, open, edit, and save files directly inside the app. |
| **⚡ 20+ Git Commands** | Run custom Git commands or use 5 one‑click quick actions (status, log, diff, branches, remotes). |
| **🛠️ File Operations** | Create, delete, and rename files in bulk – all from a clean UI. |
| **🌐 Bilingual Interface** | Switch seamlessly between English and Persian (فارسی). |
| **🎨 Customizable Colors** | Choose your own theme colors from the Settings tab. |
| **📋 Live Log & Context Menus** | Right‑click any text area for copy/paste/delete/select all, and watch all operations in the live log panel. |
| **💾 Export & ZIP** | Save reverse output to a file or compress your project into a ZIP archive. |

---

## 🚀 Installation & Requirements

### Prerequisites
- **Python 3.8 or higher**
- **Git** installed and accessible from the command line (for GitHub features)
- **requests** library (for GitHub API calls)

### Install Dependencies
```bash
pip install requests
Download & Run
bash
git clone https://github.com/mahanneman/AFAR-Ultimate.git
cd AFAR-Ultimate
python afar_ultimate_v7.py
📖 How to Use
1️⃣ Build a Structure
Open the Build tab and choose a target folder (click Browse).

Paste your list (tree, bullets, numbers, emojis) into the Raw Input area.

Click Parse to Live to clean the list and auto‑detect file extensions.

Edit the result in the Live Editor if needed.

Hit Deploy Now – your folders and files are created instantly.

2️⃣ Reverse‑engineer a Folder
Open the Reverse tab and select a source folder.

Choose your output format (Tree, JSON, XML, Markdown Checklist, or Flat List).

Optionally filter by file group or specific extension.

Click Run Reverse – the result appears in the output area.

Use the Export tab to save the result to a file.

3️⃣ Work with GitHub
Open the GitHub tab and enter your Personal Access Token (with repo and workflow scopes).

Click Login & Save – you’ll see your token status.

Click Refresh Repos to list your repositories.

To create a new repo, enter a name and description, then click Create.

Set a Local Repo Path (where you want to clone or work).

Use Clone to download a repo, then use Commit, Push, and Pull buttons.

Browse the file tree, double‑click any file to open it in the editor, edit, and click Save File.

Use the Git Commands section to run custom commands or use the 5 quick actions.

All Git operations are logged in the Git Actions Log.

🛠️ Advanced Git Commands
You can run any Git command by typing it in the Custom Command field and clicking Run.
For quick access, five common commands are provided as one‑click buttons:

git status

git log --oneline -10

git diff

git branch -a

git remote -v

🎨 Customization
Language – Change between English and Persian from the header or Settings tab.

Colors – In the Settings tab, click any color button to pick a new color for that element.

👤 Author & Credit
Developed by MA.GH.AD
🔗 https://github.com/mahanneman

📄 License
This project is licensed under the MIT License – see the LICENSE file for details.

Tip: AFAR Ultimate is designed to streamline your file architecture workflow and make GitHub management a breeze. Enjoy!
