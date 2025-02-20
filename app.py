from pathlib import Path
import pandas as pd
import json
from shiny import App, Inputs, reactive, render, ui
from shinywidgets import render_widget, output_widget
import faicons
import io
from plots import (
    choropleth_map, choropleth_data, 
    line_plot, line_plot_data, 
    heatmap, heatmap_data
)
from shared import STATE_MAPPING

data_Lluv = pd.read_csv(Path(__file__).parent / "data_Lluv.csv", index_col="time", parse_dates=True)
data_Tmean = pd.read_csv(Path(__file__).parent / "data_TMed.csv", index_col="time", parse_dates=True)
data_Tmax = pd.read_csv(Path(__file__).parent / "data_TMax.csv", index_col="time", parse_dates=True)
data_Tmin = pd.read_csv(Path(__file__).parent / "data_TMin.csv", index_col="time", parse_dates=True)
GEOJSON_DATA = json.load((Path(__file__).parent / "Mexico.json").open(encoding="utf-8"))

rain_start = data_Lluv.index.min().strftime("%Y-%m-%d")
rain_end = data_Lluv.index.max().strftime("%Y-%m-%d")

tmean_start = data_Tmean.index.min().strftime("%Y-%m-%d")
tmean_end = data_Tmean.index.max().strftime("%Y-%m-%d")

tmax_start = data_Tmax.index.min().strftime("%Y-%m-%d")
tmax_end = data_Tmax.index.max().strftime("%Y-%m-%d")

tmin_start = data_Tmin.index.min().strftime("%Y-%m-%d")
tmin_end = data_Tmin.index.max().strftime("%Y-%m-%d")

# ----- INTERFAZ DE USUARIO -----
app_ui = ui.page_navbar(
    ui.nav_spacer(),
    ui.nav_panel("Precipitación",
        ui.navset_card_underline(
            ui.nav_panel("Mapa geográfico",
                ui.input_select("year_map_rain", "Selecciona el año:",
                                choices=[str(year) for year in data_Lluv.index.year.unique()]),
                output_widget("rain_map")
            ),
            ui.nav_panel("Gráfico",
                ui.layout_columns(
                    ui.input_select("type_plot_rain", "Tipo de gráfico:", ["Anual", "Histórico"]),
                    ui.input_select("year_plot_rain", "Selecciona el año:",
                                    choices=[str(year) for year in data_Lluv.index.year.unique()]),
                    ui.input_selectize("states_rain", "Selecciona el estado:",
                                    choices=list(data_Lluv.columns), multiple=True),
                ),
                ui.output_plot("rain_plot")
            ),
            ui.nav_panel("Mapa de calor",
                ui.layout_columns(
                    ui.input_select("type_hm_rain", "Tipo de mapa:", ["Anual", "Histórico"]),
                    ui.input_select("year_hm_rain", "Selecciona el año:",
                                    choices=[str(year) for year in data_Lluv.index.year.unique()])
                ),
                output_widget("rain_hm")
            ),
            ui.nav_panel("Datos",
                ui.card(ui.card_header(
                    ui.span(ui.output_text("rain_title")),
                    ui.download_link("rain_download", "Descargar archivo",
                                     icon=faicons.icon_svg("download"), class_="btn btn-primary btn-sm"),
                                     class_="d-flex justify-content-between align-items-center"),
                    ui.input_date_range("rain_daterange", "Rango de fechas", start=rain_start, end=rain_end),
                    ui.output_data_frame("rain_data")
                ),
            ),
            title="Resúmenes anuales y mensuales de lluvia",
        )
    ),
    ui.nav_panel("Temperatura media",
        ui.navset_card_underline(
            ui.nav_panel("Mapa geográfico",
                ui.input_select("year_map_tmean", "Selecciona el año:",
                                choices=[str(year) for year in data_Tmean.index.year.unique()]),
                output_widget("tmean_map")
            ),
            ui.nav_panel("Gráfico",
                ui.layout_columns(
                    ui.input_select("type_plot_tmean", "Tipo de gráfico:", ["Anual", "Histórico"]),
                    ui.input_select("year_plot_tmean", "Selecciona el año:",
                                    choices=[str(year) for year in data_Tmean.index.year.unique()]),
                    ui.input_selectize("states_tmean", "Selecciona el estado:",
                                    choices=list(data_Tmean.columns), multiple=True),
                ),
                ui.output_plot("tmean_plot")
            ),
            ui.nav_panel("Mapa de calor",
                ui.layout_columns(
                    ui.input_select("type_hm_tmean", "Tipo de mapa:", ["Anual", "Histórico"]),
                    ui.input_select("year_hm_tmean", "Selecciona el año:",
                                    choices=[str(year) for year in data_Tmean.index.year.unique()])
                ),
                output_widget("tmean_hm")
            ),
            ui.nav_panel("Datos",
                ui.card(ui.card_header(
                    ui.span(ui.output_text("tmean_title")),
                    ui.download_link("tmean_download", "Descargar archivo",
                                     icon=faicons.icon_svg("download"), class_="btn btn-primary btn-sm"),
                                     class_="d-flex justify-content-between align-items-center"),
                    ui.input_date_range("tmean_daterange", "Rango de fechas", start=tmean_start, end=tmean_end),
                    ui.output_data_frame("tmean_data")
                ),
            ),
            title="Resúmenes anuales y mensuales de temperatura media",
        )
    ),
    ui.nav_panel("Temperatura máxima",
        ui.navset_card_underline(
            ui.nav_panel("Mapa geográfico",
                ui.input_select("year_map_tmax", "Selecciona el año:",
                                choices=[str(year) for year in data_Tmax.index.year.unique()]),
                output_widget("tmax_map")
            ),
            ui.nav_panel("Gráfico",
                ui.layout_columns(
                    ui.input_select("type_plot_tmax", "Tipo de gráfico:", ["Anual", "Histórico"]),
                    ui.input_select("year_plot_tmax", "Selecciona el año:",
                                    choices=[str(year) for year in data_Tmax.index.year.unique()]),
                    ui.input_selectize("states_tmax", "Selecciona el estado:",
                                    choices=list(data_Tmax.columns), multiple=True),
                ),
                ui.output_plot("tmax_plot")
            ),
            ui.nav_panel("Mapa de calor",
                ui.layout_columns(
                    ui.input_select("type_hm_tmax", "Tipo de mapa:", ["Anual", "Histórico"]),
                    ui.input_select("year_hm_tmax", "Selecciona el año:",
                                    choices=[str(year) for year in data_Tmax.index.year.unique()])
                ),
                output_widget("tmax_hm")
            ),
            ui.nav_panel("Datos",
                ui.card(ui.card_header(
                    ui.span(ui.output_text("tmax_title")),
                    ui.download_link("tmax_download", "Descargar archivo",
                                     icon=faicons.icon_svg("download"), class_="btn btn-primary btn-sm"),
                                     class_="d-flex justify-content-between align-items-center"),
                    ui.input_date_range("tmax_daterange", "Rango de fechas", start=tmax_start, end=tmax_end),
                    ui.output_data_frame("tmax_data")
                ),
            ),
            title="Resúmenes anuales y mensuales de temperatura máxima",
        )
    ),
    ui.nav_panel("Temperatura mínima",
        ui.navset_card_underline(
            ui.nav_panel("Mapa geográfico",
                ui.input_select("year_map_tmin", "Selecciona el año:",
                                choices=[str(year) for year in data_Tmin.index.year.unique()]),
                output_widget("tmin_map")
            ),
            ui.nav_panel("Gráfico",
                ui.layout_columns(
                    ui.input_select("type_plot_tmin", "Tipo de gráfico:", ["Anual", "Histórico"]),
                    ui.input_select("year_plot_tmin", "Selecciona el año:",
                                    choices=[str(year) for year in data_Tmin.index.year.unique()]),
                    ui.input_selectize("states_tmin", "Selecciona el estado:",
                                    choices=list(data_Tmin.columns), multiple=True),
                ),
                ui.output_plot("tmin_plot")
            ),
            ui.nav_panel("Mapa de calor",
                ui.layout_columns(
                    ui.input_select("type_hm_tmin", "Tipo de mapa:", ["Anual", "Histórico"]),
                    ui.input_select("year_hm_tmin", "Selecciona el año:",
                                    choices=[str(year) for year in data_Tmin.index.year.unique()])
                ),
                output_widget("tmin_hm")
            ),
            ui.nav_panel("Datos",
                ui.card(ui.card_header(
                    ui.span(ui.output_text("tmin_title")),
                    ui.download_link("tmin_download", "Descargar archivo",
                                     icon=faicons.icon_svg("download"), class_="btn btn-primary btn-sm"),
                                     class_="d-flex justify-content-between align-items-center"),
                    ui.input_date_range("tmin_daterange", "Rango de fechas", start=tmin_start, end=tmin_end),
                    ui.output_data_frame("tmin_data")
                ),
            ),
            title="Resúmenes anuales y mensuales de temperatura mínima",
        )
    ),
    title="Explorador CONAGUA",
    id="page"
)

# ----- SERVIDOR -----
def server(input: Inputs, output, session):
    # --- MAPA GEOGRÁFICO ---
    @render_widget
    def rain_map():
        year = int(input.year_map_rain())
        data = choropleth_data(data_Lluv, year, STATE_MAPPING, aggregation="sum")
        return choropleth_map(data, GEOJSON_DATA, f"Precipitación anual {year}", "viridis_r", "Precipitación (mm)")
    
    @render_widget
    def tmean_map():
        year = int(input.year_map_tmean())
        data = choropleth_data(data_Tmean, year, STATE_MAPPING, aggregation="mean")
        return choropleth_map(data, GEOJSON_DATA, f"Temperatura media promedio {year}", "haline", "Temperatura (°C)")
    
    @render_widget
    def tmax_map():
        year = int(input.year_map_tmax())
        data = choropleth_data(data_Tmax, year, STATE_MAPPING, aggregation="mean")
        return choropleth_map(data, GEOJSON_DATA, f"Temperatura máxima promedio {year}", "oranges", "Temperatura (°C)")
    
    @render_widget
    def tmin_map():
        year = int(input.year_map_tmin())
        data = choropleth_data(data_Tmin, year, STATE_MAPPING, aggregation="mean")
        return choropleth_map(data, GEOJSON_DATA, f"Temperatura mínima promedio {year}", "blues", "Temperatura (°C)")
    
    # --- GRÁFICO ---
    @reactive.calc
    def selected_states_rain():
        return input.states_rain()

    @render.plot
    def rain_plot():
        estados = selected_states_rain()
        if not estados:
            return None
        
        if input.type_plot_rain() == "Anual":
            year = int(input.year_plot_rain())
            data = line_plot_data(data_Lluv, year=year, states=estados, aggregation="sum")
            title = f"Precipitación mensual acumulada en {year}"
        else:
            data = line_plot_data(data_Lluv, states=estados, aggregation="mean")
            title = "Promedio histórico de precipitación mensual (2014-2024)"
        
        return line_plot(data, title, "Precipitación (mm)")
        
    @reactive.calc
    def selected_states_tmean():
        return input.states_tmean()

    @render.plot
    def tmean_plot():
        estados = selected_states_tmean()
        if not estados:
            return None
        
        if input.type_plot_tmean() == "Anual":
            year = int(input.year_plot_tmean())
            data = line_plot_data(data_Tmean, year=year, states=estados, aggregation="sum")
            title = f"Temperatura media promedio en {year}"
        else:
            data = line_plot_data(data_Tmean, states=estados, aggregation="mean")
            title = "Promedio histórico de temperatura media mensual (2014-2024)"
        
        return line_plot(data, title, "Temperatura (°C)")
    
    @reactive.calc
    def selected_states_tmax():
        return input.states_tmax()

    @render.plot
    def tmax_plot():
        estados = selected_states_tmax()
        if not estados:
            return None
        
        if input.type_plot_tmax() == "Anual":
            year = int(input.year_plot_tmax())
            data = line_plot_data(data_Tmax, year=year, states=estados, aggregation="sum")
            title = f"Temperatura máxima promedio en {year}"
        else:
            data = line_plot_data(data_Tmax, states=estados, aggregation="mean")
            title = "Promedio histórico de temperatura máxima mensual (2014-2024)"
        
        return line_plot(data, title, "Temperatura (°C)")
    
    @reactive.calc
    def selected_states_tmin():
        return input.states_tmin()

    @render.plot
    def tmin_plot():
        estados = selected_states_tmin()
        if not estados:
            return None
        
        if input.type_plot_tmin() == "Anual":
            year = int(input.year_plot_tmin())
            data = line_plot_data(data_Tmin, year=year, states=estados, aggregation="sum")
            title = f"Temperatura mínima promedio en {year}"
        else:
            data = line_plot_data(data_Tmin, states=estados, aggregation="mean")
            title = "Promedio histórico de temperatura mínima mensual (2014-2024)"
        
        return line_plot(data, title, "Temperatura (°C)")

    # --- HEATMAP ---
    @render_widget
    def rain_hm():
        # Verificar el tipo de mapa seleccionado
        if input.type_hm_rain() == "Anual":
            # Obtener el año seleccionado
            year = int(input.year_hm_rain())
            data = heatmap_data(data_Lluv, year=year, aggregation="sum", historical=False)
            title = f"Precipitación mensual acumulada en {year}"
        else:
            # Calcular promedio histórico
            data = heatmap_data(data_Lluv, aggregation="mean", historical=True)
            title = "Promedio histórico de precipitación mensual (2014-2024)"

        # Generar el heatmap
        return heatmap(data, title, "viridis", "Precipitación (mm)")
    
    @render_widget
    def tmean_hm():
        # Verificar el tipo de mapa seleccionado
        if input.type_hm_tmean() == "Anual":
            # Obtener el año seleccionado
            year = int(input.year_hm_tmean())
            data = heatmap_data(data_Tmean, year=year, aggregation="sum", historical=False)
            title = f"Variación mensual de la temperatura media promedio en {year}"
        else:
            # Calcular promedio histórico
            data = heatmap_data(data_Tmean, aggregation="mean", historical=True)
            title = "Promedio histórico de temperatura media mensual (2014-2024)"

        # Generar el heatmap
        return heatmap(data, title, "haline", "Temperatura (°C)")
    
    @render_widget
    def tmax_hm():
        # Verificar el tipo de mapa seleccionado
        if input.type_hm_tmax() == "Anual":
            # Obtener el año seleccionado
            year = int(input.year_hm_tmax())
            data = heatmap_data(data_Tmax, year=year, aggregation="sum", historical=False)
            title = f"Variación mensual de la temperatura máxima promedio en {year}"
        else:
            # Calcular promedio histórico
            data = heatmap_data(data_Tmax, aggregation="mean", historical=True)
            title = "Promedio histórico de temperatura máxima mensual (2014-2024)"

        # Generar el heatmap
        return heatmap(data, title, "oranges", "Temperatura (°C)")
    
    @render_widget
    def tmin_hm():
        # Verificar el tipo de mapa seleccionado
        if input.type_hm_tmin() == "Anual":
            # Obtener el año seleccionado
            year = int(input.year_hm_tmin())
            data = heatmap_data(data_Tmin, year=year, aggregation="sum", historical=False)
            title = f"Variación mensual de la temperatura mínima promedio en {year}"
        else:
            # Calcular promedio histórico
            data = heatmap_data(data_Tmin, aggregation="mean", historical=True)
            title = "Promedio histórico de temperatura mínima mensual (2014-2024)"

        # Generar el heatmap
        return heatmap(data, title, "blues", "Temperatura (°C)")

    # --- DATAFRAME ---
    @render.text
    def rain_title():
        return "data_Lluv.csv"

    @reactive.calc()
    def rain_date_filter() -> pd.DataFrame:
        start_date, end_date = input.rain_daterange()
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        return data_Lluv.loc[(data_Lluv.index >= start_date) & (data_Lluv.index <= end_date)]

    @render.data_frame
    def rain_data():
        df = rain_date_filter().reset_index()
        df['time'] = df['time'].dt.strftime('%Y-%m-%d')
        return df

    @render.download(filename=lambda: "data_Lluv.csv")
    def rain_download():
        df_filtrado = rain_date_filter().reset_index()
        with io.StringIO() as buf:
            df_filtrado.to_csv(buf, index=False)
            yield buf.getvalue().encode()

    @render.text
    def tmean_title():
        return "data_Tmean.csv"

    @reactive.calc()
    def tmean_date_filter() -> pd.DataFrame:
        start_date, end_date = input.tmean_daterange()
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        return data_Tmean.loc[(data_Tmean.index >= start_date) & (data_Tmean.index <= end_date)]

    @render.data_frame
    def tmean_data():
        df = tmean_date_filter().reset_index()
        return df

    @render.download(filename=lambda: "data_Tmean.csv")
    def tmean_download():
        df_filtrado = tmean_date_filter().reset_index()
        with io.StringIO() as buf:
            df_filtrado.to_csv(buf, index=False)
            yield buf.getvalue().encode()

    @render.text
    def tmax_title():
        return "data_Tmax.csv"

    @reactive.calc()
    def tmax_date_filter() -> pd.DataFrame:
        start_date, end_date = input.tmax_daterange()
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        return data_Tmax.loc[(data_Tmax.index >= start_date) & (data_Tmax.index <= end_date)]

    @render.data_frame
    def tmax_data():
        df = tmax_date_filter().reset_index()
        return df

    @render.download(filename=lambda: "data_Tmax.csv")
    def tmax_download():
        df_filtrado = tmax_date_filter().reset_index()
        with io.StringIO() as buf:
            df_filtrado.to_csv(buf, index=False)
            yield buf.getvalue().encode()

    @render.text
    def tmin_title():
        return "data_Tmin.csv"

    @reactive.calc()
    def tmin_date_filter() -> pd.DataFrame:
        start_date, end_date = input.tmin_daterange()
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        return data_Tmin.loc[(data_Tmin.index >= start_date) & (data_Tmin.index <= end_date)]

    @render.data_frame
    def tmin_data():
        df = tmin_date_filter().reset_index()
        return df

    @render.download(filename=lambda: "data_Tmin.csv")
    def tmin_download():
        df_filtrado = tmin_date_filter().reset_index()
        with io.StringIO() as buf:
            df_filtrado.to_csv(buf, index=False)
            yield buf.getvalue().encode()

# ----- EJECUCIÓN DE LA APLICACIÓN -----
app = App(app_ui, server)