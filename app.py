import streamlit as st
import pandas as pd
import json
import re

# Configuración de la página
st.set_page_config(page_title="Trapito el que lo lea", layout="centered")

st.title("IMIR 🤖📊 - Edición Martillito de Acero (Pro)")
st.markdown("Imir v.4.0 by pumps (Catálogo Completo Integrado)")

# Cargar la biblia de cuentas
@st.cache_data
def cargar_catalogo():
    try:
        with open("biblia.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

catalogo = cargar_catalogo()

# Función Mágica que consulta tu nuevo JSON
def obtener_nombre_cuenta(codigo_buscado):
    if catalogo is None:
        return "Cuenta Desconocida"
    
    codigo_str = str(codigo_buscado).strip()
    
    # Buscar primero en catalogo_separado (que tiene los códigos como string exacto)
    if "catalogo_separado" in catalogo:
        for c in catalogo["catalogo_separado"]:
            if str(c.get("Código Completo", "")).strip() == codigo_str:
                return c.get("Nombre de la Cuenta")
                
    # Si no lo encuentra, buscar en cuentas_de_mayor (por si le pasas el número pelón)
    if "cuentas_de_mayor" in catalogo:
        for c in catalogo["cuentas_de_mayor"]:
            cod = str(c.get("Código", ""))
            # Limpiamos los .0 para que cuadre
            if cod == codigo_str or cod.replace(".0", ".00") == codigo_str:
                return c.get("Nombre de la Cuenta")

    return "Cuenta Desconocida"

if catalogo is None:
    st.error("⚠️ No se encontró el archivo 'biblia.json'. ¡Guarda tu JSON gigantesto en la misma carpeta!")
else:
    pestana_generador, pestana_buscador = st.tabs(["🚀 Procesador Masivo CMYK", "🔍 Buscador de Cuentas (Nivel Dios)"])

    with pestana_generador:
        st.subheader("1. Pega tu Bloque de Operaciones")
        st.markdown("Pega tu lista de operaciones. Imir está adaptado para tu nuevo catálogo.")
        
        texto_masivo = st.text_area(
            "Enunciados de la práctica:",
            "1. El comitente nos envía mercancía en comisión por $1,300,000.\n"
            "2. El comitente nos envía $30,000 para gastos.\n"
            "3. Se venden mercancías en comisión al contado por $590,000."
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
                st.markdown("---")
                st.markdown(f"#### 📌 Análisis: _{bloque[:80]}..._")
                
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

                # --- LÓGICA 1. RECIBIMOS MERCANCÍAS AJENAS (Cuentas de orden) ---
                if "envía mercancía" in bloque_lower or ("comisión" in bloque_lower and "envía" in bloque_lower):
                    st.info("💡 Operación: Recepción de Mercancías del Comitente (Cuentas de Orden)")
                    st.markdown(html_diario, unsafe_allow_html=True)
                    df = pd.DataFrame({
                        # Usando los códigos exactos de tu JSON:
                        "CUENTA": ["814.01", "814.03", "SUMAS"], 
                        "NOMBRE DE LA CUENTA": [obtener_nombre_cuenta("814.01"), obtener_nombre_cuenta("814.03"), "Sumas Iguales"],
                        "DEBE": [f"${monto_base:,.2f}", "", f"${monto_base:,.2f}"],
                        "HABER": ["", f"${monto_base:,.2f}", f"${monto_base:,.2f}"]
                    })
                    st.dataframe(df, use_container_width=True)

                # --- LÓGICA 2. RECIBIMOS FONDOS PARA GASTOS ---
                elif "fondos" in bloque_lower or "para gastos" in bloque_lower:
                    st.info("💡 Operación: Recepción de Fondos del Comitente (Ingreso)")
                    st.markdown(html_ingreso, unsafe_allow_html=True)
                    df = pd.DataFrame({
                        "CUENTA": ["102.00", "205.00", "SUMAS"],
                        "NOMBRE DE LA CUENTA": [obtener_nombre_cuenta("102.00"), obtener_nombre_cuenta("205.00"), "Sumas Iguales"],
                        "DEBE": [f"${monto_base:,.2f}", "", f"${monto_base:,.2f}"],
                        "HABER": ["", f"${monto_base:,.2f}", f"${monto_base:,.2f}"]
                    })
                    st.dataframe(df, use_container_width=True)

                # --- LÓGICA 3. VENTA DE MERCANCÍAS EN COMISIÓN ---
                elif "venden" in bloque_lower and "comisión" in bloque_lower:
                    st.info("💡 Operación: Venta de Mercancía Ajena (Doble Registro)")
                    
                    if "contado" in bloque_lower or "cobro" in bloque_lower:
                        st.markdown(html_ingreso, unsafe_allow_html=True)
                        cta_cargo = "102.00"  # Bancos
                    else:
                        st.markdown(html_diario, unsafe_allow_html=True)
                        cta_cargo = "103.00"  # En tu nuevo JSON, Clientes es 103.00

                    # Registro de la deuda a favor del comitente
                    df1 = pd.DataFrame({
                        "CUENTA": [cta_cargo, "205.00", "SUMAS"],
                        "NOMBRE DE LA CUENTA": [obtener_nombre_cuenta(cta_cargo), obtener_nombre_cuenta("205.00"), "Sumas Iguales"],
                        "DEBE": [f"${monto_base:,.2f}", "", f"${monto_base:,.2f}"],
                        "HABER": ["", f"${monto_base:,.2f}", f"${monto_base:,.2f}"]
                    })
                    st.dataframe(df1, use_container_width=True)
                    
                    # Baja de la mercancía en cuentas de orden
                    st.markdown("**Baja de Mercancías en Cuentas de Orden:**")
                    df2 = pd.DataFrame({
                        "CUENTA": ["814.03", "814.01", "SUMAS"],
                        "NOMBRE DE LA CUENTA": [obtener_nombre_cuenta("814.03"), obtener_nombre_cuenta("814.01"), "Sumas Iguales"],
                        "DEBE": [f"${monto_base:,.2f}", "", f"${monto_base:,.2f}"],
                        "HABER": ["", f"${monto_base:,.2f}", f"${monto_base:,.2f}"]
                    })
                    st.dataframe(df2, use_container_width=True)

                # --- CASO GENERAL (Cualquier otra operación) ---
                else:
                    if monto_base > 0:
                        st.warning(f"⚠️ Operación general detectada con monto ${monto_base:,.2f}. Revisa el bloque.")
                    else:
                        st.info("ℹ️ Operación informativa o sin montos detectados.")

    with pestana_buscador:
        st.subheader("🔍 Buscador del Catálogo (Nivel Dios)")
        busqueda = st.text_input("Introduce código o nombre (Ej: 115, cliente, comitente):")
        
        if st.button("Buscar Cuenta"):
            encontrados = []
            busq = busqueda.strip().lower()
            
            # Buscar directo en catalogo_separado porque ahí tienes absolutamente todas
            if catalogo and "catalogo_separado" in catalogo:
                for item in catalogo["catalogo_separado"]:
                    codigo = str(item.get("Código Completo", "")).lower()
                    nombre = str(item.get("Nombre de la Cuenta", "")).lower()
                    tipo = str(item.get("Tipo (M/A)", "")).upper()
                    
                    if busq in codigo or busq in nombre:
                        encontrados.append((item.get("Código Completo"), item.get("Nombre de la Cuenta"), tipo))

            if encontrados:
                st.success(f"✨ ¡Bingo! Encontré {len(encontrados)} resultados:")
                for cod, nom, tipo in encontrados:
                    # Le puse colores visuales para que sepas si es Mayor o Auxiliar
                    etiqueta_tipo = "🟢 Mayor" if tipo == "M" else "🔵 Auxiliar"
                    st.markdown(f"**{etiqueta_tipo} | Código:** `{cod}` — **{nom}**")
            else:
                st.warning("⚠️ No se encontró la cuenta en este mega catálogo.")
