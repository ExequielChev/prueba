import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
from PIL import Image, ImageTk

def ejecutar_script(script_seleccionado, aviso_label, scripts_disponibles):
    try:
        # Mostrar aviso de ejecución
        aviso_label.config(text="Ejecutando script...", fg="blue")
        aviso_label.update()

        # Obtén la ruta del script seleccionado
        ruta_script = scripts_disponibles.get(script_seleccionado)

        if ruta_script and os.path.exists(ruta_script):
            # Determinar la extensión del archivo
            _, extension = os.path.splitext(ruta_script)

            if extension.lower() == '.py':
                # Para archivos .py
                resultado = subprocess.check_output(["python", ruta_script], text=True)
            elif extension.lower() == '.robot':
                # Para archivos .robot (puede necesitar instalación de robotframework)
                resultado = subprocess.check_output(["robot", ruta_script], text=True)
            else:
                # Extensión no compatible
                raise ValueError(f"Extensión de archivo no compatible: {extension}")

            # Muestra el resultado en una ventana de mensaje
            messagebox.showinfo("Ejecución Exitosa", f"Resultado:\n\n{resultado}")
        else:
            messagebox.showerror("Error", "Script no encontrado.")

    except subprocess.CalledProcessError as e:
        # Captura errores específicos al ejecutar el script
        messagebox.showerror("Error", f"Error durante la ejecución:\n\n{e.output.decode()}")

    except Exception as e:
        # Muestra un mensaje de error si la ejecución falla
        messagebox.showerror("Error", f"Error durante la ejecución:\n\n{str(e)}")

    finally:
        # Ocultar aviso después de ejecución
        aviso_label.config(text="")
        aviso_label.update()

def redimensionar_imagen(ruta_imagen, nuevo_ancho, nuevo_alto):
    # Redimensiona la imagen y devuelve el objeto ImageTk
    imagen = Image.open(ruta_imagen)
    imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto))
    return ImageTk.PhotoImage(imagen_redimensionada)

def toggle_modo_oscuro(estilo, toggle_var):
    # Cambia los colores entre claro y oscuro
    modo_oscuro = toggle_var.get()

    if modo_oscuro:
        # Colores oscuros
        estilo.configure("TLabel", foreground="white", background="#333")
        estilo.configure("TButton", foreground="white", background="#555")
        estilo.configure("TFrame", foreground="white", background="#333")
    else:
        # Colores claros
        estilo.configure("TLabel", foreground="black", background="white")
        estilo.configure("TButton", foreground="black", background="#ddd")
        estilo.configure("TFrame",foreground="black", background="black")

def crear_interfaz(scripts_disponibles):
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Ejecución de Script")

    # Configurar la imagen de fondo
    ruta_imagen = "C:/Users/zcheveste/Documents/Robocop_project/prueba/static/muni.png"
    nueva_ancho = 220  # Ajusta según tus necesidades
    nueva_alto = 200   # Ajusta según tus necesidades
    fondo_imagen = redimensionar_imagen(ruta_imagen, nueva_ancho, nueva_alto)
    
    # Etiqueta para la imagen de fondo (como logotipo)
    logo_label = tk.Label(ventana, image=fondo_imagen)
    logo_label.pack()

    # Lista de scripts
    lista_scripts = tk.Listbox(ventana, selectmode=tk.SINGLE, font=('Arial', 12))
    for script in scripts_disponibles:
        lista_scripts.insert(tk.END, script)
    lista_scripts.pack(pady=10)

    # Etiqueta para el aviso de ejecución
    aviso_label = tk.Label(ventana, text="", fg="blue")
    aviso_label.pack()

    # Botón de ejecución
    boton_ejecutar = ttk.Button(ventana, text="Ejecutar Script Seleccionado", command=lambda: ejecutar_script_seleccionado(lista_scripts, aviso_label, scripts_disponibles))
    boton_ejecutar.pack(pady=20)

    # Función para cambiar entre los modos claro y oscuro
    def toggle_modo_oscuro_wrapper():
        toggle_modo_oscuro(estilo, toggle_var)

    # Variable para el botón de alternar
    toggle_var = tk.BooleanVar(value=False)

    # Crear un botón de alternar
    boton_toggle = ttk.Checkbutton(ventana, text="Modo Oscuro", variable=toggle_var, command=toggle_modo_oscuro_wrapper)
    boton_toggle.pack(pady=10)

    # Crear y configurar el estilo
    estilo = ttk.Style()

    # Aplicar el estilo inicial
    toggle_modo_oscuro(estilo, toggle_var)

    ventana.mainloop()
    
# Función para ejecutar el script seleccionado
def ejecutar_script_seleccionado(lista_scripts, aviso_label, scripts_disponibles):
    script_seleccionado = lista_scripts.get(tk.ACTIVE)
    ejecutar_script(script_seleccionado, aviso_label, scripts_disponibles)

# Lista de scripts disponibles
scripts_disponibles = {
    "Ocr Facturas": "C:\\Users\\zcheveste\\Documents\\Robocop_project\\OCR\\Captura_general.py",
    "Robot Compromiso": "C:\\Users\\zcheveste\\Documents\\Robocop_project\\Robot_CompromisoAysa\\tasks.robot",
    "Ocr Comprobantes": "C:\\Users\\zcheveste\\Documents\\Robocop_project\\OCR\\Captura_compr.py",
    "Robot Devengados": "C:\\Users\\zcheveste\\Documents\\Robocop_project\\Robot_Comprobante\\tasks.robot"
}

# Ejecutar la creación de la interfaz
crear_interfaz(scripts_disponibles)