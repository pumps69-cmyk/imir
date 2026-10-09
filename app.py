import streamlit as st
import pandas as pd
import json
import re

st.set_page_config(page_title="Imir - Motor Contable Inteligente", layout="centered")

st.title("IMIR 🤖📊")
st.markdown("### Motor Contable Dinámico e Inteligente - IPN")

@st.cache_data
def cargar_catalogo():
    try:
        with open("biblia.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

catalogo = cargar_catalogo()

if catalogo is None:
    st.error("⚠️ No se encontró el archivo 'biblia.json' en la raíz.")
else:
    pestana_generador, pestana_buscador = st.tabs(["🚀 Procesador Dinámico", "🔍 Buscador de Cuentas"])

    with pestana_generador:
        st.subheader("Inscribe tus Operaciones")
        st.markdown("Pega una o varias operaciones numeradas. El sistema analizará los conceptos y montos dinámicamente.")
        
        texto_input = st.text_area(
            "Enunciados a procesar:",
            """1. Se compran mercancías por $50,000.00 más IVA a crédito.
2. Se pagó con cheque el servicio de energía eléctrica por $8,584.70 más IVA, correspondiendo el 58% a ventas y el resto a administración.""",
            height=200
        )

        if st.button("Procesar Operaciones"):
            st.markdown("---")
            
            # Separar por números de operación
            bloques = re.split(r'\n(?=\d+\.)', texto_input.strip())
            if not bloques or len(bloques) == 0:
                bloques = [texto_input]

            for bloque in bloques:
                if not bloque.strip():
                    continue
                
                st.markdown(f"#### 📌 Enunciado: _{bloque.strip()[:90]}..._")
                b_lower = bloque.lower()
                
                # Extraer montos numéricos con signo de pesos
                coincidencias = re.findall(r'\$([\d,]+\.?\d*)', bloque)
                montos = []
                for c in coincidencias:
                    try:
                        montos.append(float(c.replace(',', '')))
                    except ValueError:
                        pass
                
                monto_base = montos[0] if montos else 0.0
                tiene_iva = "más iva" in b_lower or "+ iva" in b_lower or "iva" in b_lower
                iva = monto_base * 0.16 if tiene_iva else 0.0
                total = monto_base + iva

                # Detección de Porcentajes (Ventas / Admin)
                pct_ventas = 0.50
                match_pct = re.search(r'(\d+)%\s*al?\s*área\s*de\s*ventas', b_lower) or re.search(r'(\d+)%\s*a\s*ventas', b_lower)
                if match_pct:
                    pct_ventas = float(match_pct.group(1)) / 100.0
                
                pct_admin = 1.0 - pct_ventas if ("administración" in b_lower or "admin" in b_lower) else 0.0

                # --- LÓGICA DE CLASIFICACIÓN DINÁMICA ---
                
                # 1. Compras / Almacén
                if "compr" in b_lower or "mercancía" in b_lower:
                    st.info("💡 Clasificación: Compra de Mercancías / Almacén")
                    df_d = pd.DataFrame({
                        "CUENTA": ["115", "119", "201", "SUMAS"],
                        "SUB CUENTA": ["", ".02", ".01", ""],
                        "NOMBRE DE LA CUENTA": ["Almacén", "IVA por Acreditar", "Proveedores", "Sumas Iguales"],
                        "PARCIAL": ["", "", "", ""],
                        "DEBE": [f"${monto_base:,.2f}", f"${iva:,.2f}", "", f"${total:,.2f}"],
                        "HABER": ["", "", f"${total:,.2f}", f"${total:,.2f}"]
                    })
                    st.dataframe(df_d, use_container_width=True)

                    if "contado" in b_lower or "cheque" in b_lower or "transferencia" in b_lower:
                        df_e = pd.DataFrame({
                            "CUENTA": ["201", "116", "101", "119", "SUMAS"],
                            "SUB CUENTA": [".01", ".01", ".01", ".02", ""],
                            "NOMBRE DE LA CUENTA": ["Proveedores", "IVA Acreditable", "Bancos", "IVA por Acreditar", "Sumas Iguales"],
                            "PARCIAL": ["", "", "", "", ""],
                            "DEBE": [f"${total:,.2f}", f"${iva:,.2f}", "", "", f"${total + iva:,.2f}"],
                            "HABER": ["", "", f"${total:,.2f}", f"${iva:,.2f}", f"${total + iva:,.2f}"]
                        })
                        st.dataframe(df_e, use_container_width=True)

                # 2. Gastos Operativos (Servicios, Teléfono, Luz, Renta)
                elif "servicio" in b_lower or "gastos" in b_lower or "teléfono" in b_lower or "eléctrica" in b_lower or "energía" in b_lower:
                    st.info("💡 Clasificación: Gasto Operativo Desglosado")
                    m_v = monto_base * pct_ventas
                    m_a = monto_base * (1 - pct_ventas)
                    
                    df_d = pd.DataFrame({
                        "CUENTA": ["603", "602", "119", "205", "SUMAS"],
                        "SUB CUENTA": [".01", ".01", ".02", ".02", ""],
                        "NOMBRE DE LA CUENTA": ["Gastos de Venta", "Gastos de Administración", "IVA por Acreditar", "Acreedores Diversos", "Sumas Iguales"],
                        "PARCIAL": ["", "", "", "", ""],
                        "DEBE": [f"${m_v:,.2f}", f"${m_a:,.2f}", f"${iva:,.2f}", "", f"${total:,.2f}"],
                        "HABER": ["", "", "", f"${total:,.2f}", f"${total:,.2f}"]
                    })
                    st.dataframe(df_d, use_container_width=True)

                    if "cheque" in b_lower or "pagó" in b_lower or "transferencia" in b_lower:
                        df_e = pd.DataFrame({
                            "CUENTA": ["205", "116", "101", "119", "SUMAS"],
                            "SUB CUENTA": [".02", ".01", ".01", ".02", ""],
                            "NOMBRE DE LA CUENTA": ["Acreedores Diversos", "IVA Acreditable", "Bancos", "IVA por Acreditar", "Sumas Iguales"],
                            "PARCIAL": ["", "", "", "", ""],
                            "DEBE": [f"${total:,.2f}", f"${iva:,.2f}", "", "", f"${total + iva:,.2f}"],
                            "HABER": ["", "", f"${total:,.2f}", f"${iva:,.2f}", f"${total + iva:,.2f}"]
                        })
                        st.dataframe(df_e, use_container_width=True)

                # 3. Caso General / Abierto
                else:
                    st.info("💡 Clasificación: Registro General")
                    df_gen = pd.DataFrame({
                        "CUENTA": ["102", "301", "SUMAS"],
                        "SUB CUENTA": [".01", ".01", ""],
                        "NOMBRE DE LA CUENTA": ["Bancos", "Capital Social / Cuenta General", "Sumas Iguales"],
                        "PARCIAL": ["", "", ""],
                        "DEBE": [f"${monto_base:,.2f}", "", f"${monto_base:,.2f}"],
                        "HABER": ["", f"${monto_base:,.2f}", f"${monto_base:,.2f}"]
                    })
                    st.dataframe(df_gen, use_container_width=True)

    with pestana_buscador:
        st.subheader("🔍 Buscador de Cuentas")
        busqueda = st.text_input("Número o nombre de cuenta:")
        if st.button("Buscar en la Biblia"):
            st.info(f"Buscando '{busqueda}' en biblia.json...")
