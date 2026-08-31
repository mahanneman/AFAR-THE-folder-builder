# ============================================================================
# 0001 - AFAR ULTIMATE v7.0 – Full GitHub Control + Enterprise Git Tools
# ============================================================================
"""
Author: MA.GH.AD (https://github.com/mahanneman)
License: MIT
Description: Complete dynamic bilingual support (EN/FA). Every text element
             changes when language is switched. Includes mouse scroll support,
             right-click context menus, customizable colors, full help,
             and full GitHub integration (login, create repo, clone, commit,
             push, pull, file operations, file tree, edit files, 20+ git commands).
"""

import os
import re
import json
import shutil
import zipfile
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext, colorchooser, simpledialog
from datetime import datetime
import requests
import webbrowser
import tempfile
import threading

# ============================================================================
# 0002 - THEME (Premium Dark – Royal Spectrum)
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
# 0003 - 50 REGEX PATTERNS (unchanged, omitted for brevity)
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
    r"^[📁📂📄📃📜📊📈📉📋📌📍📎📏📐📒📓📔📕📖📗📘📙📚📛📜📝📞📟📠📡📢📣📤📥📦📧📨📩📪📫📬📭📮📯📰📱📲📳📴📵📶📷📸📹📺📻📼📽📾]\s*",
    r"^[🔍🔎🔏🔐🔑🔒🔓🔔🔕🔖🔗🔘🔙🔚🔛🔜🔝🔞🔟🔠🔡🔢🔣🔤🔥🔦🔧🔨🔩🔪🔫🔬🔭🔮🔯🔰🔱🔲🔳🔴🔵🔶🔷🔸🔹🔺🔻🔼🔽🔾🔿🕀🕁🕂🕃🕄🕅🕆🕇🕈🕉🕊🕋🕌🕍🕎🕏🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛]\s*",
    r"^[⚡⚽⚾⛳⛪⛲⛺♨♠♣♥♦♨♩♪♫♬♭♮♯♰♱♲♳♴♵♶♷♸♹♺♻♼♽♾♿]\s*",
    r"^[✨🌟⭐🌙🌚🌛🌜🌝🌞🌠🌡🌤🌥🌦🌧🌨🌩🌪🌫🌬🌭🌮🌯🌰🌱🌲🌳🌴🌵🌶🌷🌸🌹🌺🌻🌼🌽🌾🌿🍀🍁🍂🍃🍄🍅🍆🍇🍈🍉🍊🍋🍌🍍🍎🍏🍐🍑🍒🍓🍔🍕🍖🍗🍘🍙🍚🍛🍜🍝🍞🍟🍠🍡🍢🍣🍤🍥🍦🍧🍨🍩🍪🍫🍬🍭🍮🍯🍰🍱🍲🍳🍴🍵🍶🍷🍸🍹🍺🍻🍼]\s*",
    r"^[🚀🚁🚂🚃🚄🚅🚆🚇🚈🚉🚊🚋🚌🚍🚎🚏🚐🚑🚒🚓🚔🚕🚖🚗🚘🚙🚚🚛🚜🚝🚞🚟🚠🚡🚢🚣🚤🚥🚦🚧🚨🚩🚪🚫🚬🚭🚮🚯🚰🚱🚲🚳🚴🚵🚶🚷🚸🚹🚺🚻🚼🚽🚾🚿🛀🛁🛂🛃🛄🛅🛋🛌🛍🛎🛏🛐🛑🛒🛠🛡🛢🛣🛤🛥🛩🛫🛬🛰🛳]\s*",
    r"^[±×÷∑∏∫√∞≈≠≤≥±∂∇∆∅∈∉⊂⊃⊆⊇⊕⊖⊗⊘⊙⊚⊛⊜⊝]\s*",
    r"^[¬∧∨∀∃∄∅∈∉⊂⊃⊆⊇∨∧⊕⊗⊥⊤⊥⊢⊨⊩⊫⊬⊭⊮⊯]\s*",
    r"^[→←↑↓↔↕↖↗↘↙↚↛↜↝↞↟↠↡↢↣↤↥↦↧↨↩↪↫↬↭↮↯]\s*",
    r"^[⌘⌥⌦⌧⌨⌫⌬⌭⌮⌯⌰⌱⌲⌳⌴⌵⌶⌷⌸⌹⌺⌻⌼⌽⌾⌿⍀⍁⍂⍃⍄⍅⍆⍇⍈⍉⍊⍋⍌⍍⍎⍏⍐⍑⍒⍓⍔⍕⍖⍗⍘⍙⍚⍛⍜⍝⍞⍟⍠⍡⍢⍣⍤⍥⍦⍧⍨⍩⍪⍫⍬⍭⍮⍯⍰]\s*",
    r"^[⌠⌡⌢⌣⌤⌥⌦⌧⌨〈〉⌫⌬⌭⌮⌯⌰⌱⌲⌳⌴⌵⌶⌷⌸⌹⌺⌻⌼⌽⌾⌿⍀⍁⍂⍃⍄⍅⍆⍇⍈⍉⍊⍋⍌⍍⍎⍏⍐⍑⍒⍓⍔⍕⍖⍗⍘⍙⍚⍛⍜⍝⍞⍟⍠⍡⍢⍣⍤⍥⍦⍧⍨⍩⍪⍫⍬⍭⍮⍯⍰]\s*",
    r"^[═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬]\s*",
    r"^[▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕▖▗▘▙▚▛▜▝▞▟]\s*",
    r"^[─━│┃┄┅┆┇┈┉┊┋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┯┰┱┲┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╌╍╎╏]\s*",
    r"^[┌┐└┘├┤┬┴┼╭╮╯╰]\s*", r"^[╔╗╚╝╠╣╦╩╬═║╒╕╘╛╞╡╤╧╪╟╢╥╨╫]\s*",
    r"^[«»“”‘’‛″‴‵‶‷‸‹›«»‘’‚‛“”„‟†‡•‣․‥…‧‰‱′″‴‵‶‷‸‹›]\s*",
    r"^[¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿]\s*",
    r"^[ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ]\s*",
    r"^[ĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŒœŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽž]\s*",
    r"^[ﬀﬁﬂﬃﬄﬅﬆﬓﬔﬕﬖﬗיִﬞײַﬠﬡﬢﬣﬤﬥﬦﬧﬨ﬩שׁשׂשּׁשּׂאַאָאּבּגּדּהּוּזּטּיּךּכּלּמּנּסּףּפּצּקּרּשּתּוֹבֿכֿפֿﭏ]\s*",
    r"^[☀☁☂☃☄★☆☇☈☉☊☋☌☍☎☏☐☑☒☓☔☕☖☗☘☙☚☛☜☝☞☟☠☡☢☣☤☥☦☧☨☩☪☫☬☭☮☯☰☱☲☳☴☵☶☷☸☹☺☻☼☽☾☿♀♁♂♃♄♅♆♇]\s*",
    r"^[♈♉♊♋♌♍♎♏♐♑♒♓]\s*", r"^[⚀⚁⚂⚃⚄⚅]\s*", r"^[➊➋➌➍➎➏➐➑➒➓]\s*",
    r"^[🄐🄑🄒🄓🄔🄕🄖🄗🄘🄙🄚🄛🄜🄝🄞🄟🄠🄡🄢🄣🄤🄥🄦🄧🄨🄩]\s*",
]

# ============================================================================
# 0004 - FILE GROUPS (unchanged)
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
# 0005 - BILINGUAL DICTIONARY (با کلیدهای جدید)
# ============================================================================
T = {
    "en": {
        "title": "⚡ AFAR PRO v7.0 – Build, Reverse & GitHub",
        "ready": "Ready",
        "tab_build": "📥 Build",
        "tab_reverse": "📤 Reverse",
        "tab_github": "🐙 GitHub",
        "tab_help": "📖 Guide",
        "tab_export": "💾 Export",
        "tab_settings": "⚙️ Settings",
        "dest": "Target Folder",
        "browse": "Browse",
        "injectors": "Injectors & Parser",
        "fallback": "Fallback Extension:",
        "fallback_tip": "If a file has no extension, this will be added automatically. 'Auto Detect' tries to guess from content.",
        "force": "Force Modifier:",
        "force_tip": "Apply a forced extension to all files, or convert all items to folders.",
        "readme": "Generate AI Readme",
        "gitkeep": "Inject .gitkeep",
        "raw": "1. Paste your tree/list here",
        "live": "2. Live Editor (edit before deploy)",
        "parse_btn": "⚡ Parse to Live",
        "clear_raw": "Clear Raw",
        "copy": "Copy",
        "clear_live": "Clear Live",
        "deploy": "🚀 Deploy Now",
        "source": "Source Folder (reverse)",
        "browse_src": "Browse Source",
        "format": "Output Format & Filters",
        "style": "Export Style:",
        "group": "Group Filter:",
        "ext": "Specific extension:",
        "meta": "Append Size",
        "copy_out": "Copy Output",
        "clear_out": "Clear",
        "output": "Reverse Output (AI-ready)",
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
        "help_text": """1. FOLDER: add slash at end (src/)
2. FILE: include extension (index.php)
3. NESTED: use indentation, bullets, or numbers
4. AUTO-DETECT: <?php → .php, <html → .html
5. IGNORE: empty lines, comments (#, //, --)""",
        "help_ex": """▶ TREE:
src/
    controllers/
        HomeController.php
    index.php
public/
    css/style.css
README.md

▶ BULLET:
• src/
  • controllers/
    • HomeController.php

▶ NUMBERED:
1. src/
   1.1. controllers/
       1.1.1. HomeController.php""",
        "help_force": """1. Keep Original – uses given extension or fallback
2. Force MP4 – adds .mp4 to all files
3. Force MP3 – adds .mp3 to all files
4. Force HTML – adds .html to all files
5. Strip Extensions – treats all as folders""",
        "help_rev": """1. Tree Structure – classic tree with lines
2. JSON Map – structured JSON with metadata
3. XML Sheet – XML with <Dir>/<File> tags
4. Markdown Checklist – - [ ] items
5. Flat Clean List – simple relative paths""",
        "help_tips": """• Type directly in Live Editor
• Use Smart Parse to clean lists
• Right-click for context menu
• Customize colors in Settings
• Check Live Log for errors""",
        "github_token": "GitHub Token:",
        "token_login": "Login & Save",
        "token_status": "Status:",
        "repo_list": "Repositories:",
        "refresh_repos": "🔄 Refresh",
        "create_repo": "Create New Repo",
        "repo_name": "Repo name:",
        "repo_desc": "Description:",
        "create_btn": "Create",
        "local_path": "Local Repo Path:",
        "browse_local": "Browse",
        "clone_btn": "Clone",
        "clone_url": "Clone URL:",
        "commit_msg": "Commit Message:",
        "commit_btn": "Commit",
        "push_btn": "Push",
        "pull_btn": "Pull",
        "file_ops": "File Operations",
        "new_file": "New File",
        "file_name": "File name:",
        "file_content": "Content:",
        "create_file_btn": "Create",
        "delete_file": "Delete File",
        "delete_btn": "Delete",
        "rename_file": "Rename File",
        "rename_old": "Old name:",
        "rename_new": "New name:",
        "rename_btn": "Rename",
        "git_log": "Git Actions Log:",
        "credit": "Developed by MA.GH.AD",
        "credit_link": "https://github.com/mahanneman",
        "git_commands": "Git Commands:",
        "run_command": "Run",
        "quick_actions": "Quick Actions:",
        "git_status": "Status",
        "git_log_cmd": "Log",
        "git_diff": "Diff",
        "git_branch": "Branches",
        "git_remote": "Remote",
        "file_tree": "Project Files:",
        "edit_file": "Edit File Content:",
        "save_file": "Save File",
        "open_file": "Open File",
        # new keys for GitHub enhancements
        "github_files": "Repository Files:",
        "select_all": "Select All",
        "deselect_all": "Deselect All",
        "delete_selected": "Delete Selected",
        "download_selected": "Download Selected (Temp)",
        "edit_selected": "Edit Selected",
        "refresh_files": "Refresh Files",
        "file_status": "Status",
        "file_last_commit": "Last Commit",
        "open_in_explorer": "Open in Explorer",
        "git_stash": "Stash",
        "git_stash_pop": "Stash Pop",
        "git_reset_hard": "Reset Hard",
        "git_reset_soft": "Reset Soft",
        "git_revert": "Revert",
        "git_cherry_pick": "Cherry-pick",
        "git_rebase": "Rebase",
        "git_merge": "Merge",
        "git_fetch": "Fetch",
        "git_tag": "Tag",
        "git_blame": "Blame",
        "git_show": "Show",
        "git_grep": "Grep",
        "git_config": "Config",
        "git_checkout": "Checkout",
        "git_branch_new": "New Branch",
        "git_branch_delete": "Delete Branch"
    },
    "fa": {
        "title": "⚡ AFAR حرفه‌ای v7.0 – ساخت، معکوس و گیت‌هاب",
        "ready": "آماده",
        "tab_build": "📥 ساخت",
        "tab_reverse": "📤 معکوس",
        "tab_github": "🐙 گیت‌هاب",
        "tab_help": "📖 راهنما",
        "tab_export": "💾 خروجی",
        "tab_settings": "⚙️ تنظیمات",
        "dest": "پوشه مقصد",
        "browse": "مرور",
        "injectors": "تزریق‌کننده و پردازشگر",
        "fallback": "پسوند پیش‌فرض:",
        "fallback_tip": "اگر فایل پسوند نداشته باشد، این پسوند به آن اضافه می‌شود. 'تشخیص خودکار' سعی می‌کند از محتوا حدس بزند.",
        "force": "اصلاح‌گر:",
        "force_tip": "یک پسوند اجباری به همه فایل‌ها اعمال کنید، یا همه موارد را به پوشه تبدیل کنید.",
        "readme": "تولید Readme هوشمند",
        "gitkeep": "تزریق .gitkeep",
        "raw": "۱. درخت/لیست خود را جای‌گذاری کنید",
        "live": "۲. ویرایشگر زنده (قبل از استقرار)",
        "parse_btn": "⚡ پردازش به ویرایشگر",
        "clear_raw": "پاک کردن ورودی",
        "copy": "کپی",
        "clear_live": "پاک کردن ویرایشگر",
        "deploy": "🚀 استقرار",
        "source": "پوشه مبدأ (معکوس)",
        "browse_src": "مرور مبدأ",
        "format": "فرمت خروجی و فیلترها",
        "style": "سبک خروجی:",
        "group": "فیلتر گروه:",
        "ext": "پسوند خاص:",
        "meta": "افزودن اندازه",
        "copy_out": "کپی خروجی",
        "clear_out": "پاک کردن",
        "output": "خروجی معکوس (آماده)",
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
        "help_s3": "🔹 اصلاح‌گرهای ماکرو",
        "help_s4": "🔹 فرمت‌های خروجی",
        "help_s5": "🔹 نکات سریع",
        "help_text": """۱. پوشه: در انتها اسلش بگذارید (src/)
۲. فایل: پسوند داشته باشد (index.php)
۳. تو در تو: از تورفتگی، گلوله یا شماره
۴. تشخیص خودکار: <?php → .php, <html → .html
۵. خطوط خالی و کامنت‌ها نادیده گرفته می‌شوند""",
        "help_ex": """▶ درختی:
src/
    controllers/
        HomeController.php
    index.php
public/
    css/style.css
README.md

▶ گلوله‌ای:
• src/
  • controllers/
    • HomeController.php

▶ شماره‌دار:
۱. src/
   ۱.۱. controllers/
       ۱.۱.۱. HomeController.php""",
        "help_force": """۱. حفظ اصلی – از پسوند داده‌شده یا پیش‌فرض استفاده می‌کند
۲. تبدیل به MP4 – به همه فایل‌ها .mp4 اضافه می‌کند
۳. تبدیل به MP3 – به همه فایل‌ها .mp3 اضافه می‌کند
۴. تبدیل به HTML – به همه فایل‌ها .html اضافه می‌کند
۵. حذف پسوندها – همه را به‌عنوان پوشه در نظر می‌گیرد""",
        "help_rev": """۱. ساختار درختی – درخت کلاسیک با خطوط
۲. نقشه JSON – JSON ساختاریافته با فراداده
۳. برگه XML – XML با تگ‌های <Dir>/<File>
۴. چک‌لیست مارک‌داون – آیتم‌های - [ ]
۵. لیست تخت – مسیرهای ساده نسبی""",
        "help_tips": """• مستقیماً در ویرایشگر زنده تایپ کنید
• از پردازش هوشمند برای تمیز کردن لیست استفاده کنید
• راست‌کلیک برای منوی زمینه
• رنگ‌ها را در تنظیمات شخصی‌سازی کنید
• لاگ زنده را برای خطاها بررسی کنید""",
        "github_token": "توکن گیت‌هاب:",
        "token_login": "ورود و ذخیره",
        "token_status": "وضعیت:",
        "repo_list": "مخازن:",
        "refresh_repos": "🔄 به‌روزرسانی",
        "create_repo": "ایجاد مخزن جدید",
        "repo_name": "نام مخزن:",
        "repo_desc": "توضیحات:",
        "create_btn": "ایجاد",
        "local_path": "مسیر محلی مخزن:",
        "browse_local": "مرور",
        "clone_btn": "کلون",
        "clone_url": "آدرس کلون:",
        "commit_msg": "پیام کامیت:",
        "commit_btn": "کامیت",
        "push_btn": "ارسال (Push)",
        "pull_btn": "دریافت (Pull)",
        "file_ops": "عملیات فایل",
        "new_file": "فایل جدید",
        "file_name": "نام فایل:",
        "file_content": "محتوا:",
        "create_file_btn": "ایجاد",
        "delete_file": "حذف فایل",
        "delete_btn": "حذف",
        "rename_file": "تغییر نام فایل",
        "rename_old": "نام قدیمی:",
        "rename_new": "نام جدید:",
        "rename_btn": "تغییر نام",
        "git_log": "لاگ عملیات گیت:",
        "credit": "تهیه‌شده توسط MA.GH.AD",
        "credit_link": "https://github.com/mahanneman",
        "git_commands": "دستورات گیت:",
        "run_command": "اجرا",
        "quick_actions": "اقدامات سریع:",
        "git_status": "وضعیت",
        "git_log_cmd": "لاگ",
        "git_diff": "تفاوت",
        "git_branch": "شاخه‌ها",
        "git_remote": "ریموت",
        "file_tree": "فایل‌های پروژه:",
        "edit_file": "ویرایش محتوای فایل:",
        "save_file": "ذخیره فایل",
        "open_file": "باز کردن فایل",
        # new keys for GitHub enhancements
        "github_files": "فایل‌های مخزن:",
        "select_all": "انتخاب همه",
        "deselect_all": "لغو انتخاب همه",
        "delete_selected": "حذف انتخاب‌شده‌ها",
        "download_selected": "دانلود انتخاب‌شده‌ها (Temp)",
        "edit_selected": "ویرایش انتخاب‌شده",
        "refresh_files": "به‌روزرسانی فایل‌ها",
        "file_status": "وضعیت",
        "file_last_commit": "آخرین کامیت",
        "open_in_explorer": "باز کردن در Explorer",
        "git_stash": "مخفی‌سازی (Stash)",
        "git_stash_pop": "بازگردانی مخفی‌سازی",
        "git_reset_hard": "بازنشانی سخت",
        "git_reset_soft": "بازنشانی نرم",
        "git_revert": "بازگردانی",
        "git_cherry_pick": "انتخاب گیلاس",
        "git_rebase": "بازپایه",
        "git_merge": "ادغام",
        "git_fetch": "دریافت",
        "git_tag": "برچسب",
        "git_blame": "نسبت‌دهی",
        "git_show": "نمایش",
        "git_grep": "جستجو",
        "git_config": "پیکربندی",
        "git_checkout": "تغییر شاخه",
        "git_branch_new": "شاخه جدید",
        "git_branch_delete": "حذف شاخه"
    }
}

# ============================================================================
# 0006 - CONTEXT MENU & MOUSE SCROLL (با پشتیبانی از کلیپ‌بورد)
# ============================================================================
def add_context_menu(widget, lang):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label=T[lang]["context_copy"], command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label=T[lang]["context_cut"], command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_command(label=T[lang]["context_paste"], command=lambda: widget.event_generate("<<Paste>>"))
    menu.add_separator()
    menu.add_command(label=T[lang]["context_delete"], command=lambda: widget.delete("sel.first", "sel.last") if widget.tag_ranges("sel") else None)
    menu.add_command(label=T[lang]["context_select_all"], command=lambda: widget.tag_add("sel", "1.0", "end"))
    def show(e):
        try:
            menu.tk_popup(e.x_root, e.y_root)
        finally:
            menu.grab_release()
    widget.bind("<Button-3>", show)
    # برای اطمینان از کار کردن کلیپ‌بورد با کیبورد
    widget.bind("<Control-c>", lambda e: widget.event_generate("<<Copy>>"))
    widget.bind("<Control-x>", lambda e: widget.event_generate("<<Cut>>"))
    widget.bind("<Control-v>", lambda e: widget.event_generate("<<Paste>>"))
    widget.bind("<Control-a>", lambda e: widget.tag_add("sel", "1.0", "end"))
    return menu

def enable_mouse_scroll(widget):
    def on_mousewheel(event):
        if event.num == 5 or event.delta < 0:
            widget.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            widget.yview_scroll(-1, "units")
    widget.bind("<MouseWheel>", on_mousewheel)
    widget.bind("<Button-4>", on_mousewheel)
    widget.bind("<Button-5>", on_mousewheel)
    return widget

# ============================================================================
# 0007 - MAIN APPLICATION CLASS
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

        # Core variables
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

        # GitHub variables
        self.github_token = tk.StringVar()
        self.local_repo_path = tk.StringVar()
        self.repo_name = tk.StringVar()
        self.repo_desc = tk.StringVar()
        self.clone_url = tk.StringVar()
        self.commit_msg = tk.StringVar(value="Update from AFAR")
        self.new_file_name = tk.StringVar()
        self.new_file_content = tk.StringVar()
        self.delete_file_name = tk.StringVar()
        self.rename_old_name = tk.StringVar()
        self.rename_new_name = tk.StringVar()
        self.git_custom_command = tk.StringVar(value="git status")
        self.selected_file = None
        self.selected_files = []  # لیست فایل‌های انتخاب‌شده

        self.build_ui()
        self.create_status_bar()
        self.create_log()
        self.create_credit_footer()
        self.apply_theme()
        self.update_status_lang()

    # ------------------------------------------------------------------------
    # 0008 - CONFIG
    # ------------------------------------------------------------------------
    def load_config(self):
        cfg = os.path.expanduser("~/.afar.json")
        if os.path.exists(cfg):
            try:
                with open(cfg, 'r') as f:
                    d = json.load(f)
                    self.lang = d.get("lang", "en")
                    self.theme.update(d.get("theme", THEME))
                    self.github_token.set(d.get("github_token", ""))
            except:
                pass

    def save_config(self):
        cfg = os.path.expanduser("~/.afar.json")
        data = {"lang": self.lang, "theme": self.theme, "github_token": self.github_token.get()}
        with open(cfg, 'w') as f:
            json.dump(data, f, indent=2)

    # ------------------------------------------------------------------------
    # 0009 - THEME
    # ------------------------------------------------------------------------
    def apply_theme(self):
        self.root.configure(bg=self.theme["bg"])
        if hasattr(self, 'status_bar'):
            self.status_bar.config(bg=self.theme["panel"], fg="#94a3b8")
        if hasattr(self, 'txt_log'):
            self.txt_log.config(bg="#020617", fg=self.theme["warning"])
        if hasattr(self, 'git_log_text'):
            self.git_log_text.config(bg="#020617", fg=self.theme["info"])
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
                elif isinstance(w, ttk.Treeview):
                    s = ttk.Style()
                    s.configure("Treeview", background=self.theme["input"],
                               foreground=self.theme["fg"], fieldbackground=self.theme["input"])
            except:
                pass
            for ch in w.winfo_children():
                rec(ch)
        for ch in self.root.winfo_children():
            rec(ch)

    # ------------------------------------------------------------------------
    # 0010 - UI BUILD
    # ------------------------------------------------------------------------
    def build_ui(self):
        self.hdr = tk.Frame(self.root, bg=self.theme["panel"], height=50)
        self.hdr.pack(fill=tk.X, side=tk.TOP)
        self.lbl_title = tk.Label(self.hdr, text=T[self.lang]["title"], bg=self.theme["panel"],
                                  fg=self.theme["primary"], font=("Segoe UI", 13, "bold"))
        self.lbl_title.pack(side=tk.LEFT, padx=20, pady=8)

        self.lang_frame = tk.Frame(self.hdr, bg=self.theme["panel"])
        self.lang_frame.pack(side=tk.RIGHT, padx=15)
        tk.Label(self.lang_frame, text="Language:", bg=self.theme["panel"], fg=self.theme["fg"]).pack(side=tk.LEFT, padx=5)
        self.lang_cb = ttk.Combobox(self.lang_frame, values=["English", "فارسی"], state="readonly", width=10)
        self.lang_cb.set("English" if self.lang=="en" else "فارسی")
        self.lang_cb.pack(side=tk.LEFT, padx=5)
        self.lang_cb.bind("<<ComboboxSelected>>", self.change_lang)

        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        tabs = ["build", "reverse", "github", "help", "export", "settings"]
        self.frames = {}
        for t in tabs:
            f = tk.Frame(self.nb, bg=self.theme["bg"])
            self.nb.add(f, text=T[self.lang][f"tab_{t}"])
            self.frames[t] = f

        self.init_build()
        self.init_reverse()
        self.init_github()      # ← این تابع از نسخهٔ ۵ جایگزین شده است
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

    # =========================================================================
    # BUILD TAB (با رفع مشکل کلیپ‌بورد)
    # =========================================================================
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
        self.fb_tip = tk.Label(cfg, text=T[self.lang]["fallback_tip"], bg=self.theme["panel"],
                               fg=self.theme["info"], font=("Segoe UI", 8, "italic"), wraplength=200, justify=tk.LEFT)
        self.fb_tip.pack(anchor=tk.W, padx=10, pady=(0,5))

        tk.Label(cfg, text=T[self.lang]["force"], bg=self.theme["panel"], fg=self.theme["fg"]).pack(anchor=tk.W, padx=8, pady=(8,2))
        cb_fo = ttk.Combobox(cfg, textvariable=self.force,
                     values=["Keep Original", "Force MP4", "Force MP3", "Force HTML", "Strip Extensions (Folders)"],
                     state="readonly")
        cb_fo.pack(fill=tk.X, padx=8, pady=4)
        self.fo_tip = tk.Label(cfg, text=T[self.lang]["force_tip"], bg=self.theme["panel"],
                               fg=self.theme["info"], font=("Segoe UI", 8, "italic"), wraplength=200, justify=tk.LEFT)
        self.fo_tip.pack(anchor=tk.W, padx=10, pady=(0,5))

        self.cb_readme_widget = tk.Checkbutton(cfg, text=T[self.lang]["readme"], variable=self.cb_readme,
                       bg=self.theme["panel"], fg=self.theme["fg"], selectcolor=self.theme["bg"],
                       activebackground=self.theme["panel"])
        self.cb_readme_widget.pack(anchor=tk.W, padx=8, pady=2)
        self.cb_gitkeep_widget = tk.Checkbutton(cfg, text=T[self.lang]["gitkeep"], variable=self.cb_gitkeep,
                       bg=self.theme["panel"], fg=self.theme["fg"], selectcolor=self.theme["bg"],
                       activebackground=self.theme["panel"])
        self.cb_gitkeep_widget.pack(anchor=tk.W, padx=8, pady=2)

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

    # =========================================================================
    # REVERSE TAB (با رفع مشکل کلیپ‌بورد)
    # =========================================================================
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

        self.cb_meta_widget = tk.Checkbutton(cfg, text=T[self.lang]["meta"], variable=self.cb_meta,
                       bg=self.theme["panel"], fg=self.theme["fg"], selectcolor=self.theme["bg"],
                       activebackground=self.theme["panel"])
        self.cb_meta_widget.pack(anchor=tk.W, padx=8, pady=4)

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
        self.log(f"Reverse output: {len(buf)} items")

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

    # =========================================================================
    # GITHUB TAB – نسخهٔ کلاسیک از V5 (ساده و کامل)
    # =========================================================================
    def init_github(self):
        f = self.frames["github"]

        main_canvas = tk.Canvas(f, bg=self.theme["bg"], bd=0, highlightthickness=0)
        scroll = ttk.Scrollbar(f, orient="vertical", command=main_canvas.yview)
        inner = tk.Frame(main_canvas, bg=self.theme["bg"])
        inner.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
        main_canvas.create_window((0,0), window=inner, anchor="nw")
        main_canvas.configure(yscrollcommand=scroll.set)
        main_canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        enable_mouse_scroll(main_canvas)

        # ---- Token Section ----
        token_frame = tk.LabelFrame(inner, text="🔑 GitHub Authentication", bg=self.theme["panel"],
                                    fg=self.theme["primary"], font=("Segoe UI", 10, "bold"), bd=1, relief=tk.SOLID)
        token_frame.pack(fill=tk.X, padx=10, pady=8, ipady=5)
        tk.Label(token_frame, text=T[self.lang]["github_token"], bg=self.theme["panel"], fg=self.theme["fg"]).grid(row=0, column=0, padx=8, pady=5, sticky=tk.W)
        token_entry = tk.Entry(token_frame, textvariable=self.github_token, bg=self.theme["input"], fg=self.theme["fg"],
                               font=("Consolas", 10), bd=1, relief=tk.SOLID, width=50, show="*")
        token_entry.grid(row=0, column=1, padx=8, pady=5, sticky=tk.W)
        add_context_menu(token_entry, self.lang)
        tk.Button(token_frame, text=T[self.lang]["token_login"], bg=self.theme["success"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=10, pady=4, command=self.github_login).grid(row=0, column=2, padx=8, pady=5)
        self.token_status_label = tk.Label(token_frame, text=T[self.lang]["token_status"] + " Not logged in", bg=self.theme["panel"],
                                           fg=self.theme["danger"], font=("Segoe UI", 9))
        self.token_status_label.grid(row=1, column=0, columnspan=3, padx=8, pady=2, sticky=tk.W)

        # ---- Repo Management ----
        repo_frame = tk.LabelFrame(inner, text="📁 Repository Management", bg=self.theme["panel"],
                                   fg=self.theme["primary"], font=("Segoe UI", 10, "bold"), bd=1, relief=tk.SOLID)
        repo_frame.pack(fill=tk.X, padx=10, pady=8, ipady=5)
        tk.Label(repo_frame, text=T[self.lang]["repo_list"], bg=self.theme["panel"], fg=self.theme["fg"]).grid(row=0, column=0, padx=8, pady=5, sticky=tk.W)
        self.repo_listbox = tk.Listbox(repo_frame, bg=self.theme["input"], fg=self.theme["fg"],
                                       font=("Consolas", 10), height=5, bd=1, relief=tk.SOLID, selectmode=tk.SINGLE)
        self.repo_listbox.grid(row=0, column=1, padx=8, pady=5, sticky=tk.W+tk.E)
        scroll_repo = ttk.Scrollbar(repo_frame, orient="vertical", command=self.repo_listbox.yview)
        scroll_repo.grid(row=0, column=2, sticky="ns")
        self.repo_listbox.configure(yscrollcommand=scroll_repo.set)
        tk.Button(repo_frame, text=T[self.lang]["refresh_repos"], bg=self.theme["accent"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=10, pady=4, command=self.list_repos).grid(row=0, column=3, padx=8, pady=5)

        tk.Label(repo_frame, text=T[self.lang]["repo_name"], bg=self.theme["panel"], fg=self.theme["fg"]).grid(row=1, column=0, padx=8, pady=5, sticky=tk.W)
        tk.Entry(repo_frame, textvariable=self.repo_name, bg=self.theme["input"], fg=self.theme["fg"],
                 font=("Consolas", 10), bd=1, relief=tk.SOLID, width=30).grid(row=1, column=1, padx=8, pady=5, sticky=tk.W)
        tk.Label(repo_frame, text=T[self.lang]["repo_desc"], bg=self.theme["panel"], fg=self.theme["fg"]).grid(row=2, column=0, padx=8, pady=5, sticky=tk.W)
        tk.Entry(repo_frame, textvariable=self.repo_desc, bg=self.theme["input"], fg=self.theme["fg"],
                 font=("Consolas", 10), bd=1, relief=tk.SOLID, width=40).grid(row=2, column=1, columnspan=2, padx=8, pady=5, sticky=tk.W)
        tk.Button(repo_frame, text=T[self.lang]["create_btn"], bg=self.theme["primary"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=10, pady=4, command=self.create_repo).grid(row=2, column=3, padx=8, pady=5)

        # ---- Local Repository Path ----
        path_frame = tk.LabelFrame(inner, text="📂 Local Repository", bg=self.theme["panel"],
                                   fg=self.theme["primary"], font=("Segoe UI", 10, "bold"), bd=1, relief=tk.SOLID)
        path_frame.pack(fill=tk.X, padx=10, pady=8, ipady=5)
        tk.Label(path_frame, text=T[self.lang]["local_path"], bg=self.theme["panel"], fg=self.theme["fg"]).grid(row=0, column=0, padx=8, pady=5, sticky=tk.W)
        path_entry = tk.Entry(path_frame, textvariable=self.local_repo_path, bg=self.theme["input"], fg=self.theme["fg"],
                              font=("Consolas", 10), bd=1, relief=tk.SOLID, width=50)
        path_entry.grid(row=0, column=1, padx=8, pady=5, sticky=tk.W)
        add_context_menu(path_entry, self.lang)
        tk.Button(path_frame, text=T[self.lang]["browse_local"], bg=self.theme["info"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=10, pady=4, command=self.browse_local_repo).grid(row=0, column=2, padx=8, pady=5)
        tk.Button(path_frame, text=T[self.lang]["clone_btn"], bg=self.theme["warning"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=10, pady=4, command=self.clone_repo).grid(row=1, column=0, padx=8, pady=5)
        tk.Entry(path_frame, textvariable=self.clone_url, bg=self.theme["input"], fg=self.theme["fg"],
                 font=("Consolas", 10), bd=1, relief=tk.SOLID, width=40).grid(row=1, column=1, padx=8, pady=5, sticky=tk.W)
        add_context_menu(path_frame.winfo_children()[-1], self.lang)

        # ---- Git Operations ----
        git_ops_frame = tk.LabelFrame(inner, text="⚡ Git Operations", bg=self.theme["panel"],
                                      fg=self.theme["primary"], font=("Segoe UI", 10, "bold"), bd=1, relief=tk.SOLID)
        git_ops_frame.pack(fill=tk.X, padx=10, pady=8, ipady=5)

        tk.Label(git_ops_frame, text=T[self.lang]["commit_msg"], bg=self.theme["panel"], fg=self.theme["fg"]).grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        commit_entry = tk.Entry(git_ops_frame, textvariable=self.commit_msg, bg=self.theme["input"], fg=self.theme["fg"],
                                font=("Consolas", 10), bd=1, relief=tk.SOLID, width=30)
        commit_entry.grid(row=0, column=1, padx=5, pady=3, sticky=tk.W)
        add_context_menu(commit_entry, self.lang)
        tk.Button(git_ops_frame, text=T[self.lang]["commit_btn"], bg=self.theme["success"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=8, pady=3, command=self.git_commit).grid(row=0, column=2, padx=5, pady=3)
        tk.Button(git_ops_frame, text=T[self.lang]["push_btn"], bg=self.theme["primary"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=8, pady=3, command=self.git_push).grid(row=0, column=3, padx=5, pady=3)
        tk.Button(git_ops_frame, text=T[self.lang]["pull_btn"], bg=self.theme["info"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=8, pady=3, command=self.git_pull).grid(row=0, column=4, padx=5, pady=3)

        # ---- File Operations ----
        file_frame = tk.LabelFrame(inner, text=T[self.lang]["file_ops"], bg=self.theme["panel"],
                                   fg=self.theme["primary"], font=("Segoe UI", 10, "bold"), bd=1, relief=tk.SOLID)
        file_frame.pack(fill=tk.X, padx=10, pady=8, ipady=5)

        # New File
        tk.Label(file_frame, text=T[self.lang]["new_file"], bg=self.theme["panel"], fg=self.theme["fg"]).grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        tk.Entry(file_frame, textvariable=self.new_file_name, bg=self.theme["input"], fg=self.theme["fg"],
                 font=("Consolas", 10), bd=1, relief=tk.SOLID, width=20).grid(row=0, column=1, padx=5, pady=3)
        tk.Entry(file_frame, textvariable=self.new_file_content, bg=self.theme["input"], fg=self.theme["fg"],
                 font=("Consolas", 10), bd=1, relief=tk.SOLID, width=30).grid(row=0, column=2, padx=5, pady=3)
        tk.Button(file_frame, text=T[self.lang]["create_file_btn"], bg=self.theme["success"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=8, pady=3, command=self.new_file).grid(row=0, column=3, padx=5, pady=3)

        # Delete File
        tk.Label(file_frame, text=T[self.lang]["delete_file"], bg=self.theme["panel"], fg=self.theme["fg"]).grid(row=1, column=0, padx=5, pady=3, sticky=tk.W)
        tk.Entry(file_frame, textvariable=self.delete_file_name, bg=self.theme["input"], fg=self.theme["fg"],
                 font=("Consolas", 10), bd=1, relief=tk.SOLID, width=30).grid(row=1, column=1, columnspan=2, padx=5, pady=3, sticky=tk.W)
        tk.Button(file_frame, text=T[self.lang]["delete_btn"], bg=self.theme["danger"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=8, pady=3, command=self.delete_file).grid(row=1, column=3, padx=5, pady=3)

        # Rename File
        tk.Label(file_frame, text=T[self.lang]["rename_file"], bg=self.theme["panel"], fg=self.theme["fg"]).grid(row=2, column=0, padx=5, pady=3, sticky=tk.W)
        tk.Entry(file_frame, textvariable=self.rename_old_name, bg=self.theme["input"], fg=self.theme["fg"],
                 font=("Consolas", 10), bd=1, relief=tk.SOLID, width=15).grid(row=2, column=1, padx=5, pady=3)
        tk.Entry(file_frame, textvariable=self.rename_new_name, bg=self.theme["input"], fg=self.theme["fg"],
                 font=("Consolas", 10), bd=1, relief=tk.SOLID, width=15).grid(row=2, column=2, padx=5, pady=3)
        tk.Button(file_frame, text=T[self.lang]["rename_btn"], bg=self.theme["warning"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=8, pady=3, command=self.rename_file).grid(row=2, column=3, padx=5, pady=3)

        # ---- Custom Git Command ----
        adv_frame = tk.LabelFrame(inner, text=T[self.lang]["git_commands"], bg=self.theme["panel"],
                                  fg=self.theme["primary"], font=("Segoe UI", 10, "bold"), bd=1, relief=tk.SOLID)
        adv_frame.pack(fill=tk.X, padx=10, pady=8, ipady=5)
        tk.Label(adv_frame, text="Custom Command:", bg=self.theme["panel"], fg=self.theme["fg"]).grid(row=0, column=0, padx=8, pady=5, sticky=tk.W)
        cmd_entry = tk.Entry(adv_frame, textvariable=self.git_custom_command, bg=self.theme["input"], fg=self.theme["fg"],
                             font=("Consolas", 10), bd=1, relief=tk.SOLID, width=50)
        cmd_entry.grid(row=0, column=1, padx=8, pady=5, sticky=tk.W)
        add_context_menu(cmd_entry, self.lang)
        tk.Button(adv_frame, text=T[self.lang]["run_command"], bg=self.theme["primary"], fg=self.theme["bg"],
                  font=("Segoe UI", 9, "bold"), bd=0, padx=10, pady=4, command=self.run_custom_git_command).grid(row=0, column=2, padx=8, pady=5)

        # ---- Git Log ----
        log_frame = tk.LabelFrame(inner, text=T[self.lang]["git_log"], bg=self.theme["panel"],
                                  fg=self.theme["primary"], font=("Segoe UI", 10, "bold"), bd=1, relief=tk.SOLID)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8, ipady=5)
        self.git_log_text = scrolledtext.ScrolledText(log_frame, bg="#020617", fg=self.theme["info"],
                                                      font=("Consolas", 9), height=10, bd=0)
        self.git_log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        enable_mouse_scroll(self.git_log_text)
        add_context_menu(self.git_log_text, self.lang)

    # ------------------------------------------------------------------------
    # GITHUB METHODS (از V5)
    # ------------------------------------------------------------------------
    def github_login(self):
        token = self.github_token.get().strip()
        if not token:
            messagebox.showerror("Error", "Token is required.")
            return
        headers = {"Authorization": f"token {token}"}
        try:
            resp = requests.get("https://api.github.com/user", headers=headers)
            if resp.status_code == 200:
                user = resp.json()
                self.token_status_label.config(text=T[self.lang]["token_status"] + f" Logged in as {user['login']}", fg=self.theme["success"])
                self.save_config()
                self.git_log("Logged in to GitHub as " + user['login'])
                messagebox.showinfo("Success", f"Logged in as {user['login']}")
            else:
                self.token_status_label.config(text=T[self.lang]["token_status"] + " Login failed", fg=self.theme["danger"])
                messagebox.showerror("Error", f"Login failed: {resp.status_code}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def list_repos(self):
        token = self.github_token.get().strip()
        if not token:
            messagebox.showerror("Error", "Token required.")
            return
        headers = {"Authorization": f"token {token}"}
        try:
            resp = requests.get("https://api.github.com/user/repos", headers=headers)
            if resp.status_code == 200:
                repos = resp.json()
                self.repo_listbox.delete(0, tk.END)
                for r in repos:
                    self.repo_listbox.insert(tk.END, r["name"])
                self.git_log(f"Loaded {len(repos)} repositories")
            else:
                messagebox.showerror("Error", f"Failed: {resp.status_code}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_repo(self):
        token = self.github_token.get().strip()
        if not token:
            messagebox.showerror("Error", "Token required.")
            return
        name = self.repo_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Repo name is required.")
            return
        desc = self.repo_desc.get().strip()
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        data = {"name": name, "description": desc, "private": False}
        try:
            resp = requests.post("https://api.github.com/user/repos", headers=headers, json=data)
            if resp.status_code == 201:
                self.git_log(f"Repository '{name}' created.")
                messagebox.showinfo("Success", f"Repo '{name}' created.")
                self.list_repos()
            else:
                messagebox.showerror("Error", f"Failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def browse_local_repo(self):
        folder = filedialog.askdirectory()
        if folder:
            self.local_repo_path.set(folder)
            self.git_log(f"Local repo path set to {folder}")

    def clone_repo(self):
        url = self.clone_url.get().strip()
        path = self.local_repo_path.get().strip()
        if not url or not path:
            messagebox.showerror("Error", "Clone URL and local path are required.")
            return
        try:
            self.git_log(f"Cloning from {url} to {path}...")
            result = subprocess.run(["git", "clone", url, path], capture_output=True, text=True)
            if result.returncode == 0:
                self.git_log("Clone successful.")
                messagebox.showinfo("Success", "Clone completed.")
            else:
                self.git_log(f"Clone failed: {result.stderr}")
                messagebox.showerror("Error", result.stderr)
        except Exception as e:
            self.git_log(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))

    def run_git_command(self, args, cwd=None):
        if cwd is None:
            cwd = self.local_repo_path.get().strip()
            if not cwd:
                self.git_log("Error: Local repo path not set.")
                return None
        try:
            result = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
            if result.returncode == 0:
                self.git_log("> " + " ".join(args) + " -> OK")
                if result.stdout:
                    self.git_log(result.stdout.strip())
                return result.stdout
            else:
                self.git_log("> " + " ".join(args) + " -> ERROR")
                self.git_log(result.stderr.strip())
                return None
        except Exception as e:
            self.git_log(f"Exception: {str(e)}")
            return None

    def git_commit(self):
        msg = self.commit_msg.get().strip()
        if not msg:
            messagebox.showerror("Error", "Commit message required.")
            return
        self.run_git_command(["add", "."])
        res = self.run_git_command(["commit", "-m", msg])
        if res is not None:
            messagebox.showinfo("Commit", "Commit successful.")
        else:
            messagebox.showerror("Error", "Commit failed.")

    def git_push(self):
        res = self.run_git_command(["push", "-u", "origin", "main"])
        if res is None:
            res = self.run_git_command(["push", "-u", "origin", "master"])
        if res is not None:
            messagebox.showinfo("Push", "Push successful.")
        else:
            messagebox.showerror("Error", "Push failed.")

    def git_pull(self):
        res = self.run_git_command(["pull"])
        if res is not None:
            messagebox.showinfo("Pull", "Pull successful.")
        else:
            messagebox.showerror("Error", "Pull failed.")

    def new_file(self):
        name = self.new_file_name.get().strip()
        content = self.new_file_content.get().strip()
        path = self.local_repo_path.get().strip()
        if not path:
            messagebox.showerror("Error", "Local repo path not set.")
            return
        if not name:
            messagebox.showerror("Error", "File name required.")
            return
        full = os.path.join(path, name)
        try:
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, 'w', encoding='utf-8') as f:
                f.write(content)
            self.git_log(f"File created: {full}")
            messagebox.showinfo("Success", f"File '{name}' created.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_file(self):
        name = self.delete_file_name.get().strip()
        path = self.local_repo_path.get().strip()
        if not path or not name:
            messagebox.showerror("Error", "Path and file name required.")
            return
        full = os.path.join(path, name)
        if not os.path.exists(full):
            messagebox.showerror("Error", "File does not exist.")
            return
        if messagebox.askyesno("Delete", f"Delete '{full}'?"):
            try:
                os.remove(full)
                self.git_log(f"File deleted: {full}")
                messagebox.showinfo("Success", "File deleted.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def rename_file(self):
        old = self.rename_old_name.get().strip()
        new = self.rename_new_name.get().strip()
        path = self.local_repo_path.get().strip()
        if not path or not old or not new:
            messagebox.showerror("Error", "Path and names required.")
            return
        old_full = os.path.join(path, old)
        new_full = os.path.join(path, new)
        if not os.path.exists(old_full):
            messagebox.showerror("Error", "Old file does not exist.")
            return
        try:
            os.rename(old_full, new_full)
            self.git_log(f"Renamed: {old} -> {new}")
            messagebox.showinfo("Success", f"Renamed to '{new}'.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_custom_git_command(self):
        cmd = self.git_custom_command.get().strip()
        if not cmd:
            messagebox.showerror("Error", "Command cannot be empty.")
            return
        self.run_git_command(cmd.split())

    def git_log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.git_log_text.insert(tk.END, f"[{ts}] {msg}\n")
        self.git_log_text.see(tk.END)
        self.root.update_idletasks()

    # =========================================================================
    # HELP, EXPORT, SETTINGS, STATUS, LOG (بدون تغییر)
    # =========================================================================
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

    def change_lang(self, e=None):
        val = self.lang_cb.get()
        self.lang = "en" if val == "English" else "fa"
        self.save_config()
        self.refresh_ui()

    def update_status_lang(self):
        if hasattr(self, 'status_bar'):
            self.status_bar.config(text=T[self.lang]["ready"])

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

    def save_config_and_notify(self):
        self.save_config()
        messagebox.showinfo("Saved", "Settings saved.")
        self.log("Settings saved")

    # =========================================================================
    # CREDIT FOOTER (قابل کلیک)
    # =========================================================================
    def create_credit_footer(self):
        credit_frame = tk.Frame(self.root, bg=self.theme["panel"])
        credit_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=2)
        inner = tk.Frame(credit_frame, bg=self.theme["panel"])
        inner.pack(anchor="center")
        lbl = tk.Label(inner, text="Developed by", bg=self.theme["panel"],
                       fg=self.theme["fg"], font=("Segoe UI", 9, "italic"))
        lbl.pack(side=tk.LEFT, padx=(0, 5))
        link = tk.Label(inner, text="MA.GH.AD", bg=self.theme["panel"],
                        fg=self.theme["primary"], font=("Segoe UI", 9, "bold"),
                        cursor="hand2")
        link.pack(side=tk.LEFT)
        link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/mahanneman"))

# ============================================================================
# 0021 - RUN
# ============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AFAR(root)
    root.mainloop()