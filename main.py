import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
import os, json, tempfile, keyboard, pythoncom

CONFIG_FILE = os.path.join(tempfile.gettempdir(), "crosshair_config.json")

DEFAULT_CONFIG = {
    "size": 60,
    "color": "#00FF00",
    "thickness": 3,
    "gap": 6,
    "shape": "plus",
    "custom_png": None
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_config(data):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("Config kaydedilemedi:", e)


# -------------------------
# Crosshair Overlay
# -------------------------
class CrosshairOverlay:
    def __init__(self, config):
        self.config = config
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        w = h = self.config["size"] * 3
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x, y = (sw - w)//2, (sh - h)//2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.transparent_color = "#010101"
        self.root.config(bg=self.transparent_color)
        self.root.wm_attributes("-transparentcolor", self.transparent_color)
        self.canvas = tk.Canvas(self.root, width=w, height=h, highlightthickness=0, bg=self.transparent_color)
        self.canvas.pack(fill="both", expand=True)
        self.cx, self.cy = w//2, h//2
        self.draw_crosshair()

    def draw_crosshair(self):
        self.canvas.delete("all")
        shape = self.config["shape"]
        if shape == "plus":
            self.draw_plus()
        elif shape == "x":
            self.draw_x()
        elif shape == "circle":
            self.draw_circle()
        elif shape == "dot":
            self.draw_dot()
        elif shape == "png" and self.config["custom_png"]:
            self.draw_png()

    def draw_plus(self):
        s, g, t, c = self.config["size"], self.config["gap"], self.config["thickness"], self.config["color"]
        cx, cy = self.cx, self.cy
        self.canvas.create_line(cx-g-s, cy, cx-g, cy, fill=c, width=t)
        self.canvas.create_line(cx+g, cy, cx+g+s, cy, fill=c, width=t)
        self.canvas.create_line(cx, cy-g-s, cx, cy-g, fill=c, width=t)
        self.canvas.create_line(cx, cy+g, cx, cy+g+s, fill=c, width=t)

    def draw_x(self):
        s, t, c = self.config["size"], self.config["thickness"], self.config["color"]
        self.canvas.create_line(self.cx-s, self.cy-s, self.cx+s, self.cy+s, fill=c, width=t)
        self.canvas.create_line(self.cx+s, self.cy-s, self.cx-s, self.cy+s, fill=c, width=t)

    def draw_circle(self):
        r, t, c = self.config["size"]//2, self.config["thickness"], self.config["color"]
        self.canvas.create_oval(self.cx-r, self.cy-r, self.cx+r, self.cy+r, outline=c, width=t)

    def draw_dot(self):
        r, c = max(2, self.config["size"]//10), self.config["color"]
        self.canvas.create_oval(self.cx-r, self.cy-r, self.cx+r, self.cy+r, fill=c, outline=c)

    def draw_png(self):
        try:
            from PIL import Image, ImageTk
            img = Image.open(self.config["custom_png"]).convert("RGBA")
            scale = self.config["size"]/max(img.size)
            new_size = (int(img.size[0]*scale), int(img.size[1]*scale))
            img = img.resize(new_size, Image.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(self.cx, self.cy, image=self.tk_img)
        except Exception as e:
            print("PNG yüklenemedi:", e)


# -------------------------
# Settings Window (TTK Dark)
# -------------------------
class SettingsWindow:
    def __init__(self, overlay, config):
        self.overlay = overlay
        self.config = config
        self.root = tk.Toplevel()
        self.root.title("Crosshair Settings")
        self.setup_style()
        self.add_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.save_and_close)

    def setup_style(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TLabel", background="#2E2E2E", foreground="white")
        style.configure("TButton", background="#444", foreground="white", padding=5)
        style.map("TButton",
                  background=[("active","#555")],
                  foreground=[("active","white")])
        style.configure("TCombobox", fieldbackground="#444", background="#333", foreground="white")
        style.configure("TScale", background="#2E2E2E")
        self.root.configure(bg="#2E2E2E")

    def add_widgets(self):
        ttk.Label(self.root, text="Shape:").grid(row=0, column=0, padx=5, pady=5)
        self.shape_var = tk.StringVar(value=self.config["shape"])
        shape_box = ttk.Combobox(self.root, textvariable=self.shape_var, values=["plus","x","circle","dot","png"], state="readonly")
        shape_box.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Size:").grid(row=1, column=0, padx=5, pady=5)
        self.size_var = tk.IntVar(value=self.config["size"])
        ttk.Scale(self.root, from_=10, to=200, variable=self.size_var, orient="horizontal").grid(row=1,column=1,padx=5,pady=5)

        ttk.Label(self.root, text="Gap:").grid(row=2, column=0, padx=5, pady=5)
        self.gap_var = tk.IntVar(value=self.config["gap"])
        ttk.Scale(self.root, from_=0, to=50, variable=self.gap_var, orient="horizontal").grid(row=2,column=1,padx=5,pady=5)

        ttk.Label(self.root, text="Thickness:").grid(row=3, column=0, padx=5, pady=5)
        self.thickness_var = tk.IntVar(value=self.config["thickness"])
        ttk.Scale(self.root, from_=1, to=10, variable=self.thickness_var, orient="horizontal").grid(row=3,column=1,padx=5,pady=5)

        ttk.Button(self.root, text="Pick Color", command=self.pick_color).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(self.root, text="Pick PNG", command=self.pick_png).grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(self.root, text="Apply", command=self.apply).grid(row=5,column=0,padx=5,pady=10)
        ttk.Button(self.root, text="Save", command=self.save).grid(row=5,column=1,padx=5,pady=10)

    def pick_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.config["color"] = color
            self.overlay.draw_crosshair()

    def pick_png(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Files","*.png")])
        if path:
            self.config["custom_png"] = path
            self.shape_var.set("png")
            self.apply()

    def apply(self):
        self.config["shape"] = self.shape_var.get()
        self.config["size"] = self.size_var.get()
        self.config["gap"] = self.gap_var.get()
        self.config["thickness"] = self.thickness_var.get()
        self.overlay.config = self.config
        self.overlay.draw_crosshair()

    def save(self):
        save_config(self.config)
        messagebox.showinfo("Saved","Settings saved successfully!")

    def save_and_close(self):
        self.save()
        self.root.destroy()


# -------------------------
# Hotkeys
# -------------------------
def setup_hotkeys(overlay, config):
    def toggle_visibility():
        if overlay.root.state() == "withdrawn":
            overlay.root.deiconify()
        else:
            overlay.root.withdraw()
    def reset_config():
        config.update(DEFAULT_CONFIG.copy())
        save_config(config)
        overlay.config = config
        overlay.draw_crosshair()
    keyboard.add_hotkey("F8", toggle_visibility)
    keyboard.add_hotkey("F9", reset_config)


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    # Ana tk penceresini gizle
    main_root = tk.Tk()
    main_root.withdraw()

    cfg = load_config()
    overlay = CrosshairOverlay(cfg)
    setup_hotkeys(overlay, cfg)

    # Ayarlar penceresi isteğe bağlı açılacak
    SettingsWindow(overlay, cfg)

    main_root.mainloop()
