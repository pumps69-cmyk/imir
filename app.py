import streamlit as st
import pandas as pd
import json
import re

# Configuración de la página
st.set_page_config(page_title="Trapito el que lo lea", layout="centered")

st.title("IMIR 🤖📊")
st.markdown("Imir v.2.05 by pumps")

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
        st.markdown("Pega tu lista de operaciones y **Imir** detectará el tipo de operación basándose en el catálogo.")
        
        texto_masivo = st.text_area(
            "Enunciados de la práctica:",
            """1. Asiento de apertura.
2. Se compran mercancías con valor de $44,851.12 más IVA, a crédito.
7. Según estado de cuenta bancario tuvimos intereses a nuestro favor por $3,541.91.
9. Se pagó con cheque el servicio telefónico por $7,214.84 más IVA."""
        )

        if st.button("Procesar Práctica Completa"):
            st.markdown("---")
            st.markdown("### 📋 Pólizas Generadas para la Práctica")
            
            # Encabezados CMYK
            html_diario = "<div style='background-color: #00FFFF; padding: 8px; border-radius: 5px; color: black; font-weight: bold; text-align: center; font-size: 18px; margin-bottom: 10px;'>📘 PÓLIZA DE DIARIO</div>"
            html_egreso = "<div style='background-color: #FF00FF; padding: 8px; border-radius: 5px; color: white; font-weight: bold; text-align: center; font-size: 18px; margin-bottom: 10px;'>📕 PÓLIZA DE EGRESO</div>"
            html_ingreso = "<div style='background-color: #FFEA00; padding: 8px; border-radius: 5px; color: black; font-weight: bold; text-align: center; font-size: 18px; margin-bottom: 10px;'>📗 PÓLIZA DE INGRESO</div>"

            bloques = re.split(r'\n(?=\d+\.)', texto_masivo.strip())
            if not bloques or len(bloques) == 0:
                bloques = [texto_masivo]

            for idx, bloque in enumerate(bloques, start=1):
                st.markdown(f"---")
                st.markdown(f"#### 📌 Análisis: _{bloque[:70]}..._")
                
                bloque_lower = bloque.lower()
                patron_dinero = r'\$([\d,]+\.?\d*)'
                coincidencias = re.findall(patron_dinero, bloque)
                
                montos = []
                for c in coincidencias:
                    c_limpio = c.replace(',', '')
                    if c_limpio:
                        try:
                            montos.append(float(c_limpio))
                        except ValueError:
                            pass
                
                monto_base = montos[0] if montos else 0.0
                iva_calc = monto_base * 0.16
                total_op = monto_base + iva_calc

                # --- 1. ASIENTO DE APERTURA ---
                if "apertura" in bloque_lower:
                    st.info("💡 Operación: Asiento de Apertura")
                    st.markdown(html_diario, unsafe_allow_html=True)
                    df_ap = pd.DataFrame({
                        "CUENTA": ["102", "115", "301", "SUMAS"],
                        "SUB CUENTA": [".01", "", ".01", ""],
                        "NOMBRE DE LA CUENTA": ["Bancos", "Almacén", "Capital Social", "Sumas Iguales"],
                        "PARCIAL": ["", "", "", ""],
                        "DEBE": ["$3,512,561.84", "$23,314.70", "", "$3,535,876.54"],
                        "HABER": ["", "", "$3,535,876.54", "$3,535,876.54"]
                    })
                    st.dataframe(df_ap, use_container_width=True)

                # --- 2. COMPRAS DE MERCANCÍAS ---
                elif "compran mercancías" in bloque_lower or "compra" in bloque_lower:
                    if "crédito" in bloque_lower:
                        st.info("💡 Operación: Compra de Mercancías a Crédito")
                        st.markdown(html_diario, unsafe_allow_html=True)
                        df_c = pd.DataFrame({
                            "CUENTA": ["115", "119", "201", "SUMAS"],
                            "SUB CUENTA": ["", ".02", ".01", ""],
                            "NOMBRE DE LA CUENTA": ["Almacén", "IVA por Acreditar", "Proveedores", "Sumas Iguales"],
                            "PARCIAL": ["", "", "", ""],
                            "DEBE": [f"${monto_base:,.2f}", f"${iva_calc:,.2f}", "", f"${total_op:,.2f}"],
                            "HABER": ["", "", f"${total_op:,.2f}", f"${total_op:,.2f}"]
                        })
                        st.dataframe(df_c, use_container_width=True)
                    else:
                        st.info("💡 Operación: Compra al Contado (Diario + Egreso)")
                        st.markdown(html_diario, unsafe_allow_html=True)
                        df_dc = pd.DataFrame({
                            "CUENTA": ["115", "119", "201", "SUMAS"],
                            "SUB CUENTA": ["", ".02", ".01", ""],
                            "NOMBRE DE LA CUENTA": ["Almacén", "IVA por Acreditar", "Proveedores", "Sumas Iguales"],
                            "PARCIAL": ["", "", "", ""],
                            "DEBE": [f"${monto_base:,.2f}", f"${iva_calc:,.2f}", "", f"${total_op:,.2f}"],
                            "HABER": ["", "", f"${total_op:,.2f}", f"${total_op:,.2f}"]
                        })
                        st.dataframe(df_dc, use_container_width=True)
                        
                        st.markdown(html_egreso, unsafe_allow_html=True)
                        df_ec = pd.DataFrame({
                            "CUENTA": ["201", "116", "101", "119", "SUMAS"],
                            "SUB CUENTA": [".01", ".01", ".01", ".02", ""],
                            "NOMBRE DE LA CUENTA": ["Proveedores", "IVA Acreditable", "Bancos", "IVA por Acreditar", "Sumas Iguales"],
                            "PARCIAL": ["", "", "", "", ""],
                            "DEBE": [f"${total_op:,.2f}", f"${iva_calc:,.2f}", "", "", f"${total_op + iva_calc:,.2f}"],
                            "HABER": ["", "", f"${total_op:,.2f}", f"${iva_calc:,.2f}", f"${total_op + iva_calc:,.2f}"]
                        })
                        st.dataframe(df_ec, use_container_width=True)

                               # --- 3. CONSIGNACIÓN DE MERCANCÍAS (Con unidades o mercancía explícita) ---
                elif ("consignación" in bloque_lower or "enviamos" in bloque_lower) and ("unidad" in bloque_lower or "mercancía" in bloque_lower or "estufa" in bloque_lower):
                    st.info("Operación: Envío de Mercancías a Consignación")
                    st.markdown(html_diario, unsafe_allow_html=True)
                    df_cons = pd.DataFrame({
                        "CUENTA": ["115", "115", "SUMAS"],
                        "SUB CUENTA": [".06", "", ""],
                        "NOMBRE DE LA CUENTA": ["Mercancías en Consignación", "Almacén", "Sumas Iguales"],
                        "PARCIAL": ["", "", ""],
                        "DEBE": [f"${monto_base:,.2f}", "", f"${monto_base:,.2f}"],
                        "HABER": ["", f"${monto_base:,.2f}", f"${monto_base:,.2f}"]
                    })
                    st.dataframe(df_cons, use_container_width=True)

                # --- 3.1. ENVÍO DE FONDOS / GASTOS AL COMISIONISTA (Transferencia) ---
                elif "transferencia" in bloque_lower or "comisionista" in bloque_lower and "gastos" in bloque_lower:
                    st.info("Operación: Envío de Fondos al Comisionista (Egreso)")
                    st.markdown(html_egreso, unsafe_allow_html=True)
                    df_fon = pd.DataFrame({
                        "CUENTA": ["814", "101", "SUMAS"],
                        "SUB CUENTA": [".04", ".01", ""],
                        "NOMBRE DE LA CUENTA": ["Fondos del Comitente", "Bancos", "Sumas Iguales"],
                        "PARCIAL": ["", "", ""],
                        "DEBE": [f"${monto_base:,.2f}", "", f"${monto_base:,.2f}"],
                        "HABER": ["", f"${monto_base:,.2f}", f"${monto_base:,.2f}"]
                    })
                    st.dataframe(df_fon, use_container_width=True)


                # --- 4. INTERESES FINANCIEROS ---
                elif "intereses" in bloque_lower or "favor" in bloque_lower:
                    st.info("💡 Operación: Intereses a Favor (Catálogo 702)")[span_6](start_span)[span_6](end_span)
                    st.markdown(html_diario, unsafe_allow_html=True)
                    df_d7 = pd.DataFrame({
                        "CUENTA": ["107", "702", "SUMAS"],
                        "SUB CUENTA": ["", ".04", ""],
                        "NOMBRE DE LA CUENTA": ["Deudores Diversos", "Productos Financieros", "Sumas Iguales"],
                        "PARCIAL": ["", "", ""],
                        "DEBE": [f"${monto_base:,.2f}", "", f"${monto_base:,.2f}"],
                        "HABER": ["", f"${monto_base:,.2f}", f"${monto_base:,.2f}"]
                    })
                    st.dataframe(df_d7, use_container_width=True)

                    st.markdown(html_ingreso, unsafe_allow_html=True)
                    df_i7 = pd.DataFrame({
                        "CUENTA": ["101", "107", "SUMAS"],
                        "SUB CUENTA": [".01", "", ""],
                        "NOMBRE DE LA CUENTA": ["Bancos", "Deudores Diversos", "Sumas Iguales"],
                        "PARCIAL": ["", "", ""],
                        "DEBE": [f"${monto_base:,.2f}", "", f"${monto_base:,.2f}"],
                        "HABER": ["", f"${monto_base:,.2f}", f"${monto_base:,.2f}"]
                    })
                    st.dataframe(df_i7, use_container_width=True)

                # --- 5. GASTOS Y SERVICIOS (Luz, Teléfono, etc.) ---
                elif "servicio" in bloque_lower or "teléfono" in bloque_lower or "luz" in bloque_lower or "energía" in bloque_lower:
                    st.info("💡 Operación: Gastos de Operación / Servicios (Catálogo 602/603)")[span_7](start_span)[span_7](end_span)
                    st.markdown(html_diario, unsafe_allow_html=True)
                    df_d9 = pd.DataFrame({
                        "CUENTA": ["602", "119", "205", "SUMAS"],
                        "SUB CUENTA": [".28", ".02", ".02", ""],
                        "NOMBRE DE LA CUENTA": ["Gastos de Administración (Teléfonos/Luz)", "IVA por Acreditar", "Acreedores Diversos", "Sumas Iguales"],
                        "PARCIAL": ["", "", "", ""],
                        "DEBE": [f"${monto_base:,.2f}", f"${iva_calc:,.2f}", "", f"${total_op:,.2f}"],
                        "HABER": ["", "", f"${total_op:,.2f}", f"${total_op:,.2f}"]
                    })
                    st.dataframe(df_d9, use_container_width=True)

                    st.markdown(html_egreso, unsafe_allow_html=True)
                    df_e9 = pd.DataFrame({
                        "CUENTA": ["205", "116", "101", "119", "SUMAS"],
                        "SUB CUENTA": [".02", ".01", ".01", ".02", ""],
                        "NOMBRE DE LA CUENTA": ["Acreedores Diversos", "IVA Acreditable", "Bancos", "IVA por Acreditar", "Sumas Iguales"],
                        "PARCIAL": ["", "", "", "", ""],
                        "DEBE": [f"${total_op:,.2f}", f"${iva_calc:,.2f}", "", "", f"${total_op + iva_calc:,.2f}"],
                        "HABER": ["", "", f"${total_op:,.2f}", f"${iva_calc:,.2f}", f"${total_op + iva_calc:,.2f}"]
                    })
                    st.dataframe(df_e9, use_container_width=True)

                # --- CASO GENERAL ---
                else:
                    if monto_base > 0:
                        st.warning(f"⚠️ Operación general detectada con monto ${monto_base:,.2f}.")
                        st.markdown(html_diario, unsafe_allow_html=True)
                        df_gen = pd.DataFrame({
                            "CUENTA": ["102", "301", "SUMAS"],
                            "SUB CUENTA": [".01", ".01", ""],
                            "NOMBRE DE LA CUENTA": ["Bancos", "Capital Social", "Sumas Iguales"],
                            "PARCIAL": ["", "", ""],
                            "DEBE": [f"${monto_base:,.2f}", "", f"${monto_base:,.2f}"],
                            "HABER": ["", f"${monto_base:,.2f}", f"${monto_base:,.2f}"]
                        })
                        st.dataframe(df_gen, use_container_width=True)
                    else:
                        st.info("ℹ️ Operación informativa o sin montos detectados.")

            st.success("🎉 ¡Práctica procesada con éxito usando cuentas del JSON!")

    with pestana_buscador:
        st.subheader("🔍 Buscador de la Biblia de Cuentas")
        busqueda = st.text_input("Introduce código o nombre:", "115.06")
        
        if st.button("Buscar Cuenta"):
            encontrados = []
            busq = busqueda.strip().lower()
            try:
                # Buscar en las secciones del JSON que nos proporcionaste
                secciones = ["catalogo_separado", "cuentas_de_mayor", "subcuentas_y_auxiliares"]
                for sec in secciones:
                    if sec in catalogo:
                        for item in catalogo[sec]:
                            codigo = str(item.get("Código Completo", item.get("Código", ""))).lower()
                            nombre = str(item.get("Nombre de la Cuenta", "")).lower()
                            if busq in codigo or busq in nombre:
                                encontrados.append(item)
            except Exception:
                pass

            if encontrados:
                st.success("✨ Resultados en el catálogo:")
                for c in encontrados[:10]:
                    cod = c.get("Código Completo", c.get("Código", "N/A"))
                    nom = c.get("Nombre de la Cuenta", "N/A")
                    st.markdown(f"**Código:** `{cod}` — **{nom}**")
            else:
                st.warning("⚠️ No se encontró coincidencia directa.")
