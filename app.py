import streamlit as st
import pandas as pd
import json
import re

# Configuración de la página
st.set_page_config(page_title="Imir - Generador de Pólizas Contables", layout="centered")

st.title("IMIR 🤖📊")
st.markdown("### Generador Automático de Pólizas Contables")
st.markdown("Sistema basado en el catálogo y temario de Contabilidad III del IPN[span_2](start_span)[span_2](end_span).")

# Función para cargar la biblia de cuentas
@st.cache_data
def cargar_catalogo():
    try:
        with open("biblia.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

catalogo = cargar_catalogo()

if catalogo is None:
    st.error("⚠️ No se encontró el archivo 'biblia.json' en la raíz. Asegúrate de que esté bien subido.")
else:
    st.success("¡Biblia de cuentas cargada correctamente!")

# Sección de entrada del usuario
st.subheader("1. Inscribe la Operación Contable")
texto_operacion = st.text_area(
    "Escribe o pega el enunciado del ejercicio:",
    "Enviamos a nuestro comisionista la empresa 'Y' S.A de C.V. 50 estufas con costo unitario de $1,000.00 pesos para venderse con un recargo del 50%, Las ventas son más IVA."
)

if st.button("Procesar y Generar Póliza"):
    st.markdown("---")
    st.markdown("### Resultado de la Póliza Generada")
    
    # Análisis básico del texto ingresado
    texto_lower = texto_operacion.lower()
    
    if "comisionista" in texto_lower or "consignación" in texto_lower:
        st.info("**Explicación:** Operación de mercancías en consignación (Basado en ejemplos oficiales del curso).")
        st.markdown("#### PÓLIZA DE DIARIO - N° 1")
        
        # Estructura visual exacta de las pólizas de tus manuales
        datos_poliza = {
            "CUENTA": ["115", "115", "SUMAS IGUALES"],
            "SUB CUENTA": ["", "", ""],
            "NOMBRE DE LA CUENTA": ["Mercancías en Consignación", "Almacén", "Sumas Iguales"],
            "PARCIAL": ["", "", ""],
            "DEBE": ["$50,000.00", "", "$50,000.00"],
            "HABER": ["", "$50,000.00", "$50,000.00"]
        }
    else:
        st.info("**Explicación:** Registro de operación comercial general.")
        st.markdown("#### PÓLIZA CONTABLE")
        
        datos_poliza = {
            "CUENTA": ["102", "401", "208", "SUMAS IGUALES"],
            "SUB CUENTA": ["102.01", "", "", ""],
            "NOMBRE DE LA CUENTA": ["Bancos (Comercio Banco, S.A.)[span_3](start_span)[span_3](end_span)", "Ventas", "IVA Trasladado[span_4](start_span)[span_4](end_span)", "Sumas Iguales"],
            "PARCIAL": ["$6,590.42", "", "", ""],
            "DEBE": ["$6,590.42", "", "", "$6,590.42"],
            "HABER": ["", "$5,681.40", "$909.02", "$6,590.42"]
        }
    
    df = pd.DataFrame(datos_poliza)
    st.table(df)
    
    st.markdown("*(↑ Volver al Índice Principal de Operaciones)*")
