import time
import threading
import tkinter as tk
from tkinter import messagebox

import cv2
import numpy as np
from mss import mss
from PIL import Image, ImageTk, ImageGrab
import pytesseract
from googletrans import Translator

# Atur path ke executable Tesseract (sesuaikan dengan lokasi instalasi di komputer Anda)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

translator = Translator()

class ScreenTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Translator")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        
        self.region = None  # {"left":..., "top":..., "width":..., "height":...}
        
        self.text_var = tk.StringVar()
        self.label = tk.Label(root, textvariable=self.text_var, font=("Arial", 16),
                              bg="black", fg="white", justify="left")
        self.label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.btn_select = tk.Button(root, text="Pilih Area", command=self.select_area)
        self.btn_select.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.btn_start = tk.Button(root, text="Mulai Terjemahan", command=self.start_translation, state=tk.DISABLED)
        self.btn_start.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.running = False

    def select_area(self):
        self.root.withdraw()
        time.sleep(0.2)
        screenshot = ImageGrab.grab()
        self.full_img = screenshot.copy()
        
        self.sel_win = tk.Toplevel()
        self.sel_win.attributes("-fullscreen", True)
        self.sel_win.title("Pilih Area (Klik dan drag)")
        self.sel_win.bind("<Escape>", lambda e: self.cancel_selection())
        
        self.canvas = tk.Canvas(self.sel_win, width=screenshot.width, height=screenshot.height)
        self.canvas.pack()
        self.tk_img = ImageTk.PhotoImage(screenshot)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
        self.sel_win.mainloop()

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y,
                                                 self.start_x, self.start_y, outline='red', width=2)

    def on_move_press(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        left = int(min(self.start_x, end_x))
        top = int(min(self.start_y, end_y))
        width = int(abs(end_x - self.start_x))
        height = int(abs(end_y - self.start_y))
        self.region = {"left": left, "top": top, "width": width, "height": height}
        self.sel_win.destroy()
        self.root.deiconify()
        if width > 0 and height > 0:
            self.btn_start.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "Area tidak valid. Silakan coba lagi.")

    def cancel_selection(self):
        self.sel_win.destroy()
        self.root.deiconify()

    def start_translation(self):
        if not self.region:
            messagebox.showerror("Error", "Belum ada area yang dipilih!")
            return
        self.running = True
        threading.Thread(target=self.update_loop, daemon=True).start()

    def update_loop(self):
        sct = mss()
        custom_config = r'--oem 3 --psm 6'
        while self.running:
            try:
                # Capture screenshot dari area yang dipilih
                img = np.array(sct.grab(self.region))
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                # Jika teks kecil, scale up gambar (misalnya 2x)
                scale_factor = 2
                img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
                
                # Ubah ke grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Terapkan Gaussian blur untuk mengurangi noise
                blur = cv2.GaussianBlur(gray, (5, 5), 0)
                # Gunakan adaptive thresholding (Gaussian) dengan Otsu sebagai acuan
                ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                # Lakukan operasi morfologi (dilasi) untuk mengisi celah pada karakter
                kernel = np.ones((3, 3), np.uint8)
                morph = cv2.dilate(thresh, kernel, iterations=1)
                
                # Ekstrak teks dengan pytesseract menggunakan konfigurasi khusus
                extracted_text = pytesseract.image_to_string(morph, lang='jpn', config=custom_config).strip()
                
                if extracted_text:
                    translation = translator.translate(extracted_text, src='ja', dest='id')
                    output = f"JP: {extracted_text}\nEN: {translation.text}"
                else:
                    output = "Tidak ada teks terdeteksi."
                    
                self.root.after(0, self.text_var.set, output)
            except Exception as e:
                self.root.after(0, self.text_var.set, f"Error: {e}")
            time.sleep(1)

    def stop(self):
        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x180+50+50")
    app = ScreenTranslatorApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.stop()
