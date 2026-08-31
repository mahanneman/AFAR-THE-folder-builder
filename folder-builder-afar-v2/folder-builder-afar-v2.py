#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AFAR ULTIMATE V2.0 – Build, Reverse, Export & Settings
Author: MHAAN NEMAN
GitHub: https://github.com/mahanneman
License: MIT
"""

import os
import re
import json
import shutil
import zipfile
import subprocess
import webbrowser
from datetime import datetime
from xml.dom import minidom
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext, colorchooser

# ============================================================================
# THEME
# ============================================================================
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

# ============================================================================
# 50 REGEX PATTERNS
# ============================================================================
PATTERNS_50 = [
    r"^[├│└└──\s├──]+", r"^[└──\s│]+", r"^[─\s│├└]+", r"^[│\s]+",
    r"^[\s├└│─]+", r"^\d+\s*[\.\-\)]\s*", r"^\d+\s*[\.\-\)]\s*\d+[\.\-\)]\s*",
    r"^\d+\s*[\.\-\)]\s*\d+[\.\-\)]\s*\d+[\.\-\)]\s*", r"^[①-⑳]\s*", r"^[❶-❿]\s*",
    r"^[a-zA-Z][\.\-\)]\s*", r"^[A-Z][\.\-\)]\s*", r"^[a-z][\.\-\)]\s*",
    r"^[I|V|X|L|C|D|M]+[\.\-\)]\s*", r"^[i|v|x|l|c|d|m]+[\.\-\)]\s*",
    r"^[•◦▪▫►▶▸▹◆◇◈○●◎◉◊□■▣▤▥▦▧▨▩▪▫▬▭▮▯]\s*",
    r"^[➤➢➣➤➥➦➧➨➩➪➫➬➭➮➯➰➱➲➳➴➵➶➷➸➹➺➻➼➽➾]\s*",
    r"^[✧✦✩✪✫✬✭✮✯✰✱✲✳✴✵✶✷✸✹✺✻✼✽✾✿❀❁❂❃❄❅❆❇❈❉❊❋]\s*",
    r"^[❚❘❙❛❜❝❞❡❢❣❤❥❦❧❨❩❪❫❬❭❮❯❰❱❲❳❴❵]\s*", r"^[➀-➉]\s*",
    r"^§\s*", r"^¶\s*", r"^©\s*", r"^®\s*", r"^™\s*",
]

# ============================================================================
# FILE GROUPS
# ============================================================================
FILE_GROUPS = {
    "Web & Code": [".php", ".html", ".css", ".js", ".ts", ".json", ".py", ".cpp", ".go", ".rs", ".rb"],
    "Media": [".mp4", ".mkv", ".avi", ".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a"],
    "Documents": [".txt", ".md", ".pdf", ".docx", ".xlsx", ".csv", ".xml", ".yaml", ".toml"],
    "Graphics": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".psd", ".ai", ".eps", ".webp"],
    "Container": [".dockerfile", ".k8s.yaml", ".tf", ".nomad"],
    "Frontend": [".jsx", ".tsx", ".vue", ".svelte"],
    "All": []
}

# ============================================================================
# BILINGUAL DICTIONARY
# ============================================================================
T = {
    "en": {
        "title": "⚡ AFAR ULTIMATE V2.0",
        "ready": "Ready",
        "tab_build": "📥 Build",
        "tab_reverse": "📤 Reverse",
        "tab_help": "📖 Guide",
        "tab_export": "💾 Export",
        "tab_settings": "⚙️ Settings",
        "dest": "Target Folder",
        "browse": "Browse",
        "injectors": "Injectors & Parser",
        "fallback": "Fallback Extension:",
        "fallback_tip": "If a file has no extension, this will be added automatically.",
        "force": "Force Modifier:",
        "force_tip": "Apply a forced extension to all files, or convert all items to folders.",
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
        "export_title": "💾 Export & Save",
        "save_as": "Save output as:",
        "save_btn": "Save to File",
        "zip_btn": "Create ZIP",
        "settings_title": "⚙️ Settings",
        "lang": "Language:",
        "color_primary": "Primary Color:",
        "color_success": "Success Color:",
        "color_accent": "Accent Color:",
        "color_warning": "Warning Color:",
        "color_danger": "Danger Color:",
        "color_info": "Info Color:",
        "reset_colors": "Reset Colors",
        "save_settings": "Save Settings",
        "context_copy": "Copy",
        "context_cut": "Cut",
        "context_paste": "Paste",
        "context_delete": "Delete",
        "context_select_all": "Select All",
        "help_title": "📖 Comprehensive Guide",
        "help_s1": "🔹 BASIC RULES",
        "help_s2": "🔹 EXAMPLES",
        "help_s3": "🔹 FORCE MODIFIERS",
        "help_s4": "🔹 OUTPUT FORMATS",
        "help_s5": "🔹 QUICK TIPS",
        "help_text": "1. FOLDER: add slash at end (src/)\n2. FILE: include extension (index.php)\n3. NESTED: use indentation, bullets, or numbers\n4. AUTO-DETECT: <?php → .php, <html → .html\n5. IGNORE: empty lines, comments (#, //, --)",
        "help_ex": "▶ TREE:\nsrc/\n    controllers/\n        HomeController.php\n    index.php\npublic/\n    css/style.css\nREADME.md",
        "help_force": "1. Keep Original\n2. Force MP4\n3. Force MP3\n4. Force HTML\n5. Strip Extensions (Folders)",
        "help_rev": "1. Tree Structure\n2. JSON Map\n3. XML Sheet\n4. Markdown Checklist\n5. Flat Clean List",
        "help_tips": "• Right-click for context menu\n• Type directly in Live Editor\n• Customize colors in Settings",
        "credit": "Developed by MHAAN NEMAN",
        "credit_link": "https://github.com/mahanneman"
    },
    "fa": {
        "title": "⚡ آفار التیمیت نسخه ۳.۰",
        "ready": "آماده",
        "tab_build": "📥 ساخت",
        "tab_reverse": "📤 معکوس",
        "tab_help": "📖 راهنما",
        "tab_export": "💾 خروجی",
        "tab_settings": "⚙️ تنظیمات",
        "dest": "پوشه مقصد",
        "browse": "مرور",
        "injectors": "تزریق‌کننده و پردازشگر",
        "fallback": "پسوند پیش‌فرض:",
        "fallback_tip": "اگر فایل پسوند نداشته باشد، این پسوند اضافه می‌شود.",
        "force": "اصلاح‌گر:",
        "force_tip": "یک پسوند اجباری به همه فایل‌ها اعمال کنید، یا همه موارد را به پوشه تبدیل کنید.",
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
        "export_title": "💾 ذخیره و خروجی",
        "save_as": "ذخیره خروجی به‌عنوان:",
        "save_btn": "ذخیره در فایل",
        "zip_btn": "ایجاد ZIP",
        "settings_title": "⚙️ تنظیمات",
        "lang": "زبان:",
        "color_primary": "رنگ اصلی:",
        "color_success": "رنگ موفقیت:",
        "color_accent": "رنگ برجسته:",
        "color_warning": "رنگ هشدار:",
        "color_danger": "رنگ خطر:",
        "color_info": "رنگ اطلاعات:",
        "reset_colors": "بازنشانی رنگ‌ها",
        "save_settings": "ذخیره تنظیمات",
        "context_copy": "کپی",
        "context_cut": "برش",
        "context_paste": "چسباندن",
        "context_delete": "حذف",
        "context_select_all": "انتخاب همه",
        "help_title": "📖 راهنمای جامع",
        "help_s1": "🔹 قوانین پایه",
        "help_s2": "🔹 نمونه‌ها",
        "help_s3": "🔹 اصلاح‌گرها",
        "help_s4": "🔹 فرمت‌های خروجی",
        "help_s5": "🔹 نکات سریع",
        "help_text": "۱. پوشه: با اسلش تمام شود (src/)\n۲. فایل: پسوند داشته باشد (index.php)\n۳. تو در تو: از تورفتگی، گلوله یا شماره\n۴. تشخیص خودکار: <?php → .php, <html → .html\n۵. خطوط خالی و کامنت‌ها نادیده گرفته می‌شوند",
        "help_ex": "▶ درختی:\nsrc/\n    controllers/\n        HomeController.php\n    index.php\npublic/\n    css/style.css\nREADME.md",
        "help_force": "۱. حفظ اصلی\n۲. تبدیل به MP4\n۳. تبدیل به MP3\n۴. تبدیل به HTML\n۵. حذف پسوندها (پوشه)",
        "help_rev": "۱. ساختار درختی\n۲. نقشه JSON\n۳. برگه XML\n۴. چک‌لیست مارک‌داون\n۵. لیست تخت",
        "help_tips": "• راست‌کلیک برای منو\n• مستقیماً در ویرایشگر زنده تایپ کنید\n• رنگ‌ها را در تنظیمات شخصی‌سازی کنید",
        "credit": "تهیه‌شده توسط MHAAN NEMAN",
        "credit_link": "https://github.com/mahanneman"
    }
}

# ============================================================================
# CONTEXT MENU & MOUSE SCROLL
# ============================================================================
def add_context_menu(widget, lang):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label=T[lang]["context_copy"], command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label=T[lang]["context_cut"], command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_command(label=T[lang]["context_paste"], command=lambda: widget.event_generate("<<Paste>>"))
    menu.add_separator()
    menu.add_command(label=T[lang]["context_delete"], command=lambda: widget.delete("sel.first", "sel.last") if widget.tag_ranges("sel") else None)
    menu.add_command(label=T[lang]["context_select_all"], command=lambda: widget.tag_add("sel", "1.0", "end") if hasattr(widget, "tag_add") else None)
    def show(e):
        try:
            menu.tk_popup(e.x_root, e.y_root)
        finally:
            menu.grab_release()
    widget.bind("<Button-3>", show)
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

# ============================================================================
# MAIN CLASS
# ============================================================================
class AFAR:
    def __init__(self, root):
        self.root = root
        self.lang = "en"
        self.theme = THEME.copy()
        self.load_config()
        self.root.title(T[self.lang]["title"])
        self.root.geometry("1350x820")
        self.root.minsize(1150, 700)
        self.root.configure(bg=self.theme["bg"])

        self.target_dir = tk.StringVar()
        self.reverse_dir = tk.StringVar()
        self.fallback = tk.StringVar(value="Auto Detect")
        self.force = tk.StringVar(value="Keep Original")
        self.style = tk.StringVar(value="Tree Structure")
        self.group = tk.StringVar(value="All")
        self.specific_ext = tk.StringVar(value="")
        self.save_name = tk.StringVar(value="output.txt")
        self.zip_name = tk.StringVar(value="backup.zip")
        self.cb_readme = tk.BooleanVar(value=True)
        self.cb_gitkeep = tk.BooleanVar(value=False)
        self.cb_meta = tk.BooleanVar(value=True)

        self.build_ui()
        self.create_status_bar()
        self.create_log()
        self.create_credit_footer()
        self.apply_theme()
        self.update_status_lang()

    # ------------------------------------------------------------------------
    # CONFIG
    # ------------------------------------------------------------------------
    def load_config(self):
        cfg = os.path.expanduser("~/.afar.json")
        if os.path.exists(cfg):
            try:
                with open(cfg, 'r') as f:
                    d = json.load(f)
                    self.lang = d.get("lang", "en")
                    self.theme.update(d.get("theme", THEME))
            except:
                pass

    def save_config(self):
        cfg = os.path.expanduser("~/.afar.json")
        data = {"lang": self.lang, "theme": self.theme}
        with open(cfg, 'w') as f:
            json.dump(data, f, indent=2)

    # ------------------------------------------------------------------------
    # THEME APPLICATION
    # ------------------------------------------------------------------------
    def apply_theme(self):
        self.root.configure(bg=self.theme["bg"])
        if hasattr(self, 'status_bar'):
            self.status_bar.config(bg=self.theme["panel"], fg="#94a3b8")
        if hasattr(self, 'txt_log'):
            self.txt_log.config(bg="#020617", fg=self.theme["warning"])
        def rec(w):
            try:
                if isinstance(w, (tk.Frame, tk.LabelFrame, tk.PanedWindow)):
                    w.configure(bg=self.theme["panel"])
                elif isinstance(w, tk.Label):
                    w.configure(bg=self.theme["panel"] if w.master != self.root else self.theme["bg"], fg=self.theme["fg"])
                elif isinstance(w, tk.Entry):
                    w.configure(bg=self.theme["input"], fg=self.theme["fg"])
                elif isinstance(w, (tk.Text, scrolledtext.ScrolledText)):
                    w.configure(bg=self.theme["input"], fg=self.theme["fg"])
                elif isinstance(w, ttk.Combobox):
                    s = ttk.Style()
                    s.configure("TCombobox", fieldbackground=self.theme["input"],
                               background=self.theme["panel"], foreground=self.theme["fg"])
                elif isinstance(w, tk.Listbox):
                    w.configure(bg=self.theme["input"], fg=self.theme["fg"])
            except:
                pass
            for ch in w.winfo_children():
                rec(ch)
        for ch in self.root.winfo_children():
            rec(ch)

    # ------------------------------------------------------------------------
    # UI BUILD
    # ------------------------------------------------------------------------
    def build_ui(self):
        hdr = tk.Frame(self.root, bg=self.theme["panel"], height=50)
        hdr.pack(fill=tk.X, side=tk.TOP)
        tk.Label(hdr, text=T[self.lang]["title"], bg=self.theme["panel"],
                 fg=self.theme["primary"], font=("Segoe UI", 13, "bold")).pack(side=tk.LEFT, padx=20, pady=8)

        # Author & GitHub link
        author_frame = tk.Frame(hdr, bg=self.theme["panel"])
        author_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(author_frame, text="MHAAN NEMAN", bg=self.theme["panel"],
                 fg=self.theme["fg"], font=("Segoe UI", 9, "italic")).pack(side=tk.LEFT)
        github_link = tk.Label(author_frame, text="GitHub", bg=self.theme["panel"],
                               fg=self.theme["info"], font=("Segoe UI", 9, "underline"), cursor="hand2")
        github_link.pack(side=tk.LEFT, padx=(5,0))
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/mahanneman"))

        # Language selector
        lang_frame = tk.Frame(hdr, bg=self.theme["panel"])
        lang_frame.pack(side=tk.RIGHT, padx=15)
        tk.Label(lang_frame, text="Language:", bg=self.theme["panel"], fg=self.theme["fg"]).pack(side=tk.LEFT, padx=5)
        self.lang_cb = ttk.Combobox(lang_frame, values=["English", "فارسی"], state="readonly", width=10)
        self.lang_cb.set("English" if self.lang=="en" else "فارسی")
        self.lang_cb.pack(side=tk.LEFT, padx=5)
        self.lang_cb.bind("<<ComboboxSelected>>", self.change_lang)

        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        tabs = ["build", "reverse", "help", "export", "settings"]
        self.frames = {}
        for t in tabs:
            f = tk.Frame(self.nb, bg=self.theme["bg"])
            self.nb.add(f, text=T[self.lang][f"tab_{t}"])
            self.frames[t] = f

        self.init_build()
        self.init_reverse()
        self.init_help()
        self.init_export()
        self.init_settings()

    def refresh_ui(self):
        readme_val = self.cb_readme.get()
        gitkeep_val = self.cb_gitkeep.get()
        meta_val = self.cb_meta.get()
        for child in self.root.winfo_children():
            child.destroy()
        self.build_ui()
        self.create_status_bar()
        self.create_log()
        self.create_credit_footer()
        self.apply_theme()
        self.update_status_lang()
        self.cb_readme.set(readme_val)
        self.cb_gitkeep.set(gitkeep_val)
        self.cb_meta.set(meta_val)

    def change_lang(self, e=None):
        self.lang = "en" if self.lang_cb.get() == "English" else "fa"
        self.save_config()
        self.refresh_ui()

    # ------------------------------------------------------------------------
    # BUILD TAB
    # ------------------------------------------------------------------------
    def init_build(self):
        f = self.frames["build"]
        p = tk.LabelFrame(f, text=T[self.lang]["dest"], bg=self.theme["panel"],
                          fg=self.theme["primary"], font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        p.pack(fill=tk.X, padx=12, pady=6, ipady=3)
        tk.Button(p, text=T[self.lang]["browse"], bg=self.theme["primary"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=4, command=self.browse_build).pack(side=tk.RIGHT, padx=10, pady=4)
        e = tk.Entry(p, textvariable=self.target_dir, bg=self.theme["input"], fg=self.theme["fg"],
                     font=("Consolas", 10), bd=1, relief=tk.SOLID)
        e.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=4)
        add_context_menu(e, self.lang)

        mid = tk.Frame(f, bg=self.theme["bg"])
        mid.pack(fill=tk.BOTH, expand=True, padx=12)

        cfg = tk.LabelFrame(mid, text=T[self.lang]["injectors"], bg=self.theme["panel"],
                            fg=self.theme["primary"], font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        cfg.pack(side=tk.LEFT, fill=tk.Y, ipadx=10, ipady=8)

        tk.Label(cfg, text=T[self.lang]["fallback"], bg=self.theme["panel"], fg=self.theme["fg"]).pack(anchor=tk.W, padx=8, pady=(8,2))
        cb_fb = ttk.Combobox(cfg, textvariable=self.fallback,
                     values=["Auto Detect", "No Extension (Folder)", ".php", ".html", ".js", ".py", ".json", ".txt", ".md", ".css", ".cpp", ".go", ".rs", ".mp4", ".mp3", ".png", ".jpg", ".svg"],
                     state="readonly")
        cb_fb.pack(fill=tk.X, padx=8, pady=4)
        tk.Label(cfg, text=T[self.lang]["fallback_tip"], bg=self.theme["panel"],
                 fg=self.theme["info"], font=("Segoe UI", 8, "italic"), wraplength=200, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0,5))

        tk.Label(cfg, text=T[self.lang]["force"], bg=self.theme["panel"], fg=self.theme["fg"]).pack(anchor=tk.W, padx=8, pady=(8,2))
        cb_fo = ttk.Combobox(cfg, textvariable=self.force,
                     values=["Keep Original", "Force MP4", "Force MP3", "Force HTML", "Strip Extensions (Folders)"],
                     state="readonly")
        cb_fo.pack(fill=tk.X, padx=8, pady=4)
        tk.Label(cfg, text=T[self.lang]["force_tip"], bg=self.theme["panel"],
                 fg=self.theme["info"], font=("Segoe UI", 8, "italic"), wraplength=200, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0,5))

        tk.Checkbutton(cfg, text=T[self.lang]["readme"], variable=self.cb_readme,
                       bg=self.theme["panel"], fg=self.theme["fg"], selectcolor=self.theme["bg"],
                       activebackground=self.theme["panel"]).pack(anchor=tk.W, padx=8, pady=2)
        tk.Checkbutton(cfg, text=T[self.lang]["gitkeep"], variable=self.cb_gitkeep,
                       bg=self.theme["panel"], fg=self.theme["fg"], selectcolor=self.theme["bg"],
                       activebackground=self.theme["panel"]).pack(anchor=tk.W, padx=8, pady=2)

        paned = tk.PanedWindow(mid, orient=tk.HORIZONTAL, bg=self.theme["bg"], bd=0, sashwidth=4)
        paned.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(12,0))

        left = tk.LabelFrame(paned, text=T[self.lang]["raw"], bg=self.theme["panel"],
                             fg=self.theme["primary"], font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        self.txt_raw = scrolledtext.ScrolledText(left, bg=self.theme["input"], fg=self.theme["fg"],
                                                 font=("Consolas", 10), bd=0)
        self.txt_raw.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        enable_mouse_scroll(self.txt_raw)
        add_context_menu(self.txt_raw, self.lang)
        bl = tk.Frame(left, bg=self.theme["panel"])
        bl.pack(fill=tk.X, padx=4, pady=4)
        tk.Button(bl, text=T[self.lang]["parse_btn"], bg=self.theme["accent"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=10, pady=3, command=self.parse).pack(side=tk.LEFT, padx=3)
        tk.Button(bl, text=T[self.lang]["clear_raw"], bg=self.theme["panel"], fg=self.theme["danger"],
                  font=("Segoe UI", 9), bd=1, padx=10, pady=3, command=lambda: self.txt_raw.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=3)

        right = tk.LabelFrame(paned, text=T[self.lang]["live"], bg=self.theme["panel"],
                              fg=self.theme["warning"], font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        self.txt_live = scrolledtext.ScrolledText(right, bg=self.theme["input"], fg=self.theme["warning"],
                                                  font=("Consolas", 10), bd=0)
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
            line = re.sub(r"\s*(#|//|--|/\*).*$", "", line)
            for p in PATTERNS_50:
                line = re.sub(p, "", line)
            line = line.strip()
            if not line:
                continue
            if self.fallback.get() == "Auto Detect":
                ext = self.detect_ext(line)
                if ext and '.' not in line and not line.endswith('/'):
                    line += ext
            out.append(line)
        self.txt_live.delete("1.0", tk.END)
        self.txt_live.insert(tk.END, "\n".join(out))
        self.log(f"Parsed {len(out)} items")

    def detect_ext(self, line):
        known = [".php", ".html", ".js", ".py", ".json", ".txt", ".md", ".css", ".cpp", ".go", ".rs", ".mp4", ".mp3", ".png", ".jpg", ".svg", ".xml", ".yaml"]
        for e in known:
            if line.strip().endswith(e):
                return e
        if re.search(r"<\?php", line): return ".php"
        if re.search(r"<html", line, re.I): return ".html"
        if re.search(r"<script", line, re.I) or re.search(r"function\s+\w+\s*\(", line): return ".js"
        if re.search(r"def\s+\w+\s*\(.*\)\s*:", line): return ".py"
        if re.search(r"^\s*<!DOCTYPE html>", line, re.I): return ".html"
        if re.search(r"^\s*{\s*$", line): return ".json"
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
            is_dir = item.endswith('/') or item.endswith('\\') or ('.' not in item and self.fallback.get() == "No Extension (Folder)")
            force = self.force.get()
            if not is_dir and '.' not in item:
                if force == "Keep Original":
                    fb = self.fallback.get()
                    if fb not in ["Auto Detect", "No Extension (Folder)"]:
                        item += fb
                    else:
                        is_dir = True
                elif force == "Force MP4": item += ".mp4"
                elif force == "Force MP3": item += ".mp3"
                elif force == "Force HTML": item += ".html"
                elif force == "Strip Extensions (Folders)": is_dir = True
            full = os.path.join(out, item.replace('/', os.sep).replace('\\', os.sep))
            try:
                if is_dir:
                    os.makedirs(full, exist_ok=True)
                    dirs += 1
                    if self.cb_gitkeep.get():
                        open(os.path.join(full, ".gitkeep"), 'w').close()
                else:
                    os.makedirs(os.path.dirname(full), exist_ok=True)
                    open(full, 'a', encoding='utf-8').close()
                    files += 1
            except Exception as e:
                self.log(f"Error: {item} – {e}")
        if self.cb_readme.get():
            try:
                with open(os.path.join(out, "AI_README.md"), 'w', encoding='utf-8') as f:
                    f.write(f"# AI Structure\n\nDate: {datetime.now()}\nDirs: {dirs}\nFiles: {files}")
            except:
                pass
        self.log(f"Deployed: {dirs} dirs, {files} files")
        messagebox.showinfo("Done", f"Deployed: {dirs} dirs, {files} files")

    # ------------------------------------------------------------------------
    # REVERSE TAB
    # ------------------------------------------------------------------------
    def init_reverse(self):
        f = self.frames["reverse"]
        p = tk.LabelFrame(f, text=T[self.lang]["source"], bg=self.theme["panel"],
                          fg=self.theme["primary"], font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        p.pack(fill=tk.X, padx=12, pady=6, ipady=3)
        tk.Button(p, text=T[self.lang]["browse_src"], bg=self.theme["primary"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=4, command=self.browse_reverse).pack(side=tk.RIGHT, padx=10, pady=4)
        e = tk.Entry(p, textvariable=self.reverse_dir, bg=self.theme["input"], fg=self.theme["fg"],
                     font=("Consolas", 10), bd=1, relief=tk.SOLID)
        e.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=4)
        add_context_menu(e, self.lang)

        mid = tk.Frame(f, bg=self.theme["bg"])
        mid.pack(fill=tk.BOTH, expand=True, padx=12)

        cfg = tk.LabelFrame(mid, text=T[self.lang]["format"], bg=self.theme["panel"],
                            fg=self.theme["primary"], font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        cfg.pack(side=tk.LEFT, fill=tk.Y, ipadx=10, ipady=8)

        tk.Label(cfg, text=T[self.lang]["style"], bg=self.theme["panel"], fg=self.theme["fg"]).pack(anchor=tk.W, padx=8, pady=(8,2))
        ttk.Combobox(cfg, textvariable=self.style,
                     values=["Tree Structure", "JSON Map", "XML Sheet", "Markdown Checklist", "Flat Clean List"],
                     state="readonly").pack(fill=tk.X, padx=8, pady=4)

        tk.Label(cfg, text=T[self.lang]["group"], bg=self.theme["panel"], fg=self.theme["fg"]).pack(anchor=tk.W, padx=8, pady=(8,2))
        ttk.Combobox(cfg, textvariable=self.group, values=list(FILE_GROUPS.keys()), state="readonly").pack(fill=tk.X, padx=8, pady=4)

        tk.Label(cfg, text=T[self.lang]["ext"], bg=self.theme["panel"], fg=self.theme["fg"]).pack(anchor=tk.W, padx=8, pady=(8,2))
        ext_entry = tk.Entry(cfg, textvariable=self.specific_ext, bg=self.theme["input"], fg=self.theme["fg"],
                             font=("Consolas", 10), bd=1, relief=tk.SOLID)
        ext_entry.pack(fill=tk.X, padx=8, pady=4)
        add_context_menu(ext_entry, self.lang)

        tk.Checkbutton(cfg, text=T[self.lang]["meta"], variable=self.cb_meta,
                       bg=self.theme["panel"], fg=self.theme["fg"], selectcolor=self.theme["bg"],
                       activebackground=self.theme["panel"]).pack(anchor=tk.W, padx=8, pady=4)

        bf = tk.Frame(cfg, bg=self.theme["panel"])
        bf.pack(fill=tk.X, padx=8, pady=6)
        tk.Button(bf, text=T[self.lang]["copy_out"], bg=self.theme["panel"], fg=self.theme["fg"],
                  font=("Segoe UI", 9), bd=1, padx=10, pady=3, command=lambda: self.copy_to_clip(self.txt_out)).pack(side=tk.LEFT, padx=3)
        tk.Button(bf, text=T[self.lang]["clear_out"], bg=self.theme["panel"], fg=self.theme["danger"],
                  font=("Segoe UI", 9), bd=1, padx=10, pady=3, command=lambda: self.txt_out.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=3)

        out_f = tk.LabelFrame(mid, text=T[self.lang]["output"], bg=self.theme["panel"],
                              fg=self.theme["primary"], font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        out_f.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(12,0))
        self.txt_out = scrolledtext.ScrolledText(out_f, bg=self.theme["input"], fg=self.theme["fg"],
                                                 font=("Consolas", 10), bd=0)
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
        self.log(f"Reverse output generated")

    def include(self, name, allowed, use_spec, spec):
        if use_spec:
            return name.endswith(spec)
        if allowed:
            return any(name.endswith(e) for e in allowed)
        return True

    def gen_tree(self, path, pref, allowed, use_spec, spec, buf):
        try:
            items = os.listdir(path)
        except:
            return
        items.sort()
        ptrs = ['├── '] * (len(items) - 1) + ['└── ']
        for ptr, name in zip(ptrs, items):
            full = os.path.join(path, name)
            if os.path.isdir(full):
                buf.append(f"{pref}{ptr}{name}/")
                ext = "│   " if ptr == '├── ' else "    "
                self.gen_tree(full, pref + ext, allowed, use_spec, spec, buf)
            else:
                if self.include(name, allowed, use_spec, spec):
                    meta = f" ({os.path.getsize(full)} bytes)" if self.cb_meta.get() else ""
                    buf.append(f"{pref}{ptr}{name}{meta}")

    def gen_dict(self, path, allowed, use_spec, spec):
        d = {'name': os.path.basename(path), 'type': 'dir', 'children': []}
        try:
            for name in os.listdir(path):
                full = os.path.join(path, name)
                if os.path.isdir(full):
                    d['children'].append(self.gen_dict(full, allowed, use_spec, spec))
                else:
                    if self.include(name, allowed, use_spec, spec):
                        item = {'name': name, 'type': 'file'}
                        if self.cb_meta.get():
                            item['size'] = os.path.getsize(full)
                        d['children'].append(item)
        except:
            pass
        return d

    def gen_xml(self, path, parent, allowed, use_spec, spec):
        try:
            for name in os.listdir(path):
                full = os.path.join(path, name)
                if os.path.isdir(full):
                    sub = ET.SubElement(parent, "Dir", Name=name)
                    self.gen_xml(full, sub, allowed, use_spec, spec)
                else:
                    if self.include(name, allowed, use_spec, spec):
                        el = ET.SubElement(parent, "File", Name=name)
                        if self.cb_meta.get():
                            el.set("Size", str(os.path.getsize(full)))
        except:
            pass

    def gen_md(self, path, level, allowed, use_spec, spec, buf):
        ind = "  " * level
        try:
            for name in os.listdir(path):
                full = os.path.join(path, name)
                if os.path.isdir(full):
                    buf.append(f"{ind}- [ ] 📁 {name}")
                    self.gen_md(full, level+1, allowed, use_spec, spec, buf)
                else:
                    if self.include(name, allowed, use_spec, spec):
                        buf.append(f"{ind}- [ ] 📄 {name}")
        except:
            pass

    def gen_flat(self, base, cur, allowed, use_spec, spec, buf):
        try:
            for name in os.listdir(cur):
                full = os.path.join(cur, name)
                if os.path.isdir(full):
                    self.gen_flat(base, full, allowed, use_spec, spec, buf)
                else:
                    if self.include(name, allowed, use_spec, spec):
                        buf.append(os.path.relpath(full, base))
        except:
            pass

    # ------------------------------------------------------------------------
    # HELP TAB
    # ------------------------------------------------------------------------
    def init_help(self):
        f = self.frames["help"]
        canvas = tk.Canvas(f, bg=self.theme["bg"], bd=0, highlightthickness=0)
        scroll = ttk.Scrollbar(f, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=self.theme["bg"])
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        enable_mouse_scroll(canvas)

        def add_section(title, text):
            tk.Label(inner, text=title, bg=self.theme["bg"], fg=self.theme["warning"],
                     font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(10,5))
            lbl = tk.Label(inner, text=text, bg=self.theme["bg"], fg=self.theme["fg"],
                           font=("Consolas", 10), justify=tk.LEFT, anchor=tk.W)
            lbl.pack(fill=tk.X, pady=5)
            tk.Frame(inner, bg=self.theme["panel"], height=2).pack(fill=tk.X, pady=8)

        tk.Label(inner, text=T[self.lang]["help_title"], bg=self.theme["bg"],
                 fg=self.theme["primary"], font=("Segoe UI", 16, "bold")).pack(anchor=tk.W, pady=(0,10))
        add_section(T[self.lang]["help_s1"], T[self.lang]["help_text"])
        add_section(T[self.lang]["help_s2"], T[self.lang]["help_ex"])
        add_section(T[self.lang]["help_s3"], T[self.lang]["help_force"])
        add_section(T[self.lang]["help_s4"], T[self.lang]["help_rev"])
        add_section(T[self.lang]["help_s5"], T[self.lang]["help_tips"])

    # ------------------------------------------------------------------------
    # EXPORT TAB
    # ------------------------------------------------------------------------
    def init_export(self):
        f = self.frames["export"]
        p = tk.LabelFrame(f, text=T[self.lang]["export_title"], bg=self.theme["panel"],
                          fg=self.theme["primary"], font=("Segoe UI", 10, "bold"), bd=1, relief=tk.SOLID)
        p.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, ipady=15)

        tk.Label(p, text=T[self.lang]["save_as"], bg=self.theme["panel"], fg=self.theme["fg"]).pack(anchor=tk.W, padx=20, pady=(15,5))
        e1 = tk.Entry(p, textvariable=self.save_name, bg=self.theme["input"], fg=self.theme["fg"], font=("Consolas", 10), bd=1, relief=tk.SOLID)
        e1.pack(fill=tk.X, padx=20, pady=5)
        add_context_menu(e1, self.lang)
        tk.Button(p, text=T[self.lang]["save_btn"], bg=self.theme["success"], fg=self.theme["bg"],
                  font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=6, command=self.save_output).pack(pady=8)

        tk.Label(p, text="ZIP Archive", bg=self.theme["panel"], fg=self.theme["fg"]).pack(anchor=tk.W, padx=20, pady=(15,5))
        e2 = tk.Entry(p, textvariable=self.zip_name, bg=self.theme["input"], fg=self.theme["fg"], font=("Consolas", 10), bd=1, relief=tk.SOLID)
        e2.pack(fill=tk.X, padx=20, pady=5)
        add_context_menu(e2, self.lang)
        tk.Button(p, text=T[self.lang]["zip_btn"], bg=self.theme["warning"], fg=self.theme["bg"],
                  font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=6, command=self.zip_project).pack(pady=8)

        self.txt_preview = scrolledtext.ScrolledText(p, bg=self.theme["input"], fg=self.theme["fg"],
                                                     font=("Consolas", 10), height=8, bd=0)
        self.txt_preview.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        enable_mouse_scroll(self.txt_preview)
        add_context_menu(self.txt_preview, self.lang)

    def save_output(self):
        content = self.txt_out.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No output to save.")
            return
        fname = self.save_name.get().strip() or "output.txt"
        target = self.reverse_dir.get() or self.target_dir.get() or os.getcwd()
        full = os.path.join(target, fname)
        try:
            with open(full, 'w', encoding='utf-8') as f:
                f.write(content)
            self.log(f"Saved: {full}")
            self.txt_preview.delete("1.0", tk.END)
            self.txt_preview.insert(tk.END, f"✅ Saved to: {full}\n\n" + content[:500] + ("..." if len(content)>500 else ""))
            messagebox.showinfo("Saved", f"Saved to {full}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def zip_project(self):
        target = self.target_dir.get()
        if not target or not os.path.exists(target):
            messagebox.showerror("Error", "Target folder not set.")
            return
        zname = self.zip_name.get().strip() or "backup.zip"
        zpath = os.path.join(os.path.dirname(target), zname)
        try:
            with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
                for root, _, files in os.walk(target):
                    for f in files:
                        fp = os.path.join(root, f)
                        z.write(fp, os.path.relpath(fp, os.path.dirname(target)))
            self.log(f"ZIP created: {zpath}")
            messagebox.showinfo("ZIP", f"Created: {zpath}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------------------------------------------------------------
    # SETTINGS TAB
    # ------------------------------------------------------------------------
    def init_settings(self):
        f = self.frames["settings"]
        main = tk.Frame(f, bg=self.theme["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        left = tk.LabelFrame(main, text=T[self.lang]["settings_title"], bg=self.theme["panel"],
                             fg=self.theme["primary"], font=("Segoe UI", 10, "bold"), bd=1, relief=tk.SOLID)
        left.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=(0,10), ipadx=15, ipady=15)

        tk.Label(left, text=T[self.lang]["lang"], bg=self.theme["panel"], fg=self.theme["fg"]).pack(anchor=tk.W, padx=10, pady=(10,5))
        lc = ttk.Combobox(left, values=["English", "فارسی"], state="readonly")
        lc.set("English" if self.lang=="en" else "فارسی")
        lc.pack(fill=tk.X, padx=10, pady=5)
        lc.bind("<<ComboboxSelected>>", lambda e: self.set_lang(lc.get()))

        colors = [("primary", "Primary"), ("success", "Success"), ("accent", "Accent"),
                  ("warning", "Warning"), ("danger", "Danger"), ("info", "Info")]
        for k, label in colors:
            tk.Label(left, text=T[self.lang][f"color_{k}"], bg=self.theme["panel"],
                     fg=self.theme["fg"]).pack(anchor=tk.W, padx=10, pady=(8,2))
            btn = tk.Button(left, bg=self.theme[k], fg="white", text="Choose",
                            bd=1, relief=tk.SOLID, command=lambda key=k: self.choose_color(key))
            btn.pack(anchor=tk.W, padx=10, pady=2)

        bf = tk.Frame(left, bg=self.theme["panel"])
        bf.pack(fill=tk.X, padx=10, pady=15)
        tk.Button(bf, text=T[self.lang]["reset_colors"], bg=self.theme["danger"], fg="white",
                  font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=6, command=self.reset_colors).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text=T[self.lang]["save_settings"], bg=self.theme["success"], fg="white",
                  font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=6, command=self.save_config_and_notify).pack(side=tk.LEFT, padx=5)

        right = tk.LabelFrame(main, text="🎨 Color Preview", bg=self.theme["panel"],
                              fg=self.theme["accent"], font=("Segoe UI", 10, "bold"), bd=1, relief=tk.SOLID)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10,0), ipadx=15, ipady=15)
        preview = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    COLOR PREVIEW                               ║
╚══════════════════════════════════════════════════════════════════╝

Primary:   ████████████  (Main buttons, headers)
Success:   ████████████  (Deploy, save)
Accent:    ████████████  (Parse, highlight)
Warning:   ████████████  (Zip, warnings)
Danger:    ████████████  (Errors, delete)
Info:      ████████████  (Tips, info)

Background: ████████████  (Main window)
Panel:      ████████████  (Frames)
Input:      ████████████  (Text boxes)

💡 Click any color button to change it.
"""
        self.preview_lbl = tk.Label(right, text=preview, bg=self.theme["input"], fg=self.theme["fg"],
                                    font=("Consolas", 10), justify=tk.LEFT, anchor=tk.W, padx=15, pady=15)
        self.preview_lbl.pack(fill=tk.BOTH, expand=True)

    def choose_color(self, key):
        col = colorchooser.askcolor(title=f"Choose {key}", color=self.theme[key])
        if col and col[1]:
            self.theme[key] = col[1]
            self.apply_theme()
            self.log(f"Color {key} changed")

    def reset_colors(self):
        self.theme.update(THEME)
        self.apply_theme()
        self.log("Colors reset")

    def set_lang(self, val):
        self.lang = "en" if val == "English" else "fa"
        self.save_config()
        self.refresh_ui()

    # ------------------------------------------------------------------------
    # STATUS, LOG, FOOTER
    # ------------------------------------------------------------------------
    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, text=T[self.lang]["ready"], bg=self.theme["panel"],
                                   fg="#94a3b8", anchor=tk.W, font=("Segoe UI", 9), padx=10)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_log(self):
        f = tk.LabelFrame(self.root, text="📋 Live Log", bg=self.theme["panel"],
                          fg=self.theme["warning"], font=("Segoe UI", 9, "bold"), bd=1, relief=tk.SOLID)
        f.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=(0,6))
        self.txt_log = scrolledtext.ScrolledText(f, bg="#020617", fg=self.theme["warning"],
                                                 font=("Consolas", 9), height=4, bd=0)
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        enable_mouse_scroll(self.txt_log)
        add_context_menu(self.txt_log, self.lang)
        tk.Button(f, text="Clear Log", bg=self.theme["panel"], fg=self.theme["fg"],
                  font=("Segoe UI", 9), bd=1, padx=10, pady=2, command=self.clear_log).pack(side=tk.RIGHT, padx=4, pady=4)

    def clear_log(self):
        self.txt_log.delete("1.0", tk.END)

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.txt_log.insert(tk.END, f"[{ts}] {msg}\n")
        self.txt_log.see(tk.END)
        self.root.update_idletasks()

    def copy_to_clip(self, widget):
        self.root.clipboard_clear()
        self.root.clipboard_append(widget.get("1.0", tk.END).strip())
        self.log("Copied to clipboard")

    def update_status_lang(self):
        if hasattr(self, 'status_bar'):
            self.status_bar.config(text=T[self.lang]["ready"])

    def save_config_and_notify(self):
        self.save_config()
        messagebox.showinfo("Saved", "Settings saved.")
        self.log("Settings saved")

    def create_credit_footer(self):
        credit_frame = tk.Frame(self.root, bg=self.theme["panel"])
        credit_frame.pack(side=tk.BOTTOM, fill=tk.X)
        credit_text = T[self.lang]["credit"] + " - " + T[self.lang]["credit_link"]
        self.credit_label = tk.Label(credit_frame, text=credit_text, bg=self.theme["panel"],
                                     fg=self.theme["info"], font=("Segoe UI", 9, "italic"))
        self.credit_label.pack(pady=2)

# ============================================================================
# RUN
# ============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AFAR(root)
    root.mainloop()