import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import random

class BurgerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tundag Burger")
        self.root.geometry("800x600")
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack(fill="both", expand=True)
        self.obj_size = 220
        self.name_text = "Danilo Tundag Jr."
        self.bg_color = (30, 30, 30, 180)
        self.obj_x, self.obj_y = 100, 100
        self.obj_dx, self.obj_dy = 5, 4
        self.paused = False
        self.base_img = self.load_burger_image()
        self.img = None
        self.img_id = None
        self.create_widgets()
        self.root.bind('<KeyPress-space>', self.toggle_pause)
        self.animate()

    def load_burger_image(self):
        try:
            img = Image.open("./burger.png").resize((self.obj_size, self.obj_size), Image.Resampling.LANCZOS).convert('RGBA')
        except Exception:
            img = Image.new('RGBA', (self.obj_size, self.obj_size), (200, 200, 200, 255))
        return img

    def draw_burger_with_name(self, bg_color):
        img = self.base_img.copy()
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        # Calculate text size
        try:
            bbox = draw.textbbox((0, 0), self.name_text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except AttributeError:
            text_w, text_h = font.getsize(self.name_text)
        # Centered rectangle and text
        rect_w, rect_h = text_w + 24, text_h + 12
        rect_x = (self.obj_size - rect_w) // 2
        rect_y = (self.obj_size - rect_h) // 2
        draw.rectangle([rect_x, rect_y, rect_x + rect_w, rect_y + rect_h], fill=bg_color)
        draw.text((rect_x + 12, rect_y + 6), self.name_text, fill='white', font=font)
        return img

    def random_overlay_color(self):
        return tuple(random.choices(range(60, 256), k=3) + [180])

    def create_widgets(self):
        pil_img = self.draw_burger_with_name(self.bg_color)
        self.img = ImageTk.PhotoImage(pil_img)
        self.img_id = self.canvas.create_image(self.obj_x, self.obj_y, image=self.img, anchor='nw')

    def animate(self):
        if self.paused:
            return
        self.obj_x += self.obj_dx
        self.obj_y += self.obj_dy
        collision = False
        if self.obj_x <= 0 or self.obj_x + self.obj_size >= 800:
            self.obj_dx = -self.obj_dx
            collision = True
        if self.obj_y <= 0 or self.obj_y + self.obj_size >= 600:
            self.obj_dy = -self.obj_dy
            collision = True
        if collision:
            self.bg_color = self.random_overlay_color()
            pil_img = self.draw_burger_with_name(self.bg_color)
            self.img = ImageTk.PhotoImage(pil_img)
            self.canvas.itemconfig(self.img_id, image=self.img)
        self.canvas.coords(self.img_id, self.obj_x, self.obj_y)
        self.root.after(16, self.animate)

    def toggle_pause(self, event=None):
        self.paused = not self.paused
        if not self.paused:
            self.animate()

if __name__ == "__main__":
    root = tk.Tk()
    app = BurgerApp(root)
    root.mainloop()
