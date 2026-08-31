#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AFAR ULTIMATE v1.0 – Build, Reverse & Guide
Author: MA.GH.AD (https://github.com/mahanneman)
License: MIT
"""

import os
import re
import json
import shutil
import zipfile
import subprocess
import tempfile
import webbrowser
import shlex
from datetime import datetime
from xml.dom import minidom
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import requests  # only used for GitHub login; we can remove if not used, but keep it harmless

THEME = {
    "bg": "#0a0e17",
    "panel": "#141d2b",
    "input": "#0d1520",
    "fg": "#e8edf5",
    "primary": "#818cf8",
    "success": "#34d399",
    "accent": "#f472b6",
    "warning": "#fbbf24",
    "danger": "#f87171",
    "info": "#60a5fa"
}

PATTERNS_50 = [
    r"^[├│└└──\s├──]+", r"^[└──\s│]+", r"^[─\s│├└]+", r"^[│\s]+",
    r"^[\s├└│─]+", r"^\d+\s*[\.\-\)]\s*", r"^\d+\s*[\.\-\)]\s*\d+[\.\-\)]\s*",
    r"^[•◦▪▫►▶▸▹◆◇◈○●◎◉◊□■]\s*", r"^[a-zA-Z][\.\-\)]\s*",
]

FILE_GROUPS = {
    "Web & Code": [".php", ".html", ".css", ".js", ".ts", ".json", ".py"],
    "Documents": [".txt", ".md", ".pdf", ".docx", ".xlsx", ".csv"],
    "Graphics": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"],
    "All": []
}

T = {
    "en": {
        "title": "AFAR ULTIMATE v1.0",
        "ready": "Ready",
        "tab_build": "📥 Build",
        "tab_reverse": "📤 Reverse",
        "tab_help": "📖 Guide",
        "dest": "Target Folder",
        "browse": "Browse",
        "injectors": "Injectors & Parser",
        "fallback": "Fallback Extension:",
        "force": "Force Modifier:",
        "readme": "Generate AI Readme",
        "gitkeep": "Inject .gitkeep",
        "raw": "1. Paste your tree/list here",
        "live": "2. Live Editor",
        "parse_btn": "⚡ Parse to Live",
        "clear_raw": "Clear Raw",
        "copy": "Copy",
        "clear_live": "Clear Live",
        "deploy": "🚀 Deploy Now",
        "source": "Source Folder",
        "browse_src": "Browse Source",
        "format": "Output Format & Filters",
        "style": "Export Style:",
        "group": "Group Filter:",
        "ext": "Specific extension:",
        "meta": "Append Size",
        "copy_out": "Copy Output",
        "clear_out": "Clear",
        "output": "Reverse Output",
        "run_rev": "⚡ Run Reverse",
        "help_title": "📖 Comprehensive Guide",
        "help_text": (
            "1️⃣ FOLDER: add slash at end (src/)\n"
            "2️⃣ FILE: include extension (index.php)\n"
            "3️⃣ NESTED: use indentation, bullets, or numbers\n"
            "4️⃣ AUTO‑DETECT: <?php → .php, <html → .html\n"
            "5️⃣ IGNORE: empty lines, comments (#, //, --)\n\n"
            "📘 EXAMPLES:\n"
            "src/\n"
            "    controllers/\n"
            "        HomeController.php\n"
            "    index.php\n"
            "public/\n"
            "    css/style.css\n"
            "README.md\n\n"
            "🔧 FORCE MODIFIERS:\n"
            "• Keep Original\n"
            "• Force MP4\n"
            "• Force MP3\n"
            "• Force HTML\n"
            "• Strip Extensions (Folders)\n\n"
            "📊 OUTPUT FORMATS:\n"
            "• Tree Structure\n"
            "• JSON Map\n"
            "• XML Sheet\n"
            "• Markdown Checklist\n"
            "• Flat Clean List\n\n"
            "💡 TIPS:\n"
            "• Right‑click for context menu\n"
            "• Use Preview in Code Injector\n"
            "• Customize colors in Settings"
        ),
        "context_copy": "Copy",
        "context_cut": "Cut",
        "context_paste": "Paste",
        "context_delete": "Delete",
        "context_select_all": "Select All",
    },
    "fa": {
        "title": "آفار التیمیت نسخه ۱.۰",
        "ready": "آماده",
        "tab_build": "📥 ساخت",
        "tab_reverse": "📤 معکوس",
        "tab_help": "📖 راهنما",
        "dest": "پوشه مقصد",
        "browse": "مرور",
        "injectors": "تزریق‌کننده و پردازشگر",
        "fallback": "پسوند پیش‌فرض:",
        "force": "اصلاح‌گر:",
        "readme": "تولید Readme هوشمند",
        "gitkeep": "تزریق .gitkeep",
        "raw": "۱. درخت/لیست را جای‌گذاری کنید",
        "live": "۲. ویرایشگر زنده",
        "parse_btn": "⚡ پردازش به ویرایشگر",
        "clear_raw": "پاک کردن ورودی",
        "copy": "کپی",
        "clear_live": "پاک کردن ویرایشگر",
        "deploy": "🚀 استقرار",
        "source": "پوشه مبدأ",
        "browse_src": "مرور مبدأ",
        "format": "فرمت خروجی و فیلترها",
        "style": "سبک خروجی:",
        "group": "فیلتر گروه:",
        "ext": "پسوند خاص:",
        "meta": "افزودن اندازه",
        "copy_out": "کپی خروجی",
        "clear_out": "پاک کردن",
        "output": "خروجی معکوس",
        "run_rev": "⚡ اجرای معکوس",
        "help_title": "📖 راهنمای جامع",
        "help_text": (
            "۱️⃣ پوشه: با اسلش تمام شود (src/)\n"
            "۲️⃣ فایل: پسوند داشته باشد (index.php)\n"
            "۳️⃣ تو در تو: از تورفتگی، گلوله یا شماره استفاده کنید\n"
            "۴️⃣ تشخیص خودکار: <?php → .php، <html → .html\n"
            "۵️⃣ نادیده گرفتن: خطوط خالی، کامنت‌ها (#, //, --)\n\n"
            "📘 نمونه‌ها:\n"
            "src/\n"
            "    controllers/\n"
            "        HomeController.php\n"
            "    index.php\n"
            "public/\n"
            "    css/style.css\n"
            "README.md\n\n"
            "🔧 اصلاح‌گرها:\n"
            "• حفظ اصلی\n"
            "• Force MP4\n"
            "• Force MP3\n"
            "• Force HTML\n"
            "• حذف پسوندها (پوشه)\n\n"
            "📊 فرمت‌های خروجی:\n"
            "• ساختار درختی\n"
            "• JSON\n"
            "• XML\n"
            "• Markdown چک‌لیست\n"
            "• لیست تخت\n\n"
            "💡 نکات:\n"
            "• راست‌کلیک برای منو\n"
            "• از Preview استفاده کنید\n"
            "• تنظیمات رنگ در Settings"
        ),
        "context_copy": "کپی",
        "context_cut": "برش",
        "context_paste": "چسباندن",
        "context_delete": "حذف",
        "context_select_all": "انتخاب همه",
    }
}


def add_context_menu(widget, lang):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label=T[lang]["context_copy"], command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label=T[lang]["context_cut"], command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_command(label=T[lang]["context_paste"], command=lambda: widget.event_generate("<<Paste>>"))
    menu.add_separator()
    menu.add_command(label=T[lang]["context_select_all"],
                     command=lambda: widget.tag_add("sel", "1.0", "end") if hasattr(widget, "tag_add") else None)

    def do_copy(e=None):
        try:
            widget.event_generate("<<Copy>>")
        except Exception:
            pass
        return "break"

    def do_cut(e=None):
        try:
            widget.event_generate("<<Cut>>")
        except Exception:
            pass
        return "break"

    def do_paste(e=None):
        try:
            widget.event_generate("<<Paste>>")
        except Exception:
            pass
        return "break"

    def do_select_all(e=None):
        try:
            if isinstance(widget, (tk.Text, scrolledtext.ScrolledText)):
                widget.tag_add("sel", "1.0", "end")
                widget.mark_set("insert", "1.0")
            else:
                widget.select_range(0, tk.END)
        except Exception:
            pass
        return "break"

    for seq in ("<Control-c>", "<Control-C>", "<Control-Insert>"):
        widget.bind(seq, do_copy)
    for seq in ("<Control-x>", "<Control-X>", "<Shift-Delete>"):
        widget.bind(seq, do_cut)
    for seq in ("<Control-v>", "<Control-V>", "<Shift-Insert>"):
        widget.bind(seq, do_paste)
    for seq in ("<Control-a>", "<Control-A>"):
        widget.bind(seq, do_select_all)

    def show_menu(e):
        try:
            widget.focus_set()
            menu.tk_popup(e.x_root, e.y_root)
        finally:
            menu.grab_release()
        return "break"

    widget.bind("<Button-3>", show_menu)
    widget.bind("<Button-1>", lambda e: widget.focus_set())
    return menu


def enable_mouse_scroll(widget):
    def on_mousewheel(event):
        if event.num == 5 or getattr(event, "delta", 0) < 0:
            widget.yview_scroll(1, "units")
        elif event.num == 4 or getattr(event, "delta", 0) > 0:
            widget.yview_scroll(-1, "units")
    widget.bind("<MouseWheel>", on_mousewheel)
    widget.bind("<Button-4>", on_mousewheel)
    widget.bind("<Button-5>", on_mousewheel)
    return widget


class AFAR:
    def __init__(self, root):
        self.root = root
        self.lang = "en"
        self.theme = THEME.copy()
        self.load_config()
        self.root.title(T[self.lang]["title"])
        self.root.geometry("1400x860")
        self.root.minsize(1200, 750)
        self.root.configure(bg=self.theme["bg"])

        self.target_dir = tk.StringVar()
        self.reverse_dir = tk.StringVar()
        self.fallback = tk.StringVar(value="Auto Detect")
        self.force = tk.StringVar(value="Keep Original")
        self.style = tk.StringVar(value="Tree Structure")
        self.group = tk.StringVar(value="All")
        self.specific_ext = tk.StringVar(value="")
        self.save_name = tk.StringVar(value="output.txt")
        self.cb_readme = tk.BooleanVar(value=True)
        self.cb_gitkeep = tk.BooleanVar(value=False)
        self.cb_meta = tk.BooleanVar(value=True)

        self.build_ui()
        self.create_status_bar()
        self.create_log()
        self.apply_theme()

    def load_config(self):
        cfg = os.path.expanduser("~/.afar.json")
        if os.path.exists(cfg):
            try:
                with open(cfg, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    self.lang = d.get("lang", "en")
                    self.theme.update(d.get("theme", THEME))
            except Exception:
                pass

    def save_config(self):
        cfg = os.path.expanduser("~/.afar.json")
        data = {"lang": self.lang, "theme": self.theme}
        try:
            with open(cfg, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def apply_theme(self):
        self.root.configure(bg=self.theme["bg"])
        if hasattr(self, "status_bar"):
            self.status_bar.config(bg=self.theme["panel"], fg="#94a3b8")
        if hasattr(self, "txt_log"):
            self.txt_log.config(bg="#020617", fg=self.theme["warning"])

    def build_ui(self):
        hdr = tk.Frame(self.root, bg=self.theme["panel"], height=50)
        hdr.pack(fill=tk.X, side=tk.TOP)

        # عنوان
        tk.Label(hdr, text=T[self.lang]["title"], bg=self.theme["panel"],
                 fg=self.theme["primary"], font=("Segoe UI", 13, "bold")).pack(side=tk.LEFT, padx=20, pady=8)

        # نویسنده و گیت‌هاب
        author_frame = tk.Frame(hdr, bg=self.theme["panel"])
        author_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(author_frame, text="MA.GH.AD", bg=self.theme["panel"],
                 fg=self.theme["fg"], font=("Segoe UI", 9, "italic")).pack(side=tk.LEFT)
        github_link = tk.Label(author_frame, text="GitHub", bg=self.theme["panel"],
                               fg=self.theme["info"], font=("Segoe UI", 9, "underline"), cursor="hand2")
        github_link.pack(side=tk.LEFT, padx=(5, 0))
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/mahanneman"))

        # زبان
        lang_frame = tk.Frame(hdr, bg=self.theme["panel"])
        lang_frame.pack(side=tk.RIGHT, padx=15)
        tk.Label(lang_frame, text="Language:", bg=self.theme["panel"], fg=self.theme["fg"]).pack(side=tk.LEFT, padx=5)
        self.lang_cb = ttk.Combobox(lang_frame, values=["English", "فارسی"], state="readonly", width=10)
        self.lang_cb.set("English" if self.lang == "en" else "فارسی")
        self.lang_cb.pack(side=tk.LEFT, padx=5)
        self.lang_cb.bind("<<ComboboxSelected>>", self.change_lang)

        # نوت‌بوک
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.frames = {}
        for key in ["build", "reverse", "help"]:
            f = tk.Frame(self.nb, bg=self.theme["bg"])
            self.nb.add(f, text=T[self.lang][f"tab_{key}"])
            self.frames[key] = f

        self.init_build()
        self.init_reverse()
        self.init_help()

    def change_lang(self, e=None):
        self.lang = "en" if self.lang_cb.get() == "English" else "fa"
        self.save_config()
        # بازسازی کامل UI
        for child in self.root.winfo_children():
            child.destroy()
        self.build_ui()
        self.create_status_bar()
        self.create_log()
        self.apply_theme()

    # ================= BUILD =================
    def init_build(self):
        f = self.frames["build"]
        p = tk.LabelFrame(f, text=T[self.lang]["dest"], bg=self.theme["panel"], fg=self.theme["primary"],
                          font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        p.pack(fill=tk.X, padx=12, pady=6, ipady=3)
        tk.Button(p, text=T[self.lang]["browse"], bg=self.theme["primary"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=4, command=self.browse_build).pack(side=tk.RIGHT, padx=10, pady=4)
        e = tk.Entry(p, textvariable=self.target_dir, bg=self.theme["input"], fg=self.theme["fg"],
                     font=("Consolas", 10), bd=1, relief=tk.SOLID, insertbackground=self.theme["fg"])
        e.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=4)
        add_context_menu(e, self.lang)

        mid = tk.Frame(f, bg=self.theme["bg"])
        mid.pack(fill=tk.BOTH, expand=True, padx=12)

        cfg = tk.LabelFrame(mid, text=T[self.lang]["injectors"], bg=self.theme["panel"], fg=self.theme["primary"],
                            font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        cfg.pack(side=tk.LEFT, fill=tk.Y, ipadx=10, ipady=8)

        tk.Label(cfg, text=T[self.lang]["fallback"], bg=self.theme["panel"], fg=self.theme["fg"]).pack(anchor=tk.W, padx=8, pady=(8, 2))
        ttk.Combobox(cfg, textvariable=self.fallback,
                     values=["Auto Detect", "No Extension (Folder)", ".php", ".html", ".js", ".py", ".json", ".txt", ".md", ".css"],
                     state="readonly").pack(fill=tk.X, padx=8, pady=4)

        tk.Label(cfg, text=T[self.lang]["force"], bg=self.theme["panel"], fg=self.theme["fg"]).pack(anchor=tk.W, padx=8, pady=(8, 2))
        ttk.Combobox(cfg, textvariable=self.force,
                     values=["Keep Original", "Force MP4", "Force MP3", "Force HTML", "Strip Extensions (Folders)"],
                     state="readonly").pack(fill=tk.X, padx=8, pady=4)

        tk.Checkbutton(cfg, text=T[self.lang]["readme"], variable=self.cb_readme,
                       bg=self.theme["panel"], fg=self.theme["fg"], selectcolor=self.theme["bg"]).pack(anchor=tk.W, padx=8, pady=2)
        tk.Checkbutton(cfg, text=T[self.lang]["gitkeep"], variable=self.cb_gitkeep,
                       bg=self.theme["panel"], fg=self.theme["fg"], selectcolor=self.theme["bg"]).pack(anchor=tk.W, padx=8, pady=2)

        paned = tk.PanedWindow(mid, orient=tk.HORIZONTAL, bg=self.theme["bg"], bd=0, sashwidth=4)
        paned.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(12, 0))

        left = tk.LabelFrame(paned, text=T[self.lang]["raw"], bg=self.theme["panel"], fg=self.theme["primary"],
                             font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        self.txt_raw = scrolledtext.ScrolledText(left, bg=self.theme["input"], fg=self.theme["fg"],
                                                 font=("Consolas", 10), bd=0, insertbackground=self.theme["fg"])
        self.txt_raw.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        enable_mouse_scroll(self.txt_raw)
        add_context_menu(self.txt_raw, self.lang)
        bl = tk.Frame(left, bg=self.theme["panel"])
        bl.pack(fill=tk.X, padx=4, pady=4)
        tk.Button(bl, text=T[self.lang]["parse_btn"], bg=self.theme["accent"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=10, pady=3, command=self.parse).pack(side=tk.LEFT, padx=3)
        tk.Button(bl, text=T[self.lang]["clear_raw"], bg=self.theme["panel"], fg=self.theme["danger"],
                  font=("Segoe UI", 9), bd=1, padx=10, pady=3, command=lambda: self.txt_raw.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=3)

        right = tk.LabelFrame(paned, text=T[self.lang]["live"], bg=self.theme["panel"], fg=self.theme["warning"],
                              font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        self.txt_live = scrolledtext.ScrolledText(right, bg=self.theme["input"], fg=self.theme["warning"],
                                                  font=("Consolas", 10), bd=0, insertbackground=self.theme["fg"])
        self.txt_live.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        enable_mouse_scroll(self.txt_live)
        add_context_menu(self.txt_live, self.lang)
        br = tk.Frame(right, bg=self.theme["panel"])
        br.pack(fill=tk.X, padx=4, pady=4)
        tk.Button(br, text=T[self.lang]["copy"], bg=self.theme["panel"], fg=self.theme["fg"],
                  font=("Segoe UI", 9), bd=1, padx=10, pady=3, command=lambda: self.copy_to_clip(self.txt_live)).pack(side=tk.LEFT, padx=3)
        tk.Button(br, text=T[self.lang]["clear_live"], bg=self.theme["panel"], fg=self.theme["danger"],
                  font=("Segoe UI", 9), bd=1, padx=10, pady=3, command=lambda: self.txt_live.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=3)

        paned.add(left, width=450)
        paned.add(right, width=450)

        tk.Button(f, text=T[self.lang]["deploy"], bg=self.theme["success"], fg=self.theme["bg"],
                  font=("Segoe UI", 12, "bold"), bd=0, pady=10, command=self.deploy).pack(fill=tk.X, padx=12, pady=10)

    def browse_build(self):
        d = filedialog.askdirectory()
        if d:
            self.target_dir.set(d)
            self.log("Target: " + d)

    def parse(self):
        raw = self.txt_raw.get("1.0", tk.END).strip()
        if not raw:
            messagebox.showwarning("Warning", "Raw input is empty!")
            return
        lines = raw.splitlines()
        out = []
        for line in lines:
            line = re.sub(r"\s*(#|//|--).*$", "", line)
            for p in PATTERNS_50:
                line = re.sub(p, "", line)
            line = line.strip()
            if not line:
                continue
            if self.fallback.get() == "Auto Detect":
                ext = self.detect_ext(line)
                if ext and "." not in line and not line.endswith("/"):
                    line += ext
            out.append(line)
        self.txt_live.delete("1.0", tk.END)
        self.txt_live.insert(tk.END, "\n".join(out))
        self.log(f"Parsed {len(out)} items")

    def detect_ext(self, line):
        known = [".php", ".html", ".js", ".py", ".json", ".txt", ".md", ".css"]
        for e in known:
            if line.strip().endswith(e):
                return e
        if re.search(r"<\?php", line):
            return ".php"
        if re.search(r"<html", line, re.I):
            return ".html"
        if re.search(r"def\s+\w+\s*\(", line):
            return ".py"
        return None

    def deploy(self):
        out = self.target_dir.get()
        if not out:
            messagebox.showerror("Error", "Target folder not set.")
            return
        text = self.txt_live.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Live editor empty.")
            return
        lines = text.splitlines()
        dirs, files = 0, 0
        for item in lines:
            item = item.strip()
            if not item:
                continue
            is_dir = item.endswith("/") or item.endswith("\\") or ("." not in item and self.fallback.get() == "No Extension (Folder)")
            force = self.force.get()
            if not is_dir and "." not in item:
                if force == "Keep Original":
                    fb = self.fallback.get()
                    if fb not in ["Auto Detect", "No Extension (Folder)"]:
                        item += fb
                    else:
                        is_dir = True
                elif force == "Force MP4":
                    item += ".mp4"
                elif force == "Force MP3":
                    item += ".mp3"
                elif force == "Force HTML":
                    item += ".html"
                elif force == "Strip Extensions (Folders)":
                    is_dir = True
            full = os.path.join(out, item.replace("/", os.sep).replace("\\", os.sep))
            try:
                if is_dir:
                    os.makedirs(full, exist_ok=True)
                    dirs += 1
                    if self.cb_gitkeep.get():
                        open(os.path.join(full, ".gitkeep"), "w").close()
                else:
                    os.makedirs(os.path.dirname(full) or full, exist_ok=True)
                    open(full, "a", encoding="utf-8").close()
                    files += 1
            except Exception as e:
                self.log(f"Error: {item} – {e}")
        if self.cb_readme.get():
            try:
                with open(os.path.join(out, "AI_README.md"), "w", encoding="utf-8") as f:
                    f.write(f"# AI Structure\n\nDate: {datetime.now()}\nDirs: {dirs}\nFiles: {files}")
            except Exception:
                pass
        self.log(f"Deployed: {dirs} dirs, {files} files")
        messagebox.showinfo("Done", f"Deployed: {dirs} dirs, {files} files")

    # ================= REVERSE =================
    def init_reverse(self):
        f = self.frames["reverse"]
        p = tk.LabelFrame(f, text=T[self.lang]["source"], bg=self.theme["panel"], fg=self.theme["primary"],
                          font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        p.pack(fill=tk.X, padx=12, pady=6, ipady=3)
        tk.Button(p, text=T[self.lang]["browse_src"], bg=self.theme["primary"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=4, command=self.browse_reverse).pack(side=tk.RIGHT, padx=10, pady=4)
        e = tk.Entry(p, textvariable=self.reverse_dir, bg=self.theme["input"], fg=self.theme["fg"],
                     font=("Consolas", 10), bd=1, relief=tk.SOLID, insertbackground=self.theme["fg"])
        e.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=4)
        add_context_menu(e, self.lang)

        mid = tk.Frame(f, bg=self.theme["bg"])
        mid.pack(fill=tk.BOTH, expand=True, padx=12)

        cfg = tk.LabelFrame(mid, text=T[self.lang]["format"], bg=self.theme["panel"], fg=self.theme["primary"],
                            font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        cfg.pack(side=tk.LEFT, fill=tk.Y, ipadx=10, ipady=8)

        tk.Label(cfg, text=T[self.lang]["style"], bg=self.theme["panel"], fg=self.theme["fg"]).pack(anchor=tk.W, padx=8, pady=(8, 2))
        ttk.Combobox(cfg, textvariable=self.style,
                     values=["Tree Structure", "JSON Map", "XML Sheet", "Markdown Checklist", "Flat Clean List"],
                     state="readonly").pack(fill=tk.X, padx=8, pady=4)

        tk.Label(cfg, text=T[self.lang]["group"], bg=self.theme["panel"], fg=self.theme["fg"]).pack(anchor=tk.W, padx=8, pady=(8, 2))
        ttk.Combobox(cfg, textvariable=self.group, values=list(FILE_GROUPS.keys()), state="readonly").pack(fill=tk.X, padx=8, pady=4)

        tk.Label(cfg, text=T[self.lang]["ext"], bg=self.theme["panel"], fg=self.theme["fg"]).pack(anchor=tk.W, padx=8, pady=(8, 2))
        ext_entry = tk.Entry(cfg, textvariable=self.specific_ext, bg=self.theme["input"], fg=self.theme["fg"],
                             font=("Consolas", 10), bd=1, relief=tk.SOLID, insertbackground=self.theme["fg"])
        ext_entry.pack(fill=tk.X, padx=8, pady=4)
        add_context_menu(ext_entry, self.lang)

        tk.Checkbutton(cfg, text=T[self.lang]["meta"], variable=self.cb_meta,
                       bg=self.theme["panel"], fg=self.theme["fg"], selectcolor=self.theme["bg"]).pack(anchor=tk.W, padx=8, pady=4)

        bf = tk.Frame(cfg, bg=self.theme["panel"])
        bf.pack(fill=tk.X, padx=8, pady=6)
        tk.Button(bf, text=T[self.lang]["copy_out"], bg=self.theme["panel"], fg=self.theme["fg"],
                  font=("Segoe UI", 9), bd=1, padx=10, pady=3, command=lambda: self.copy_to_clip(self.txt_out)).pack(side=tk.LEFT, padx=3)
        tk.Button(bf, text=T[self.lang]["clear_out"], bg=self.theme["panel"], fg=self.theme["danger"],
                  font=("Segoe UI", 9), bd=1, padx=10, pady=3, command=lambda: self.txt_out.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=3)

        out_f = tk.LabelFrame(mid, text=T[self.lang]["output"], bg=self.theme["panel"], fg=self.theme["primary"],
                              font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        out_f.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(12, 0))
        self.txt_out = scrolledtext.ScrolledText(out_f, bg=self.theme["input"], fg=self.theme["fg"],
                                                 font=("Consolas", 10), bd=0, insertbackground=self.theme["fg"])
        self.txt_out.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        enable_mouse_scroll(self.txt_out)
        add_context_menu(self.txt_out, self.lang)

        tk.Button(f, text=T[self.lang]["run_rev"], bg=self.theme["primary"], fg=self.theme["bg"],
                  font=("Segoe UI", 12, "bold"), bd=0, pady=10, command=self.run_reverse).pack(fill=tk.X, padx=12, pady=10)

    def browse_reverse(self):
        d = filedialog.askdirectory()
        if d:
            self.reverse_dir.set(d)
            self.log("Source: " + d)

    def run_reverse(self):
        src = self.reverse_dir.get()
        if not src or not os.path.exists(src):
            messagebox.showerror("Error", "Invalid source folder.")
            return
        style = self.style.get()
        grp = self.group.get()
        spec = self.specific_ext.get().strip()
        allowed = FILE_GROUPS.get(grp, []) if grp != "All" else []
        use_spec = bool(spec)
        buf = []
        if style == "Tree Structure":
            self.gen_tree(src, "", allowed, use_spec, spec, buf)
            final = "\n".join(buf)
        elif style == "JSON Map":
            data = self.gen_dict(src, allowed, use_spec, spec)
            final = json.dumps(data, indent=4, ensure_ascii=False)
        elif style == "XML Sheet":
            root = ET.Element("Structure", Name=os.path.basename(src))
            self.gen_xml(src, root, allowed, use_spec, spec)
            final = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        elif style == "Markdown Checklist":
            self.gen_md(src, 0, allowed, use_spec, spec, buf)
            final = "\n".join(buf)
        else:
            self.gen_flat(src, src, allowed, use_spec, spec, buf)
            final = "\n".join(buf)
        self.txt_out.delete("1.0", tk.END)
        self.txt_out.insert(tk.END, final)
        self.log("Reverse output generated")

    def include(self, name, allowed, use_spec, spec):
        if use_spec:
            return name.endswith(spec)
        if allowed:
            return any(name.endswith(e) for e in allowed)
        return True

    def gen_tree(self, path, pref, allowed, use_spec, spec, buf):
        try:
            items = sorted(os.listdir(path))
        except Exception:
            return
        ptrs = ["├── "] * (len(items) - 1) + ["└── "]
        for ptr, name in zip(ptrs, items):
            full = os.path.join(path, name)
            if os.path.isdir(full):
                buf.append(f"{pref}{ptr}{name}/")
                ext = "│   " if ptr == "├── " else "    "
                self.gen_tree(full, pref + ext, allowed, use_spec, spec, buf)
            else:
                if self.include(name, allowed, use_spec, spec):
                    meta = f" ({os.path.getsize(full)} bytes)" if self.cb_meta.get() else ""
                    buf.append(f"{pref}{ptr}{name}{meta}")

    def gen_dict(self, path, allowed, use_spec, spec):
        d = {"name": os.path.basename(path), "type": "dir", "children": []}
        try:
            for name in sorted(os.listdir(path)):
                full = os.path.join(path, name)
                if os.path.isdir(full):
                    d["children"].append(self.gen_dict(full, allowed, use_spec, spec))
                else:
                    if self.include(name, allowed, use_spec, spec):
                        item = {"name": name, "type": "file"}
                        if self.cb_meta.get():
                            item["size"] = os.path.getsize(full)
                        d["children"].append(item)
        except Exception:
            pass
        return d

    def gen_xml(self, path, parent, allowed, use_spec, spec):
        try:
            for name in sorted(os.listdir(path)):
                full = os.path.join(path, name)
                if os.path.isdir(full):
                    sub = ET.SubElement(parent, "Dir", Name=name)
                    self.gen_xml(full, sub, allowed, use_spec, spec)
                else:
                    if self.include(name, allowed, use_spec, spec):
                        el = ET.SubElement(parent, "File", Name=name)
                        if self.cb_meta.get():
                            el.set("Size", str(os.path.getsize(full)))
        except Exception:
            pass

    def gen_md(self, path, level, allowed, use_spec, spec, buf):
        ind = "  " * level
        try:
            for name in sorted(os.listdir(path)):
                full = os.path.join(path, name)
                if os.path.isdir(full):
                    buf.append(f"{ind}- [ ] 📁 {name}")
                    self.gen_md(full, level + 1, allowed, use_spec, spec, buf)
                else:
                    if self.include(name, allowed, use_spec, spec):
                        buf.append(f"{ind}- [ ] 📄 {name}")
        except Exception:
            pass

    def gen_flat(self, base, cur, allowed, use_spec, spec, buf):
        try:
            for name in sorted(os.listdir(cur)):
                full = os.path.join(cur, name)
                if os.path.isdir(full):
                    self.gen_flat(base, full, allowed, use_spec, spec, buf)
                else:
                    if self.include(name, allowed, use_spec, spec):
                        buf.append(os.path.relpath(full, base))
        except Exception:
            pass

    # ================= HELP =================
    def init_help(self):
        f = self.frames["help"]
        txt = scrolledtext.ScrolledText(f, bg=self.theme["input"], fg=self.theme["fg"],
                                        font=("Consolas", 11), bd=0)
        txt.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        txt.insert(tk.END, T[self.lang]["help_text"])
        txt.config(state="disabled")
        add_context_menu(txt, self.lang)

    # ================= STATUS & LOG =================
    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, text=T[self.lang]["ready"], bg=self.theme["panel"],
                                   fg="#94a3b8", anchor=tk.W, font=("Segoe UI", 9), padx=10)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_log(self):
        f = tk.LabelFrame(self.root, text="📋 Live Log", bg=self.theme["panel"], fg=self.theme["warning"],
                          font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        f.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=(0, 6))
        self.txt_log = scrolledtext.ScrolledText(f, bg="#020617", fg=self.theme["warning"],
                                                 font=("Consolas", 9), height=4, bd=0, insertbackground=self.theme["fg"])
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        enable_mouse_scroll(self.txt_log)
        add_context_menu(self.txt_log, self.lang)

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.txt_log.insert(tk.END, f"[{ts}] {msg}\n")
        self.txt_log.see(tk.END)

    def copy_to_clip(self, widget):
        self.root.clipboard_clear()
        self.root.clipboard_append(widget.get("1.0", tk.END).strip())
        self.log("Copied to clipboard")


if __name__ == "__main__":
    root = tk.Tk()
    app = AFAR(root)
    root.mainloop()