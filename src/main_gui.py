import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from tkinter import PhotoImage
import os
from services.flow_trainer_gui import lanzar_creador_flujo

# -------- CONFIGURACIÓN --------
root = tk.Tk()
root.title("Bot Ejecutor Inteligente")
root.geometry("500x600")
root.resizable(False, False)

# Tema moderno oscuro
style = Style("darkly")
root.configure(bg=style.colors.bg)

# -------- ANIMACIÓN ENTRADA --------
def fade_in(widget, delay=10, alpha=0.0):
    if alpha < 1.0:
        alpha += 0.05
        widget.attributes("-alpha", alpha)
        root.after(delay, fade_in, widget, delay, alpha)

root.attributes("-alpha", 0.0)
fade_in(root)

# -------- CONTENEDOR PRINCIPAL --------
main_frame = tk.Frame(root, bg=style.colors.bg)
main_frame.pack(expand=True)

# -------- ICONO --------
icon_path = os.path.join(os.path.dirname(__file__), "icon_bot.png")
if os.path.exists(icon_path):
    bot_icon = PhotoImage(file=icon_path)
    icon_label = tk.Label(main_frame, image=bot_icon, bg=style.colors.bg)
    icon_label.pack(pady=(40, 10))
else:
    icon_label = tk.Label(main_frame, text="🤖", font=("Segoe UI Emoji", 40), bg=style.colors.bg)
    icon_label.pack(pady=(40, 10))

# -------- TÍTULO --------
title = tk.Label(main_frame, text="Bot Ejecutor Inteligente", font=("Helvetica", 18, "bold"), fg="white", bg=style.colors.bg)
title.pack(pady=(0, 30))

# -------- FUNCIÓN PLACEHOLDER --------
def placeholder(name):
    print(f"🔘 {name} clickeado")

# -------- BOTONES --------
botones = [
    ("+ Crear nuevo flujo", lanzar_creador_flujo),
    ("Instrucción por texto (GPT)", lambda: placeholder("GPT")),
    ("Ejecutar flujo existente", lambda: placeholder("Ejecutar flujo")),
    ("Configuración", lambda: placeholder("Configuración"))
]

for texto, comando in botones:
    tk.Button(
        main_frame,
        text=texto,
        font=("Helvetica", 12),
        width=30,
        height=2,
        bg="#246bfd",
        fg="white",
        bd=0,
        relief="flat",
        activebackground="#1e56c6",
        activeforeground="white",
        command=comando,
        cursor="hand2"
    ).pack(pady=10)

root.mainloop()
