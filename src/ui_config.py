from ttkbootstrap import Style

# Instancia del estilo oscuro
style = Style("darkly")
colors = style.colors


def aplicar_estilo_ventana(ventana, titulo="Bot Ejecutor Inteligente", tamaño="600x400"):
    """Aplica el estilo visual a una ventana dada."""
    ventana.title(titulo)
    ventana.geometry(tamaño)
    ventana.configure(bg=colors.bg)
    ventana.resizable(False, False)
    return style, colors
