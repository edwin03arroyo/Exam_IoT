import psutil
import time
import paho.mqtt.client as mqtt

def get_memory_usage():
    """
    Obtiene el uso de la memoria.
    """
    memory = psutil.virtual_memory()
    return memory.used

def get_cpu_speed():
    """
    Obtiene la velocidad del CPU en GHz con dos decimales.
    """
    # Obtener la información del CPU
    cpu_freq = psutil.cpu_freq()
    if cpu_freq is not None:
        # Redondear a dos decimales
        return round(cpu_freq.current/1000,2)
    else:
        return "N/A"  # Si no se puede obtener la velocidad del CPU

def to_GB(bytes):
    """
    Convierte bytes a GB con dos decimales.
    """
    return round(bytes / 1073741824, 2)

# Configuración MQTT
mqtt_broker = "localhost"  # Cambia esto por tu broker MQTT
mqtt_port = 1883
mqtt_topic_memoria = "memoria"
mqtt_topic_cpu_speed = "cpu_velo"

# Crear cliente MQTT
client = mqtt.Client()

# Conectar al broker MQTT
client.connect(mqtt_broker, mqtt_port, 60)

try:
    while True:
        # Obtener el uso de la memoria y la velocidad del CPU
        memory_usage = get_memory_usage()
        cpu_speed = get_cpu_speed()

        # Convertir bytes a GB para memoria
        memory_usage_gb = to_GB(memory_usage)

        # Enviar datos por MQTT
        client.publish(mqtt_topic_memoria, memory_usage_gb)
        client.publish(mqtt_topic_cpu_speed, cpu_speed)

        print(f"Datos enviados:\nMemoria: {memory_usage_gb} GB\nVelocidad del CPU: {cpu_speed} GHz")

        # Esperar 3 segundos antes de la próxima lectura
        time.sleep(3)

except KeyboardInterrupt:
    print("Programa terminado")
    client.disconnect()
