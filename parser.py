import re
import pandas as pd

def parse_ssh_logs(file_content):
    """
    Parsea un archivo auth.log y devuelve un DataFrame con intentos SSH.
    """
    parsed_data = []
    
    # Si el archivo viene de st.file_uploader, necesitamos decodificar los bytes a texto
    if isinstance(file_content, bytes):
        content = file_content.decode('utf-8')
    else:
        content = file_content
        
    # Procesamos línea por línea
    for line in content.splitlines():
        # Descartamos líneas que no sean del servicio SSH
        if 'sshd' not in line:
            continue
            
        # Diccionario base para la fila actual
        row = {
            'timestamp': None,
            'user': None,
            'ip': None,
            'status': None
        }
        
        # 1. Extraer la marca de tiempo (Ej: "Aug 24 12:30:01")
        time_match = re.search(r"^([A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2})", line)
        if time_match:
            row['timestamp'] = time_match.group(1)
            
        # 2. Extraer IP (buscamos un patrón IPv4 estándar)
        ip_match = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
        if ip_match:
            row['ip'] = ip_match.group(1)
            
        # 3. Determinar el estado y extraer el usuario
        if "Accepted" in line:
            row['status'] = "Success"
            user_match = re.search(r"Accepted \w+ for (\S+)", line)
            if user_match:
                row['user'] = user_match.group(1)
                
        elif "Failed" in line:
            row['status'] = "Failed"
            # Captura casos como "Failed password for root" o "Failed password for invalid user admin"
            user_match = re.search(r"Failed \w+ for (?:invalid user )?(\S+)", line)
            if user_match:
                row['user'] = user_match.group(1)
                
        elif "Invalid user" in line:
            row['status'] = "Failed"
            user_match = re.search(r"Invalid user (\S+)", line)
            if user_match:
                row['user'] = user_match.group(1)
                
        # Solo añadimos la fila si logramos extraer una IP y un estado
        if row['ip'] and row['status']:
            parsed_data.append(row)
            
    # Convertimos la lista de diccionarios en un DataFrame
    df = pd.DataFrame(parsed_data)
    
    return df