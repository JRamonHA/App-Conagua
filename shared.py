# Configuración de nombres de meses
MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

# Mapeo de estados
STATE_MAPPING = {
    "AGU": "Aguascalientes", "BCN": "Baja California", "BCS": "Baja California Sur",
    "CAM": "Campeche", "CHH": "Chihuahua", "CHP": "Chiapas", "CMX": "Ciudad de México",
    "COA": "Coahuila", "COL": "Colima", "DUR": "Durango", "GRO": "Guerrero",
    "GUA": "Guanajuato", "HID": "Hidalgo", "JAL": "Jalisco", "MEX": "México",
    "MIC": "Michoacán", "MOR": "Morelos", "NAY": "Nayarit", "NLE": "Nuevo León",
    "OAX": "Oaxaca", "PUE": "Puebla", "QUE": "Querétaro", "ROO": "Quintana Roo",
    "SIN": "Sinaloa", "SLP": "San Luis Potosí", "SON": "Sonora", "TAB": "Tabasco",
    "TAM": "Tamaulipas", "TLA": "Tlaxcala", "VER": "Veracruz", "YUC": "Yucatán", "ZAC": "Zacatecas"
}

# ----- FUNCIONES AUXILIARES -----
def month_names():
    """
    Devuelve la lista de nombres de los meses.
    """
    return MESES

def state_abbreviations(data):
    """
    Mapear las abreviaturas de los estados a sus nombres completos.
    """
    return data.rename(columns={"Abbreviation": "State"}).replace({"State": STATE_MAPPING})