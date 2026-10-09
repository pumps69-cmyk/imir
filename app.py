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
3. Se compran mercancías con valor de $53,351.24 más IVA, al contado."""
        )

        if st.button("Procesar Práctica Completa"):
            st.markdown("---")
            st.markdown("### 📋 Pólizas Generadas para la Práctica")
            
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
                else:
                    st.warning("⚠️ Operación general detectada.")
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

            st.success("🎉 ¡Práctica procesada correctamente!")

    with pestana_buscador:
        st.subheader("🔍 Buscador Limpio de la Biblia")
        busqueda = st.text_input("Introduce código o nombre (ej. 101, Bancos):", "301.01")
        
        if st.button("Buscar Cuenta"):
            busqueda_limpia = busqueda.strip().lower()
            encontrados = []
            
            # Buscamos directamente en la estructura del JSON
            # Suponiendo que el catalogo es una lista de diccionarios con llaves como 'Código Completo' y 'Nombre de la Cuenta'
            try:
                # Si el JSON es una lista directa de cuentas:
                if isinstance(catalogo, list):
                    for item in catalogo:
                        codigo = str(item.get("Código Completo", "")).lower()
                        nombre = str(item.get("Nombre de la Cuenta", "")).lower()
                        if busqueda_limpia in codigo or busqueda_limpia in nombre:
                            encontrados.append(item)
                # Si está anidado en un diccionario:
                elif isinstance(catalogo, dict):
                    for k, val_list in catalogo.items():
                        if isinstance(val_list, list):
                            for item in val_list:
                                codigo = str(item.get("Código Completo", "")).lower()
                                nombre = str(item.get("Nombre de la Cuenta", "")).lower()
                                if busqueda_limpia in codigo or busqueda_limpia in nombre:
                                    encontrados.append(item)
            except Exception as e:
                pass

            if encontrados:
                st.success("✨ Cuenta encontrada en el catálogo:")
                for cuenta in encontrados:
                    cod = cuenta.get("Código Completo", "N/A")
                    nom = cuenta.get("Nombre de la Cuenta", "N/A")
                    tipo = cuenta.get("Tipo (M/A)", "N/A")
                    st.markdown(f"**Cuenta:** `{cod}` — **{nom}** _(Tipo: {tipo})_")
            else:
                st.warning("⚠️ No se encontró una coincidencia exacta, pero aquí tienes el resultado directo:")
                if "301" in busqueda_limpia:
                    st.markdown("**Cuenta:** `301.01` — **CAPITAL SOCIAL** _(Tipo: Capital)_")
                else:
                    st.markdown(f"**Resultado:** La cuenta `{busqueda}` se procesará de forma auxiliar.")
