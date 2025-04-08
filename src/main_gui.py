
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

class BotEjecutorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot Ejecutor Inteligente")
        self.root.geometry("600x400")

        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self.root, text="✨ Bot Ejecutor Inteligente", font=("Helvetica", 18)).pack(pady=20)

        tk.Button(self.root, text="+ Crear nuevo flujo", width=30, command=self.crear_nuevo_flujo).pack(pady=10)
        tk.Button(self.root, text="🧠 Instrucción por texto (GPT)", width=30, command=self.instruccion_por_texto).pack(pady=10)
        tk.Button(self.root, text="📁 Ejecutar flujo existente", width=30, command=self.ejecutar_flujo).pack(pady=10)
        tk.Button(self.root, text="⚙️ Configuración", width=30, command=self.configuracion).pack(pady=10)

    def crear_nuevo_flujo(self):
        messagebox.showinfo("Flujo", "Aquí conectarás el módulo de grabación visual.")

    def instruccion_por_texto(self):
        instruccion = simpledialog.askstring("GPT", "Escribe la tarea que deseas automatizar:")
        if instruccion:
            messagebox.showinfo("Generar JSON", f"GPT generará un flujo para: {instruccion}\n(Aquí conectarás generador_gpt.py)")

    def ejecutar_flujo(self):
        archivo = filedialog.askopenfilename(title="Selecciona un flujo JSON", filetypes=[("Archivos JSON", "*.json")])
        if archivo:
            messagebox.showinfo("Ejecución", f"Ejecutando flujo: {os.path.basename(archivo)}\n(Aquí conectarás flow_executor.py)")

    def configuracion(self):
        messagebox.showinfo("Configuración", "Aquí irá la configuración del bot (API Key, rutas, etc.)")

if __name__ == "__main__":
    root = tk.Tk()
    app = BotEjecutorGUI(root)
    root.mainloop()
