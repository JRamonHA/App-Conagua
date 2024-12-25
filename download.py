import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def fix_file(df, file_name):
    """Corrige estructuras específicas de archivos según su nombre."""
    if file_name == "201401010000Lluv.csv":
        if 'CVE_SIH' in df.columns and 'ESTADO' in df.columns:
            df['ESTADO'] = df['CVE_SIH']
            df.drop(columns=['CVE_SIH'], inplace=True)
    elif file_name == "202109010000Lluv.csv" and '09-sep' in df.columns:
        df.rename(columns={'09-sep': 'sep-21'}, inplace=True)
    return df

def process_conagua_data(df, variable):
    """Procesa datos específicos de temperatura o lluvia."""
    if variable == "TMed" and 'Edo' in df.columns and 'Tmed' in df.columns:
        df = df[['Edo', 'Tmed']]
        df = df.groupby('Edo').mean().T
    elif variable == "TMax" and 'Edo' in df.columns and 'Tmax' in df.columns:
        df = df[['Edo', 'Tmax']]
        df = df.groupby('Edo').mean().T
    elif variable == "TMin" and 'Edo' in df.columns and 'Tmin' in df.columns:
        df = df[['Edo', 'Tmin']]
        df = df.groupby('Edo').mean().T
    else:
        month_column = next((col for col in df.columns if col.lower().startswith(
            ('ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'))), None)
        if month_column:
            state_column = 'ESTADO' if 'ESTADO' in df.columns else 'EDO'
            df = df[[state_column, month_column]]
            df = df.groupby(state_column).mean().T
    
    # Redondear los datos a 2 decimales
    df = df.round(2)
    return df

def read_conagua(path, variable):
    """Carga y procesa un archivo CSV de CONAGUA con diferentes estructuras."""
    try:
        df = pd.read_csv(path, encoding='latin-1')
        file_name = path.split('/')[-1]
        df = fix_file(df, file_name)
        df = process_conagua_data(df, variable)

        # Agregar columna de tiempo
        year, month = file_name[:4], file_name[4:6]
        df['time'] = pd.to_datetime(year + month, format='%Y%m')
        df.set_index('time', inplace=True)
        return df
    except Exception as e:
        return None

def gather_columns(df):
    """Unifica columnas duplicadas en el DataFrame."""
    if 'CDMX' in df.columns and 'DF' in df.columns:
        df['CMX'] = df['CDMX'] + df['DF']
    if 'MÉX' in df.columns:
        df['MEX'] = df['MÉX'] + df['MEX']
    if 'TAMP' in df.columns:
        df['TAM'] = df.get('TAMP', 0) + df.get('TAMPS', 0) + df.get('TAMS', 0)
    if 'HDO' in df.columns:
        df['HGO'] = df['HDO'] + df['HGO']
    if 'B.C.' in df.columns:
        df['BC'] = df['B.C.'] + df['BC']
    if 'B.C.S.' in df.columns:
        df['BCS'] = df['B.C.S.'] + df['BCS']
    # Eliminar columnas redundantes
    df.drop(columns=['DF', 'CDMX', 'MÉX', 'TAMPS', 'TAMS', 'TAMP', 'HDO', 'B.C.', 'B.C.S.'], errors='ignore', inplace=True)
    return df

def rename_columns(df):
    """Renombra las columnas del DataFrame según el estándar ISO 3166-2:MX."""
    iso_mapping = {
        'AGS': 'AGU', 'BC': 'BCN', 'BCS': 'BCS', 'CAMP': 'CAM', 'CHIH': 'CHH',
        'CHIS': 'CHP', 'COAH': 'COA', 'COL': 'COL', 'DGO': 'DUR', 'GRO': 'GRO',
        'GTO': 'GUA', 'HGO': 'HID', 'JAL': 'JAL', 'MEX': 'MEX', 'MICH': 'MIC',
        'MOR': 'MOR', 'NAY': 'NAY', 'NL': 'NLE', 'OAX': 'OAX', 'PUE': 'PUE',
        'QRO': 'QUE', 'QROO': 'ROO', 'SIN': 'SIN', 'SLP': 'SLP', 'SON': 'SON',
        'TAB': 'TAB', 'TLAX': 'TLA', 'VER': 'VER', 'YUC': 'YUC', 'ZAC': 'ZAC',
        'CMX': 'CMX', 'TAM': 'TAM'
    }
    return df.rename(columns=iso_mapping, errors='ignore')

def get_conagua_data(base_url, years, months, variable):
    """Descarga y procesa datos de múltiples meses y años para una variable específica."""
    def process_file(year, month):
        path = f'{base_url}/{year}{month:02d}010000{variable}.csv'
        return read_conagua(path, variable)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, year, month) for year in years for month in months]
        results = [future.result() for future in futures if future.result() is not None]

    if results:
        combined_data = pd.concat(results)
        combined_data.fillna(0, inplace=True)
        combined_data = gather_columns(combined_data)
        combined_data = rename_columns(combined_data)
        return combined_data
    else:
        return None

def save_to_csv(name, df):
    """Guarda un DataFrame en un archivo CSV con columnas en orden alfabético."""
    if df is not None:
        df = df[sorted(df.columns)]
        df.to_csv(f'{name}.csv')

# URL base para los datos
base_url = 'https://smn.conagua.gob.mx/tools/RESOURCES/com_archivo_datos_resumenes'

# Años y meses a procesar
years = range(2014, 2025, 1)
months = range(1, 13, 1)

# Variables a procesar
variables = ["Lluv", "TMed", "TMax", "TMin"]
for variable in variables:
    data = get_conagua_data(base_url, years, months, variable)
    save_to_csv(f"data_{variable}", data)
