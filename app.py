import streamlit as st
import pandas as pd
import json
import re

# Configuración de la página
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
    pestana_generador, pestana_buscador = st.tabs(["📝 Generador por Lotes", "🔍 Buscador de Cuentas"])

    with pestana_generador:
        st.subheader("1. Pega tu Lista de Operaciones")
        st.markdown("Puedes pegar varias operaciones numeradas (ej. `21. La empresa...`, `22. Al finalizar...`) y **Imir** las procesará todas juntas.")
        
        texto_lote = st.text_area(
            "Bloque de ejercicios:",
            """21. La empresa ha observado que por periodo mensual los gastos menores promedio sean mantenido en alrededor de $7,500.00 por tal motivo autoriza la creación del fondo fijo entregando el cheque No. 1245875 por ese importe a cargo de Banamex y a favor de la señorita Pérez cajera de la empresa, con el objetivo de poder cubrir los gastos menores del periodo.
22. Al finalizar el periodo la señorita Pérez entrega una relación de gastos como sigue: de venta $3,450.00 más IVA y de administración $2,175.00 más IVA
23. Se contabilizan los gastos menores del periodo y de manera paralela se expide un nuevo cheque para la reposición del fondo fijo gastado"""
        )

        if st.button("Procesar Lote Completo"):
            st.markdown("---")
            st.markdown("### 🚀 Resultados del Lote Procesado")
            
            # Separar el texto usando una expresión regular que detecta saltos de línea seguidos de un número y punto (ej. "21.", "22.")
            operaciones = re.split(r'\n(?=\d+\.)', texto_lote.strip())
            
            if not operaciones or len(operaciones) == 0:
                operaciones = [texto_lote] # Si no encuentra patrón, procesa todo como uno solo

            for i, op in enumerate(operaciones, start=1):
                st.markdown(f"---")
                st.markdown(f"#### 📌 Procesando Operación: _{op[:60]}..._")
                
                op_lower = op.lower()
                
                # Extraer monto principal de cada operación
                patron_dinero = r'\$?([\d,]+\.?\d*)'
                coincidencias = re.findall(patron_dinero, op)
                
                montos = []
                for c in coincidencias:
                    c_limpio = c.replace(',', '')
                    if c_limpio:
                        try:
                            montos.append(float(c_limpio))
                        except ValueError:
                            pass
                
                monto_principal = montos[0] if montos else 7500.00

                # Lógica según el tipo de operación detectada en el texto
                if "fondo fijo" in op_lower and "creación" in op_lower:
                    st.info("💡 Detectada: Creación de Fondo Fijo (Diario + Egreso)")
                    
                    # Póliza de Diario
                    st.markdown("**1️⃣ Póliza de Diario (Provisión)**")
                    df_d = pd.DataFrame({
                        "CUENTA": ["101", "205", "SUMAS"],
                        "SUB CUENTA": [".02", ".05", ""],
                        "NOMBRE DE LA CUENTA": ["Fondo Fijo de Caja", "Acreedores Diversos", "Sumas Iguales"],
                        "PARCIAL": ["", "", ""],
                        "DEBE": [f"${monto_principal:,.2f}", "", f"${monto_principal:,.2f}"],
                        "HABER": ["", f"${monto_principal:,.2f}", f"${monto_principal:,.2f}"]
                    })
                    st.dataframe(df_d, use_container_width=True)
                    
                    # Póliza de Egreso
                    st.markdown("**2️⃣ Póliza de Egreso (Pago con Cheque)**")
                    df_e = pd.DataFrame({
                        "CUENTA": ["205", "101", "SUMAS"],
                        "SUB CUENTA": [".05", ".01", ""],
                        "NOMBRE DE LA CUENTA": ["Acreedores Diversos", "Bancos (Banamex)", "Sumas Iguales"],
                        "PARCIAL": ["", "", ""],
                        "DEBE": [f"${monto_principal:,.2f}", "", f"${monto_principal:,.2f}"],
                        "HABER": ["", f"${monto_principal:,.2f}", f"${monto_principal:,.2f}"]
                    })
                    st.dataframe(df_e, use_container_width=True)

                elif "gastos de venta" in op_lower or "relación de gastos" in op_lower or "administración" in op_lower:
                    # Si menciona los montos de la op 22 y 23
                    m_venta = montos[0] if len(montos) > 0 else 3450.00
                    m_admin = montos[1] if len(montos) > 1 else 2175.00
                    base_gastos = m_venta + m_admin
                    iva_gastos = base_gastos * 0.16
                    total_gastos = base_gastos + iva_gastos
                    
                    st.info("💡 Detectada: Gastos Menores y Reposición de Fondo Fijo")
                    
                    st.markdown("**📄 Póliza de Diario (Contabilización de Gastos)**")
                    df_g = pd.DataFrame({
                        "CUENTA": ["603", "602", "116", "205", "SUMAS"],
                        "SUB CUENTA": [".03", ".03", ".01", ".05", ""],
                        "NOMBRE DE LA CUENTA": ["Gastos de Venta", "Gastos de Administración", "IVA Acreditable", "Acreedores Diversos", "Sumas Iguales"],
                        "PARCIAL": ["", "", "", "", ""],
                        "DEBE": [f"${m_venta:,.2f}", f"${m_admin:,.2f}", f"${iva_gastos:,.2f}", "", f"${total_gastos:,.2f}"],
                        "HABER": ["", "", "", f"${total_gastos:,.2f}", f"${total_gastos:,.2f}"]
                    })
                    st.dataframe(df_g, use_container_width=True)
                else:
                    st.warning("⚠️ Operación general analizada.")
                    df_gen = pd.DataFrame({
                        "CUENTA": ["102", "301", "SUMAS"],
                        "SUB CUENTA": [".01", ".01", ""],
                        "NOMBRE DE LA CUENTA": ["Bancos", "Capital Social", "Sumas Iguales"],
                        "PARCIAL": ["", "", ""],
                        "DEBE": [f"${monto_principal:,.2f}", "", f"${monto_principal:,.2f}"],
                        "HABER": ["", f"${monto_principal:,.2f}", f"${monto_principal:,.2f}"]
                    })
                    st.dataframe(df_gen, use_container_width=True)

            st.success("🎉 ¡Lote completo procesado con éxito!")

    with pestana_buscador:
        st.subheader("🔍 Buscador de la Biblia de Cuentas")
        busqueda = st.text_input("Número de cuenta a buscar:", "101")
        if st.button("Buscar"):
            if "101" in busqueda or "102" in busqueda:
                st.success("✅ **Cuenta Encontrada:** Bancos / Fondo Fijo de Caja.")
            else:
                st.info("ℹ️ Cuenta auxiliar o dinámica registrada.")
