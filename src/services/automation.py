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
    """Abre una aplicación solo si no está en ejecución y espera hasta que cargue, luego maximiza."""
    if nombre in APPS:
        if not verificar_app_abierta(nombre):
            print(f"🚀 Abriendo {nombre}...")
            if nombre == "whatsapp":
                os.system(APPS[nombre])  # Usar start whatsapp://
                if esperar_hasta_carga_whatsapp():  # Esperar hasta que WhatsApp se cargue
                    print("✅ WhatsApp Web cargado correctamente.")
                    maximizar_ventana("WhatsApp")  # <-- AQUÍ
                else:
                    print("⚠ No se detectó WhatsApp Web después del tiempo límite.")
            else:
                os.startfile(APPS[nombre])  # Abrir otras apps
                time.sleep(2)  # Darle tiempo a que aparezca la ventana
                maximizar_ventana(nombre)  # <-- AQUÍ también
        else:
            print(f"✅ {nombre} ya estaba abierto.")
            traer_ventana_al_frente(nombre)
            maximizar_ventana(nombre)  # <-- También si ya estaba abierto
        return True
    else:
        print(f"⚠ No se encontró la ruta para {nombre}.")
        return False

def maximizar_ventana(nombre_ventana):
    """Maximiza la ventana si está minimizada o en modo normal."""
    ventanas = gw.getWindowsWithTitle(nombre_ventana)
    for ventana in ventanas:
        if nombre_ventana.lower() in ventana.title.lower():
            try:
                ventana.maximize()
                print(f"🧱 Ventana '{ventana.title}' maximizada.")
                return True
            except Exception as e:
                print(f"❌ No se pudo maximizar la ventana '{ventana.title}': {e}")
    print(f"⚠ No se encontró ninguna ventana activa con el nombre: {nombre_ventana}")
    return False



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

    """Detecta la barra de búsqueda (vacía o llena), hace clic y borra si es necesario."""
    imagenes = {
        "empty": "data/search_bar_empty.png",
        "filled": "data/search_bar_filled.png",
        "focus": "data/search_bar_focus.png",
        "dark_empty": "data/dark_search_bar_empty.png",
        "dark_filled": "data/dark_search_bar_filled.png",
        "dark_focus": "data/dark_search_bar_focus.png"
    }

    resultado = detectar_y_hacer_clic(imagenes)

    if resultado is None:
        return False

    if "filled" in resultado:
        print("🗑 Barra de búsqueda detectada con texto. Borrando contenido...")
        borrar_texto_actual()
        
    time.sleep(1)  # Esperar para asegurarse de que la barra de búsqueda esté activa
    pyautogui.write(nombre, interval=0.1)
    time.sleep(1)
    # TODO keyboard.press("enter")
    # TODO keyboard.release("enter")
    print(f"✅ Contacto {nombre} abierto en WhatsApp Web.")

def borrar_texto_actual():
    """Borra el texto que haya en un campo de entrada activo."""
    time.sleep(0.3)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    print("🗑 Texto anterior eliminado.")

SEARCH_BAR_IMAGE = "data/search_bar.png"


def detectar_y_hacer_clic(imagenes_dict, threshold=0.75):
    """
    Busca imágenes en pantalla y hace clic en la que encuentre con mayor coincidencia.
    
    - imagenes_dict: dict[str, str] con {clave: ruta de imagen}
    - threshold: valor mínimo de coincidencia
    - return: clave de la imagen detectada, o None si no detecta nada
    """
    print("🔍 Buscando imágenes en pantalla...")

    screenshot = pyautogui.screenshot()
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    for key, path in imagenes_dict.items():
        template = cv2.imread(path, cv2.IMREAD_COLOR)
        if template is None:
            print(f"❌ No se pudo cargar la imagen '{path}'")
            continue

        h, w, _ = template.shape
        result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        print(f"🔍 [{key}] Coincidencia: {max_val:.2f}")

        if max_val >= threshold:
            x, y = max_loc
            cx, cy = x + w // 2, y + h // 2

            cv2.rectangle(screenshot_cv, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imwrite("data/detection_result.png", screenshot_cv)

            pyautogui.click(cx, cy)
            print(f"✅ Imagen '{key}' detectada y clickeada en ({cx}, {cy})")
            return key  # <-- clave detectada

    print("❌ No se detectó ninguna imagen.")
    cv2.imwrite("data/detection_failed.png", screenshot_cv)
    return None

def detectar_y_hacer_clic_en_zona_con_variantes(imagenes_dict, zona="superior_derecha", threshold=0.75):
    """
    Detecta una imagen entre múltiples variantes en una zona específica de la pantalla y hace clic.
    Dibuja también el punto del clic en data/detection_result.png para depuración visual.
    """
    print(f"🔍 Buscando imagen en zona: {zona} con variantes...")

    screenshot = pyautogui.screenshot()
    full_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    h, w, _ = full_img.shape
    offset_x, offset_y = 0, 0

    # Zona recortada
    if zona == "superior_derecha":
        recorte = full_img[0:150, w-250:w]
        offset_x = w - 250
    elif zona == "superior_izquierda":
        recorte = full_img[0:150, 0:250]
    else:
        recorte = full_img

    for variante, ruta in imagenes_dict.items():
        template = cv2.imread(ruta, cv2.IMREAD_COLOR)
        if template is None:
            print(f"❌ No se pudo cargar la imagen: {ruta}")
            continue

        th, tw, _ = template.shape
        result = cv2.matchTemplate(recorte, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        print(f"🔍 [{variante}] Coincidencia: {max_val:.2f}")

        if max_val >= threshold:
            x, y = max_loc

            # Ajustes manuales para centrar clic mejor
            ajuste_x = -10
            ajuste_y = 10

            clic_x = offset_x + x + (tw // 2) + ajuste_x
            clic_y = offset_y + y + (th // 2) + ajuste_y

            # Dibujar detección y punto de clic
            cv2.rectangle(full_img, (offset_x + x, offset_y + y),
                          (offset_x + x + tw, offset_y + y + th), (0, 255, 0), 2)
            cv2.circle(full_img, (clic_x, clic_y), 5, (0, 0, 255), -1)  # punto del clic en rojo
            cv2.imwrite("data/detection_result.png", full_img)

            pyautogui.click(clic_x, clic_y)
            print(f"✅ Imagen '{variante}' detectada y clickeada en ({clic_x}, {clic_y})")
            return variante

    print("❌ Ninguna variante detectada.")
    cv2.imwrite("data/detection_failed.png", full_img)
    return None


def acceder_perfil(isChromeOpen):

    if isChromeOpen:
        imagenes = {
            "opened_white": "data/profile_chrome_opened_white.png",
            "opened_dark": "data/profile_chrome_opened_dark.png",
        }
        detectar_y_hacer_clic_en_zona_con_variantes(imagenes)
        time.sleep(1)
        perfiles_aldotk = {
            "dark": "data/perfil_usuario_dark.png",
            "light": "data/perfil_usuario_light.png"
        }

        resultado = detectar_y_hacer_clic_en_zona_con_variantes(perfiles_aldotk, zona="centro", threshold=0.8)

        if resultado:
            print(f"✅ Perfil 'Aldo (itkeeper.net)' detectado y seleccionado ({resultado})")
        else:
            print("❌ No se detectó el perfil deseado.")

    else:
        
        imagenes = {
                "recently_opened": "data/profile_chrome_first_openning_dark.png"
            }
        detectar_y_hacer_clic(imagenes)