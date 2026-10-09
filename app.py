import streamlit as st
import pandas as pd
import json
import re

# Configuración de la página
st.set_page_config(page_title="Imir - Motor Contable CMYK", layout="centered")

st.title("IMIR 🤖📊")
st.markdown("### Motor Masivo de Pólizas Contables - IPN")

# Cargar la biblia de cuentas
@st.cache_data
def cargar_catalogo():
    try:
        with open("biblia.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

catalogo = cargar_catalogo()

if catalogo is None:
    st.error("⚠️ No se encontró el archivo 'biblia.json' en la raíz del repositorio.")
else:
    pestana_generador, pestana_buscador = st.tabs(["🚀 Procesador Masivo CMYK", "🔍 Buscador de Cuentas"])

    with pestana_generador:
        st.subheader("1. Pega tu Bloque de Operaciones")
        st.markdown("Pega tu lista de operaciones y **Imir** las desglosará ordenadamente.")
        
        texto_masivo = st.text_area(
            "Enunciados de la práctica:",
            """1. Asiento de apertura.
2. Se compran mercancías con valor de $44,851.12 más IVA, a crédito.
3. Se compran mercancías con valor de $53,351.24 más IVA, al contado.
7. Según estado de cuenta bancario tuvimos intereses a nuestro favor por $3,541.91.
8. El banco nos informa que las comisiones bancarias fueron por $842.37 más IVA.
9. Se pagó con cheque el servicio telefónico por $7,214.84 más IVA, correspondiendo el 43% al área de ventas y el resto al área de administración."""
        )

        if st.button("Procesar Práctica Completa"):
            st.markdown("---")
            st.markdown("### 📋 Pólizas Generadas para la Práctica")
            
            # --- BLOQUES HTML PARA COLORES CMYK ---
            html_diario = "<div style='background-color: #00FFFF; padding: 8px; border-radius: 5px; color: black; font-weight: bold; text-align: center; font-size: 18px; margin-bottom: 10px;'>📘 PÓLIZA DE DIARIO</div>"
            html_egreso = "<div style='background-color: #FF00FF; padding: 8px; border-radius: 5px; color: white; font-weight: bold; text-align: center; font-size: 18px; margin-bottom: 10px;'>📕 PÓLIZA DE EGRESO</div>"
            html_ingreso = "<div style='background-color: #FFEA00; padding: 8px; border-radius: 5px; color: black; font-weight: bold; text-align: center; font-size: 18px; margin-bottom: 10px;'>📗 PÓLIZA DE INGRESO</div>"

            # Dividir el texto por número de operación
            bloques = re.split(r'\n(?=\d
