import plotly.express as px
from plotnine import (
    ggplot, aes, geom_line, geom_point, labs, theme_minimal, scale_x_continuous, theme
)
import pandas as pd
from shared import MESES

# ----- FUNCIONES PARA MAPAS -----

def choropleth_map(data, geojson_data, title, color_scale, value_label="Value"):
    """
    Genera un mapa choropleth con Plotly Express.

    Parameters:
    - data: DataFrame con las columnas ['State', 'Value']
    - geojson_data: GeoJSON con la geometría de los estados
    - title: Título del mapa
    - color_scale: Escala de color para el mapa
    - value_label: Etiqueta para los valores en la leyenda

    Returns:
    - fig: Figura de Plotly
    """
    fig = px.choropleth(
        data,
        geojson=geojson_data,
        locations="State",
        featureidkey="properties.ESTADO",
        color="Value",
        color_continuous_scale=color_scale,
        title=title,
        labels={"Value": value_label},
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_x=0.5)
    return fig


def choropleth_data(data, year, state_mapping, aggregation="mean"):
    """
    Filtra y procesa datos para mapas, devolviendo un DataFrame con columnas 'State' y 'Value'.

    Parameters:
    - data: DataFrame con datos de los estados
    - year: Año a filtrar
    - state_mapping: Diccionario para mapear abreviaturas a nombres de estados
    - aggregation: Método de agregación ('mean' o 'sum')

    Returns:
    - DataFrame listo para usarse en el mapa choropleth
    """
    filtered_data = data[data.index.year == year]
    if aggregation == "mean":
        processed_data = filtered_data.mean(axis=0).reset_index()
    else:
        processed_data = filtered_data.sum(axis=0).reset_index()
    
    processed_data.columns = ["Abbreviation", "Value"]
    processed_data["State"] = processed_data["Abbreviation"].map(state_mapping)
    return processed_data[["State", "Value"]]


# ----- FUNCIONES PARA GRÁFICAS -----

def line_plot(df_plot, title, subtitle, y_label):
    """
    Genera un gráfico de líneas usando plotnine.

    Parameters:
    - df_plot: DataFrame con las columnas ['Mes', 'Value', 'Estado']
    - title: Título del gráfico
    - subtitle: Subtítulo del gráfico
    - y_label: Etiqueta para el eje Y

    Returns:
    - Gráfico generado con plotnine
    """
    return (
        ggplot(df_plot, aes(x="Mes", y="Value", color="Estado"))
        + geom_line(size=1.25)
        + geom_point(size=2.5)
        + labs(title=title, subtitle=subtitle, x="Mes", y=y_label)
        + scale_x_continuous(breaks=range(1, 13), labels=MESES)
        + theme_minimal()
        + theme(figure_size=(10, 4))
    )


def line_plot_data(data, year=None, states=None, aggregation="mean"):
    """
    Prepara datos para un gráfico de líneas.

    Parameters:
    - data: DataFrame con datos de los estados
    - year: Año a filtrar (opcional)
    - states: Lista de estados seleccionados
    - aggregation: Tipo de agregación ('mean' o 'sum')

    Returns:
    - DataFrame listo para usarse en el gráfico
    """
    if year:
        data = data[data.index.year == year]
    if aggregation == "mean":
        data = data.groupby(data.index.month).mean()
    else:
        data = data.groupby(data.index.month).sum()
    
    df_plot = pd.DataFrame()
    for state in states:
        if state in data.columns:
            temp_df = data[[state]].reset_index()
            temp_df.columns = ["Mes", "Value"]
            temp_df["Estado"] = state
            df_plot = pd.concat([df_plot, temp_df], ignore_index=True)
    
    df_plot["Mes"] = df_plot["Mes"].astype(int)
    return df_plot

# ----- FUNCIONES PARA HEATMAPS -----

def heatmap(data, title, color_scale, value_label="Value"):
    """
    Genera un heatmap con Plotly Express.

    Parameters:
    - data: DataFrame con los meses como filas y estados como columnas.
    - title: Título del heatmap.
    - color_scale: Escala de colores para el heatmap.
    - value_label: Etiqueta para los valores en la leyenda.

    Returns:
    - fig: Figura de Plotly.
    """
    fig = px.imshow(
        data,
        labels=dict(x="Estado", y="Mes", color=value_label),
        x=data.columns,
        y=data.index,
        color_continuous_scale=color_scale,
        aspect="auto",
    )
    fig.update_layout(title=title, title_x=0.5, xaxis_title="Estado", yaxis_title="Mes")
    return fig


def heatmap_data(data, year=None, aggregation="sum", historical=False):
    """
    Prepara datos para un heatmap a partir de un DataFrame.

    Parameters:
    - data: DataFrame con datos de los estados y tiempo.
    - year: Año a filtrar (opcional).
    - aggregation: Método de agregación ('sum' o 'mean').
    - historical: Si es True, calcula promedios históricos, de lo contrario procesa el año.

    Returns:
    - DataFrame pivotado con los meses como índices y estados como columnas.
    """
    data = data.copy()
    data["Mes"] = data.index.month

    if historical:
        # Promedios históricos por mes
        data_long = data.melt(id_vars=["Mes"], var_name="Estado", value_name="Valor")
        grouped_data = data_long.groupby(["Mes", "Estado"], as_index=False).agg({"Valor": "mean"})
    else:
        # Filtrar por año y agrupar por mes y estado
        if year:
            data = data[data.index.year == year]
        data_long = data.melt(id_vars=["Mes"], var_name="Estado", value_name="Valor")
        grouped_data = data_long.groupby(["Mes", "Estado"], as_index=False).agg({"Valor": aggregation})

    # Crear tabla pivotada
    pivot_data = grouped_data.pivot(index="Mes", columns="Estado", values="Valor")

    # Reemplazar el índice numérico de los meses con nombres de meses
    pivot_data.index = MESES [:len(pivot_data)]
    
    pivot_data = pivot_data.fillna(0)
    return pivot_data
