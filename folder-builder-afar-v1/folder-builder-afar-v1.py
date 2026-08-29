# =============================================================================
# 0001 - IMPORTS & HEADER
# =============================================================================
"""
AFAR ULTIMATE PRO v4.0 - Intelligent Folder Builder & Reverse Engineer
Author: AI Assistant (INTJ/ENTJ Perspective)
License: MIT
Description: Fully bilingual (EN/FA) with customizable theme, context menus,
             web input, and comprehensive help system.
"""

import os
import re
import json
import shutil
import zipfile
import xml.etree.ElementTree as ET
from xml.dom import minidom
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext, simpledialog, colorchooser
from datetime import datetime
import webbrowser
import requests
import threading

# =============================================================================
# 0002 - THEME & COLOR SYSTEM (Fully Customizable)
# =============================================================================
DEFAULT_THEME = {
    "bg_main": "#0b1120",
    "bg_panel": "#1a2332",
    "bg_input": "#0f172a",
    "fg_main": "#e8edf5",
    "color_primary": "#22d3ee",    # Cyan
    "color_success": "#34d399",    # Emerald
    "color_warning": "#fb923c",    # Orange
    "color_purple": "#a78bfa",     # Purple
    "color_alert": "#f87171",      # Red
    "font_family": "Segoe UI",
    "font_mono": "Cascadia Code, Consolas, monospace"
}

class ThemeManager:
    """Manages application theme with ability to change colors."""
    def __init__(self):
        self.theme = DEFAULT_THEME.copy()
        self.load_theme()
    
    def load_theme(self):
        config_file = os.path.expanduser("~/.afar_theme.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    saved = json.load(f)
                    self.theme.update(saved)
            except:
                pass
    
    def save_theme(self):
        config_file = os.path.expanduser("~/.afar_theme.json")
        with open(config_file, 'w') as f:
            json.dump(self.theme, f, indent=2)
    
    def get(self, key):
        return self.theme.get(key, DEFAULT_THEME.get(key))
    
    def set_color(self, key, color):
        if key in self.theme:
            self.theme[key] = color
            self.save_theme()
            return True
        return False
    
    def get_all_colors(self):
        return {k: v for k, v in self.theme.items() if k.startswith(("bg_", "fg_", "color_"))}

# =============================================================================
# 0003 - 50 REGEX PATTERNS
# =============================================================================
PATTERNS_50 = [
    # 1-5: Tree patterns
    r"^[├│└└──\s├──]+",
    r"^[└──\s│]+",
    r"^[─\s│├└]+",
    r"^[│\s]+",
    r"^[\s├└│─]+",
    # 6-10: Numbering
    r"^\d+\s*[\.\-\)]\s*",
    r"^\d+\s*[\.\-\)]\s*\d+[\.\-\)]\s*",
    r"^\d+\s*[\.\-\)]\s*\d+[\.\-\)]\s*\d+[\.\-\)]\s*",
    r"^[①-⑳]\s*",
    r"^[❶-❿]\s*",
    # 11-15: Letters
    r"^[a-zA-Z][\.\-\)]\s*",
    r"^[A-Z][\.\-\)]\s*",
    r"^[a-z][\.\-\)]\s*",
    r"^[I|V|X|L|C|D|M]+[\.\-\)]\s*",
    r"^[i|v|x|l|c|d|m]+[\.\-\)]\s*",
    # 16-20: Bullets
    r"^[•◦▪▫►▶▸▹◆◇◈○●◎◉◊□■▣▤▥▦▧▨▩▪▫▬▭▮▯]\s*",
    r"^[➤➢➣➤➥➦➧➨➩➪➫➬➭➮➯➰➱➲➳➴➵➶➷➸➹➺➻➼➽➾]\s*",
    r"^[✧✦✩✪✫✬✭✮✯✰✱✲✳✴✵✶✷✸✹✺✻✼✽✾✿❀❁❂❃❄❅❆❇❈❉❊❋]\s*",
    r"^[❚❘❙❛❜❝❞❡❢❣❤❥❦❧❨❩❪❫❬❭❮❯❰❱❲❳❴❵]\s*",
    r"^[➀-➉]\s*",
    # 21-25: Special symbols
    r"^§\s*", r"^¶\s*", r"^©\s*", r"^®\s*", r"^™\s*",
    # 26-30: Emojis
    r"^[📁📂📄📃📜📊📈📉📋📌📍📎📏📐📒📓📔📕📖📗📘📙📚📛📜📝📞📟📠📡📢📣📤📥📦📧📨📩📪📫📬📭📮📯📰📱📲📳📴📵📶📷📸📹📺📻📼📽📾]\s*",
    r"^[🔍🔎🔏🔐🔑🔒🔓🔔🔕🔖🔗🔘🔙🔚🔛🔜🔝🔞🔟🔠🔡🔢🔣🔤🔥🔦🔧🔨🔩🔪🔫🔬🔭🔮🔯🔰🔱🔲🔳🔴🔵🔶🔷🔸🔹🔺🔻🔼🔽🔾🔿🕀🕁🕂🕃🕄🕅🕆🕇🕈🕉🕊🕋🕌🕍🕎🕏🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛]\s*",
    r"^[⚡⚽⚾⛳⛪⛲⛺♨♠♣♥♦♨♩♪♫♬♭♮♯♰♱♲♳♴♵♶♷♸♹♺♻♼♽♾♿]\s*",
    r"^[✨🌟⭐🌙🌚🌛🌜🌝🌞🌠🌡🌤🌥🌦🌧🌨🌩🌪🌫🌬🌭🌮🌯🌰🌱🌲🌳🌴🌵🌶🌷🌸🌹🌺🌻🌼🌽🌾🌿🍀🍁🍂🍃🍄🍅🍆🍇🍈🍉🍊🍋🍌🍍🍎🍏🍐🍑🍒🍓🍔🍕🍖🍗🍘🍙🍚🍛🍜🍝🍞🍟🍠🍡🍢🍣🍤🍥🍦🍧🍨🍩🍪🍫🍬🍭🍮🍯🍰🍱🍲🍳🍴🍵🍶🍷🍸🍹🍺🍻🍼]\s*",
    r"^[🚀🚁🚂🚃🚄🚅🚆🚇🚈🚉🚊🚋🚌🚍🚎🚏🚐🚑🚒🚓🚔🚕🚖🚗🚘🚙🚚🚛🚜🚝🚞🚟🚠🚡🚢🚣🚤🚥🚦🚧🚨🚩🚪🚫🚬🚭🚮🚯🚰🚱🚲🚳🚴🚵🚶🚷🚸🚹🚺🚻🚼🚽🚾🚿🛀🛁🛂🛃🛄🛅🛋🛌🛍🛎🛏🛐🛑🛒🛠🛡🛢🛣🛤🛥🛩🛫🛬🛰🛳]\s*",
    # 31-35: Math & logic
    r"^[±×÷∑∏∫√∞≈≠≤≥±∂∇∆∅∈∉⊂⊃⊆⊇⊕⊖⊗⊘⊙⊚⊛⊜⊝]\s*",
    r"^[¬∧∨∀∃∄∅∈∉⊂⊃⊆⊇∨∧⊕⊗⊥⊤⊥⊢⊨⊩⊫⊬⊭⊮⊯]\s*",
    r"^[→←↑↓↔↕↖↗↘↙↚↛↜↝↞↟↠↡↢↣↤↥↦↧↨↩↪↫↬↭↮↯]\s*",
    r"^[⌘⌥⌦⌧⌨⌫⌬⌭⌮⌯⌰⌱⌲⌳⌴⌵⌶⌷⌸⌹⌺⌻⌼⌽⌾⌿⍀⍁⍂⍃⍄⍅⍆⍇⍈⍉⍊⍋⍌⍍⍎⍏⍐⍑⍒⍓⍔⍕⍖⍗⍘⍙⍚⍛⍜⍝⍞⍟⍠⍡⍢⍣⍤⍥⍦⍧⍨⍩⍪⍫⍬⍭⍮⍯⍰]\s*",
    r"^[⌠⌡⌢⌣⌤⌥⌦⌧⌨〈〉⌫⌬⌭⌮⌯⌰⌱⌲⌳⌴⌵⌶⌷⌸⌹⌺⌻⌼⌽⌾⌿⍀⍁⍂⍃⍄⍅⍆⍇⍈⍉⍊⍋⍌⍍⍎⍏⍐⍑⍒⍓⍔⍕⍖⍗⍘⍙⍚⍛⍜⍝⍞⍟⍠⍡⍢⍣⍤⍥⍦⍧⍨⍩⍪⍫⍬⍭⍮⍯⍰]\s*",
    # 36-40: Lines & tables
    r"^[═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬]\s*",
    r"^[▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕▖▗▘▙▚▛▜▝▞▟]\s*",
    r"^[─━│┃┄┅┆┇┈┉┊┋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┯┰┱┲┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╌╍╎╏]\s*",
    r"^[┌┐└┘├┤┬┴┼╭╮╯╰]\s*",
    r"^[╔╗╚╝╠╣╦╩╬═║╒╕╘╛╞╡╤╧╪╟╢╥╨╫]\s*",
    # 41-45: Quotes & punctuation
    r"^[«»“”‘’‛″‴‵‶‷‸‹›«»‘’‚‛“”„‟†‡•‣․‥…‧‰‱′″‴‵‶‷‸‹›]\s*",
    r"^[¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿]\s*",
    r"^[ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ]\s*",
    r"^[ĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŒœŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽž]\s*",
    r"^[ﬀﬁﬂﬃﬄﬅﬆﬓﬔﬕﬖﬗיִﬞײַﬠﬡﬢﬣﬤﬥﬦﬧﬨ﬩שׁשׂשּׁשּׂאַאָאּבּגּדּהּוּזּטּיּךּכּלּמּנּסּףּפּצּקּרּשּתּוֹבֿכֿפֿﭏ]\s*",
    # 46-50: Miscellaneous
    r"^[☀☁☂☃☄★☆☇☈☉☊☋☌☍☎☏☐☑☒☓☔☕☖☗☘☙☚☛☜☝☞☟☠☡☢☣☤☥☦☧☨☩☪☫☬☭☮☯☰☱☲☳☴☵☶☷☸☹☺☻☼☽☾☿♀♁♂♃♄♅♆♇]\s*",
    r"^[♈♉♊♋♌♍♎♏♐♑♒♓]\s*",
    r"^[⚀⚁⚂⚃⚄⚅]\s*",
    r"^[➊➋➌➍➎➏➐➑➒➓]\s*",
    r"^[🄐🄑🄒🄓🄔🄕🄖🄗🄘🄙🄚🄛🄜🄝🄞🄟🄠🄡🄢🄣🄤🄥🄦🄧🄨🄩]\s*",
]

# =============================================================================
# 0004 - FILE TYPE GROUPS
# =============================================================================
FORMAT_GROUPS = {
    "Web & Code": [".php", ".html", ".css", ".js", ".ts", ".json", ".py", ".cpp", ".go", ".rs", ".rb"],
    "Media (Video/Audio)": [".mp4", ".mkv", ".avi", ".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a"],
    "Documents & Data": [".txt", ".md", ".pdf", ".docx", ".xlsx", ".csv", ".xml", ".yaml", ".toml"],
    "Graphics & Design": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".psd", ".ai", ".eps", ".webp"],
    "Container & Virtualization": [".dockerfile", ".k8s.yaml", ".tf", ".nomad"],
    "Frontend Frameworks": [".jsx", ".tsx", ".vue", ".svelte"],
    "All Available Formats": []
}

# =============================================================================
# 0005 - BILINGUAL LANGUAGE DICTIONARY (FULL)
# =============================================================================
LANG = {
    "en": {
        "app_title": "⚡ AFAR ULTIMATE PRO v4.0 | Builder & Reverse Engineer",
        "status_ready": "Ready",
        "tab_forward": "📥 Forward Engine (Build)",
        "tab_reverse": "📤 Reverse Engine (List)",
        "tab_help": "📖 Help & Guide",
        "tab_export": "💾 Export / Save",
        "tab_extra": "🔧 Extra Tools",
        "tab_theme": "🎨 Theme",
        "target_dest": "TARGET DESTINATION",
        "browse": "📂 Browse",
        "injectors": "INJECTORS & PARSER",
        "fallback_ext": "Fallback Extension:",
        "macro_force": "Force Modifier:",
        "gen_readme": "Generate AI Readme.md",
        "inject_gitkeep": "Inject .gitkeep",
        "smart_parse": "🔮 Smart Auto-Parse Input",
        "raw_input": "1. RAW INPUT (paste your tree/list here)",
        "live_editor": "2. LIVE EDITOR (edit before deploy)",
        "smart_parse_btn": "⚡ Smart Parse → Live Editor",
        "clear_raw": "🗑️ Clear Raw",
        "copy_clip": "📋 Copy to Clipboard",
        "clear_live": "🗑️ Clear Live",
        "deploy_btn": "🚀 DEPLOY FROM LIVE EDITOR",
        "source_folder": "SOURCE FOLDER (reverse from disk)",
        "browse_source": "📂 Browse Source",
        "output_format": "OUTPUT FORMAT & FILTERS",
        "export_style": "Export Structure Style:",
        "group_filter": "Group Filter:",
        "specific_ext": "Specific extension (e.g. .py):",
        "append_meta": "Append Size Meta",
        "copy_output": "📋 Copy Output",
        "clear_output": "🗑️ Clear",
        "reverse_output": "REVERSE OUTPUT (AI Prompt Ready)",
        "run_reverse": "⚡ RUN REVERSE ENGINE",
        "export_title": "💾 EXPORT / SAVE OPTIONS",
        "save_as_file": "Save Output as File:",
        "save_btn": "💾 Save to File",
        "zip_project": "Compress Project as ZIP:",
        "zip_btn": "📦 Create ZIP Archive",
        "preview_title": "📄 Preview Structure",
        "extra_title": "🔧 EXTRA TOOLS",
        "batch_rename": "Batch Rename Files (in source folder):",
        "rename_btn": "🔄 Rename",
        "find_duplicates": "Find Duplicate Files:",
        "find_dup_btn": "🔍 Find Duplicates",
        "clear_dups": "Clear Dups List",
        "dups_output": "Duplicates Report:",
        "theme_title": "🎨 CUSTOMIZE THEME",
        "theme_desc": "Click a color button to change that color:",
        "reset_theme": "↺ Reset to Default",
        "web_input": "🌐 Paste from URL:",
        "fetch_btn": "📥 Fetch Content",
        "live_log": "📋 Live Log",
        "clear_log": "Clear Log",
        "error": "Error",
        "warning": "Warning",
        "success": "Success",
        "info": "Info",
        "context_copy": "Copy",
        "context_cut": "Cut",
        "context_paste": "Paste",
        "context_delete": "Delete",
        "context_select_all": "Select All"
    },
    "fa": {
        "app_title": "⚡ AFAR نهایی حرفه‌ای v1 | ساخت پوشه و مهندسی معکوس",
        "status_ready": "آماده",
        "tab_forward": "📥 موتور پیشرو (ساخت)",
        "tab_reverse": "📤 موتور معکوس (لیست)",
        "tab_help": "📖 راهنما",
        "tab_export": "💾 ذخیره / خروجی",
        "tab_extra": "🔧 ابزارهای اضافی",
        "tab_theme": "🎨 تم",
        "target_dest": "مقصد نهایی",
        "browse": "📂 مرور",
        "injectors": "تزریق‌کننده‌ها و پردازشگر",
        "fallback_ext": "پسوند پیش‌فرض:",
        "macro_force": "اصلاح‌گر:",
        "gen_readme": "تولید Readme.md هوشمند",
        "inject_gitkeep": "تزریق .gitkeep",
        "smart_parse": "🔮 پردازش خودکار ورودی",
        "raw_input": "۱. ورودی خام (درخت/لیست را جای‌گذاری کنید)",
        "live_editor": "۲. ویرایشگر زنده (قبل از استقرار ویرایش کنید)",
        "smart_parse_btn": "⚡ پردازش هوشمند → ویرایشگر زنده",
        "clear_raw": "🗑️ پاک کردن ورودی",
        "copy_clip": "📋 کپی در کلیپ‌بورد",
        "clear_live": "🗑️ پاک کردن ویرایشگر",
        "deploy_btn": "🚀 استقرار از ویرایشگر زنده",
        "source_folder": "پوشه مبدأ (برای مهندسی معکوس)",
        "browse_source": "📂 مرور مبدأ",
        "output_format": "فرمت خروجی و فیلترها",
        "export_style": "سبک ساختار خروجی:",
        "group_filter": "فیلتر گروه:",
        "specific_ext": "پسوند خاص (مثلاً .py):",
        "append_meta": "افزودن اطلاعات اندازه",
        "copy_output": "📋 کپی خروجی",
        "clear_output": "🗑️ پاک کردن",
        "reverse_output": "خروجی معکوس (آماده برای پرامپت)",
        "run_reverse": "⚡ اجرای موتور معکوس",
        "export_title": "💾 گزینه‌های ذخیره و خروجی",
        "save_as_file": "ذخیره خروجی در فایل:",
        "save_btn": "💾 ذخیره در فایل",
        "zip_project": "فشرده‌سازی پروژه به ZIP:",
        "zip_btn": "📦 ایجاد آرشیو ZIP",
        "preview_title": "📄 پیش‌نمایش ساختار",
        "extra_title": "🔧 ابزارهای اضافی",
        "batch_rename": "تغییر نام دسته‌جمعی فایل‌ها (در پوشه مبدأ):",
        "rename_btn": "🔄 تغییر نام",
        "find_duplicates": "یافتن فایل‌های تکراری:",
        "find_dup_btn": "🔍 یافتن تکراری‌ها",
        "clear_dups": "پاک کردن لیست تکراری‌ها",
        "dups_output": "گزارش تکراری‌ها:",
        "theme_title": "🎨 شخصی‌سازی تم",
        "theme_desc": "برای تغییر هر رنگ، روی دکمه آن کلیک کنید:",
        "reset_theme": "↺ بازگشت به پیش‌فرض",
        "web_input": "🌐 دریافت از URL:",
        "fetch_btn": "📥 دریافت محتوا",
        "live_log": "📋 لاگ زنده",
        "clear_log": "پاک کردن لاگ",
        "error": "خطا",
        "warning": "هشدار",
        "success": "موفقیت",
        "info": "اطلاعات",
        "context_copy": "کپی",
        "context_cut": "برش",
        "context_paste": "چسباندن",
        "context_delete": "حذف",
        "context_select_all": "انتخاب همه"
    }
}

# =============================================================================
# 0006 - CONTEXT MENU (Right-Click) FOR ALL TEXT WIDGETS
# =============================================================================
def add_context_menu(widget, lang="en"):
    """Adds a right-click context menu to any text widget."""
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label=LANG[lang]["context_copy"], command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label=LANG[lang]["context_cut"], command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_command(label=LANG[lang]["context_paste"], command=lambda: widget.event_generate("<<Paste>>"))
    menu.add_command(label=LANG[lang]["context_delete"], command=lambda: widget.delete("sel.first", "sel.last") if widget.tag_ranges("sel") else None)
    menu.add_separator()
    menu.add_command(label=LANG[lang]["context_select_all"], command=lambda: widget.tag_add("sel", "1.0", "end"))
    
    def show_menu(event):
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    widget.bind("<Button-3>", show_menu)
    return menu

# =============================================================================
# 0007 - MAIN APPLICATION CLASS
# =============================================================================
class AFARUltimatePro:
    def __init__(self, root):
        self.root = root
        self.lang = "en"
        self.theme_manager = ThemeManager()
        self.load_language()
        self.setup_theme()
        
        # Window size (smaller)
        self.root.geometry("1300x820")
        self.root.minsize(1100, 700)
        self.root.title(LANG[self.lang]["app_title"])
        self.root.configure(bg=self.theme_manager.get("bg_main"))
        
        # Core variables
        self.target_dir = tk.StringVar()
        self.reverse_dir = tk.StringVar()
        self.default_extension = tk.StringVar(value="Auto Detect")
        self.macro_format_mode = tk.StringVar(value="Keep Original")
        self.export_format = tk.StringVar(value="Tree Structure")
        self.reverse_group_filter = tk.StringVar(value="All Available Formats")
        self.rename_pattern = tk.StringVar(value=".txt->.md")
        self.web_url = tk.StringVar(value="https://example.com/structure.txt")
        
        self.duplicates_list = []
        self.setup_styles()
        self.build_layout()
        self.create_status_bar()
        self.create_live_log()
        self.update_ui_language()
        self.apply_theme_to_all()

    # -------------------------------------------------------------------------
    # 0008 - LANGUAGE & THEME HELPERS
    # -------------------------------------------------------------------------
    def load_language(self):
        config_file = os.path.expanduser("~/.afar_config.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    self.lang = data.get("lang", "en")
            except:
                pass

    def save_language(self):
        config_file = os.path.expanduser("~/.afar_config.json")
        data = {"lang": self.lang}
        with open(config_file, 'w') as f:
            json.dump(data, f)

    def setup_theme(self):
        # Apply theme to root
        self.root.configure(bg=self.theme_manager.get("bg_main"))
        self.fg_main = self.theme_manager.get("fg_main")
        self.bg_panel = self.theme_manager.get("bg_panel")
        self.bg_input = self.theme_manager.get("bg_input")
        self.color_primary = self.theme_manager.get("color_primary")
        self.color_success = self.theme_manager.get("color_success")
        self.color_warning = self.theme_manager.get("color_warning")
        self.color_purple = self.theme_manager.get("color_purple")
        self.color_alert = self.theme_manager.get("color_alert")

    def apply_theme_to_widget(self, widget):
        """Recursively apply theme to a widget and its children."""
        try:
            if isinstance(widget, (tk.Frame, tk.LabelFrame, tk.PanedWindow)):
                widget.configure(bg=self.theme_manager.get("bg_panel"))
            elif isinstance(widget, tk.Label):
                widget.configure(bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"))
            elif isinstance(widget, (tk.Button, ttk.Button)):
                widget.configure(bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"))
            elif isinstance(widget, tk.Entry):
                widget.configure(bg=self.theme_manager.get("bg_input"), fg=self.theme_manager.get("fg_main"))
            elif isinstance(widget, (tk.Text, scrolledtext.ScrolledText)):
                # For ScrolledText, we need to apply to the internal text widget
                if hasattr(widget, "text") or isinstance(widget, scrolledtext.ScrolledText):
                    try:
                        text_widget = widget
                        text_widget.configure(bg=self.theme_manager.get("bg_input"), fg=self.theme_manager.get("fg_main"))
                    except:
                        pass
                else:
                    widget.configure(bg=self.theme_manager.get("bg_input"), fg=self.theme_manager.get("fg_main"))
            elif isinstance(widget, ttk.Combobox):
                style = ttk.Style()
                style.configure("TCombobox", fieldbackground=self.theme_manager.get("bg_input"),
                               background=self.theme_manager.get("bg_panel"),
                               foreground=self.theme_manager.get("fg_main"))
            
            # Apply to children
            for child in widget.winfo_children():
                self.apply_theme_to_widget(child)
        except:
            pass

    def apply_theme_to_all(self):
        """Apply current theme to all widgets in the main window."""
        self.root.configure(bg=self.theme_manager.get("bg_main"))
        for child in self.root.winfo_children():
            self.apply_theme_to_widget(child)
        self.setup_styles()
        self.update_ui_language()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=self.theme_manager.get("bg_main"), borderwidth=0)
        style.configure("TNotebook.Tab", background=self.theme_manager.get("bg_panel"),
                       foreground="#94a3b8", padding=10, font=(self.theme_manager.get("font_family"), 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", self.theme_manager.get("bg_main"))],
                 foreground=[("selected", self.theme_manager.get("color_primary"))])
        style.configure("TCombobox", fieldbackground=self.theme_manager.get("bg_input"),
                       background=self.theme_manager.get("bg_panel"),
                       foreground=self.theme_manager.get("fg_main"),
                       arrowcolor=self.theme_manager.get("color_primary"))
        style.configure("TLabel", background=self.theme_manager.get("bg_main"),
                       foreground=self.theme_manager.get("fg_main"))
        style.configure("TFrame", background=self.theme_manager.get("bg_main"))

    # -------------------------------------------------------------------------
    # 0009 - BUILD LAYOUT (5 Tabs)
    # -------------------------------------------------------------------------
    def build_layout(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.theme_manager.get("bg_panel"), height=60, bd=0)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        left_header = tk.Frame(header_frame, bg=self.theme_manager.get("bg_panel"))
        left_header.pack(side=tk.LEFT, padx=20, pady=8)
        self.lbl_title = tk.Label(left_header, text=LANG[self.lang]["app_title"],
                                 bg=self.theme_manager.get("bg_panel"),
                                 fg=self.theme_manager.get("color_primary"),
                                 font=(self.theme_manager.get("font_family"), 14, "bold"))
        self.lbl_title.pack(side=tk.LEFT)

        right_header = tk.Frame(header_frame, bg=self.theme_manager.get("bg_panel"))
        right_header.pack(side=tk.RIGHT, padx=20, pady=8)
        tk.Label(right_header, text="Language:", bg=self.theme_manager.get("bg_panel"),
                fg=self.theme_manager.get("fg_main"), font=(self.theme_manager.get("font_family"), 9)).pack(side=tk.LEFT, padx=5)
        self.lang_combo = ttk.Combobox(right_header, values=["English", "فارسی"], state="readonly", width=10)
        self.lang_combo.set("English" if self.lang == "en" else "فارسی")
        self.lang_combo.pack(side=tk.LEFT, padx=5)
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)

        # ----- CREDIT FOOTER (اضافه شده) -----
        self.create_credit_footer()
        # ------------------------------------

        # Notebook with 6 tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        self.tab_forward = tk.Frame(self.notebook, bg=self.theme_manager.get("bg_main"))
        self.tab_reverse = tk.Frame(self.notebook, bg=self.theme_manager.get("bg_main"))
        self.tab_help = tk.Frame(self.notebook, bg=self.theme_manager.get("bg_main"))
        self.tab_export = tk.Frame(self.notebook, bg=self.theme_manager.get("bg_main"))
        self.tab_extra = tk.Frame(self.notebook, bg=self.theme_manager.get("bg_main"))
        self.tab_theme = tk.Frame(self.notebook, bg=self.theme_manager.get("bg_main"))

        self.notebook.add(self.tab_forward, text=LANG[self.lang]["tab_forward"])
        self.notebook.add(self.tab_reverse, text=LANG[self.lang]["tab_reverse"])
        self.notebook.add(self.tab_help, text=LANG[self.lang]["tab_help"])
        self.notebook.add(self.tab_export, text=LANG[self.lang]["tab_export"])
        self.notebook.add(self.tab_extra, text=LANG[self.lang]["tab_extra"])
        self.notebook.add(self.tab_theme, text=LANG[self.lang]["tab_theme"])

        self.init_forward_tab()
        self.init_reverse_tab()
        self.init_help_tab()
        self.init_export_tab()
        self.init_extra_tab()
        self.init_theme_tab()

    # ----- متد جدید برای ایجاد متن اعتباری -----
    def create_credit_footer(self):
        """ایجاد فریم اعتباری با لینک کلیک‌پذیر، زیر هدر و وسط‌چین"""
        self.credit_frame = tk.Frame(self.root, bg=self.theme_manager.get("bg_panel"))
        self.credit_frame.pack(side=tk.TOP, fill=tk.X, pady=(2, 4))

        inner = tk.Frame(self.credit_frame, bg=self.theme_manager.get("bg_panel"))
        inner.pack(anchor="center")

        lbl = tk.Label(inner, text="Developed by", bg=self.theme_manager.get("bg_panel"),
                       fg=self.theme_manager.get("fg_main"),
                       font=(self.theme_manager.get("font_family"), 9, "italic"))
        lbl.pack(side=tk.LEFT, padx=(0, 5))

        link = tk.Label(inner, text="MA.GH.AD", bg=self.theme_manager.get("bg_panel"),
                        fg=self.theme_manager.get("color_primary"),
                        font=(self.theme_manager.get("font_family"), 9, "bold"),
                        cursor="hand2")
        link.pack(side=tk.LEFT)
        link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/mahanneman"))
    # ------------------------------------------------

    # -------------------------------------------------------------------------
    # 0010 - FORWARD ENGINE TAB
    # -------------------------------------------------------------------------
    def init_forward_tab(self):
        path_frame = tk.LabelFrame(self.tab_forward, text=LANG[self.lang]["target_dest"],
                                  bg=self.theme_manager.get("bg_panel"),
                                  fg=self.theme_manager.get("color_primary"),
                                  font=(self.theme_manager.get("font_family"), 9, "bold"),
                                  bd=1, relief=tk.SOLID)
        path_frame.pack(fill=tk.X, padx=15, pady=8, ipady=5)
        
        tk.Button(path_frame, text=LANG[self.lang]["browse"],
                 bg=self.theme_manager.get("color_primary"), fg=self.theme_manager.get("bg_main"),
                 font=(self.theme_manager.get("font_family"), 9, "bold"),
                 bd=0, padx=15, pady=5, command=self.browse_forward, cursor="hand2").pack(side=tk.RIGHT, padx=15, pady=8)
        
        tk.Entry(path_frame, textvariable=self.target_dir,
                bg=self.theme_manager.get("bg_input"), fg=self.theme_manager.get("fg_main"),
                insertbackground=self.theme_manager.get("fg_main"),
                font=(self.theme_manager.get("font_mono"), 10), bd=1, relief=tk.SOLID).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15, pady=8)
        add_context_menu(path_frame.winfo_children()[-1], self.lang)

        # ---- Web Input ----
        web_frame = tk.Frame(self.tab_forward, bg=self.theme_manager.get("bg_main"))
        web_frame.pack(fill=tk.X, padx=15, pady=5)
        tk.Label(web_frame, text=LANG[self.lang]["web_input"],
                bg=self.theme_manager.get("bg_main"), fg=self.theme_manager.get("fg_main"),
                font=(self.theme_manager.get("font_family"), 9)).pack(side=tk.LEFT, padx=5)
        url_entry = tk.Entry(web_frame, textvariable=self.web_url,
                            bg=self.theme_manager.get("bg_input"), fg=self.theme_manager.get("fg_main"),
                            font=(self.theme_manager.get("font_mono"), 9), bd=1, relief=tk.SOLID, width=50)
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        add_context_menu(url_entry, self.lang)
        tk.Button(web_frame, text=LANG[self.lang]["fetch_btn"],
                 bg=self.theme_manager.get("color_purple"), fg=self.theme_manager.get("bg_main"),
                 font=(self.theme_manager.get("font_family"), 9, "bold"),
                 bd=0, padx=10, pady=3, command=self.fetch_web_content).pack(side=tk.LEFT, padx=5)

        # ---- Middle Section ----
        mid_frame = tk.Frame(self.tab_forward, bg=self.theme_manager.get("bg_main"))
        mid_frame.pack(fill=tk.BOTH, expand=True, padx=15)

        config_frame = tk.LabelFrame(mid_frame, text=LANG[self.lang]["injectors"],
                                    bg=self.theme_manager.get("bg_panel"),
                                    fg=self.theme_manager.get("color_primary"),
                                    font=(self.theme_manager.get("font_family"), 9, "bold"),
                                    bd=1, relief=tk.SOLID)
        config_frame.pack(side=tk.LEFT, fill=tk.Y, ipadx=10, ipady=10)

        tk.Label(config_frame, text=LANG[self.lang]["fallback_ext"],
                bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"),
                font=(self.theme_manager.get("font_family"), 9)).pack(anchor=tk.W, padx=10, pady=(15,2))
        ext_choices = ["Auto Detect", "No Extension (Create Folder)", ".php", ".html", ".js", ".py",
                       ".json", ".txt", ".md", ".css", ".cpp", ".go", ".rs", ".mp4", ".mp3",
                       ".png", ".jpg", ".svg", ".xml", ".yaml"]
        combo_ext = ttk.Combobox(config_frame, textvariable=self.default_extension, values=ext_choices, state="readonly")
        combo_ext.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(config_frame, text=LANG[self.lang]["macro_force"],
                bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"),
                font=(self.theme_manager.get("font_family"), 9)).pack(anchor=tk.W, padx=10, pady=(15,2))
        combo_force = ttk.Combobox(config_frame, textvariable=self.macro_format_mode,
                                   values=["Keep Original", "Force All to MP4", "Force All to MP3",
                                           "Force All to Web Formats (.html)", "Strip All Extensions (Pure Folders)"],
                                   state="readonly")
        combo_force.pack(fill=tk.X, padx=10, pady=5)

        self.cb_auto_readme = tk.BooleanVar(value=True)
        tk.Checkbutton(config_frame, text=LANG[self.lang]["gen_readme"],
                      variable=self.cb_auto_readme, bg=self.theme_manager.get("bg_panel"),
                      fg=self.theme_manager.get("fg_main"), selectcolor=self.theme_manager.get("bg_main"),
                      activebackground=self.theme_manager.get("bg_panel")).pack(anchor=tk.W, padx=10, pady=5)
        self.cb_git_keep = tk.BooleanVar(value=False)
        tk.Checkbutton(config_frame, text=LANG[self.lang]["inject_gitkeep"],
                      variable=self.cb_git_keep, bg=self.theme_manager.get("bg_panel"),
                      fg=self.theme_manager.get("fg_main"), selectcolor=self.theme_manager.get("bg_main"),
                      activebackground=self.theme_manager.get("bg_panel")).pack(anchor=tk.W, padx=10, pady=5)

        # Paned windows for raw and live
        paned = tk.PanedWindow(mid_frame, orient=tk.HORIZONTAL, bg=self.theme_manager.get("bg_main"),
                              bd=0, sashwidth=5)
        paned.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))

        left_box = tk.LabelFrame(paned, text=LANG[self.lang]["raw_input"],
                                bg=self.theme_manager.get("bg_panel"),
                                fg=self.theme_manager.get("color_primary"),
                                font=(self.theme_manager.get("font_family"), 9, "bold"),
                                bd=1, relief=tk.SOLID)
        self.txt_raw = scrolledtext.ScrolledText(left_box, bg=self.theme_manager.get("bg_input"),
                                                fg=self.theme_manager.get("fg_main"),
                                                insertbackground=self.theme_manager.get("fg_main"),
                                                font=(self.theme_manager.get("font_mono"), 11), bd=0)
        self.txt_raw.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        add_context_menu(self.txt_raw, self.lang)

        btn_frame_left = tk.Frame(left_box, bg=self.theme_manager.get("bg_panel"))
        btn_frame_left.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(btn_frame_left, text=LANG[self.lang]["smart_parse_btn"],
                 bg=self.theme_manager.get("color_purple"), fg=self.theme_manager.get("bg_main"),
                 font=(self.theme_manager.get("font_family"), 9, "bold"),
                 bd=0, padx=10, pady=3, command=self.smart_parse_to_live).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame_left, text=LANG[self.lang]["clear_raw"],
                 bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("color_alert"),
                 font=(self.theme_manager.get("font_family"), 9), bd=1, padx=10, pady=3,
                 command=lambda: self.txt_raw.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=5)

        right_box = tk.LabelFrame(paned, text=LANG[self.lang]["live_editor"],
                                 bg=self.theme_manager.get("bg_panel"),
                                 fg=self.theme_manager.get("color_warning"),
                                 font=(self.theme_manager.get("font_family"), 9, "bold"),
                                 bd=1, relief=tk.SOLID)
        self.txt_live = scrolledtext.ScrolledText(right_box, bg=self.theme_manager.get("bg_input"),
                                                 fg=self.theme_manager.get("color_warning"),
                                                 insertbackground=self.theme_manager.get("color_warning"),
                                                 font=(self.theme_manager.get("font_mono"), 11), bd=0)
        self.txt_live.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        add_context_menu(self.txt_live, self.lang)

        btn_frame_right = tk.Frame(right_box, bg=self.theme_manager.get("bg_panel"))
        btn_frame_right.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(btn_frame_right, text=LANG[self.lang]["copy_clip"],
                 bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"),
                 font=(self.theme_manager.get("font_family"), 9), bd=1, padx=10, pady=3,
                 command=lambda: self.copy_to_clip(self.txt_live)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame_right, text=LANG[self.lang]["clear_live"],
                 bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("color_alert"),
                 font=(self.theme_manager.get("font_family"), 9), bd=1, padx=10, pady=3,
                 command=lambda: self.txt_live.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=5)

        paned.add(left_box, width=500)
        paned.add(right_box, width=500)

        tk.Button(self.tab_forward, text=LANG[self.lang]["deploy_btn"],
                 bg=self.theme_manager.get("color_success"), fg=self.theme_manager.get("bg_main"),
                 font=(self.theme_manager.get("font_family"), 12, "bold"),
                 bd=0, pady=12, command=self.deploy_from_live).pack(fill=tk.X, padx=15, pady=12)

    # -------------------------------------------------------------------------
    # 0011 - REVERSE ENGINE TAB
    # -------------------------------------------------------------------------
    def init_reverse_tab(self):
        path_frame = tk.LabelFrame(self.tab_reverse, text=LANG[self.lang]["source_folder"],
                                  bg=self.theme_manager.get("bg_panel"),
                                  fg=self.theme_manager.get("color_primary"),
                                  font=(self.theme_manager.get("font_family"), 9, "bold"),
                                  bd=1, relief=tk.SOLID)
        path_frame.pack(fill=tk.X, padx=15, pady=8, ipady=5)
        tk.Button(path_frame, text=LANG[self.lang]["browse_source"],
                 bg=self.theme_manager.get("color_primary"), fg=self.theme_manager.get("bg_main"),
                 font=(self.theme_manager.get("font_family"), 9, "bold"),
                 bd=0, padx=15, pady=5, command=self.browse_reverse).pack(side=tk.RIGHT, padx=15, pady=8)
        entry_rev = tk.Entry(path_frame, textvariable=self.reverse_dir,
                            bg=self.theme_manager.get("bg_input"), fg=self.theme_manager.get("fg_main"),
                            insertbackground=self.theme_manager.get("fg_main"),
                            font=(self.theme_manager.get("font_mono"), 10), bd=1, relief=tk.SOLID)
        entry_rev.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15, pady=8)
        add_context_menu(entry_rev, self.lang)

        mid_frame = tk.Frame(self.tab_reverse, bg=self.theme_manager.get("bg_main"))
        mid_frame.pack(fill=tk.BOTH, expand=True, padx=15)

        config_frame = tk.LabelFrame(mid_frame, text=LANG[self.lang]["output_format"],
                                    bg=self.theme_manager.get("bg_panel"),
                                    fg=self.theme_manager.get("color_primary"),
                                    font=(self.theme_manager.get("font_family"), 9, "bold"),
                                    bd=1, relief=tk.SOLID)
        config_frame.pack(side=tk.LEFT, fill=tk.Y, ipadx=10, ipady=10)

        tk.Label(config_frame, text=LANG[self.lang]["export_style"],
                bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"),
                font=(self.theme_manager.get("font_family"), 9)).pack(anchor=tk.W, padx=10, pady=(15,2))
        ttk.Combobox(config_frame, textvariable=self.export_format,
                    values=["Tree Structure", "JSON Map", "XML Sheet", "Markdown Checklist", "Flat Clean List"],
                    state="readonly").pack(fill=tk.X, padx=10, pady=5)

        tk.Label(config_frame, text=LANG[self.lang]["group_filter"],
                bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"),
                font=(self.theme_manager.get("font_family"), 9)).pack(anchor=tk.W, padx=10, pady=(15,2))
        self.combo_grp = ttk.Combobox(config_frame, textvariable=self.reverse_group_filter,
                                     values=list(FORMAT_GROUPS.keys()), state="readonly")
        self.combo_grp.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(config_frame, text=LANG[self.lang]["specific_ext"],
                bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"),
                font=(self.theme_manager.get("font_family"), 9)).pack(anchor=tk.W, padx=10, pady=(15,2))
        entry_ext = tk.Entry(config_frame, bg=self.theme_manager.get("bg_input"),
                            fg=self.theme_manager.get("fg_main"),
                            font=(self.theme_manager.get("font_mono"), 10), bd=1, relief=tk.SOLID)
        entry_ext.pack(fill=tk.X, padx=10, pady=5)
        add_context_menu(entry_ext, self.lang)
        # store reference to entry for later use in reverse engine
        self.single_ext_entry = entry_ext

        self.cb_include_stats = tk.BooleanVar(value=True)
        tk.Checkbutton(config_frame, text=LANG[self.lang]["append_meta"],
                      variable=self.cb_include_stats, bg=self.theme_manager.get("bg_panel"),
                      fg=self.theme_manager.get("fg_main"), selectcolor=self.theme_manager.get("bg_main"),
                      activebackground=self.theme_manager.get("bg_panel")).pack(anchor=tk.W, padx=10, pady=10)

        btn_frame_rev = tk.Frame(config_frame, bg=self.theme_manager.get("bg_panel"))
        btn_frame_rev.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(btn_frame_rev, text=LANG[self.lang]["copy_output"],
                 bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"),
                 font=(self.theme_manager.get("font_family"), 9), bd=1, padx=10, pady=3,
                 command=lambda: self.copy_to_clip(self.txt_reverse_output)).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame_rev, text=LANG[self.lang]["clear_output"],
                 bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("color_alert"),
                 font=(self.theme_manager.get("font_family"), 9), bd=1, padx=10, pady=3,
                 command=lambda: self.txt_reverse_output.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=2)

        output_frame = tk.LabelFrame(mid_frame, text=LANG[self.lang]["reverse_output"],
                                    bg=self.theme_manager.get("bg_panel"),
                                    fg=self.theme_manager.get("color_primary"),
                                    font=(self.theme_manager.get("font_family"), 9, "bold"),
                                    bd=1, relief=tk.SOLID)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15,0))
        self.txt_reverse_output = scrolledtext.ScrolledText(output_frame,
                                                           bg=self.theme_manager.get("bg_input"),
                                                           fg=self.theme_manager.get("fg_main"),
                                                           insertbackground=self.theme_manager.get("fg_main"),
                                                           font=(self.theme_manager.get("font_mono"), 11), bd=0)
        self.txt_reverse_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        add_context_menu(self.txt_reverse_output, self.lang)

        tk.Button(self.tab_reverse, text=LANG[self.lang]["run_reverse"],
                 bg=self.theme_manager.get("color_primary"), fg=self.theme_manager.get("bg_main"),
                 font=(self.theme_manager.get("font_family"), 12, "bold"),
                 bd=0, pady=12, command=self.execute_reverse_engineering).pack(fill=tk.X, padx=15, pady=12)

    # -------------------------------------------------------------------------
    # 0012 - HELP TAB (Comprehensive)
    # -------------------------------------------------------------------------
    def init_help_tab(self):
        main_frame = tk.Frame(self.tab_help, bg=self.theme_manager.get("bg_main"))
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        canvas = tk.Canvas(main_frame, bg=self.theme_manager.get("bg_main"), bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme_manager.get("bg_main"))
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Title
        tk.Label(scrollable_frame, text="📖 Comprehensive Guide & Help",
                bg=self.theme_manager.get("bg_main"), fg=self.theme_manager.get("color_primary"),
                font=(self.theme_manager.get("font_family"), 16, "bold")).pack(pady=(0, 15), anchor=tk.W)

        # Section 1: Basic Rules
        tk.Label(scrollable_frame, text="🔹 BASIC RULES FOR ENTRY",
                bg=self.theme_manager.get("bg_main"), fg=self.theme_manager.get("color_warning"),
                font=(self.theme_manager.get("font_family"), 12, "bold")).pack(anchor=tk.W, pady=(10,5))
        rules_text = """
1. DIRECTORY (Folder):
   • Add a slash (/) or backslash (\\) at the end of the name
   • Or select "No Extension (Create Folder)" as fallback
   • Example:  src/  ,  images/  ,  templates\\

2. FILE (with extension):
   • Include a dot (.) with a known extension
   • Or rely on Auto-Detect to add extension from content
   • Example:  index.php  ,  style.css  ,  app.js

3. NESTED STRUCTURE (Indentation):
   • Spaces (2 or 4), Tabs, Tree characters (├── └── │)
   • Bullets (• - * ➤), Numbers (1. 2. 3.), Emojis (📁 📄)

4. AUTO-DETECT EXTENSIONS:
   • <?php → .php   • <html → .html
   • <script or function → .js   • def → .py
   • { → .json

5. WHAT TO AVOID:
   • Spaces or special characters in folder/file names
   • Mixing different separators inconsistently
   • Empty lines (they will be ignored)
"""
        tk.Label(scrollable_frame, text=rules_text, bg=self.theme_manager.get("bg_main"),
                fg=self.theme_manager.get("fg_main"), font=(self.theme_manager.get("font_mono"), 10),
                justify=tk.LEFT, anchor=tk.W).pack(fill=tk.X, pady=5)

        # Separator
        tk.Frame(scrollable_frame, bg=self.theme_manager.get("bg_panel"), height=2).pack(fill=tk.X, pady=15)

        # Section 2: Examples
        tk.Label(scrollable_frame, text="🔹 EXAMPLES OF VALID INPUTS",
                bg=self.theme_manager.get("bg_main"), fg=self.theme_manager.get("color_warning"),
                font=(self.theme_manager.get("font_family"), 12, "bold")).pack(anchor=tk.W, pady=(10,5))
        examples_text = """
▶ TREE FORMAT (with indentation):
src/
    controllers/
        HomeController.php
    models/
        UserModel.py
    views/
        home.html
    index.php
public/
    css/
        style.css
    js/
        main.js
README.md

▶ BULLET LIST:
• src/
  • controllers/
    • HomeController.php
  • models/
    • UserModel.py
  • views/
    • home.html
  • index.php
• public/
  • css/
    • style.css
  • js/
    • main.js
• README.md

▶ NUMBERED LIST:
1. src/
   1.1. controllers/
       1.1.1. HomeController.php
   1.2. models/
       1.2.1. UserModel.py
   1.3. views/
       1.3.1. home.html
   1.4. index.php
2. public/
   2.1. css/
       2.1.1. style.css
   2.2. js/
       2.2.1. main.js
3. README.md

▶ FLAT LIST (paths):
src/
src/controllers/
src/controllers/HomeController.php
src/models/
src/models/UserModel.py
src/views/
src/views/home.html
src/index.php
public/
public/css/
public/css/style.css
public/js/
public/js/main.js
README.md

▶ WITH EMOJIS:
📁 src/
    📁 controllers/
        📄 HomeController.php
    📁 models/
        📄 UserModel.py
    📁 views/
        📄 home.html
    📄 index.php
📁 public/
    📁 css/
        📄 style.css
    📁 js/
        📄 main.js
📄 README.md
"""
        tk.Label(scrollable_frame, text=examples_text, bg=self.theme_manager.get("bg_main"),
                fg=self.theme_manager.get("fg_main"), font=(self.theme_manager.get("font_mono"), 10),
                justify=tk.LEFT, anchor=tk.W).pack(fill=tk.X, pady=5)

        # Separator
        tk.Frame(scrollable_frame, bg=self.theme_manager.get("bg_panel"), height=2).pack(fill=tk.X, pady=15)

        # Section 3: Force Modifiers
        tk.Label(scrollable_frame, text="🔹 MACRO FORCE MODIFIER OPTIONS",
                bg=self.theme_manager.get("bg_main"), fg=self.theme_manager.get("color_warning"),
                font=(self.theme_manager.get("font_family"), 12, "bold")).pack(anchor=tk.W, pady=(10,5))
        force_text = """
1. Keep Original        → Uses the extension as written, or fallback if missing
2. Force All to MP4     → Adds .mp4 to every file (video projects)
3. Force All to MP3     → Adds .mp3 to every file (audio projects)
4. Force All to Web     → Adds .html to every file (static websites)
5. Strip Extensions     → Treats everything as folders (removes all extensions)
"""
        tk.Label(scrollable_frame, text=force_text, bg=self.theme_manager.get("bg_main"),
                fg=self.theme_manager.get("fg_main"), font=(self.theme_manager.get("font_mono"), 10),
                justify=tk.LEFT, anchor=tk.W).pack(fill=tk.X, pady=5)

        # Separator
        tk.Frame(scrollable_frame, bg=self.theme_manager.get("bg_panel"), height=2).pack(fill=tk.X, pady=15)

        # Section 4: Reverse Output Formats
        tk.Label(scrollable_frame, text="🔹 REVERSE ENGINE OUTPUT FORMATS",
                bg=self.theme_manager.get("bg_main"), fg=self.theme_manager.get("color_warning"),
                font=(self.theme_manager.get("font_family"), 12, "bold")).pack(anchor=tk.W, pady=(10,5))
        reverse_text = """
1. Tree Structure      → Classic tree with connecting lines (├── └── │)
2. JSON Map            → Structured JSON with hierarchy and metadata
3. XML Sheet           → XML format with <Directory> and <File> tags
4. Markdown Checklist  → Markdown checklist with - [ ] items
5. Flat Clean List     → Simple list of paths (relative to source)
"""
        tk.Label(scrollable_frame, text=reverse_text, bg=self.theme_manager.get("bg_main"),
                fg=self.theme_manager.get("fg_main"), font=(self.theme_manager.get("font_mono"), 10),
                justify=tk.LEFT, anchor=tk.W).pack(fill=tk.X, pady=5)

        # Separator
        tk.Frame(scrollable_frame, bg=self.theme_manager.get("bg_panel"), height=2).pack(fill=tk.X, pady=15)

        # Section 5: Quick Tips
        tk.Label(scrollable_frame, text="🔹 QUICK TIPS",
                bg=self.theme_manager.get("bg_main"), fg=self.theme_manager.get("color_success"),
                font=(self.theme_manager.get("font_family"), 12, "bold")).pack(anchor=tk.W, pady=(10,5))
        tips_text = """
• You can type directly in the LIVE EDITOR without using Smart Parse.
• Use slashes (/) to create nested folders.
• Files without extension will use the fallback extension or become folders.
• The system ignores empty lines and comments (#, //, --).
• Use the Copy to Clipboard button to copy the parsed list.
• Always check the LIVE LOG for errors and warnings.
• You can import structure from a URL using the "Paste from URL" feature.
• Customize colors in the Theme tab to match your preference.
• Right-click on any text box for copy/paste/select all options.
"""
        tk.Label(scrollable_frame, text=tips_text, bg=self.theme_manager.get("bg_main"),
                fg=self.theme_manager.get("color_primary"), font=(self.theme_manager.get("font_mono"), 10),
                justify=tk.LEFT, anchor=tk.W).pack(fill=tk.X, pady=5)

    # -------------------------------------------------------------------------
    # 0013 - EXPORT TAB
    # -------------------------------------------------------------------------
    def init_export_tab(self):
        frame = tk.LabelFrame(self.tab_export, text=LANG[self.lang]["export_title"],
                             bg=self.theme_manager.get("bg_panel"),
                             fg=self.theme_manager.get("color_primary"),
                             font=(self.theme_manager.get("font_family"), 10, "bold"),
                             bd=1, relief=tk.SOLID)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, ipady=15)

        tk.Label(frame, text=LANG[self.lang]["save_as_file"],
                bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"),
                font=(self.theme_manager.get("font_family"), 10)).pack(anchor=tk.W, padx=20, pady=(20,5))
        self.save_filename = tk.Entry(frame, bg=self.theme_manager.get("bg_input"),
                                     fg=self.theme_manager.get("fg_main"),
                                     font=(self.theme_manager.get("font_mono"), 10), bd=1, relief=tk.SOLID, width=60)
        self.save_filename.insert(0, "output_structure.txt")
        self.save_filename.pack(fill=tk.X, padx=20, pady=5)
        add_context_menu(self.save_filename, self.lang)
        tk.Button(frame, text=LANG[self.lang]["save_btn"],
                 bg=self.theme_manager.get("color_success"), fg=self.theme_manager.get("bg_main"),
                 font=(self.theme_manager.get("font_family"), 10, "bold"),
                 bd=0, padx=20, pady=8, command=self.save_output_to_file).pack(pady=10)

        tk.Label(frame, text=LANG[self.lang]["zip_project"],
                bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"),
                font=(self.theme_manager.get("font_family"), 10)).pack(anchor=tk.W, padx=20, pady=(20,5))
        self.zip_filename = tk.Entry(frame, bg=self.theme_manager.get("bg_input"),
                                    fg=self.theme_manager.get("fg_main"),
                                    font=(self.theme_manager.get("font_mono"), 10), bd=1, relief=tk.SOLID, width=60)
        self.zip_filename.insert(0, "project_backup.zip")
        self.zip_filename.pack(fill=tk.X, padx=20, pady=5)
        add_context_menu(self.zip_filename, self.lang)
        tk.Button(frame, text=LANG[self.lang]["zip_btn"],
                 bg=self.theme_manager.get("color_warning"), fg=self.theme_manager.get("bg_main"),
                 font=(self.theme_manager.get("font_family"), 10, "bold"),
                 bd=0, padx=20, pady=8, command=self.zip_project).pack(pady=10)

        tk.Label(frame, text=LANG[self.lang]["preview_title"],
                bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"),
                font=(self.theme_manager.get("font_family"), 10)).pack(anchor=tk.W, padx=20, pady=(20,5))
        self.preview_text = scrolledtext.ScrolledText(frame, bg=self.theme_manager.get("bg_input"),
                                                     fg=self.theme_manager.get("fg_main"),
                                                     font=(self.theme_manager.get("font_mono"), 10), height=8, bd=0)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        add_context_menu(self.preview_text, self.lang)

    # -------------------------------------------------------------------------
    # 0014 - EXTRA TOOLS TAB
    # -------------------------------------------------------------------------
    def init_extra_tab(self):
        frame = tk.LabelFrame(self.tab_extra, text=LANG[self.lang]["extra_title"],
                             bg=self.theme_manager.get("bg_panel"),
                             fg=self.theme_manager.get("color_purple"),
                             font=(self.theme_manager.get("font_family"), 10, "bold"),
                             bd=1, relief=tk.SOLID)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, ipady=15)

        tk.Label(frame, text=LANG[self.lang]["batch_rename"],
                bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"),
                font=(self.theme_manager.get("font_family"), 10)).pack(anchor=tk.W, padx=20, pady=(20,5))
        rename_entry = tk.Entry(frame, textvariable=self.rename_pattern,
                               bg=self.theme_manager.get("bg_input"), fg=self.theme_manager.get("fg_main"),
                               font=(self.theme_manager.get("font_mono"), 10), bd=1, relief=tk.SOLID, width=40)
        rename_entry.pack(fill=tk.X, padx=20, pady=5)
        add_context_menu(rename_entry, self.lang)
        tk.Button(frame, text=LANG[self.lang]["rename_btn"],
                 bg=self.theme_manager.get("color_warning"), fg=self.theme_manager.get("bg_main"),
                 font=(self.theme_manager.get("font_family"), 10, "bold"),
                 bd=0, padx=20, pady=8, command=self.batch_rename).pack(pady=10)

        tk.Label(frame, text=LANG[self.lang]["find_duplicates"],
                bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"),
                font=(self.theme_manager.get("font_family"), 10)).pack(anchor=tk.W, padx=20, pady=(20,5))
        btn_dup_frame = tk.Frame(frame, bg=self.theme_manager.get("bg_panel"))
        btn_dup_frame.pack(fill=tk.X, padx=20, pady=5)
        tk.Button(btn_dup_frame, text=LANG[self.lang]["find_dup_btn"],
                 bg=self.theme_manager.get("color_purple"), fg=self.theme_manager.get("bg_main"),
                 font=(self.theme_manager.get("font_family"), 10, "bold"),
                 bd=0, padx=20, pady=8, command=self.find_duplicates).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_dup_frame, text=LANG[self.lang]["clear_dups"],
                 bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("color_alert"),
                 font=(self.theme_manager.get("font_family"), 10), bd=1, padx=20, pady=8,
                 command=self.clear_duplicates).pack(side=tk.LEFT, padx=5)

        self.txt_dups = scrolledtext.ScrolledText(frame, bg=self.theme_manager.get("bg_input"),
                                                 fg=self.theme_manager.get("color_alert"),
                                                 font=(self.theme_manager.get("font_mono"), 10), height=8, bd=0)
        self.txt_dups.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        add_context_menu(self.txt_dups, self.lang)

    # -------------------------------------------------------------------------
    # 0015 - THEME CUSTOMIZATION TAB
    # -------------------------------------------------------------------------
    def init_theme_tab(self):
        frame = tk.LabelFrame(self.tab_theme, text=LANG[self.lang]["theme_title"],
                             bg=self.theme_manager.get("bg_panel"),
                             fg=self.theme_manager.get("color_primary"),
                             font=(self.theme_manager.get("font_family"), 10, "bold"),
                             bd=1, relief=tk.SOLID)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, ipady=15)

        tk.Label(frame, text=LANG[self.lang]["theme_desc"],
                bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"),
                font=(self.theme_manager.get("font_family"), 10)).pack(anchor=tk.W, padx=20, pady=10)

        # Color buttons
        color_names = {
            "bg_main": "Background Main",
            "bg_panel": "Panel Background",
            "bg_input": "Input Background",
            "fg_main": "Foreground Text",
            "color_primary": "Primary Accent",
            "color_success": "Success Green",
            "color_warning": "Warning Orange",
            "color_purple": "Purple Accent",
            "color_alert": "Alert Red"
        }
        self.color_buttons = {}
        btn_frame = tk.Frame(frame, bg=self.theme_manager.get("bg_panel"))
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

        for key, label in color_names.items():
            sub_frame = tk.Frame(btn_frame, bg=self.theme_manager.get("bg_panel"))
            sub_frame.pack(side=tk.LEFT, padx=10, pady=5)
            tk.Label(sub_frame, text=label, bg=self.theme_manager.get("bg_panel"),
                    fg=self.theme_manager.get("fg_main"),
                    font=(self.theme_manager.get("font_family"), 9)).pack()
            btn = tk.Button(sub_frame, bg=self.theme_manager.get(key),
                           width=12, height=2,
                           command=lambda k=key: self.change_color(k))
            btn.pack(pady=2)
            self.color_buttons[key] = btn

        tk.Button(frame, text=LANG[self.lang]["reset_theme"],
                 bg=self.theme_manager.get("color_warning"), fg=self.theme_manager.get("bg_main"),
                 font=(self.theme_manager.get("font_family"), 10, "bold"),
                 bd=0, padx=20, pady=8, command=self.reset_theme).pack(pady=20)

    def change_color(self, key):
        color = colorchooser.askcolor(title=f"Choose {key}", color=self.theme_manager.get(key))
        if color and color[1]:
            self.theme_manager.set_color(key, color[1])
            self.setup_theme()
            self.apply_theme_to_all()
            # Update color button
            if key in self.color_buttons:
                self.color_buttons[key].config(bg=color[1])
            self.log(f"Color {key} changed to {color[1]}")

    def reset_theme(self):
        self.theme_manager.theme = DEFAULT_THEME.copy()
        self.theme_manager.save_theme()
        self.setup_theme()
        self.apply_theme_to_all()
        # Update color buttons
        for key, btn in self.color_buttons.items():
            btn.config(bg=self.theme_manager.get(key))
        self.log("Theme reset to default")

    # -------------------------------------------------------------------------
    # 0016 - CORE FUNCTIONALITY METHODS
    # -------------------------------------------------------------------------
    def browse_forward(self):
        folder = filedialog.askdirectory()
        if folder:
            self.target_dir.set(folder)
            self.log(f"Target set to: {folder}")
            self.set_status(f"Target: {folder}")

    def browse_reverse(self):
        folder = filedialog.askdirectory()
        if folder:
            self.reverse_dir.set(folder)
            self.log(f"Source set to: {folder}")

    def copy_to_clip(self, widget):
        self.root.clipboard_clear()
        self.root.clipboard_append(widget.get("1.0", tk.END).strip())
        self.log("Copied to clipboard")

    def set_status(self, msg):
        self.status_bar.config(text=msg)
        self.root.update_idletasks()

    def log(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.txt_log.insert(tk.END, f"[{timestamp}] {msg}\n")
        self.txt_log.see(tk.END)
        self.root.update_idletasks()

    def clear_log(self):
        self.txt_log.delete("1.0", tk.END)

    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, text=LANG[self.lang]["status_ready"],
                                  bg=self.theme_manager.get("bg_panel"),
                                  fg="#94a3b8", anchor=tk.W,
                                  font=(self.theme_manager.get("font_family"), 9), padx=10)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_live_log(self):
        log_frame = tk.LabelFrame(self.root, text="📋 Live Log",
                                 bg=self.theme_manager.get("bg_panel"),
                                 fg=self.theme_manager.get("color_warning"),
                                 font=(self.theme_manager.get("font_family"), 9, "bold"),
                                 bd=1, relief=tk.SOLID)
        log_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0,5))
        self.txt_log = scrolledtext.ScrolledText(log_frame, bg="#020617",
                                                fg=self.theme_manager.get("color_warning"),
                                                font=(self.theme_manager.get("font_mono"), 9), height=5, bd=0)
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        add_context_menu(self.txt_log, self.lang)
        tk.Button(log_frame, text=LANG[self.lang]["clear_log"],
                 bg=self.theme_manager.get("bg_panel"), fg=self.theme_manager.get("fg_main"),
                 font=(self.theme_manager.get("font_family"), 9), bd=1, padx=10, pady=2,
                 command=self.clear_log).pack(side=tk.RIGHT, padx=5, pady=2)

    # -------------------------------------------------------------------------
    # 0017 - LANGUAGE CHANGE
    # -------------------------------------------------------------------------
    def change_language(self, event=None):
        selected = self.lang_combo.get()
        self.lang = "en" if selected == "English" else "fa"
        self.save_language()
        self.update_ui_language()
        self.log(f"Language changed to {selected}")

    def update_ui_language(self):
        # Update all widgets with new language strings.
        self.lbl_title.config(text=LANG[self.lang]["app_title"])
        self.root.title(LANG[self.lang]["app_title"])
        self.notebook.tab(0, text=LANG[self.lang]["tab_forward"])
        self.notebook.tab(1, text=LANG[self.lang]["tab_reverse"])
        self.notebook.tab(2, text=LANG[self.lang]["tab_help"])
        self.notebook.tab(3, text=LANG[self.lang]["tab_export"])
        self.notebook.tab(4, text=LANG[self.lang]["tab_extra"])
        self.notebook.tab(5, text=LANG[self.lang]["tab_theme"])
        self.status_bar.config(text=LANG[self.lang]["status_ready"])

        # Update context menus of all text widgets (re-add with new language)
        # This is done by walking through all children and re-applying context menu
        for child in self.root.winfo_children():
            self.update_context_menu_for_widget(child)

    def update_context_menu_for_widget(self, widget):
        """Recursively update context menus for all text widgets."""
        if isinstance(widget, (tk.Text, tk.Entry, scrolledtext.ScrolledText)):
            # For ScrolledText, we need to get the actual text widget
            if isinstance(widget, scrolledtext.ScrolledText):
                # Re-bind the context menu to the internal text widget
                try:
                    add_context_menu(widget, self.lang)
                except:
                    pass
            else:
                add_context_menu(widget, self.lang)
        for child in widget.winfo_children():
            self.update_context_menu_for_widget(child)

    # -------------------------------------------------------------------------
    # 0018 - FORWARD ENGINE CORE
    # -------------------------------------------------------------------------
    def clean_line_advanced(self, line):
        line = re.sub(r"\s*(#|//|--|/\*).*$", "", line)
        for pattern in PATTERNS_50:
            line = re.sub(pattern, "", line)
        return line.strip()

    def detect_extension_from_content(self, line):
        known_exts = [".php", ".html", ".js", ".py", ".json", ".txt", ".md", ".css",
                      ".cpp", ".go", ".rs", ".mp4", ".mp3", ".png", ".jpg", ".svg", ".xml", ".yaml"]
        for ext in known_exts:
            if line.strip().endswith(ext):
                return ext
        if re.search(r"<\?php", line):
            return ".php"
        if re.search(r"<html", line, re.I):
            return ".html"
        if re.search(r"<script", line, re.I) or re.search(r"function\s+\w+\s*\(", line):
            return ".js"
        if re.search(r"def\s+\w+\s*\(.*\)\s*:", line):
            return ".py"
        if re.search(r"^\s*<!DOCTYPE html>", line, re.I):
            return ".html"
        if re.search(r"^\s*{\s*$", line):
            return ".json"
        return None

    def smart_parse_to_live(self):
        raw = self.txt_raw.get("1.0", tk.END).strip()
        if not raw:
            messagebox.showwarning(LANG[self.lang]["warning"], "Raw input is empty!")
            return
        lines = raw.splitlines()
        parsed = []
        for line in lines:
            cleaned = self.clean_line_advanced(line)
            if not cleaned:
                continue
            if self.default_extension.get() == "Auto Detect":
                ext = self.detect_extension_from_content(cleaned)
                if ext and '.' not in cleaned and not cleaned.endswith('/'):
                    cleaned += ext
            parsed.append(cleaned)
        self.txt_live.delete("1.0", tk.END)
        self.txt_live.insert(tk.END, "\n".join(parsed))
        self.log(f"Smart parsed {len(parsed)} items")
        self.set_status(f"Parsed {len(parsed)} items")

    def deploy_from_live(self):
        output_dir = self.target_dir.get()
        if not output_dir:
            messagebox.showerror(LANG[self.lang]["error"], "Target folder not selected.")
            return
        live_text = self.txt_live.get("1.0", tk.END).strip()
        if not live_text:
            messagebox.showerror(LANG[self.lang]["error"], "Live editor is empty.")
            return
        lines = live_text.splitlines()
        f_count = 0
        d_count = 0
        errors = []
        for item in lines:
            item = item.strip()
            if not item:
                continue
            is_dir = item.endswith('/') or item.endswith('\\') or ('.' not in item and self.default_extension.get() == "No Extension (Create Folder)")
            macro_mode = self.macro_format_mode.get()
            if not is_dir and '.' not in item:
                if macro_mode == "Keep Original":
                    fallback = self.default_extension.get()
                    if fallback not in ["Auto Detect", "No Extension (Create Folder)"]:
                        item += fallback
                    else:
                        is_dir = True
                elif macro_mode == "Force All to MP4":
                    item += ".mp4"
                elif macro_mode == "Force All to MP3":
                    item += ".mp3"
                elif macro_mode == "Force All to Web Formats (.html)":
                    item += ".html"
                elif macro_mode == "Strip All Extensions (Pure Folders)":
                    is_dir = True
            full_path = os.path.join(output_dir, item.replace('/', os.sep).replace('\\', os.sep))
            try:
                if is_dir:
                    os.makedirs(full_path, exist_ok=True)
                    d_count += 1
                    if self.cb_git_keep.get():
                        with open(os.path.join(full_path, ".gitkeep"), 'w') as gk:
                            pass
                else:
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    with open(full_path, 'a', encoding='utf-8') as f:
                        pass
                    f_count += 1
            except Exception as e:
                errors.append(f"{item}: {str(e)}")
        if self.cb_auto_readme.get():
            try:
                with open(os.path.join(output_dir, "AI_README.md"), 'w', encoding='utf-8') as rm:
                    rm.write(f"# AI-Generated Architecture\n\n- Date: {datetime.now()}\n- Directories: {d_count}\n- Files: {f_count}\n- Tool: AFAR Ultimate Pro v4.0\n")
            except:
                pass
        msg = f"Deployed: {d_count} dirs, {f_count} files"
        if errors:
            msg += f", {len(errors)} errors"
        self.log(msg)
        messagebox.showinfo(LANG[self.lang]["success"], msg)
        self.set_status(msg)

    # -------------------------------------------------------------------------
    # 0019 - REVERSE ENGINE CORE
    # -------------------------------------------------------------------------
    def execute_reverse_engineering(self):
        src = self.reverse_dir.get()
        if not src or not os.path.exists(src):
            messagebox.showerror(LANG[self.lang]["error"], "Invalid source folder.")
            return
        style = self.export_format.get()
        grp = self.reverse_group_filter.get()
        single_ext = self.single_ext_entry.get().strip()
        allowed_exts = FORMAT_GROUPS.get(grp, [])
        use_single = bool(single_ext)
        output_buffer = []

        if style == "Tree Structure":
            self.generate_tree_string(src, "", allowed_exts, use_single, single_ext, output_buffer)
            final = "\n".join(output_buffer)
        elif style == "JSON Map":
            data = self.generate_dict_tree(src, allowed_exts, use_single, single_ext)
            final = json.dumps(data, indent=4, ensure_ascii=False)
        elif style == "XML Sheet":
            root = ET.Element("Architecture", Name=os.path.basename(src))
            self.generate_xml_tree(src, root, allowed_exts, use_single, single_ext)
            xml_str = ET.tostring(root, encoding="utf-8")
            final = minidom.parseString(xml_str).toprettyxml(indent="  ")
        elif style == "Markdown Checklist":
            self.generate_markdown_checklist(src, 0, allowed_exts, use_single, single_ext, output_buffer)
            final = "\n".join(output_buffer)
        else:
            self.generate_flat_list(src, src, allowed_exts, use_single, single_ext, output_buffer)
            final = "\n".join(output_buffer)

        self.txt_reverse_output.delete("1.0", tk.END)
        self.txt_reverse_output.insert(tk.END, final)
        self.log(f"Reverse output generated ({len(output_buffer)} items)")
        self.set_status(f"Reverse: {len(output_buffer)} items")

    def should_include_file(self, filename, allowed_exts, use_single, single_ext):
        if use_single:
            return filename.endswith(single_ext)
        if allowed_exts:
            return any(filename.endswith(ext) for ext in allowed_exts)
        return True

    def generate_tree_string(self, dir_path, prefix, allowed_exts, use_single, single_ext, buffer):
        try:
            items = os.listdir(dir_path)
        except:
            return
        items.sort()
        pointers = ['├── '] * (len(items) - 1) + ['└── ']
        for ptr, name in zip(pointers, items):
            full = os.path.join(dir_path, name)
            if os.path.isdir(full):
                buffer.append(f"{prefix}{ptr}{name}/")
                ext = "│   " if ptr == '├── ' else "    "
                self.generate_tree_string(full, prefix + ext, allowed_exts, use_single, single_ext, buffer)
            else:
                if self.should_include_file(name, allowed_exts, use_single, single_ext):
                    meta = f" ({os.path.getsize(full)} bytes)" if self.cb_include_stats.get() else ""
                    buffer.append(f"{prefix}{ptr}{name}{meta}")

    def generate_dict_tree(self, dir_path, allowed_exts, use_single, single_ext):
        d = {'name': os.path.basename(dir_path), 'type': 'dir', 'children': []}
        try:
            for name in os.listdir(dir_path):
                full = os.path.join(dir_path, name)
                if os.path.isdir(full):
                    d['children'].append(self.generate_dict_tree(full, allowed_exts, use_single, single_ext))
                else:
                    if self.should_include_file(name, allowed_exts, use_single, single_ext):
                        item = {'name': name, 'type': 'file'}
                        if self.cb_include_stats.get():
                            item['size'] = os.path.getsize(full)
                        d['children'].append(item)
        except:
            pass
        return d

    def generate_xml_tree(self, dir_path, parent, allowed_exts, use_single, single_ext):
        try:
            for name in os.listdir(dir_path):
                full = os.path.join(dir_path, name)
                if os.path.isdir(full):
                    sub = ET.SubElement(parent, "Directory", Name=name)
                    self.generate_xml_tree(full, sub, allowed_exts, use_single, single_ext)
                else:
                    if self.should_include_file(name, allowed_exts, use_single, single_ext):
                        el = ET.SubElement(parent, "File", Name=name)
                        if self.cb_include_stats.get():
                            el.set("Size", str(os.path.getsize(full)))
        except:
            pass

    def generate_markdown_checklist(self, dir_path, level, allowed_exts, use_single, single_ext, buffer):
        indent = "  " * level
        try:
            for name in os.listdir(dir_path):
                full = os.path.join(dir_path, name)
                if os.path.isdir(full):
                    buffer.append(f"{indent}- [ ] 📁 {name}")
                    self.generate_markdown_checklist(full, level+1, allowed_exts, use_single, single_ext, buffer)
                else:
                    if self.should_include_file(name, allowed_exts, use_single, single_ext):
                        buffer.append(f"{indent}- [ ] 📄 {name}")
        except:
            pass

    def generate_flat_list(self, base, current, allowed_exts, use_single, single_ext, buffer):
        try:
            for name in os.listdir(current):
                full = os.path.join(current, name)
                if os.path.isdir(full):
                    self.generate_flat_list(base, full, allowed_exts, use_single, single_ext, buffer)
                else:
                    if self.should_include_file(name, allowed_exts, use_single, single_ext):
                        buffer.append(os.path.relpath(full, base))
        except:
            pass

    # -------------------------------------------------------------------------
    # 0020 - EXPORT & EXTRA TOOLS IMPLEMENTATIONS
    # -------------------------------------------------------------------------
    def save_output_to_file(self):
        content = self.txt_reverse_output.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning(LANG[self.lang]["warning"], "No output to save. Please run Reverse Engine first.")
            return
        fname = self.save_filename.get().strip()
        if not fname:
            fname = "output_structure.txt"
        target_dir = self.reverse_dir.get() or self.target_dir.get() or os.getcwd()
        full_path = os.path.join(target_dir, fname)
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.log(f"Saved output to {full_path}")
            messagebox.showinfo(LANG[self.lang]["success"], f"Saved to {full_path}")
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.insert(tk.END, f"Saved to: {full_path}\n\n" + content[:500] + ("..." if len(content) > 500 else ""))
        except Exception as e:
            messagebox.showerror(LANG[self.lang]["error"], str(e))
            self.log(f"Error saving: {str(e)}")

    def zip_project(self):
        target = self.target_dir.get()
        if not target or not os.path.exists(target):
            messagebox.showerror(LANG[self.lang]["error"], "Target folder not set or does not exist.")
            return
        zip_name = self.zip_filename.get().strip()
        if not zip_name:
            zip_name = "project_backup.zip"
        zip_path = os.path.join(os.path.dirname(target), zip_name)
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(target):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(target))
                        zipf.write(file_path, arcname)
            self.log(f"Project zipped to {zip_path}")
            messagebox.showinfo(LANG[self.lang]["success"], f"ZIP created: {zip_path}")
        except Exception as e:
            messagebox.showerror(LANG[self.lang]["error"], str(e))
            self.log(f"Error zipping: {str(e)}")

    def batch_rename(self):
        src = self.reverse_dir.get()
        if not src or not os.path.exists(src):
            messagebox.showerror(LANG[self.lang]["error"], "Source folder not set.")
            return
        pattern = self.rename_pattern.get().strip()
        if not pattern or "->" not in pattern:
            messagebox.showerror(LANG[self.lang]["error"], "Invalid pattern. Use old->new (e.g., .txt->.md)")
            return
        old, new = pattern.split("->", 1)
        count = 0
        for root, _, files in os.walk(src):
            for f in files:
                if f.endswith(old):
                    old_path = os.path.join(root, f)
                    new_path = os.path.join(root, f.replace(old, new))
                    try:
                        os.rename(old_path, new_path)
                        count += 1
                    except:
                        pass
        self.log(f"Renamed {count} files")
        messagebox.showinfo(LANG[self.lang]["success"], f"Renamed {count} files.")

    def find_duplicates(self):
        src = self.reverse_dir.get()
        if not src or not os.path.exists(src):
            messagebox.showerror(LANG[self.lang]["error"], "Source folder not set.")
            return
        hashes = {}
        dups = []
        for root, _, files in os.walk(src):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    with open(fp, 'rb') as file:
                        h = hash(file.read())
                    if h in hashes:
                        dups.append(fp)
                    else:
                        hashes[h] = fp
                except:
                    pass
        self.duplicates_list = dups
        self.txt_dups.delete("1.0", tk.END)
        if dups:
            self.txt_dups.insert(tk.END, "\n".join(dups))
            self.log(f"Found {len(dups)} duplicate files")
            messagebox.showinfo(LANG[self.lang]["info"], f"Found {len(dups)} duplicates.")
        else:
            self.txt_dups.insert(tk.END, "No duplicates found.")
            messagebox.showinfo(LANG[self.lang]["info"], "No duplicates found.")

    def clear_duplicates(self):
        self.txt_dups.delete("1.0", tk.END)
        self.duplicates_list = []
        self.log("Duplicates list cleared.")

    # -------------------------------------------------------------------------
    # 0021 - WEB INPUT FETCH
    # -------------------------------------------------------------------------
    def fetch_web_content(self):
        url = self.web_url.get().strip()
        if not url:
            messagebox.showwarning(LANG[self.lang]["warning"], "Please enter a valid URL.")
            return
        try:
            self.set_status("Fetching content from URL...")
            response = requests.get(url, timeout=15)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                content = response.text
                # Try to extract structure from the page if it's HTML
                if url.endswith(('.html', '.htm')):
                    # Look for pre, code, or textarea content
                    match = re.search(r'<(?:pre|code|textarea)[^>]*>(.*?)</(?:pre|code|textarea)>', content, re.DOTALL | re.IGNORECASE)
                    if match:
                        content = match.group(1).strip()
                self.txt_raw.delete("1.0", tk.END)
                self.txt_raw.insert(tk.END, content)
                self.log(f"Content fetched from {url}")
                self.set_status(f"Content loaded from URL ({len(content)} chars)")
                messagebox.showinfo(LANG[self.lang]["success"], f"Content fetched successfully!\nLoaded {len(content)} characters.")
            else:
                messagebox.showerror(LANG[self.lang]["error"], f"Failed to fetch content: HTTP {response.status_code}")
                self.log(f"Web fetch error: {response.status_code}")
        except Exception as e:
            messagebox.showerror(LANG[self.lang]["error"], f"Error fetching URL: {str(e)}")
            self.log(f"Web fetch error: {str(e)}")
        finally:
            self.set_status(LANG[self.lang]["status_ready"])

# =============================================================================
# 0022 - APPLICATION ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AFARUltimatePro(root)
    root.mainloop()