import random
from datetime import datetime, timedelta

# Configuración
NUM_LINEAS = 500
ARCHIVO_SALIDA = "fake_auth.log"
HOSTNAME = "servidor-prod-01"

# Diccionarios de datos simulados
# Simulamos un par de IPs muy agresivas y otras secundarias
IPS_ATACANTES = ["203.0.113.42", "203.0.113.42", "203.0.113.42", "198.51.100.23", "45.33.32.156"] 
IP_LEGITIMA = "84.12.43.201"

USUARIOS_VALIDOS = ["root", "admin", "ubuntu", "pi", "deploy"]
USUARIOS_INVALIDOS = ["guest", "oracle", "minecraft", "test", "ftp"]

def generar_fecha_secuencial(inicio, incrementos_segundos):
    """Genera fechas que avanzan unos segundos para simular ataques seguidos"""
    nueva_fecha = inicio + timedelta(seconds=incrementos_segundos)
    # Formato esperado por tu regex: Aug 24 12:30:01 (Omitimos el 0 inicial del día si es menor a 10 para mayor realismo, pero el %d lo pone)
    # Reemplazamos el primer cero del día por un espacio si lo hay, tal como hace syslog
    fecha_str = nueva_fecha.strftime("%b %d %H:%M:%S").replace(" 0", "  ")
    return nueva_fecha, fecha_str

def generar_linea():
    fecha_actual = datetime.now() - timedelta(days=2) # Empezamos hace 2 días
    
    with open(ARCHIVO_SALIDA, "w") as f:
        for i in range(NUM_LINEAS):
            # Avanzamos el tiempo aleatoriamente (ataques de fuerza bruta son rápidos)
            fecha_actual, fecha_str = generar_fecha_secuencial(fecha_actual, random.randint(1, 5))
            
            pid = random.randint(10000, 30000)
            puerto = random.randint(30000, 60000)
            
            # 5% de probabilidad de ser un login legítimo exitoso
            if random.random() < 0.05:
                usuario = "admin"
                linea = f"{fecha_str} {HOSTNAME} sshd[{pid}]: Accepted publickey for {usuario} from {IP_LEGITIMA} port {puerto} ssh2\n"
            else:
                # 95% de probabilidad de ser un ataque (Failed o Invalid)
                ip_atacante = random.choice(IPS_ATACANTES)
                
                if random.random() < 0.5:
                    # Intento fallido con usuario que "existe"
                    usuario = random.choice(USUARIOS_VALIDOS)
                    linea = f"{fecha_str} {HOSTNAME} sshd[{pid}]: Failed password for {usuario} from {ip_atacante} port {puerto} ssh2\n"
                else:
                    # Intento fallido con usuario inventado
                    usuario = random.choice(USUARIOS_INVALIDOS)
                    linea = f"{fecha_str} {HOSTNAME} sshd[{pid}]: Invalid user {usuario} from {ip_atacante} port {puerto} ssh2\n"
            
            f.write(linea)

if __name__ == "__main__":
    print(f"Generando {NUM_LINEAS} registros de prueba...")
    generar_linea()
    print(f"✅ Archivo '{ARCHIVO_SALIDA}' creado con éxito. ¡Listo para subir a Streamlit!")