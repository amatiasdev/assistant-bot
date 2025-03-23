from services.automation import abrir_aplicacion, buscar_contacto, detectar_y_hacer_clic_en_zona_con_variantes, detectar_y_hacer_clic, acceder_perfil
import time

# Abrir WhatsApp y asegurarse de que está en primer plano
#nombre_contacto = "Aldo Mexico"# input("📌 Ingresa el nombre del contacto o grupo: ")

#abrir_aplicacion("whatsapp")
# Buscar un contacto (ajustar el nombre según sea necesario)
#buscar_contacto(nombre_contacto)  # Puedes cambiarlo por cualquier contacto o grupo

#abrir_aplicacion("rdp")
chromeIsOpen = abrir_aplicacion("chrome")
acceder_perfil(chromeIsOpen)


#TODO Cuando hay una aplicacion que contiene un archivo y ese archivo tiene el nombre de la aplicacion que se quiere abrir se detecta como si fuese whatsapp o chrome.

