import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# Asegúrate de tener tu archivo parser.py en el mismo directorio
from parser import parse_ssh_logs 

# Configuración inicial de la página
st.set_page_config(page_title="Security Log Analyzer", layout="wide")

# Inicialización de Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.warning("⚠️ No se ha detectado la variable de entorno GEMINI_API_KEY. Configúrala para usar la IA.")

# --- PROMPT DEL SISTEMA ---
SYSTEM_PROMPT = """
Eres un analista experto de un SOC (Security Operations Center). 
Tu tarea es analizar un resumen de logs de intentos fallidos de autenticación SSH y proporcionar un diagnóstico de seguridad rápido y accionable.

Te entregaré los datos en formato CSV con las siguientes columnas:
- ip: La dirección IP de origen.
- intentos: Número de intentos fallidos.
- usuarios_probados: Cuentas de usuario que intentaron vulnerar.

Debes devolver tu análisis estrictamente en el siguiente formato Markdown:

### 🔴 Nivel de Amenaza Estimado
[Indica si es Bajo, Medio, Alto o Crítico y justifica brevemente por qué].

### 🕵️ Diagnóstico del Incidente
[Explica qué tipo de ataque parece ser. Ej: Ataque de fuerza bruta focalizado, rociado de credenciales (credential stuffing), escaneo automatizado, etc.].

### 🛡️ Plan de Mitigación
[Proporciona 2 o 3 pasos técnicos precisos para bloquear la amenaza. Ej: reglas de iptables, configuración de fail2ban, o bloqueo de red].
"""

# --- FUNCIONES DE SOPORTE ---
def preparar_datos_para_ia(df_failed):
    """Agrupa los intentos fallidos por IP y lista los usuarios atacados."""
    # Eliminamos nulos en 'user' para evitar fallos al agrupar
    df_clean = df_failed.dropna(subset=['user'])
    
    resumen = df_clean.groupby('ip').agg(
        intentos=('status', 'count'),
        usuarios_probados=('user', lambda x: ', '.join(set(x)))
    ).reset_index()
    
    # Top 10 atacantes
    top_atacantes = resumen.sort_values(by='intentos', ascending=False).head(10)
    return top_atacantes.to_csv(index=False)

# --- INTERFAZ PRINCIPAL ---
st.title("🛡️ Analizador de Logs de Seguridad con IA")

uploaded_file = st.file_uploader("Sube tu archivo auth.log", type=['log', 'txt'])

if uploaded_file is not None:
    st.info("Archivo cargado correctamente. Procesando datos...")
    
    raw_content = uploaded_file.getvalue()
    
    # Llamada al motor de parseo
    df = parse_ssh_logs(raw_content)
    
    if not df.empty:
        st.success(f"Se han extraído {len(df)} eventos SSH.")
        
        # Mostrar tabla global
        st.dataframe(df, use_container_width=True)
        
        df_failed = df[df['status'] == 'Failed']
        st.warning(f"Se detectaron {len(df_failed)} intentos fallidos de conexión.")
        
        # --- NUEVO: GRÁFICO DE BARRAS ---
        if not df_failed.empty:
            st.subheader("📊 Top 10 IPs con más intentos fallidos")
            top_ips_chart = df_failed['ip'].value_counts().head(10)
            st.bar_chart(top_ips_chart, color="#ff4b4b") 
        
        # --- BLOQUE DE IA ---
        if not df_failed.empty:
            if st.button("Analizar anomalías con Gemini"):
                if not api_key:
                    st.error("Necesitas configurar la API Key de Gemini para ejecutar el análisis.")
                else:
                    with st.spinner("Generando diagnóstico de seguridad..."):
                        datos_csv = preparar_datos_para_ia(df_failed)
                        
                        model = genai.GenerativeModel(
                            model_name='gemini-1.5-flash',
                            system_instruction=SYSTEM_PROMPT
                        )
                        
                        user_message = f"Por favor, analiza estos registros de ataques SSH:\n\n{datos_csv}"
                        
                        try:
                            response = model.generate_content(user_message)
                            st.markdown("---")
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"Error al conectar con la API: {e}")
                            
    else:
        st.error("No se encontraron eventos SSH válidos en el archivo.")