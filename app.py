from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import signal

app = Flask(__name__)
cancelar_ejecucion = False
proceso_ejecucion = None
procesos_ejecucion = []  # Declarar la variable

def ejecutar_archivo(archivo_path, resultado):
    global cancelar_ejecucion, proceso_ejecucion, procesos_ejecucion  # Corregir el nombre de la variable

    try:
        # Inicia un subproceso para ejecutar el archivo
        proceso_ejecucion = subprocess.Popen(['python', archivo_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Espera hasta que el archivo termine o se indique cancelar
        while not cancelar_ejecucion and proceso_ejecucion.poll() is None:
            pass

    except subprocess.CalledProcessError as e:
        resultado.append({"tipo": "Error", "contenido": f"Error al ejecutar el archivo: {e.stderr.strip()}"})
    except Exception as e:
        resultado.append({"tipo": "Error", "contenido": f"Error inesperado al ejecutar el archivo: {str(e)}"})

    # Reinicia las variables globales para la próxima ejecución
    cancelar_ejecucion = False
    proceso_ejecucion = None

def ejecutar_archivo_en_hilo(archivo_path, resultado):
    global procesos_ejecucion  # Corregir el nombre de la variable
    hilo_ejecucion = threading.Thread(target=ejecutar_archivo, args=(archivo_path, resultado))
    hilo_ejecucion.start()
    procesos_ejecucion.append(hilo_ejecucion)

@app.route('/execute', methods=['POST'])
def execute_script():
    global cancelar_ejecucion, procesos_ejecucion

    script_name = request.form.get('nombre_script')
    
    # Mapea el nombre del script al archivo correspondiente
    script_path_mapping = {
        'ejecutar1': 'C:\\Users\\zcheveste\\Documents\\Robocop_project\\Ejecucion\\ejecutar1.py',
        'ejecutar2': 'C:\\Users\\zcheveste\\Documents\\Robocop_project\\Ejecucion\\ejecutar2.py',
        'robot1': 'C:\\Users\\zcheveste\\Documents\\Robocop_project\\Robot_CompromisoAysa\\tasks.robot',
        'robot2': 'C:\\Users\\zcheveste\\Documents\\Robocop_project\\Robot_Comprobante\\tasks.robot',
    }

    if script_name not in script_path_mapping:
        return jsonify(result="Script no válido")

    script_path = script_path_mapping[script_name]

    resultado = []

    # Verifica si hay un archivo en ejecución
    if any(proceso.is_alive() for proceso in procesos_ejecucion):
        return jsonify(result="Ya hay un archivo en ejecución...", resultado=resultado)

    # Ejecuta la función en un hilo separado
    ejecutar_archivo_en_hilo(script_path, resultado)

    return jsonify(result="Ejecutando archivo...", resultado=resultado)

@app.route('/cancelar', methods=['POST'])
def cancelar_ejecucion_script():
    global cancelar_ejecucion, procesos_ejecucion
    cancelar_ejecucion = True

    # Espera a que todos los procesos terminen completamente
    for proceso in procesos_ejecucion:
        proceso.join()

    return jsonify(result="Cancelando ejecución del archivo...")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
