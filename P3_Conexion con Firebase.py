import psutil
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Configura Firebase
cred = credentials.Certificate("tu base")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://exam-supl-iot-default-rtdb.firebaseio.com/'
})

def get_cpu_speed():
    """
    Obtiene la velocidad del CPU en GHz con dos decimales.
    """
    try:
        cpu_freq = psutil.cpu_freq()
        if cpu_freq is not None:
            # Convertir MHz a GHz y redondear a dos decimales
            return round(cpu_freq.current / 1000, 2)
        else:
            return "N/A"  # Si no se puede obtener la velocidad del CPU
    except Exception as e:
        print(f"Error al obtener la velocidad del CPU: {e}")
        return "N/A"

def obtener_datos():
    """
    Obtiene el uso de la memoria y la velocidad del CPU.
    """
    memory_usage = psutil.virtual_memory().used
    cpu_speed = get_cpu_speed()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    datos = {
        'Memoria_Usada': round(memory_usage / 1073741824, 2),  # Convertir bytes a GB
        'Velocidad_CPU': cpu_speed
    }
    return timestamp, datos

def enviar_a_firebase(timestamp, datos):
    """
    Envía los datos a Firebase.
    """
    ref = db.reference(f'Registros/{timestamp}')
    ref.set(datos)

while True:
    timestamp, datos = obtener_datos()
    if datos['Memoria_Usada'] > 12:  # Solo enviar si la memoria usada supera los 12 GB
        enviar_a_firebase(timestamp, datos)
        print(f"Datos enviados:\nMemoria: {datos['Memoria_Usada']} GB\nVelocidad del CPU: {datos['Velocidad_CPU']} GHz")
    else:
        print(f"Datos no enviados: Memoria actual {datos['Memoria_Usada']} GB")
    time.sleep(5)
