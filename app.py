import pandas as pd
from shared import *
import plotly.express as px
from plotnine import (
    ggplot, aes, geom_line, geom_point, labs, theme_minimal, 
    scale_x_continuous, theme
)
from shiny import App, Inputs, reactive, render, ui
from shinywidgets import render_widget, output_widget

# Definición de la interfaz de usuario
app_ui = ui.page_navbar(
    ui.nav_spacer(),
    ui.nav_panel("Precipitación",
        ui.navset_card_underline(
            ui.nav_panel("Mapa geográfico",
                ui.input_select(
                    "year_precipitation",
                    "Selecciona el año:",
                    choices=[str(year) for year in data_lluv.index.year.unique()],
                ),
                output_widget("precipitation_map"),
            ),
            ui.nav_panel("Gráfico",
            ui.layout_columns(
                ui.input_select(
                    "type_plot_rain",
                    "Selecciona el tipo de gráfico:",
                    choices=["Anual", "Histórico"],
                    selected="Anual",
                ),
                ui.input_select(
                    "year_precipitation_plot",
                    "Selecciona el año:",
                    choices=[str(year) for year in data_lluv.index.year.unique()],
                ),     
                ui.input_selectize(  
                    "precipitation_states",  
                    "Selecciona el estado:",  
                    choices=lluvia,  
                    multiple=True,  
                ),
            ), 
                ui.output_plot("precipitation_plot"),
            ),
            ui.nav_panel("Mapa de calor",
            ui.layout_columns(
                ui.input_select(
                    "type_hm_rain",
                    "Selecciona el tipo de mapa:",
                    choices=["Anual", "Histórico"],
                    selected="Anual",
                ),
                ui.input_select(
                    "year_precipitation_hm",
                    "Selecciona el año:",
                    choices=[str(year) for year in data_lluv.index.year.unique()],
                ),
            ), 
                output_widget("precipitation_hm"),
            ),
            title="Resúmenes anuales y mensuales de lluvia",
        )
    ),
    ui.nav_panel("Temperatura media",
        ui.navset_card_underline(
            ui.nav_panel("Mapa geográfico",
                ui.input_select(
                    "year_temp_mean",
                    "Selecciona el año:",
                    {str(year): str(year) for year in range(2013, 2025)},
                ),
                output_widget("temp_mean_map"),
            ),
            ui.nav_panel("Gráfico",
            ui.layout_columns(
                ui.input_select(
                    "type_plot_tmean",
                    "Selecciona el tipo de gráfico:",
                    choices=["Anual", "Histórico"],
                    selected="Anual",
                ),
                ui.input_select(
                    "year_tmean_plot",
                    "Selecciona el año:",
                    choices=[str(year) for year in data_Tmean.index.year.unique()],
                ),     
                ui.input_selectize(  
                    "tmean_states",  
                    "Selecciona el estado:",  
                    choices=media,  
                    multiple=True,  
                ),
            ), 
                ui.output_plot("tmean_plot"),
            ),
            ui.nav_panel("Mapa de calor",
            ui.layout_columns(
                ui.input_select(
                    "type_hm_tmean",
                    "Selecciona el tipo de mapa:",
                    choices=["Anual", "Histórico"],
                    selected="Anual",
                ),
                ui.input_select(
                    "year_tmean_hm",
                    "Selecciona el año:",
                    choices=[str(year) for year in data_Tmean.index.year.unique()],
                ),
            ), 
                output_widget("tmean_hm"),
            ),
            title="Resúmenes anuales y mensuales de temperatura media",
        )
    ),
    ui.nav_panel("Temperatura máxima",
        ui.navset_card_underline(
            ui.nav_panel("Mapa geográfico",
                ui.input_select(
                    "year_temp_max",
                    "Selecciona el año:",
                    {str(year): str(year) for year in range(2013, 2025)},
                ),
                output_widget("temp_max_map"),
            ),
            ui.nav_panel("Gráfico",
            ui.layout_columns(
                ui.input_select(
                    "type_plot_tmax",
                    "Selecciona el tipo de gráfico:",
                    choices=["Anual", "Histórico"],
                    selected="Anual",
                ),
                ui.input_select(
                    "year_tmax_plot",
                    "Selecciona el año:",
                    choices=[str(year) for year in data_Tmax.index.year.unique()],
                ),     
                ui.input_selectize(  
                    "tmax_states",  
                    "Selecciona el estado:",  
                    choices=maxima,  
                    multiple=True,  
                ),
            ), 
                ui.output_plot("tmax_plot"),
            ),
            ui.nav_panel("Mapa de calor",
            ui.layout_columns(
                ui.input_select(
                    "type_hm_tmax",
                    "Selecciona el tipo de mapa:",
                    choices=["Anual", "Histórico"],
                    selected="Anual",
                ),
                ui.input_select(
                    "year_tmax_hm",
                    "Selecciona el año:",
                    choices=[str(year) for year in data_Tmax.index.year.unique()],
                ),
            ), 
                output_widget("tmax_hm"),
            ),
            title="Resúmenes anuales y mensuales de temperatura máxima",
        )
    ),
    ui.nav_panel("Temperatura mínima",
        ui.navset_card_underline(
            ui.nav_panel("Mapa geográfico",
                ui.input_select(
                    "year_temp_min",
                    "Selecciona el año:",
                    {str(year): str(year) for year in range(2013, 2025)},
                ),
                output_widget("temp_min_map"),
            ),
            ui.nav_panel("Gráfico",
            ui.layout_columns(
                ui.input_select(
                    "type_plot_tmin",
                    "Selecciona el tipo de gráfico:",
                    choices=["Anual", "Histórico"],
                    selected="Anual",
                ),
                ui.input_select(
                    "year_tmin_plot",
                    "Selecciona el año:",
                    choices=[str(year) for year in data_Tmin.index.year.unique()],
                ),     
                ui.input_selectize(  
                    "tmin_states",  
                    "Selecciona el estado:",  
                    choices=minima,  
                    multiple=True,  
                ),
            ), 
                ui.output_plot("tmin_plot"),
            ),
            ui.nav_panel("Mapa de calor",
            ui.layout_columns(
                ui.input_select(
                    "type_hm_tmin",
                    "Selecciona el tipo de mapa:",
                    choices=["Anual", "Histórico"],
                    selected="Anual",
                ),
                ui.input_select(
                    "year_tmin_hm",
                    "Selecciona el año:",
                    choices=[str(year) for year in data_Tmin.index.year.unique()],
                ),
            ), 
                output_widget("tmin_hm"),
            ),
            title="Resúmenes anuales y mensuales de temperatura mínima",
        )
    ),
    title="Explorador CONAGUA",
    id="page",
)

# Definición del servidor
def server(input:Inputs, output, session):
    @render_widget
    def precipitation_map():
        # Filtrar los datos del año seleccionado
        selected_year = int(input.year_precipitation())  # Año seleccionado por el usuario
        data_rain = data_lluv[data_lluv.index.year == selected_year]

        # Agrupar los datos por estado
        data_year_selected = data_rain.sum(axis=0).reset_index()
        data_year_selected.columns = ['Abbreviation', 'Value']
        data_year_selected['Value'] /= 10  # Convertir de mm a cm

        # Mapear las abreviaturas de los estados a sus nombres completos
        data_year_selected['State'] = data_year_selected['Abbreviation'].map(state_mapping)

        # Unir los datos con el GeoJSON de los estados
        geojson_states = {feature["properties"]["ESTADO"]: feature for feature in geojson_data["features"]}
        anual = data_year_selected[['State', 'Value']]

        # Crear el gráfico interactivo con Plotly
        fig = px.choropleth(
            anual,
            geojson=geojson_data,
            locations="State",
            featureidkey="properties.ESTADO",
            color="Value",
            color_continuous_scale="Viridis_r",
            title=f"Precipitación anual {selected_year}",
            labels={"Value": "Precipitación (cm)"}
        )

        # Ajustar la visualización del mapa
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(title_x=0.5)

        return fig
    
    @render_widget
    def temp_mean_map():
        # Filtrar los datos del año seleccionado
        selected_year = int(input.year_temp_mean())  # Año seleccionado por el usuario
        data_mean = data_Tmean[data_Tmean.index.year == selected_year]

        # Agrupar los datos por estado 
        data_year_selected = data_mean.mean(axis=0).reset_index()
        data_year_selected.columns = ['Abbreviation', 'Value']
        
        # Mapear las abreviaturas de los estados a sus nombres completos
        data_year_selected['State'] = data_year_selected['Abbreviation'].map(state_mapping)

        # Unir los datos con el GeoJSON de los estados
        geojson_states = {feature["properties"]["ESTADO"]: feature for feature in geojson_data["features"]}
        anual = data_year_selected[['State', 'Value']]

        # Crear el gráfico interactivo con Plotly
        fig = px.choropleth(
            anual,
            geojson=geojson_data,
            locations="State",
            featureidkey="properties.ESTADO", 
            color="Value",
            color_continuous_scale="sunsetdark",
            title=f"Temperatura media promedio {selected_year}",
            labels={"Value": "Temperatura (°C)"}
        )

        # Ajustar la visualización del mapa
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(title_x=0.5) 

        return fig
    
    @render_widget
    def temp_max_map():
        # Filtrar los datos del año seleccionado
        selected_year = int(input.year_temp_max())  # Año seleccionado por el usuario
        data_max = data_Tmax[data_Tmax.index.year == selected_year]

        # Agrupar los datos por estado 
        data_year_selected = data_max.mean(axis=0).reset_index()
        data_year_selected.columns = ['Abbreviation', 'Value']
        
        # Mapear las abreviaturas de los estados a sus nombres completos
        data_year_selected['State'] = data_year_selected['Abbreviation'].map(state_mapping)

        # Unir los datos con el GeoJSON de los estados
        geojson_states = {feature["properties"]["ESTADO"]: feature for feature in geojson_data["features"]}
        anual = data_year_selected[['State', 'Value']]

        # Crear el gráfico interactivo con Plotly
        fig = px.choropleth(
            anual,
            geojson=geojson_data,
            locations="State",
            featureidkey="properties.ESTADO", 
            color="Value",
            color_continuous_scale="oranges",
            title=f"Temperatura máxima promedio {selected_year}",
            labels={"Value": "Temperatura (°C)"}
        )

        # Ajustar la visualización del mapa
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(title_x=0.5)

        return fig
    
    @render_widget
    def temp_min_map():
        # Filtrar los datos del año seleccionado
        selected_year = int(input.year_temp_min())  # Año seleccionado por el usuario
        data_min = data_Tmin[data_Tmin.index.year == selected_year]

        # Agrupar los datos por estado
        data_year_selected = data_min.mean(axis=0).reset_index()
        data_year_selected.columns = ['Abbreviation', 'Value']
        
        # Mapear las abreviaturas de los estados a sus nombres completos
        data_year_selected['State'] = data_year_selected['Abbreviation'].map(state_mapping)

        # Unir los datos con el GeoJSON de los estados
        geojson_states = {feature["properties"]["ESTADO"]: feature for feature in geojson_data["features"]}
        anual = data_year_selected[['State', 'Value']]

        # Crear el gráfico interactivo con Plotly
        fig = px.choropleth(
            anual,
            geojson=geojson_data,
            locations="State",
            featureidkey="properties.ESTADO", 
            color="Value",
            color_continuous_scale="blues",
            title=f"Temperatura mínima promedio {selected_year}",
            labels={"Value": "Temperatura (°C)"}
        )

        # Ajustar la visualización del mapa
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(title_x=0.5,)

        return fig
    
    @reactive.calc()
    def selected_states_rain():
        return input.precipitation_states()

    @reactive.calc()
    def selected_year_rain():
        return int(input.year_precipitation_plot())  

    @render.plot
    def precipitation_plot():
        # Obtener estados seleccionados
        estados = selected_states_rain()
        if not estados:
            return None  # No generar gráfico si no hay estados seleccionados

        # Verificamos el tipo de gráfico seleccionado
        if input.type_plot_rain() == "Anual":
            # Obtener el año seleccionado
            year = selected_year_rain()

            # Filtrar los datos para el año deseado
            data_lluv_year = data_lluv[data_lluv.index.year == year]

            # Crear un DataFrame vacío para almacenar los datos combinados
            df_plot = pd.DataFrame()

            # Iterar sobre los estados seleccionados
            for estado in estados:
                if estado in data_lluv_year.columns:
                    temp_df = data_lluv_year[[estado]].reset_index().rename(columns={"time": "Mes", estado: "Precipitación"})
                    temp_df["Mes"] = temp_df["Mes"].dt.month  # Extraer el mes
                    temp_df["Precipitación"] = temp_df["Precipitación"] / 10  # Convertir de mm a cm
                    temp_df["Estado"] = estado
                    df_plot = pd.concat([df_plot, temp_df], ignore_index=True)

            # Asegurarse de que el DataFrame no esté vacío
            if df_plot.empty:
                return None

            # Crear el gráfico con plotnine
            plot = (
                ggplot(df_plot, aes(x="Mes", y="Precipitación", color="Estado"))
                + geom_line(size=1.25, show_legend=True, linetype="solid")
                + geom_point(size=2.5)
                + labs(
                    title="Precipitación mensual acumulada", subtitle=f"Distribución de lluvia total por mes en el año {year}",
                    x="Mes", y="Precipitación (cm)"
                )
                + scale_x_continuous(breaks=range(1, 13), labels=meses)
                + theme_minimal()
                + theme(figure_size=(10, 4))
            )

        else:
            estados = selected_states_rain()
            
            if not estados:
                return None  # No generar gráfico si no se selecciona ningún estado
        
            # Agrupar los datos por mes
            grouped_data = data_lluv.groupby(data_lluv.index.month).mean() / 10

            # Crear un DataFrame vacío para almacenar los datos combinados
            df_plot = pd.DataFrame()

            # Iterar sobre los estados seleccionados
            for estado in estados:
                if estado in grouped_data.columns:
                    temp_df = grouped_data.reset_index()[["time", estado]].rename(columns={"time": "Mes", estado: "Precipitación"})
                    temp_df["Estado"] = estado
                    df_plot = pd.concat([df_plot, temp_df], ignore_index=True)

            # Convertir la columna "Mes" en tipo entero
            df_plot["Mes"] = df_plot["Mes"].astype(int)

            # Crear el gráfico con plotnine
            plot = (
                ggplot(df_plot, aes(x="Mes", y="Precipitación", color="Estado"))
                + geom_line(size=1.25, show_legend=True, linetype="solid")
                + geom_point(size=2)
                + labs(
                    title="Promedio histórico de precipitación mensual", subtitle="Datos calculados a partir de los registros de 2013 a 2024",
                    x="Mes", y="Precipitación (cm)"
                )
                + scale_x_continuous(breaks=range(1, 13), labels=meses) 
                + theme_minimal()
                + theme(figure_size=(10, 4))
            )

        return plot
    
    @reactive.calc()
    def selected_states_tmean():
        return input.tmean_states()

    @reactive.calc()
    def selected_year_tmean():
        return int(input.year_tmean_plot())  

    @render.plot
    def tmean_plot():
        # Obtener estados seleccionados
        estados = selected_states_tmean()
        if not estados:
            return None  # No generar gráfico si no hay estados seleccionados

        # Verificamos el tipo de gráfico seleccionado
        if input.type_plot_tmean() == "Anual":
            # Obtener el año seleccionado
            year = selected_year_tmean()

            # Filtrar los datos para el año deseado
            data_tmean_year = data_Tmean[data_Tmean.index.year == year]

            # Crear un DataFrame vacío para almacenar los datos combinados
            df_plot = pd.DataFrame()

            # Iterar sobre los estados seleccionados
            for estado in estados:
                if estado in data_tmean_year.columns:
                    temp_df = data_tmean_year[[estado]].reset_index().rename(columns={"time": "Mes", estado: "Temperatura"})
                    temp_df["Mes"] = temp_df["Mes"].dt.month  # Extraer el mes
                    temp_df["Estado"] = estado
                    df_plot = pd.concat([df_plot, temp_df], ignore_index=True)

            # Asegurarse de que el DataFrame no esté vacío
            if df_plot.empty:
                return None

            # Crear el gráfico con plotnine
            plot = (
                ggplot(df_plot, aes(x="Mes", y="Temperatura", color="Estado"))
                + geom_line(size=1.25, show_legend=True, linetype="solid")
                + geom_point(size=2.5)
                + labs(
                    title="Temperatura media promedio", subtitle=f"Variación de la temperatura media por mes en el año {year}",
                    x="Mes", y="Temperatura (°C)"
                )
                + scale_x_continuous(breaks=range(1, 13), labels=meses)
                + theme_minimal()
                + theme(figure_size=(10, 4))
            )

        else:
            estados = selected_states_tmean()
            
            if not estados:
                return None  # No generar gráfico si no se selecciona ningún estado
        
            # Agrupar los datos por mes
            grouped_data = data_Tmean.groupby(data_Tmean.index.month).mean()

            # Crear un DataFrame vacío para almacenar los datos combinados
            df_plot = pd.DataFrame()

            # Iterar sobre los estados seleccionados
            for estado in estados:
                if estado in grouped_data.columns:
                    temp_df = grouped_data.reset_index()[["time", estado]].rename(columns={"time": "Mes", estado: "Temperatura"})
                    temp_df["Estado"] = estado
                    df_plot = pd.concat([df_plot, temp_df], ignore_index=True)

            # Convertir la columna "Mes" en tipo entero
            df_plot["Mes"] = df_plot["Mes"].astype(int)

            # Crear el gráfico con plotnine
            plot = (
                ggplot(df_plot, aes(x="Mes", y="Temperatura", color="Estado"))
                + geom_line(size=1.25, show_legend=True, linetype="solid")
                + geom_point(size=2)
                + labs(
                    title="Promedio histórico de temperatura media mensual", subtitle="Datos calculados a partir de los registros de 2013 a 2024",
                    x="Mes", y="Temperatura (°C)"
                )
                + scale_x_continuous(breaks=range(1, 13), labels=meses) 
                + theme_minimal()
                + theme(figure_size=(10, 4))
            )

        return plot
    
    @reactive.calc()
    def selected_states_tmax():
        return input.tmax_states()

    @reactive.calc()
    def selected_year_tmax():
        return int(input.year_tmax_plot())  

    @render.plot
    def tmax_plot():
        # Obtener estados seleccionados
        estados = selected_states_tmax()
        if not estados:
            return None  # No generar gráfico si no hay estados seleccionados

        # Verificamos el tipo de gráfico seleccionado
        if input.type_plot_tmax() == "Anual":
            # Obtener el año seleccionado
            year = selected_year_tmax()

            # Filtrar los datos para el año deseado
            data_tmax_year = data_Tmax[data_Tmax.index.year == year]

            # Crear un DataFrame vacío para almacenar los datos combinados
            df_plot = pd.DataFrame()

            # Iterar sobre los estados seleccionados
            for estado in estados:
                if estado in data_tmax_year.columns:
                    temp_df = data_tmax_year[[estado]].reset_index().rename(columns={"time": "Mes", estado: "Temperatura"})
                    temp_df["Mes"] = temp_df["Mes"].dt.month  # Extraer el mes
                    temp_df["Estado"] = estado
                    df_plot = pd.concat([df_plot, temp_df], ignore_index=True)

            # Asegurarse de que el DataFrame no esté vacío
            if df_plot.empty:
                return None

            # Crear el gráfico con plotnine
            plot = (
                ggplot(df_plot, aes(x="Mes", y="Temperatura", color="Estado"))
                + geom_line(size=1.25, show_legend=True, linetype="solid")
                + geom_point(size=2.5)
                + labs(
                    title="Temperatura máxima promedio", subtitle=f"Variación de la temperatura máxima por mes en el año {year}",
                    x="Mes", y="Temperatura (°C)"
                )
                + scale_x_continuous(breaks=range(1, 13), labels=meses)
                + theme_minimal()
                + theme(figure_size=(10, 4))
            )

        else:
            estados = selected_states_tmax()
            
            if not estados:
                return None  # No generar gráfico si no se selecciona ningún estado
        
            # Agrupar los datos por mes
            grouped_data = data_Tmax.groupby(data_Tmax.index.month).mean()

            # Crear un DataFrame vacío para almacenar los datos combinados
            df_plot = pd.DataFrame()

            # Iterar sobre los estados seleccionados
            for estado in estados:
                if estado in grouped_data.columns:
                    temp_df = grouped_data.reset_index()[["time", estado]].rename(columns={"time": "Mes", estado: "Temperatura"})
                    temp_df["Estado"] = estado
                    df_plot = pd.concat([df_plot, temp_df], ignore_index=True)

            # Convertir la columna "Mes" en tipo entero
            df_plot["Mes"] = df_plot["Mes"].astype(int)

            # Crear el gráfico con plotnine
            plot = (
                ggplot(df_plot, aes(x="Mes", y="Temperatura", color="Estado"))
                + geom_line(size=1.25, show_legend=True, linetype="solid")
                + geom_point(size=2)
                + labs(
                    title="Promedio histórico de temperatura máxima mensual", subtitle="Datos calculados a partir de los registros de 2013 a 2024",
                    x="Mes", y="Temperatura (°C)"
                )
                + scale_x_continuous(breaks=range(1, 13), labels=meses) 
                + theme_minimal()
                + theme(figure_size=(10, 4))
            )

        return plot
    
    @reactive.calc()
    def selected_states_tmin():
        return input.tmin_states()

    @reactive.calc()
    def selected_year_tmin():
        return int(input.year_tmin_plot())  

    @render.plot
    def tmin_plot():
        # Obtener estados seleccionados
        estados = selected_states_tmin()
        if not estados:
            return None  # No generar gráfico si no hay estados seleccionados

        # Verificamos el tipo de gráfico seleccionado
        if input.type_plot_tmin() == "Anual":
            # Obtener el año seleccionado
            year = selected_year_tmin()

            # Filtrar los datos para el año deseado
            data_tmin_year = data_Tmin[data_Tmin.index.year == year]

            # Crear un DataFrame vacío para almacenar los datos combinados
            df_plot = pd.DataFrame()

            # Iterar sobre los estados seleccionados
            for estado in estados:
                if estado in data_tmin_year.columns:
                    temp_df = data_tmin_year[[estado]].reset_index().rename(columns={"time": "Mes", estado: "Temperatura"})
                    temp_df["Mes"] = temp_df["Mes"].dt.month  # Extraer el mes
                    temp_df["Estado"] = estado
                    df_plot = pd.concat([df_plot, temp_df], ignore_index=True)

            # Asegurarse de que el DataFrame no esté vacío
            if df_plot.empty:
                return None

            # Crear el gráfico con plotnine
            plot = (
                ggplot(df_plot, aes(x="Mes", y="Temperatura", color="Estado"))
                + geom_line(size=1.25, show_legend=True, linetype="solid")
                + geom_point(size=2.5)
                + labs(
                    title="Temperatura mínima promedio", subtitle=f"Variación de la temperatura mínima por mes en el año {year}",
                    x="Mes", y="Temperatura (°C)"
                )
                + scale_x_continuous(breaks=range(1, 13), labels=meses)
                + theme_minimal()
                + theme(figure_size=(10, 4))
            )

        else:
            estados = selected_states_tmin()
            
            if not estados:
                return None  # No generar gráfico si no se selecciona ningún estado
        
            # Agrupar los datos por mes
            grouped_data = data_Tmin.groupby(data_Tmin.index.month).mean()

            # Crear un DataFrame vacío para almacenar los datos combinados
            df_plot = pd.DataFrame()

            # Iterar sobre los estados seleccionados
            for estado in estados:
                if estado in grouped_data.columns:
                    temp_df = grouped_data.reset_index()[["time", estado]].rename(columns={"time": "Mes", estado: "Temperatura"})
                    temp_df["Estado"] = estado
                    df_plot = pd.concat([df_plot, temp_df], ignore_index=True)

            # Convertir la columna "Mes" en tipo entero
            df_plot["Mes"] = df_plot["Mes"].astype(int)

            # Crear el gráfico con plotnine
            plot = (
                ggplot(df_plot, aes(x="Mes", y="Temperatura", color="Estado"))
                + geom_line(size=1.25, show_legend=True, linetype="solid")
                + geom_point(size=2)
                + labs(
                    title="Promedio histórico de temperatura mínima mensual", subtitle="Datos calculados a partir de los registros de 2013 a 2024",
                    x="Mes", y="Temperatura (°C)"
                )
                + scale_x_continuous(breaks=range(1, 13), labels=meses) 
                + theme_minimal()
                + theme(figure_size=(10, 4))
            )

        return plot

    @render_widget
    def precipitation_hm():
        # Verificamos el tipo de gráfico seleccionado
        if input.type_hm_rain() == "Anual":
            # Filtrar los datos para el año deseado
            year = int(input.year_precipitation_hm())  # Año seleccionado por el usuario
            data_rain = data_lluv[data_lluv.index.year == year].copy()

            # Crear una nueva columna con el número de mes
            data_rain['Mes'] = data_rain.index.month

            # Derretir el DataFrame para obtener una versión "larga" (long-form)
            data_long = data_rain.reset_index().melt(id_vars=["time", "Mes"], 
                                                    var_name="Estado", 
                                                    value_name="Precipitación")

            # Reemplazar los números de los meses con nombres
            data_long["Mes"] = data_long["Mes"].apply(lambda x: meses[x-1])

            # Convertir los valores de precipitación de mm a cm
            data_long["Precipitación"] = data_long["Precipitación"] / 10

            # Crear una tabla dinámica con los meses como filas y los estados como columnas
            heatmap_data = data_long.pivot_table(index="Mes", columns="Estado", values="Precipitación", aggfunc="sum")

            # Asegurarse de que los meses estén en el orden correcto
            heatmap_data = heatmap_data.reindex(meses)

            # Rellenar los valores NaN con 0 (o el valor que prefieras)
            heatmap_data = heatmap_data.fillna(0)

            # Crear el heatmap con Plotly Express
            fig = px.imshow(heatmap_data,
                            labels=dict(x="Estado", y="Mes", color="Precipitación (cm)"),
                            x=heatmap_data.columns,
                            y=heatmap_data.index,
                            color_continuous_scale="viridis",
                            aspect="auto")

            # Configurar el diseño
            fig.update_layout(title=f"Precipitación mensual acumulada en {year}",
                            title_x=0.5,
                            xaxis_title="Estado",
                            yaxis_title="Mes")

        else:
            # Trabajar con una copia para evitar modificar el DataFrame global
            data_rain = data_lluv.copy()

            # Crear una nueva columna con el número de mes y año
            data_rain['Mes'] = data_rain.index.month
            data_rain['Año'] = data_rain.index.year

            # Derretir el DataFrame para obtener una versión "larga" (long-form)
            data_long = data_rain.reset_index().melt(id_vars=["time", "Mes", "Año"], 
                                                    var_name="Estado", 
                                                    value_name="Precipitación")

            # Reemplazar los números de los meses con nombres
            data_long["Mes"] = data_long["Mes"].apply(lambda x: meses[x-1])

            # Convertir los valores de precipitación de mm a cm
            data_long["Precipitación"] = data_long["Precipitación"] / 10

            # Asegurarse de que los meses estén en el orden correcto
            data_avg = data_long.groupby(["Mes", "Estado"]).agg({"Precipitación": "mean"}).reset_index()

            # Crear una tabla dinámica con los meses como filas y los estados como columnas
            heatmap_data = data_avg.pivot_table(index="Mes", columns="Estado", values="Precipitación", aggfunc="mean")

            # Asegurarse de que los meses estén en el orden correcto
            heatmap_data = heatmap_data.reindex(meses)

            # Rellenar los valores NaN con 0
            heatmap_data = heatmap_data.fillna(0)

            # Crear el heatmap con Plotly Express
            fig = px.imshow(heatmap_data,
                            labels=dict(x="Estado", y="Mes", color="Precipitación (cm)"),
                            x=heatmap_data.columns,
                            y=heatmap_data.index,
                            color_continuous_scale="viridis",
                            aspect="auto")

            # Configurar el diseño
            fig.update_layout(title="Promedio histórico de precipitación mensual (2013-2024)",
                            title_x=0.5,
                            xaxis_title="Estado",
                            yaxis_title="Mes")

        return fig
    
    @render_widget
    def tmean_hm():
        # Verificamos el tipo de gráfico seleccionado
        if input.type_hm_tmean() == "Anual":
            # Filtrar los datos para el año deseado
            year = int(input.year_tmean_hm())  # Año seleccionado por el usuario
            data_mean = data_Tmean[data_Tmean.index.year == year].copy()

            # Crear una nueva columna con el número de mes
            data_mean['Mes'] = data_mean.index.month

            # Derretir el DataFrame para obtener una versión "larga" (long-form)
            data_long = data_mean.reset_index().melt(id_vars=["time", "Mes"], 
                                                    var_name="Estado", 
                                                    value_name="Temperatura")

            # Reemplazar los números de los meses con nombres
            data_long["Mes"] = data_long["Mes"].apply(lambda x: meses[x-1])

            # Crear una tabla dinámica con los meses como filas y los estados como columnas
            heatmap_data = data_long.pivot_table(index="Mes", columns="Estado", values="Temperatura", aggfunc="sum")

            # Asegurarse de que los meses estén en el orden correcto
            heatmap_data = heatmap_data.reindex(meses)

            # Rellenar los valores NaN con 0 (o el valor que prefieras)
            heatmap_data = heatmap_data.fillna(0)

            # Crear el heatmap con Plotly Express
            fig = px.imshow(heatmap_data,
                            labels=dict(x="Estado", y="Mes", color="Temperatura (°C)"),
                            x=heatmap_data.columns,
                            y=heatmap_data.index,
                            color_continuous_scale="sunsetdark",
                            aspect="auto")

            # Configurar el diseño
            fig.update_layout(title=f"Variación mensual de la temperatura media promedio en el año {year}",
                            title_x=0.5,
                            xaxis_title="Estado",
                            yaxis_title="Mes")

        else:
            # Trabajar con una copia para evitar modificar el DataFrame global
            data_mean = data_Tmean.copy()

            # Crear una nueva columna con el número de mes y año
            data_mean['Mes'] = data_mean.index.month
            data_mean['Año'] = data_mean.index.year

            # Derretir el DataFrame para obtener una versión "larga" (long-form)
            data_long = data_mean.reset_index().melt(id_vars=["time", "Mes", "Año"], 
                                                    var_name="Estado", 
                                                    value_name="Temperatura")

            # Reemplazar los números de los meses con nombres
            data_long["Mes"] = data_long["Mes"].apply(lambda x: meses[x-1])

            # Asegurarse de que los meses estén en el orden correcto
            data_avg = data_long.groupby(["Mes", "Estado"]).agg({"Temperatura": "mean"}).reset_index()

            # Crear una tabla dinámica con los meses como filas y los estados como columnas
            heatmap_data = data_avg.pivot_table(index="Mes", columns="Estado", values="Temperatura", aggfunc="mean")

            # Asegurarse de que los meses estén en el orden correcto
            heatmap_data = heatmap_data.reindex(meses)

            # Rellenar los valores NaN con 0
            heatmap_data = heatmap_data.fillna(0)

            # Crear el heatmap con Plotly Express
            fig = px.imshow(heatmap_data,
                            labels=dict(x="Estado", y="Mes", color="Temperatura (°C)"),
                            x=heatmap_data.columns,
                            y=heatmap_data.index,
                            color_continuous_scale="sunsetdark",
                            aspect="auto")

            # Configurar el diseño
            fig.update_layout(title="Promedio histórico de temperatura media mensual (2013-2024)",
                            title_x=0.5,
                            xaxis_title="Estado",
                            yaxis_title="Mes")

        return fig
    
    @render_widget
    def tmax_hm():
        # Verificamos el tipo de gráfico seleccionado
        if input.type_hm_tmax() == "Anual":
            # Filtrar los datos para el año deseado
            year = int(input.year_tmax_hm())  # Año seleccionado por el usuario
            data_max = data_Tmax[data_Tmax.index.year == year].copy()

            # Crear una nueva columna con el número de mes
            data_max['Mes'] = data_max.index.month

            # Derretir el DataFrame para obtener una versión "larga" (long-form)
            data_long = data_max.reset_index().melt(id_vars=["time", "Mes"], 
                                                    var_name="Estado", 
                                                    value_name="Temperatura")

            # Reemplazar los números de los meses con nombres
            data_long["Mes"] = data_long["Mes"].apply(lambda x: meses[x-1])

            # Crear una tabla dinámica con los meses como filas y los estados como columnas
            heatmap_data = data_long.pivot_table(index="Mes", columns="Estado", values="Temperatura", aggfunc="sum")

            # Asegurarse de que los meses estén en el orden correcto
            heatmap_data = heatmap_data.reindex(meses)

            # Rellenar los valores NaN con 0 (o el valor que prefieras)
            heatmap_data = heatmap_data.fillna(0)

            # Crear el heatmap con Plotly Express
            fig = px.imshow(heatmap_data,
                            labels=dict(x="Estado", y="Mes", color="Temperatura (°C)"),
                            x=heatmap_data.columns,
                            y=heatmap_data.index,
                            color_continuous_scale="oranges",
                            aspect="auto")

            # Configurar el diseño
            fig.update_layout(title=f"Variación mensual de la temperatura máxima promedio en el año {year}",
                            title_x=0.5,
                            xaxis_title="Estado",
                            yaxis_title="Mes")

        else:
            # Trabajar con una copia para evitar modificar el DataFrame global
            data_max = data_Tmax.copy()

            # Crear una nueva columna con el número de mes y año
            data_max['Mes'] = data_max.index.month
            data_max['Año'] = data_max.index.year

            # Derretir el DataFrame para obtener una versión "larga" (long-form)
            data_long = data_max.reset_index().melt(id_vars=["time", "Mes", "Año"], 
                                                    var_name="Estado", 
                                                    value_name="Temperatura")

            # Reemplazar los números de los meses con nombres
            data_long["Mes"] = data_long["Mes"].apply(lambda x: meses[x-1])

            # Asegurarse de que los meses estén en el orden correcto
            data_avg = data_long.groupby(["Mes", "Estado"]).agg({"Temperatura": "mean"}).reset_index()

            # Crear una tabla dinámica con los meses como filas y los estados como columnas
            heatmap_data = data_avg.pivot_table(index="Mes", columns="Estado", values="Temperatura", aggfunc="mean")

            # Asegurarse de que los meses estén en el orden correcto
            heatmap_data = heatmap_data.reindex(meses)

            # Rellenar los valores NaN con 0
            heatmap_data = heatmap_data.fillna(0)

            # Crear el heatmap con Plotly Express
            fig = px.imshow(heatmap_data,
                            labels=dict(x="Estado", y="Mes", color="Temperatura (°C)"),
                            x=heatmap_data.columns,
                            y=heatmap_data.index,
                            color_continuous_scale="oranges",
                            aspect="auto")

            # Configurar el diseño
            fig.update_layout(title="Promedio histórico de temperatura máxima mensual (2013-2024)",
                            title_x=0.5,
                            xaxis_title="Estado",
                            yaxis_title="Mes")

        return fig
    
    @render_widget
    def tmin_hm():
        # Verificamos el tipo de gráfico seleccionado
        if input.type_hm_tmin() == "Anual":
            # Filtrar los datos para el año deseado
            year = int(input.year_tmin_hm())  # Año seleccionado por el usuario
            data_min = data_Tmin[data_Tmin.index.year == year].copy()

            # Crear una nueva columna con el número de mes
            data_min['Mes'] = data_min.index.month

            # Derretir el DataFrame para obtener una versión "larga" (long-form)
            data_long = data_min.reset_index().melt(id_vars=["time", "Mes"], 
                                                    var_name="Estado", 
                                                    value_name="Temperatura")

            # Reemplazar los números de los meses con nombres
            data_long["Mes"] = data_long["Mes"].apply(lambda x: meses[x-1])

            # Crear una tabla dinámica con los meses como filas y los estados como columnas
            heatmap_data = data_long.pivot_table(index="Mes", columns="Estado", values="Temperatura", aggfunc="sum")

            # Asegurarse de que los meses estén en el orden correcto
            heatmap_data = heatmap_data.reindex(meses)

            # Rellenar los valores NaN con 0 (o el valor que prefieras)
            heatmap_data = heatmap_data.fillna(0)

            # Crear el heatmap con Plotly Express
            fig = px.imshow(heatmap_data,
                            labels=dict(x="Estado", y="Mes", color="Temperatura (°C)"),
                            x=heatmap_data.columns,
                            y=heatmap_data.index,
                            color_continuous_scale="blues",
                            aspect="auto")

            # Configurar el diseño
            fig.update_layout(title=f"Variación mensual de la temperatura mínima promedio en el año {year}",
                            title_x=0.5,
                            xaxis_title="Estado",
                            yaxis_title="Mes")

        else:
            # Trabajar con una copia para evitar modificar el DataFrame global
            data_min = data_Tmin.copy()

            # Crear una nueva columna con el número de mes y año
            data_min['Mes'] = data_min.index.month
            data_min['Año'] = data_min.index.year

            # Derretir el DataFrame para obtener una versión "larga" (long-form)
            data_long = data_min.reset_index().melt(id_vars=["time", "Mes", "Año"], 
                                                    var_name="Estado", 
                                                    value_name="Temperatura")

            # Reemplazar los números de los meses con nombres
            data_long["Mes"] = data_long["Mes"].apply(lambda x: meses[x-1])

            # Asegurarse de que los meses estén en el orden correcto
            data_avg = data_long.groupby(["Mes", "Estado"]).agg({"Temperatura": "mean"}).reset_index()

            # Crear una tabla dinámica con los meses como filas y los estados como columnas
            heatmap_data = data_avg.pivot_table(index="Mes", columns="Estado", values="Temperatura", aggfunc="mean")

            # Asegurarse de que los meses estén en el orden correcto
            heatmap_data = heatmap_data.reindex(meses)

            # Rellenar los valores NaN con 0
            heatmap_data = heatmap_data.fillna(0)

            # Crear el heatmap con Plotly Express
            fig = px.imshow(heatmap_data,
                            labels=dict(x="Estado", y="Mes", color="Temperatura (°C)"),
                            x=heatmap_data.columns,
                            y=heatmap_data.index,
                            color_continuous_scale="blues",
                            aspect="auto")

            # Configurar el diseño
            fig.update_layout(title="Promedio histórico de temperatura mínima mensual (2013-2024)",
                            title_x=0.5,
                            xaxis_title="Estado",
                            yaxis_title="Mes")

        return fig

# Crear la aplicación con la interfaz de usuario y el servidor
app = App(app_ui, server)
