from __future__ import annotations

import tkinter as tk
from tkinter import ttk

# Approved SATURN visual palette (derived from the accepted mockups).
BLUE = "#0A7BC1"
BLUE_DARK = "#143F74"
BLUE_DEEP = "#17364D"
BLUE_LIGHT = "#EAF4FB"
BLUE_MID = "#D9EAF6"
WHITE = "#FFFFFF"
BG = "#F7FAFC"
PANEL = "#FFFFFF"
BORDER = "#D4E0EA"
TEXT = "#173A5E"
MUTED = "#6C8298"
GREEN = "#078A48"
GREEN_LIGHT = "#EEF9F3"
ORANGE = "#E88A19"
RED = "#D64545"
TERMINAL = "#101B25"
TERMINAL_BAR = "#142432"
TERMINAL_TEXT = "#E6EDF3"
TERMINAL_MUTED = "#AAB7C4"


def configure_styles(root: tk.Misc) -> ttk.Style:
    style = ttk.Style(root)
    # clam behaves consistently on Windows/Linux and allows complete color control.
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("TFrame", background=BG)
    style.configure("Panel.TFrame", background=PANEL, relief="solid", borderwidth=1, bordercolor=BORDER)
    style.configure("Header.TFrame", background=WHITE)
    style.configure("Topbar.TFrame", background="#ECF3F7")
    style.configure("Sidebar.TFrame", background=BLUE_DEEP)
    style.configure("Status.TFrame", background=WHITE)

    style.configure("TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 10))
    style.configure("Panel.TLabel", background=PANEL, foreground=TEXT, font=("Segoe UI", 10))
    style.configure("Muted.Panel.TLabel", background=PANEL, foreground=MUTED, font=("Segoe UI", 9))
    style.configure("Title.TLabel", background=BG, foreground=BLUE_DARK, font=("Segoe UI", 20, "bold"))
    style.configure("Section.Panel.TLabel", background=PANEL, foreground=BLUE_DARK, font=("Segoe UI", 10, "bold"))
    style.configure("Brand.TLabel", background=WHITE, foreground=BLUE_DARK, font=("Segoe UI", 18, "bold"))
    style.configure("BrandSub.TLabel", background=WHITE, foreground=BLUE_DARK, font=("Segoe UI", 9, "bold"))
    style.configure("SidebarBrand.TLabel", background=BLUE_DEEP, foreground=WHITE, font=("Segoe UI", 17, "bold"))
    style.configure("SidebarMuted.TLabel", background=BLUE_DEEP, foreground="#9EC7E0", font=("Segoe UI", 8, "bold"))

    style.configure(
        "Sidebar.TButton",
        background=BLUE_DEEP,
        foreground="#D5E3EE",
        font=("Segoe UI", 10),
        anchor="w",
        padding=(16, 12),
        borderwidth=0,
    )
    style.map("Sidebar.TButton", background=[("active", "#21475F")], foreground=[("active", WHITE)])
    style.configure(
        "SidebarActive.TButton",
        background=BLUE,
        foreground=WHITE,
        font=("Segoe UI", 10, "bold"),
        anchor="w",
        padding=(16, 12),
        borderwidth=0,
    )
    style.map("SidebarActive.TButton", background=[("active", "#096EAF")])

    style.configure("Toolbar.TButton", background=WHITE, foreground=BLUE_DARK, font=("Segoe UI", 9, "bold"), padding=(11, 7), bordercolor=BORDER)
    style.map("Toolbar.TButton", background=[("active", BLUE_LIGHT)])
    style.configure("Primary.TButton", background=BLUE, foreground=WHITE, font=("Segoe UI", 10, "bold"), padding=(15, 8), bordercolor=BLUE)
    style.map("Primary.TButton", background=[("active", "#096EAF"), ("disabled", "#A7BED7")])
    style.configure("Danger.TButton", background="#FFF5F5", foreground=RED, font=("Segoe UI", 9, "bold"), padding=(12, 8), bordercolor="#FFB8BC")

    style.configure("TEntry", fieldbackground=WHITE, foreground=TEXT, bordercolor="#C8D7E3", lightcolor="#C8D7E3", darkcolor="#C8D7E3", padding=5)
    style.configure("TCombobox", fieldbackground=WHITE, foreground=TEXT, bordercolor="#C8D7E3", arrowsize=14, padding=4)
    style.configure("Treeview", background=WHITE, fieldbackground=WHITE, foreground=TEXT, rowheight=26, bordercolor=BORDER, font=("Segoe UI", 9))
    style.configure("Treeview.Heading", background="#F2F6F9", foreground="#254E74", font=("Segoe UI", 9, "bold"), relief="flat")
    style.map("Treeview", background=[("selected", "#DFF0FC")], foreground=[("selected", BLUE_DARK)])
    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab", padding=(14, 7), background="#EDF2F7", foreground=TEXT, font=("Segoe UI", 9, "bold"))
    style.map("TNotebook.Tab", background=[("selected", BLUE)], foreground=[("selected", WHITE)])
    style.configure("Horizontal.TProgressbar", background=BLUE, troughcolor="#D7E4ED", bordercolor="#D7E4ED", lightcolor=BLUE, darkcolor=BLUE)
    return style
