# 🛡️ Analizador de Logs de Seguridad con IA

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-FF4B4B.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458.svg)
![Gemini AI](https://img.shields.io/badge/Google_Gemini-API-4285F4.svg)

Una herramienta de observabilidad de seguridad que ingiere registros de servidores (SSH `auth.log`), visualiza patrones de ataque mediante gráficos interactivos y utiliza la Inteligencia Artificial de Google Gemini (actuando como un analista SOC de Nivel 1) para diagnosticar amenazas y proponer planes de mitigación exactos (ej. reglas de `iptables` o `fail2ban`).

---

## 🚀 Características Principales

- **Parseo Inteligente:** Utiliza expresiones regulares (`re`) y `pandas` para transformar miles de líneas de texto plano en DataFrames estructurados en milisegundos.
- **Visualización Interactiva:** Gráficos de barras nativos con Streamlit para identificar rápidamente las direcciones IP más agresivas.
- **Diagnóstico SOC Automatizado:** Agrupa el comportamiento malicioso y lo envía a **Gemini 1.5 Flash** mediante un *System Prompt* estricto para obtener reportes en formato Markdown.
- **Generador de Logs de Prueba:** Incluye un script (`generar_logs.py`) para simular ataques de fuerza bruta y probar la aplicación sin exponer datos reales de servidores de producción.

---

## 🛠️ Stack Tecnológico

- **Frontend / UI:** [Streamlit](https://streamlit.io/)
- **Procesamiento de Datos:** [Pandas](https://pandas.pydata.org/)
- **Inteligencia Artificial:** [Google Generative AI (Gemini API)](https://ai.google.dev/)
- **Lenguaje:** Python

---

## ⚙️ Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu entorno local.

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/security-log-analyzer.git](https://github.com/TU_USUARIO/security-log-analyzer.git)
cd security-log-analyzer
```
### 2. Crear un entorno virtual e instalar dependencias
Es altamente recomendable usar un entorno virtual:
```bash
# En Windows
python -m venv venv
.\venv\Scripts\activate

# Instalar librerías
pip install streamlit pandas google-generativeai
```

### 3. 3. Configurar la API Key de Google Gemini
Para que el motor de IA funcione, necesitas una clave de API de Google AI Studio (debe empezar por AIza...).

#### En Windows (PowerShell):
```PowerShell
$env:GEMINI_API_KEY="tu_clave_api_aqui"
```
#### En Linux/Mac:
```Bash
export GEMINI_API_KEY="tu_clave_api_aqui"
```

## 🖥️ Uso de la Aplicación
### Iniciar el Dashboard
Una vez configurada la clave, levanta el servidor de Streamlit:
```Bash
python -m streamlit run main.py
```
Se abrirá automáticamente una pestaña en tu navegador web en http://localhost:8501.
### ¿No tienes un archivo auth.log a mano?
Puedes simular uno ejecutando el script generador de pruebas. Esto creará un archivo llamado `fake_auth.log` con un ataque de fuerza bruta simulado, ideal para probar la IA:
```Bash
python generar_logs.py
```
Sube el archivo fake_auth.log generado a la interfaz web y pulsa "Analizar anomalías con Gemini".

## 📁 Estructura del Proyecto
```Plaintext
📦 security-log-analyzer
 ┣ 📜 main.py              # Archivo principal y UI de Streamlit
 ┣ 📜 parser.py            # Motor de expresiones regulares para procesar los logs
 ┣ 📜 generar_logs.py      # Script para crear archivos auth.log sintéticos
 ┗ 📜 README.md            # Documentación del proyecto
```
## 🤝 Contribuciones
¡Las contribuciones son bienvenidas! Si tienes ideas para añadir soporte para otros tipos de logs (como Nginx, Apache o VPNs), siéntete libre de hacer un fork del repositorio y enviar un Pull Request.

## 📄 Licencia
Este proyecto está bajo la Licencia MIT - mira el archivo LICENSE para más detalles.
