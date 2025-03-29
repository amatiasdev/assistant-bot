import json
import time
import pyautogui
import os

# Importa tu función personalizada desde el módulo donde la tengas guardada
from automation import detectar_y_hacer_clic_en_zona_con_variantes, maximizar_ventana_activa

def ejecutar_flujo(ruta_json):
    """Ejecuta paso a paso un flujo definido en formato JSON."""
    if not os.path.exists(ruta_json):
        print(f"❌ No se encontró el archivo: {ruta_json}")
        return

    with open(ruta_json, "r", encoding="utf-8") as f:
        pasos = json.load(f)

    print(f"🚀 Ejecutando flujo: {ruta_json}")
    for i, paso in enumerate(pasos):
        tipo = paso.get("tipo")
        print(f"\n🔹 Paso {i+1}: {tipo}")

        # -------------------- Detectar Imagen y Hacer Clic --------------------
        if tipo == "detectar_imagen":
            imagenes_dict = paso.get("imagen", {})
            zona = paso.get("zona", "completa")
            descripcion = paso.get("descripcion", "Detectar imagen y hacer clic")

            print(f"🔍 {descripcion}")
            resultado = detectar_y_hacer_clic_en_zona_con_variantes(imagenes_dict, zona=zona)
            if resultado:
                print(f"✅ Variante detectada: {resultado}")
            else:
                print("❌ No se pudo detectar ninguna variante.")
            esperar(paso.get("esperar", 0))
    
        # -------------------- Esperar Imagen --------------------
        elif tipo == "esperar_imagen":
            imagenes_dict = paso.get("imagen", {})
            zona = paso.get("zona", "completa")
            descripcion = paso.get("descripcion", "Esperar aparición de imagen")

            print(f"⏳ {descripcion}")
            for intento in range(30):  # Máximo 15 segundos
                resultado = detectar_y_hacer_clic_en_zona_con_variantes(imagenes_dict, zona=zona, threshold=0.8)
                if resultado:
                    print(f"✅ Imagen detectada: {resultado}")
                    break
                time.sleep(0.5)
            else:
                print("❌ Tiempo de espera agotado.")
            esperar(paso.get("esperar", 0))
        # -------------------- Teclear Texto --------------------
        elif tipo == "teclear":
            texto = paso.get("texto", "")
            pyautogui.write(texto, interval=0.05)
            print(f"⌨ Texto tecleado: {texto}")
            esperar(paso.get("esperar", 0))

        # -------------------- Presionar Enter --------------------
        elif tipo == "enter":
            pyautogui.press("enter")
            print("↩ ENTER presionado")
            esperar(paso.get("esperar", 0))

        elif tipo == "presionar_combinacion":
            teclas = paso.get("teclas", [])
            descripcion = paso.get("descripcion", "Presionar combinación de teclas")
            print(f"🎹 {descripcion}: {' + '.join(teclas)}")
            pyautogui.hotkey(*teclas)


        # -------------------- Acción Desconocida --------------------
        else:
            print(f"⚠ Acción desconocida o no implementada: {tipo}")
        
        if paso.get("maximizar") is True:
            time.sleep(1)
            maximizar_ventana_activa()
    time.sleep(1)
    print("\n✅ Flujo finalizado.")

def esperar(espera):
    if espera > 0:
        print(f"⏱ Esperando {espera} segundos...")
        time.sleep(espera)

# Ejemplo de uso directo
if __name__ == "__main__":
    ejecutar_flujo("flows/clic_inicio_windows.json")
    ejecutar_flujo("flows/abrir_chrome.json")
    ejecutar_flujo("flows/seleccionar_perfil_chrome.json")
    ejecutar_flujo("flows/abrir_nueva_pestana_chrome.json")
    ejecutar_flujo("flows/abrir_gmail.json")
    ejecutar_flujo("flows/abrir_ejecutar_windows.json")
    ejecutar_flujo("flows/abrir_mstsc.json")
    ejecutar_flujo("flows/clic_inicio_windows.json")
    ejecutar_flujo("flows/abrir_whatsapp_desktop.json")
    
