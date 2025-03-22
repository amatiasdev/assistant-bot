import os
import time
import pyautogui
import psutil
import pygetwindow as gw
import keyboard
import cv2
import numpy as np

# Diccionario con rutas de aplicaciones en Windows
APPS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "rdp": "mstsc",
    "whatsapp": "start whatsapp://"
}


def verificar_app_abierta(nombre_app):
    """Verifica si una aplicación está en ejecución Y con ventana visible."""
    # Primero revisamos si hay una ventana visible con ese nombre
    for window in gw.getAllWindows():
        if nombre_app.lower() in window.title.lower() and window.visible:
            print(f"🟢 Ventana activa encontrada: {window.title}")
            return True

    # Si no hay ventana visible, verificamos si el proceso existe (posiblemente en segundo plano)
    for proceso in psutil.process_iter(['pid', 'name']):
        if nombre_app.lower() in proceso.info['name'].lower():
            print(f"⚠ Proceso en segundo plano encontrado: {proceso.info['name']}")
            return False  # Lo tratamos como cerrado (sin ventana)
    
    return False  # No está ejecutándose


def esperar_hasta_carga_whatsapp(timeout=10):
    """Espera hasta que WhatsApp Web esté completamente cargado detectando una imagen de referencia."""
    print("⏳ Esperando a que WhatsApp Web cargue...")

    WHATSAPP_LOADED_IMAGE = "data/whatsapp_loaded.png"  # Imagen de referencia

    start_time = time.time()

    while time.time() - start_time < timeout:
        # Tomar una captura de pantalla
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Cargar la imagen de referencia
        template = cv2.imread(WHATSAPP_LOADED_IMAGE, cv2.IMREAD_COLOR)

        if template is None:
            print("❌ ERROR: No se pudo cargar la imagen de referencia de WhatsApp Web.")
            return False

        # Buscar la imagen en la pantalla actual
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val > 0.75:  # Si la imagen se detecta con suficiente precisión
            print("✅ WhatsApp Web detectado, listo para continuar.")
            return True

        time.sleep(0.5)  # Esperar un poco antes de volver a intentarlo

    print("❌ Tiempo de espera agotado. WhatsApp Web no se detectó.")
    return False


def abrir_aplicacion(nombre):
    """Abre una aplicación solo si no está en ejecución y espera hasta que WhatsApp Web cargue."""
    if nombre in APPS:
        if not verificar_app_abierta(nombre):
            print(f"🚀 Abriendo {nombre}...")
            if nombre == "whatsapp":
                os.system(APPS[nombre])  # Usar start whatsapp://
                if esperar_hasta_carga_whatsapp():  # Esperar hasta que WhatsApp se cargue
                    print("✅ WhatsApp Web cargado correctamente.")
                else:
                    print("⚠ No se detectó WhatsApp Web después del tiempo límite.")
            else:
                os.startfile(APPS[nombre])  # Abrir aplicaciones normales
        else:
            print(f"✅ {nombre} ya estaba abierto.")
            traer_ventana_al_frente("whatsApp")
    else:
        print(f"⚠ No se encontró la ruta para {nombre}.")


def traer_ventana_al_frente(nombre_ventana):
    """Trae la ventana de WhatsApp Web al frente asegurando que sea la correcta."""
    time.sleep(2)  # Esperar a que la ventana se abra correctamente

    # Obtener todas las ventanas abiertas y buscar "WhatsApp" en los títulos
    ventanas = gw.getAllTitles()
    ventana_correcta = None

    for titulo in ventanas:
        print("titulo:" + titulo)
        if nombre_ventana.lower() in titulo.lower():
            ventana_correcta = titulo
            break  # Nos quedamos con la primera coincidencia real
    
    if ventana_correcta:
        print(f"🔍 Intentando activar la ventana: {ventana_correcta}")

        try:
            ventana = gw.getWindowsWithTitle(ventana_correcta)[0]  # Obtener la ventana exacta
            if ventana.isMinimized:
                ventana.restore()
                time.sleep(1)
            ventana.activate()
            print(f"✅ Ventana {ventana_correcta} activada correctamente.")
        except Exception:
            print(f"⚠ No se pudo activar la ventana de WhatsApp. Usando ALT + TAB.")
            pyautogui.hotkey("alt", "tab")  # Alternativa con ALT + TAB
            time.sleep(1)
    else:
        print(f"❌ No se encontró ninguna ventana de WhatsApp. Intentando ALT + TAB...")
        pyautogui.hotkey("alt", "tab")  # Última opción para traer WhatsApp al frente
def cerrar_aplicacion(nombre_app):
    """Cierra una aplicación si está en ejecución."""
    for proceso in psutil.process_iter(['pid', 'name']):
        if nombre_app.lower() in proceso.info['name'].lower():
            print(f"❌ Cerrando {nombre_app}...")
            psutil.Process(proceso.info['pid']).terminate()
            return
    print(f"⚠ {nombre_app} no estaba abierto.")

def buscar_contacto(nombre):
    """Busca un contacto o grupo en WhatsApp Web y lo abre."""
    if detectar_y_hacer_clic_en_busqueda():
        time.sleep(1)  # Esperar para asegurarse de que la barra de búsqueda esté activa
        pyautogui.write(nombre, interval=0.1)
        time.sleep(1)
        # TODO keyboard.press("enter")
        # TODO keyboard.release("enter")
        print(f"✅ Contacto {nombre} abierto en WhatsApp Web.")
    else:
        print("⚠ No se pudo buscar el contacto porque la barra de búsqueda no fue encontrada.")

SEARCH_BAR_IMAGE = "data/search_bar.png"

def detectar_y_hacer_clic_en_busqueda():
    """Detecta la barra de búsqueda en WhatsApp Web, ya sea vacía o con texto, hace clic en ella y borra el contenido si es necesario."""
    print("🔍 Buscando la barra de búsqueda en WhatsApp Web...")

    # Tomar una captura de pantalla
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Cargar ambas imágenes de referencia
    templates = {
        "empty": cv2.imread("data/search_bar_empty.png", cv2.IMREAD_COLOR),
        "filled": cv2.imread("data/search_bar_filled.png", cv2.IMREAD_COLOR),
        "focus": cv2.imread("data/search_bar_focus.png", cv2.IMREAD_COLOR),
        "dark_empty": cv2.imread("data/dark_search_bar_empty.png", cv2.IMREAD_COLOR),
        "dark_filled": cv2.imread("data/dark_search_bar_filled.png", cv2.IMREAD_COLOR),
        "dar_focus": cv2.imread("data/dark_search_bar_focus.png", cv2.IMREAD_COLOR)
    }

    for key, template in templates.items():
        if template is None:
            print(f"❌ ERROR: No se pudo cargar la imagen de referencia ({key}).")
            continue

        # Obtener dimensiones de la imagen de referencia
        h, w, _ = template.shape

        # Buscar la imagen en la pantalla actual
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        print(f"🔍 [{key}] Nivel de coincidencia: {max_val:.2f}")

        # Verificar si la coincidencia es suficiente
        if max_val > 0.75:
            x, y = max_loc
            click_x, click_y = x + w // 2, y + h // 2  # Hacer clic en el centro de la barra

            # Dibujar rectángulo de detección y guardar imagen
            cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imwrite("data/detection_result.png", screenshot)

            # Simular clic en la barra de búsqueda
            pyautogui.click(click_x, click_y)
            print(f"✅ Barra de búsqueda detectada y clickeada en ({click_x}, {click_y}) [{key}]")

            # Si la barra estaba llena, borrar el texto
            if key == "filled":
                print("🗑 Barra de búsqueda detectada con texto. Borrando contenido...")
                pyautogui.hotkey("ctrl", "a")  # Seleccionar todo el texto
                pyautogui.press("backspace")   # Borrar el texto
                time.sleep(0.5)  # Esperar para asegurar que se borre completamente

            return True

    print("❌ No se pudo detectar la barra de búsqueda en ninguno de los estados. Verifica las imágenes de referencia.")
    cv2.imwrite("data/detection_failed.png", screenshot)  # Guardar la captura cuando falla
    return False
