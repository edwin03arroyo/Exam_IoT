import psutil
import time
import json
import wmi

def obtener_datos():
    # Obtener el uso de CPU en %
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Obtener el uso de RAM en %
    ram_usage = psutil.virtual_memory().percent
    
    
    # Obtener el timestamp actual
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Crear un diccionario con los datos y etiquetas
    datos = {
        'timestamp': timestamp,
        'cpu_usage': f'{cpu_usage} %',
        'ram_usage': f'{ram_usage} %',
    }
    
    # Convertir los datos a formato JSON para un procesamiento posterior
    return json.dumps(datos)

while True:
    datos = obtener_datos()
    print(datos)
    time.sleep(20)  # Repetir cada 5 segundos
