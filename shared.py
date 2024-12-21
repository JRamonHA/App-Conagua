import pandas as pd
import json

# ----- RUTAS Y CONFIGURACIÓN -----
app_dir = "./data/"

# Cargar datasets
def load_data(file_name):
    """
    Carga un archivo CSV en un DataFrame.
    """
    file_path = app_dir + file_name
    return pd.read_csv(file_path, index_col="time", parse_dates=True)

data_Lluv = load_data("data_Lluv.csv")
data_Tmean = load_data("data_TMed.csv")
data_Tmax = load_data("data_TMax.csv")
data_Tmin = load_data("data_TMin.csv")

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

# Cargar archivo GeoJSON
def load_geojson(file_name):
    """
    Carga un archivo GeoJSON .
    """
    file_path = app_dir + file_name
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)

GEOJSON_DATA = load_geojson("Mexico.json")

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
