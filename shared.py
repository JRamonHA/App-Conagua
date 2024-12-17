from pathlib import Path
import pandas as pd
import json

app_dir = Path(__file__).parent/'data'

data_lluv = pd.read_csv(app_dir / "data_lluv.csv",index_col="time", parse_dates=True)
data_Tmean = pd.read_csv(app_dir / "data_Tmean.csv", index_col="time", parse_dates=True)
data_Tmax = pd.read_csv(app_dir / "data_Tmax.csv", index_col="time", parse_dates=True)
data_Tmin= pd.read_csv(app_dir / "data_Tmin.csv", index_col="time", parse_dates=True)

data_lluv.fillna(0, inplace=True)
data_Tmean.fillna(0, inplace=True)
data_Tmax.fillna(0, inplace=True)
data_Tmin.fillna(0, inplace=True)

lluvia = list(data_lluv.columns)
media = list(data_Tmean.columns)
maxima =list(data_Tmax)
minima = list(data_Tmin)

meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# Crear un mapeo de abreviaturas de estados a nombres completos
state_mapping = {
    "AGU": "Aguascalientes", "BCN": "Baja California", "BCS": "Baja California Sur",
    "CAM": "Campeche", "CHH": "Chihuahua", "CHP": "Chiapas",
    "CMX": "Ciudad de México", "COA": "Coahuila", "COL": "Colima", "DUR": "Durango", "GRO": "Guerrero",
    "GUA": "Guanajuato", "HID": "Hidalgo", "JAL": "Jalisco", "MEX": "México",
    "MIC": "Michoacán", "MOR": "Morelos", "NAY": "Nayarit", "NLE": "Nuevo León",
    "OAX": "Oaxaca", "PUE": "Puebla", "QUE": "Querétaro", "ROO": "Quintana Roo",
    "SIN": "Sinaloa", "SLP": "San Luis Potosí", "SON": "Sonora", "TAB": "Tabasco",
    "TAM": "Tamaulipas", "TLA": "Tlaxcala", "VER": "Veracruz", "YUC": "Yucatán", "ZAC": "Zacatecas"
}

# Cargar el archivo GeoJSON de los estados de México
with open("data/Mexico.json", encoding="utf-8") as f:
    geojson_data = json.load(f)
