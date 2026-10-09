import streamlit as st
import pandas as pd
import json

# Configuración de la página
st.set_page_config(page_title="Imir - Generador de Pólizas Contables", layout="centered")

st.title("IMIR 🤖📊")
st.markdown("### Generador Automático de Pólizas Contables")
st.markdown("Sistema basado en el catálogo y temario de Contabilidad III del IPN[span_0](start_span)[span_0](end_span).")

# Intentamos cargar el catálogo de cuentas
@st.cache_data
def cargar_catalogo():
    try:
        with open("Catalogo_de_Cuentas_Completo.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

catalogo = cargar_catalogo()

if catalogo is None:
    st.error("⚠️ No se encontró el archivo 'Catalogo_de_Cuentas_Completo.json' en la raíz. Por favor súbelo.")
else:
    st.success("Catálogo de cuentas cargado correctamente.")

# Sección de entrada del usuario
st.subheader("1. Inscribe la Operación Contable")
texto_operacion = st.text_area(
    "Escribe o pega el enunciado del ejercicio:",
    "Enviamos a nuestro comisionista la empresa 'Y' S.A de C.V. 50 estufas con costo unitario de $1,000.00 pesos para venderse con un recargo del 50%, Las ventas son más IVA."
)

if st.button("Procesar y Generar Póliza"):
    st.markdown("---")
    st.markdown("### Resultado de la Póliza Generada")
    
    # Aquí simulamos la salida estructurada idéntica a tus ejemplos (Ej. Operación 1 de Consignación)
    st.info("**Explicación:** Envío de mercancías al comisionista bajo inventarios perpetuos.")
    
    st.markdown("#### PÓLIZA DE DIARIO - N° 1")
    
    # Estructura visual exacta de las pólizas de tus manuales
    datos_poliza = {
        "CUENTA": ["Mercancías en Consignación", "Almacén", "TOTALES"],
        "SUB CUENTA": ["", "", ""],
        "NOMBRE DE LA CUENTA": ["Mercancías en Consignación", "Almacén", "Sumas Iguales"],
        "PARCIAL": ["", "", ""],
        "DEBE": ["$50,000.00", "", "$50,000.00"],
        "HABER": ["", "$50,000.00", "$50,000.00"]
    }
    
    df = pd.DataFrame(datos_poliza)
    st.table(df)
    
    st.markdown("*(↑ Volver al Índice Principal de Operaciones)*")
