import os
import time
import pyautogui
import pygetwindow as gw
import cv2
import numpy as np

def maximizar_ventana_activa():
    """Intenta maximizar la ventana actualmente activa."""
    try:
        ventana = gw.getActiveWindow()
        print(ventana)
        if ventana:
            time.sleep(1)
            ventana.maximize()
            print(f"🪟 Ventana '{ventana.title}' maximizada")
        else:
            print("⚠ No se detectó ninguna ventana activa para maximizar.")
    except Exception as e:
        print(f"❌ Error al maximizar ventana: {e}")

def detectar_y_hacer_clic_en_zona_con_variantes(imagenes_dict, zona="completa", threshold=0.75):
    """
    Detecta una imagen entre múltiples variantes en una zona específica de la pantalla y hace clic.
    Dibuja también el punto del clic en data/detection_result.png para depuración visual.
    
    :param imagenes_dict: Diccionario con variantes {"nombre": "ruta/a/imagen.png"}
    :param zona: "completa", "superior_derecha", "superior_izquierda"
    :param threshold: Umbral de coincidencia mínima (entre 0 y 1)
    :return: Nombre de la variante detectada, o None si no se encontró ninguna
    """
    print(f"🔍 Buscando imagen en zona: {zona} con variantes...")
    os.makedirs("data", exist_ok=True)

    screenshot = pyautogui.screenshot()
    full_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    h, w, _ = full_img.shape
    offset_x, offset_y = 0, 0

    # Recorte por zona
    if zona == "superior_derecha":
        recorte = full_img[0:150, w-250:w]
        offset_x = w - 250
    elif zona == "superior_izquierda":
        recorte = full_img[0:150, 0:250]
    else:
        recorte = full_img  # Zona completa

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

            # Ajustes opcionales (personaliza si el clic no queda centrado)
            ajuste_x = -10
            ajuste_y = 10

            clic_x = offset_x + x + (tw // 2) + ajuste_x
            clic_y = offset_y + y + (th // 2) + ajuste_y

            # Dibujar detección
            cv2.rectangle(full_img, (offset_x + x, offset_y + y),
                          (offset_x + x + tw, offset_y + y + th), (0, 255, 0), 2)
            cv2.circle(full_img, (clic_x, clic_y), 5, (0, 0, 255), -1)

            # Guardar resultado visual
            cv2.imwrite("data/detection_result.png", full_img)

            pyautogui.moveTo(clic_x, clic_y, duration=0.3)
            pyautogui.click()
            print(f"✅ Imagen '{variante}' detectada y clickeada en ({clic_x}, {clic_y})")
            return variante

    print("❌ Ninguna variante detectada.")
    cv2.imwrite("data/detection_failed.png", full_img)
    return None
