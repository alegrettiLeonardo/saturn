from __future__ import annotations

import tkinter as tk
from tkinter import ttk

# Palette sampled from the approved SATURN mock-ups.
NAVY = "#15364E"
NAVY_DARK = "#0D2C43"
NAVY_DEEP = "#08253A"
BLUE = "#0A83D8"
BLUE_DARK = "#075EA8"
BLUE_STRONG = "#006FC6"
BLUE_LIGHT = "#EAF5FD"
BLUE_PALE = "#F3F8FC"
TOPBAR = "#EDF4F8"
WHITE = "#FFFFFF"
BG = "#FAFCFE"
PANEL = "#FFFFFF"
BORDER = "#D7E3EC"
BORDER_DARK = "#C7D5E0"
TEXT = "#123E69"
TEXT_DARK = "#183B5A"
MUTED = "#627D95"
GREEN = "#18A56D"
GREEN_DARK = "#0C7F51"
GREEN_LIGHT = "#E9F8F2"
RED = "#DF3131"
RED_LIGHT = "#FFF0F0"
ORANGE = "#D98917"
AMBER = "#E3A21A"
TERMINAL = "#111B25"
TERMINAL_BAR = "#172633"
TERMINAL_TEXT = "#E7EEF5"
TERMINAL_MUTED = "#9FB2C3"
GRID = "#D9E4EC"

# Backwards-compatible aliases used by small helper modules/tests.
BLUE_MID = "#D8ECF9"

FONT_UI = "Segoe UI"
FONT_MONO = "Consolas"


def configure_styles(root: tk.Misc) -> ttk.Style:
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("TFrame", background=BG)
    style.configure("Content.TFrame", background=BG)
    style.configure("Header.TFrame", background=WHITE)
    style.configure("Topbar.TFrame", background=TOPBAR)
    style.configure("Sidebar.TFrame", background=NAVY)
    style.configure("Panel.TFrame", background=PANEL, relief="solid", borderwidth=1, bordercolor=BORDER)
    style.configure("FlatPanel.TFrame", background=PANEL)
    style.configure("Status.TFrame", background=WHITE)

    style.configure("TLabel", background=BG, foreground=TEXT_DARK, font=(FONT_UI, 10))
    style.configure("Panel.TLabel", background=PANEL, foreground=TEXT_DARK, font=(FONT_UI, 9))
    style.configure("Muted.Panel.TLabel", background=PANEL, foreground=MUTED, font=(FONT_UI, 8))
    style.configure("Title.TLabel", background=BG, foreground=TEXT, font=(FONT_UI, 20, "bold"))
    style.configure("Subtitle.TLabel", background=BG, foreground=TEXT, font=(FONT_UI, 10))
    style.configure("Section.Panel.TLabel", background=PANEL, foreground=TEXT, font=(FONT_UI, 10, "bold"))
    style.configure("CardTitle.TLabel", background=PANEL, foreground=TEXT, font=(FONT_UI, 8))
    style.configure("CardValue.TLabel", background=PANEL, foreground=TEXT, font=(FONT_UI, 17, "bold"))
    style.configure("Brand.TLabel", background=WHITE, foreground=TEXT, font=(FONT_UI, 18, "bold"))
    style.configure("BrandSub.TLabel", background=WHITE, foreground=TEXT_DARK, font=(FONT_UI, 9))

    style.configure("Sidebar.TButton", background=NAVY, foreground="#D4E8F7", font=(FONT_UI, 10), anchor="w", padding=(18, 12), borderwidth=0, relief="flat")
    style.map("Sidebar.TButton", background=[("active", "#1B4765")], foreground=[("active", WHITE)])
    style.configure("SidebarActive.TButton", background=BLUE, foreground=WHITE, font=(FONT_UI, 10, "bold"), anchor="w", padding=(18, 12), borderwidth=0, relief="flat")
    style.map("SidebarActive.TButton", background=[("active", BLUE_STRONG)], foreground=[("active", WHITE)])

    style.configure("Toolbar.TButton", background=WHITE, foreground=BLUE_DARK, font=(FONT_UI, 9), padding=(11, 7), borderwidth=1, bordercolor=BORDER, relief="solid")
    style.map("Toolbar.TButton", background=[("active", BLUE_LIGHT), ("disabled", "#F7F9FB")], foreground=[("disabled", "#98AABD")])
    style.configure("Ghost.TButton", background=TOPBAR, foreground=TEXT, font=(FONT_UI, 9), padding=(9, 6), borderwidth=0, relief="flat")
    style.map("Ghost.TButton", background=[("active", "#DFEBF3")])
    style.configure("Primary.TButton", background=BLUE_STRONG, foreground=WHITE, font=(FONT_UI, 9, "bold"), padding=(16, 9), borderwidth=1, bordercolor=BLUE_STRONG, relief="solid")
    style.map("Primary.TButton", background=[("active", BLUE_DARK), ("disabled", "#A7BED1")])
    style.configure("Danger.TButton", background=RED_LIGHT, foreground=RED, font=(FONT_UI, 9, "bold"), padding=(14, 8), borderwidth=1, bordercolor="#F0A9A9", relief="solid")
    style.map("Danger.TButton", background=[("active", "#FFE1E1")])

    style.configure("TEntry", fieldbackground=WHITE, foreground=TEXT_DARK, bordercolor=BORDER_DARK, lightcolor=BORDER_DARK, darkcolor=BORDER_DARK, padding=5, insertcolor=TEXT_DARK)
    style.configure("TCombobox", fieldbackground=WHITE, foreground=TEXT_DARK, background=WHITE, bordercolor=BORDER_DARK, arrowsize=13, padding=4)
    style.map("TCombobox", fieldbackground=[("readonly", WHITE)], foreground=[("readonly", TEXT_DARK)])
    style.configure("TCheckbutton", background=PANEL, foreground=TEXT_DARK, font=(FONT_UI, 8))
    style.map("TCheckbutton", background=[("active", PANEL)])
    style.configure("TRadiobutton", background=PANEL, foreground=TEXT_DARK, font=(FONT_UI, 8))
    style.map("TRadiobutton", background=[("active", PANEL)])

    style.configure("Treeview", background=WHITE, fieldbackground=WHITE, foreground=TEXT_DARK, rowheight=27, bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER, font=(FONT_UI, 8))
    style.configure("Treeview.Heading", background="#F4F8FB", foreground=TEXT, font=(FONT_UI, 8, "bold"), relief="flat", bordercolor=BORDER, padding=(5, 5))
    style.map("Treeview", background=[("selected", "#DCEFFC")], foreground=[("selected", TEXT)])

    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab", padding=(14, 7), background="#EFF5F8", foreground=TEXT_DARK, font=(FONT_UI, 8, "bold"))
    style.map("TNotebook.Tab", background=[("selected", WHITE)], foreground=[("selected", BLUE_DARK)])

    style.configure("Horizontal.TProgressbar", background=BLUE_STRONG, troughcolor="#D9E7F1", bordercolor="#D9E7F1", lightcolor=BLUE_STRONG, darkcolor=BLUE_STRONG, thickness=14)
    return style
