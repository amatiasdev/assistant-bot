from PIL import ImageGrab
import tkinter as tk
import keyboard
import os

def seleccionar_region_y_guardar(nombre_archivo, flujo):
    """Abre una ventana de selección y guarda el recorte como imagen."""
    
    print("🕹 Esperando que presiones la tecla [Supr] para iniciar recorte...")
    
    # Esperar que se presione la tecla Supr (Delete)
    keyboard.wait('delete')

    # Captura pantalla completa
    imagen_completa = ImageGrab.grab()

    # Interfaz para seleccionar zona
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.3)  # semi-transparente
    canvas = tk.Canvas(root, cursor="cross", bg="black")
    canvas.pack(fill=tk.BOTH, expand=True)

    rect = None
    start_x = start_y = curX = curY = 0

    def on_button_press(event):
        nonlocal start_x, start_y, rect
        start_x, start_y = event.x, event.y
        rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', width=2)

    def on_move_press(event):
        nonlocal rect
        curX, curY = event.x, event.y
        canvas.coords(rect, start_x, start_y, curX, curY)

    def on_button_release(event):
        x1 = min(start_x, event.x)
        y1 = min(start_y, event.y)
        x2 = max(start_x, event.x)
        y2 = max(start_y, event.y)

        # Guardar el recorte
        recorte = imagen_completa.crop((x1, y1, x2, y2))
        os.makedirs("screenshots/"+flujo+"/light", exist_ok=True)
        os.makedirs("screenshots/"+flujo+"/dark", exist_ok=True)
        ruta_light = os.path.join("screenshots/"+flujo+"/light/", nombre_archivo)
        ruta_dark = os.path.join("screenshots/"+flujo+"/dark/", nombre_archivo)
        recorte.save(ruta_light)
        recorte.save(ruta_dark)
        print(f"✅ Imagen recortada guardada en: {ruta_light} y {ruta_dark}")
        root.destroy()

    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_move_press)
    canvas.bind("<ButtonRelease-1>", on_button_release)

    root.mainloop()
    return nombre_archivo
