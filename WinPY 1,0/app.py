import tkinter as tk
from tkinter import colorchooser

ACCENT = "#3b82f6"
HOVER = "#dbeafe"
BTN_BG = "#f3f4f6"
DARK = "#111827"

class WinPYApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WinPY")
        self.geometry("1100x650")
        self.wallpaper = "#e5efff"
        self.configure(bg=self.wallpaper)

        self.virtual_desktop = []
        self.desktop_icons = []

        self.create_taskbar()
        self.refresh_desktop()

        self.bind("<Button-3>", self.desktop_right_click)

    def create_app_window(self, title, size="700x450"):
        win = tk.Toplevel(self)
        win.overrideredirect(True)
        win.geometry(size)
        win.configure(bg="#c7cdd8")
        outer = tk.Frame(win, bg="#c7cdd8")
        outer.pack(fill="both", expand=True, padx=2, pady=2)
        frame = tk.Frame(outer, bg="white")
        frame.pack(fill="both", expand=True)
        titlebar = tk.Frame(frame, bg=BTN_BG, height=32)
        titlebar.pack(fill="x")
        tk.Label(titlebar, text=title, bg=BTN_BG,
                 font=("Segoe UI", 10)).pack(side="left", padx=10)
        close = tk.Label(titlebar, text="✕", bg=BTN_BG)
        close.pack(side="right", padx=10)
        close.bind("<Button-1>", lambda e: win.destroy())
        close.bind("<Enter>", lambda e: close.config(bg="#fee2e2"))
        close.bind("<Leave>", lambda e: close.config(bg=BTN_BG))
        def start(e): win.x, win.y = e.x, e.y
        def drag(e): win.geometry(f"+{e.x_root-win.x}+{e.y_root-win.y}")
        titlebar.bind("<Button-1>", start)
        titlebar.bind("<B1-Motion>", drag)
        content = tk.Frame(frame, bg="white")
        content.pack(fill="both", expand=True)
        return content

    def create_taskbar(self):
        bar = tk.Frame(self, bg=DARK, height=44)
        bar.pack(side="bottom", fill="x")
        start = tk.Label(bar, text="⊞", fg="white",
                         bg=DARK, font=("Segoe UI", 14))
        start.place(relx=0.5, rely=0.5, anchor="center")
        start.bind("<Enter>", lambda e: start.config(bg="#1f2937"))
        start.bind("<Leave>", lambda e: start.config(bg=DARK))
        start.bind("<Button-1>", lambda e: self.open_start_menu())

    def open_start_menu(self):
        menu = tk.Toplevel(self)
        menu.overrideredirect(True)
        w, h = 420, 520
        x = (self.winfo_screenwidth() - w) // 2
        y = self.winfo_screenheight() - h - 60
        menu.geometry(f"{w}x{h}+{x}+{y}")
        menu.configure(bg="#e5e7eb")
        panel = tk.Frame(menu, bg="white")
        panel.pack(fill="both", expand=True, padx=10, pady=10)
        apps = [("📁 WinPY Explorer", self.open_explorer),
                ("⚙️ Settings", self.open_settings),
                ("🐍 Python Shell", self.open_shell)]
        for text, cmd in apps:
            btn = tk.Label(panel, text=text, bg=BTN_BG,
                           anchor="w", padx=12, height=2)
            btn.pack(fill="x", pady=4)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BTN_BG))
            btn.bind("<Button-1>", lambda e, c=cmd: c())

    def desktop_right_click(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="📁 New Folder", command=self.create_virtual_folder)
        menu.add_command(label="🔃 Sort", command=self.sort_desktop)
        menu.add_separator()
        menu.add_command(label="⚙️ Settings", command=self.open_settings)
        menu.tk_popup(event.x_root, event.y_root)

    def create_virtual_folder(self):
        base = "New Folder"
        names = [i["name"] for i in self.virtual_desktop]
        name = base
        n = 1
        while name in names:
            name = f"{base} ({n})"
            n += 1
        self.virtual_desktop.append({"type": "folder", "name": name})
        self.refresh_desktop()

    def refresh_desktop(self):
        for icon in getattr(self, "desktop_icons", []):
            icon.destroy()
        self.desktop_icons = []
        y = 60
        for item in self.virtual_desktop:
            icon = tk.Label(self, text=f"📁\n{item['name']}",
                            bg=self.wallpaper, width=10, height=4,
                            font=("Segoe UI", 9), justify="center")
            icon.place(x=50, y=y)
            icon.bind("<Enter>", lambda e, b=icon: b.config(bg=HOVER))
            icon.bind("<Leave>", lambda e, b=icon: b.config(bg=self.wallpaper))
            self.desktop_icons.append(icon)
            y += 100

    def sort_desktop(self):
        self.virtual_desktop.sort(key=lambda x: x["name"].lower())
        self.refresh_desktop()

    def open_explorer(self, folder=None):
        c = self.create_app_window("WinPY Explorer")
        sidebar = tk.Frame(c, bg="#f1f5f9", width=180)
        sidebar.pack(side="left", fill="y")
        main = tk.Frame(c, bg="white")
        main.pack(side="right", fill="both", expand=True)
        tk.Label(sidebar, text="Quick Access", bg="#f1f5f9", font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=10)
        tk.Label(sidebar, text="Desktop", bg="#f1f5f9").pack(anchor="w", padx=20)
        path = tk.Label(main, text="Desktop", bg="white", fg="gray")
        path.pack(anchor="w", padx=10, pady=6)
        files = tk.Frame(main, bg="white")
        files.pack(fill="both", expand=True, padx=10)
        for item in self.virtual_desktop:
            tile = tk.Label(files, text=f"📁 {item['name']}", bg=BTN_BG, anchor="w", padx=10, height=2)
            tile.pack(fill="x", pady=4)
            tile.bind("<Enter>", lambda e, t=tile: t.config(bg=HOVER))
            tile.bind("<Leave>", lambda e, t=tile: t.config(bg=BTN_BG))

    def open_settings(self):
        c = self.create_app_window("Settings")
        sidebar = tk.Frame(c, bg="#f1f5f9", width=200)
        sidebar.pack(side="left", fill="y")
        content = tk.Frame(c, bg="white")
        content.pack(side="right", fill="both", expand=True)
        def clear():
            for w in content.winfo_children(): w.destroy()
        def personalisation():
            clear()
            tk.Label(content, text="Personalisation", font=("Segoe UI", 14)).pack(pady=10)
            def pick():
                col = colorchooser.askcolor()[1]
                if col:
                    self.wallpaper = col
                    self.configure(bg=col)
                    self.refresh_desktop()
            tk.Button(content, text="Change Wallpaper Color", command=pick).pack(pady=10)
        def system():
            clear()
            tk.Label(content, text="System", font=("Segoe UI", 14)).pack(pady=10)
            tk.Label(content, text="WinPY OS\nSandboxed Python Desktop").pack(pady=5)
        def about():
            clear()
            tk.Label(content, text="About", font=("Segoe UI", 14)).pack(pady=10)
            tk.Label(content, text="WinPY\nVersion 1.1\nBuilt with Python + Tkinter").pack(pady=5)
        for name, cmd in [("🎨 Personalisation", personalisation), ("🖥 System", system), ("ℹ️ About", about)]:
            btn = tk.Label(sidebar, text=name, bg="#f1f5f9", anchor="w", padx=12, height=2)
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#f1f5f9"))
            btn.bind("<Button-1>", lambda e, c=cmd: c())
        personalisation()
    def open_shell(self):
        c = self.create_app_window("Python Shell")
        entry = tk.Entry(c)
        entry.pack(fill="x", padx=10, pady=5)
        out = tk.Text(c, height=10)
        out.pack(fill="both", expand=True, padx=10)
        def run():
            try:
                exec(entry.get(), {}, {"winpy": self})
                out.insert("end", "✔ Executed\n")
            except Exception as e:
                out.insert("end", f"Error: {e}\n")
        tk.Button(c, text="Run", command=run).pack(pady=5)

if __name__ == "__main__":
    WinPYApp().mainloop()
