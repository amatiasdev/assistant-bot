import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
import sys
from services.capture_image import seleccionar_region_y_guardar

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui_config import aplicar_estilo_ventana

def lanzar_creador_flujo():
    acciones = []
    contador_imagen = 1

    root = tk.Toplevel()
    style, colors = aplicar_estilo_ventana(root, tamaño="700x500")

    lista_acciones = tk.Listbox()

    def capturar_imagen(flujo):
        nonlocal contador_imagen
        nombre_imagen = f"img_step_{contador_imagen}.png"
        exito = seleccionar_region_y_guardar(nombre_imagen, flujo)
        if not exito:
            print("🚫 Captura cancelada. No se agregó acción.")
            return None
        contador_imagen += 1
        return nombre_imagen

    def agregar_clic():
        imagen = capturar_imagen(flujo_nombre)
        if imagen:
            acciones.append({"tipo": "clic", "imagen": imagen})
            actualizar_lista_acciones()

    def agregar_teclear():
        texto = simpledialog.askstring("Teclear", "Escribe el texto que se debe teclear:", parent=root)
        if texto:
            acciones.append({"tipo": "teclear", "texto": texto, "esperar": 1})
            actualizar_lista_acciones()

    def agregar_enter():
        acciones.append({"tipo": "enter"})
        actualizar_lista_acciones()

    def agregar_captura_pantalla():
        imagen = capturar_imagen(flujo_nombre)
        root.update_idletasks()
        if imagen:
            acciones.append({
                "tipo": "detectar_imagen",
                "imagen": {
                    f"light_{flujo_nombre}_{imagen}": f"screenshots/{flujo_nombre}/light/{imagen}",
                    f"dark_{flujo_nombre}_{imagen}": f"screenshots/{flujo_nombre}/dark/{imagen}"
                },
                "descripcion": "Agregar descripcion",
                "zona": "completa"
            })
            actualizar_lista_acciones()

    def mover_abajo():
        seleccion = lista_acciones.curselection()
        if seleccion:
            idx = seleccion[0]
            if idx < len(acciones) - 1:
                acciones[idx], acciones[idx + 1] = acciones[idx + 1], acciones[idx]
                actualizar_lista_acciones()
                lista_acciones.selection_set(idx + 1)

    def mover_arriba():
        seleccion = lista_acciones.curselection()
        if seleccion:
            idx = seleccion[0]
            if idx > 0:
                acciones[idx], acciones[idx - 1] = acciones[idx - 1], acciones[idx]
                actualizar_lista_acciones()
                lista_acciones.selection_set(idx - 1)

    def eliminar_accion():
        seleccion = lista_acciones.curselection()
        if seleccion:
            acciones.pop(seleccion[0])
            actualizar_lista_acciones()

    def guardar_flujo():
        if not flujo_nombre:
            messagebox.showerror("Error", "Primero debes nombrar el flujo.", parent=root)
            return
        if not acciones:
            messagebox.showwarning("Vacío", "No has agregado ninguna acción al flujo.", parent=root)
            return
        ruta = os.path.join("flows", f"{flujo_nombre}.json")
        os.makedirs("flows", exist_ok=True)
        with open(ruta, "w") as f:
            json.dump(acciones, f, indent=2)
        messagebox.showinfo("Éxito", f"Flujo guardado en {ruta}", parent=root)
        root.after(300, root.destroy)

    def actualizar_lista_acciones():
        lista_acciones.delete(0, tk.END)
        for i, acc in enumerate(acciones):
            lista_acciones.insert(tk.END, f"{i+1}. {acc['tipo']}")

    flujo_nombre = simpledialog.askstring("Nombre del flujo", "Ingresa el nombre del flujo (sin extensión):", parent=root)
    if not flujo_nombre:
        messagebox.showwarning("Cancelado", "Debes ingresar un nombre para comenzar.", parent=root)
        root.destroy()
        return

    contenedor_principal = tk.Frame(root, bg=colors.bg)
    contenedor_principal.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    frame_lista = tk.Frame(contenedor_principal, bg=colors.bg)
    frame_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    label = tk.Label(frame_lista, text="Acciones grabadas:", font=("Helvetica", 12), fg="white", bg=colors.bg)
    label.pack(anchor="w")

    frame_botones_horizontales = tk.Frame(frame_lista, bg=colors.bg)
    frame_botones_horizontales.pack(pady=5)

    for texto, accion in [
        ("Agregar clic", agregar_clic),
        ("Agregar texto", agregar_teclear),
        ("Agregar Enter", agregar_enter),
        ("Detectar imagen", agregar_captura_pantalla),
        ("Guardar flujo", guardar_flujo)
    ]:
        tk.Button(frame_botones_horizontales, text=texto, command=accion).pack(side=tk.LEFT, padx=2)

    lista_acciones = tk.Listbox(frame_lista, width=50, height=15)
    lista_acciones.pack(fill=tk.BOTH, expand=True)

    frame_botones_verticales = tk.Frame(contenedor_principal, bg=colors.bg)
    frame_botones_verticales.pack(side=tk.RIGHT, padx=10)

    for texto, accion in [
        ("Mover arriba", mover_arriba),
        ("Mover abajo", mover_abajo),
        ("Eliminar acción", eliminar_accion)
    ]:
        tk.Button(frame_botones_verticales, text=texto, width=20, command=accion).pack(pady=3)

    root.wait_window()

if __name__ == "__main__":
    root = tk.Tk()
    style, colors = aplicar_estilo_ventana(root, tamaño="700x500")
    lanzar_creador_flujo()
    root.mainloop()
