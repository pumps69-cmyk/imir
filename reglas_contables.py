def calcular_iva(monto_base, tipo="mas_iva"):
    """
    Calcula el IVA dependiendo de si el monto ya lo incluye o hay que agregarlo.
    Tasa estándar: 16% (0.16)
    """
    tasa = 0.16
    if tipo == "mas_iva":
        iva = monto_base * tasa
        total = monto_base + iva
        return {"base": monto_base, "iva": iva, "total": total}
    elif tipo == "incluido":
        base = monto_base / (1 + tasa)
        iva = monto_base - base
        return {"base": base, "iva": iva, "total": monto_base}
    return {"base": monto_base, "iva": 0.0, "total": monto_base}

def determinar_tipo_poliza(operacion):
    """
    Determina si la póliza debe ser de Ingreso, Egreso o Diario
    según las reglas contables generales.
    """
    if "transferencia" in operacion.lower() or "cheque" in operacion.lower():
        if "enviamos" in operacion.lower() or "pago" in operacion.lower():
            return "PÓLIZA DE EGRESO"
        elif "recibimos" in operacion.lower() or "depósito" in operacion.lower():
            return "PÓLIZA DE INGRESO"
    
    # Por defecto, operaciones a crédito o traspasos internos van por Diario
    return "PÓLIZA DE DIARIO"
