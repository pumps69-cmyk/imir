import re

def extraer_datos_operacion(texto):
    """
    Analiza el texto de entrada y extrae la acción principal,
    el monto base y si involucra IVA o condiciones especiales.
    """
    texto_lower = texto.lower()
    
    # 1. Detectar la acción principal
    accion = "desconocida"
    if "enviamos" in texto_lower or "envío" in texto_lower:
        accion = "envio_consignacion"
    elif "vendid" in texto_lower or "vendió" in texto_lower:
        accion = "venta"
    elif "compr" in texto_lower:
        accion = "compra"
    elif "gastos" in texto_lower or "pago" in texto_lower:
        accion = "gasto_o_pago"
    elif "devoluci" in texto_lower:
        accion = "devolucion"

    # 2. Extraer montos numéricos usando expresiones regulares
    # Busca números con formato de dinero (ej. $1,000.00 o 50)
    patron_dinero = r'\$?([\d,]+\.?\d*)'
    coincidencias = re.findall(patron_dinero, texto)
    
    # Limpiamos y convertimos a flotantes los números encontrados
    montos = []
    for c in coincidencias:
        c_limpio = c.replace(',', '')
        if c_limpio:
            try:
                montos.append(float(c_limpio))
            except ValueError:
                pass

    # 3. Detectar impuestos o condiciones fiscales
    incluye_iva = "más iva" in texto_lower or "mas iva" in texto_lower
    iva_incluido = "iva incluido" in texto_lower

    return {
        "accion": accion,
        "montos_detectados": montos,
        "mas_iva": incluye_iva,
        "iva_incluido": iva_incluido
    }
