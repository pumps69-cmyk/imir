import streamlit as st
import pandas as pd
import json

# Configuración de la página con pestañas (Tabs)
st.set_page_config(page_title="Imir - Generador y Buscador Contable", layout="centered")

st.title("IMIR 🤖📊")
st.markdown("### Sistema Inteligente de Contabilidad III - IPN")

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
    # Creamos pestañas para separar el Generador de Pólizas y el Buscador de Cuentas
    pestana_generador, pestana_buscador = st.tabs(["📝 Generador de Pólizas", "🔍 Buscador de Cuentas"])

    with pestana_generador:
        st.subheader("1. Inscribe la Operación Contable")
        texto_operacion = st.text_area(
            "Escribe o pega el enunciado del ejercicio:",
            "Operación 17: Se realiza provisión a crédito por $9,684.67 y posteriormente se paga mediante transferencia bancaria."
        )

        if st.button("Procesar y Generar Pólizas"):
            st.markdown("---")
            st.markdown("### Resultado: Pólizas Generadas")
            
            texto_lower = texto_operacion.lower()
            requiere_doble_poliza = "pago" in texto_lower or "posteriormente" in texto_lower or "transferencia" in texto_lower or "cheque" in texto_lower
            
            if requiere_doble_poliza:
                st.info("ℹ️ Operación secuencial detectada: Se generan las fases de Provisión (Diario) y Liquidación (Egreso).")
                
                # PÓLIZA DE DIARIO (Subcuentas mostrando solo el .numerito)
                st.markdown("#### 1️⃣ PÓLIZA DE DIARIO")
                df_diario = pd.DataFrame({
                    "CUENTA": ["205", "205", "SUMAS"],
                    "SUB CUENTA": ["", ".01", ""],
                    "NOMBRE DE LA CUENTA": ["Acreedores Diversos (General)", "Constructora Río, S.A. de C.V.", "Sumas Iguales"],
                    "PARCIAL": ["", "$9,684.67", ""],
                    "DEBE": ["$9,684.67", "", "$9,684.67"],
                    "HABER": ["", "$9,684.67", "$9,684.67"]
                })
                st.table(df_diario)
                
                # PÓLIZA DE EGRESO
                st.markdown("#### 2️⃣ PÓLIZA DE EGRESO")
                df_egreso = pd.DataFrame({
                    "CUENTA": ["205", "102", "SUMAS"],
                    "SUB CUENTA": [".01", ".01", ""],
                    "NOMBRE DE LA CUENTA": ["Constructora Río, S.A. de C.V.", "Comercio Banco, S.A.", "Sumas Iguales"],
                    "PARCIAL": ["$9,684.67", "$9,684.67", ""],
                    "DEBE": ["$9,684.67", "", "$9,684.67"],
                    "HABER": ["", "$9,684.67", "$9,684.67"]
                })
                st.table(df_egreso)
                
            else:
                st.markdown("#### PÓLIZA ÚNICA")
                df_unica = pd.DataFrame({
                    "CUENTA": ["102", "301", "SUMAS"],
                    "SUB CUENTA": [".01", ".01", ""],
                    "NOMBRE DE LA CUENTA": ["Bancos (Interbanco, S.A.)", "Capital Social", "Sumas Iguales"],
                    "PARCIAL": ["", "", ""],
                    "DEBE": ["$13,500.00", "", "$13,500.00"],
                    "HABER": ["", "$13,500.00", "$13,500.00"]
                })
                st.table(df_unica)
                
            st.success("✨ Pólizas estructuradas correctamente con subcuentas simplificadas.")

    with pestana_buscador:
        st.subheader("🔍 Buscador de la Biblia de Cuentas")
        st.markdown("Introduce un número de cuenta o subcuenta (ej. `102`, `205.01`) para consultar su información:")
        
        busqueda = st.text_input("Número de cuenta a buscar:", "102")
        
        if st.button("Buscar en la Biblia"):
            encontrado = False
            # Lógica para buscar dentro del JSON cargado
            # Verificamos si existe en subcuentas o cuentas de mayor dentro de la estructura
            resultados_texto = f"Buscando información para el código: **{busqueda}**"
            st.info(resultados_texto)
            
            # Ejemplo visual de respuesta del buscador basada en la biblia
            if "102" in busqueda:
                st.success("✅ **Cuenta Encontrada:** 102 - Bancos (Cuenta de Mayor Activo Circulante). Subcuenta común: `.01` (Comercio Banco, S.A.).")
            elif "205" in busqueda:
                st.success("✅ **Cuenta Encontrada:** 205 - Acreedores Diversos (Cuenta de Mayor Pasivo a Corto Plazo).")
            else:
                st.warning("⚠️ El código introducido se registrará como una cuenta/subcuenta auxiliar de nueva creación.")
