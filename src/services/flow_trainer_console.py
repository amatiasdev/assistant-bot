import json
import os
from capture_image import seleccionar_region_y_guardar
acciones = []
contador_imagen = 1

def capturar_imagen(flujo):
    global contador_imagen
    nombre_imagen = f"img_step_{contador_imagen}.png"
    seleccionar_region_y_guardar(nombre_imagen, flujo)
    contador_imagen += 1
    return nombre_imagen

def agregar_clic():
    imagen = capturar_imagen()
    acciones.append({"tipo": "clic", "imagen": imagen})

def agregar_teclear():
    texto = input("⌨ Escribe el texto que se debe teclear: ")
    acciones.append({"tipo": "teclear", "texto": texto, "esperar": 1})

def agregar_enter():
    acciones.append({"tipo": "enter"})

def agregar_captura_pantalla(flujo):
    imagen = capturar_imagen(flujo)

    acciones.append({
    "tipo": "detectar_imagen",
    "imagen": {
        "light_"+flujo+"_"+imagen: f"screenshots/"+flujo+"/light/"+imagen,
        "dark_"+flujo+"_"+imagen: f"screenshots/"+flujo+"/dark/"+imagen
    },
    "descripcion": "Agregar descripcion",
    "zona": "completa"
    })

def guardar_flujo(nombre):
    ruta = os.path.join("flows", f"{nombre}.json")
    os.makedirs("flows", exist_ok=True)
    with open(ruta, "w") as f:
        json.dump(acciones, f, indent=2)
    print(f"✅ Flujo guardado en {ruta}")

def mostrar_menu():
    
    nombre = input("📝 Nombre del flujo (sin extensión): ")
    while True:
        print("\n--- Grabador de Flujos ---")
        print("1. Agregar clic")
        print("2. Agregar teclear")
        print("3. Agregar enter")
        print("4. Capturar seleccion pantalla")
        print("5. Guardar flujo")
        print("6. Cancelar y salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            agregar_clic()
        elif opcion == "2":
            agregar_teclear()
        elif opcion == "3":
            agregar_enter()
        elif opcion == "4":
            agregar_captura_pantalla(nombre)
        elif opcion == "5":
            guardar_flujo(nombre)
            break
        elif opcion == "6":
            print("🚫 Grabación cancelada.")
            break
        else:
            print("❌ Opción inválida.")

if __name__ == "__main__":
    mostrar_menu()
