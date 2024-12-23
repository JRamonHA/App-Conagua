from shiny import App, Inputs, reactive, render, ui
from shinywidgets import render_widget, output_widget
import faicons
import io
from plots import (
    choropleth_map, choropleth_data, 
    line_plot, line_plot_data, 
    heatmap, heatmap_data
)
from shared import data_Lluv, data_Tmean, data_Tmax, data_Tmin, STATE_MAPPING, GEOJSON_DATA

# ----- INTERFAZ DE USUARIO -----
app_ui = ui.page_navbar(
    ui.nav_spacer(),
    ui.nav_panel("Precipitación",
        ui.navset_card_underline(
            ui.nav_panel("Mapa geográfico",
                ui.input_select("year_map_rain", "Selecciona el año:",
                                choices=[str(year) for year in data_Lluv.index.year.unique()]),
                output_widget("rain_map"),
            ),
            ui.nav_panel("Gráfico",
                ui.layout_columns(
                    ui.input_select("type_plot_rain", "Tipo de gráfico:", ["Anual", "Histórico"]),
                    ui.input_select("year_plot_rain", "Selecciona el año:",
                                    choices=[str(year) for year in data_Lluv.index.year.unique()]),
                    ui.input_selectize("states_rain", "Selecciona el estado:",
                                    choices=list(data_Lluv.columns), multiple=True),
                ),
                ui.output_plot("rain_plot"),
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
                output_widget("tmean_map"),
            ),
            ui.nav_panel("Gráfico",
                ui.layout_columns(
                    ui.input_select("type_plot_tmean", "Tipo de gráfico:", ["Anual", "Histórico"]),
                    ui.input_select("year_plot_tmean", "Selecciona el año:",
                                    choices=[str(year) for year in data_Tmean.index.year.unique()]),
                    ui.input_selectize("states_tmean", "Selecciona el estado:",
                                    choices=list(data_Tmean.columns), multiple=True),
                ),
                ui.output_plot("tmean_plot"),
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
                output_widget("tmax_map"),
            ),
            ui.nav_panel("Gráfico",
                ui.layout_columns(
                    ui.input_select("type_plot_tmax", "Tipo de gráfico:", ["Anual", "Histórico"]),
                    ui.input_select("year_plot_tmax", "Selecciona el año:",
                                    choices=[str(year) for year in data_Tmax.index.year.unique()]),
                    ui.input_selectize("states_tmax", "Selecciona el estado:",
                                    choices=list(data_Tmax.columns), multiple=True),
                ),
                ui.output_plot("tmax_plot"),
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
                output_widget("tmin_map"),
            ),
            ui.nav_panel("Gráfico",
                ui.layout_columns(
                    ui.input_select("type_plot_tmin", "Tipo de gráfico:", ["Anual", "Histórico"]),
                    ui.input_select("year_plot_tmin", "Selecciona el año:",
                                    choices=[str(year) for year in data_Tmin.index.year.unique()]),
                    ui.input_selectize("states_tmin", "Selecciona el estado:",
                                    choices=list(data_Tmin.columns), multiple=True),
                ),
                ui.output_plot("tmin_plot"),
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
            subtitle = "Distribución de lluvia total por mes"
        else:
            data = line_plot_data(data_Lluv, states=estados, aggregation="mean")
            title = "Promedio histórico de precipitación mensual (2014-2024)"
            subtitle = "Datos calculados a partir de los registros históricos"
        
        return line_plot(data, title, subtitle, "Precipitación (mm)")
        
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
            subtitle = "Variación de la temperatura media por mes"
        else:
            data = line_plot_data(data_Tmean, states=estados, aggregation="mean")
            title = "Promedio histórico de temperatura media mensual (2014-2024)"
            subtitle = "Datos calculados a partir de los registros históricos"
        
        return line_plot(data, title, subtitle, "Temperatura (°C)")
    
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
            subtitle = "Variación de la temperatura máxima por mes"
        else:
            data = line_plot_data(data_Tmax, states=estados, aggregation="mean")
            title = "Promedio histórico de temperatura máxima mensual (2014-2024)"
            subtitle = "Datos calculados a partir de los registros históricos"
        
        return line_plot(data, title, subtitle, "Temperatura (°C)")
    
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
            subtitle = "Variación de la temperatura mínima por mes"
        else:
            data = line_plot_data(data_Tmin, states=estados, aggregation="mean")
            title = "Promedio histórico de temperatura mínima mensual (2014-2024)"
            subtitle = "Datos calculados a partir de los registros históricos"
        
        return line_plot(data, title, subtitle, "Temperatura (°C)")

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
    @render.data_frame
    def rain_data():
        df = data_Lluv.reset_index()
        return df

    @render.text
    def rain_title():
        return "data_Lluv.csv"
    
    @render.download(filename=lambda: "data_Lluv.csv")
    def rain_download():
        df = data_Lluv.reset_index()
        with io.StringIO() as buf:
            df.to_csv(buf, index=False)
            yield buf.getvalue().encode()

    @render.data_frame
    def tmean_data():
        df = data_Tmean.reset_index()
        return df

    @render.text
    def tmean_title():
        return "data_Tmean.csv"
    
    @render.download(filename=lambda: "data_Tmean.csv")
    def tmean_download():
        df = data_Tmean.reset_index()
        with io.StringIO() as buf:
            df.to_csv(buf, index=False)
            yield buf.getvalue().encode()

    @render.data_frame
    def tmax_data():
        df = data_Tmax.reset_index()
        return df

    @render.text
    def tmax_title():
        return "data_Tmax.csv"
    
    @render.download(filename=lambda: "data_Tmax.csv")
    def tmax_download():
        df = data_Tmax.reset_index()
        with io.StringIO() as buf:
            df.to_csv(buf, index=False)
            yield buf.getvalue().encode()

    @render.data_frame
    def tmin_data():
        df = data_Tmin.reset_index()
        return df

    @render.text
    def tmin_title():
        return "data_Tmin.csv"
    
    @render.download(filename=lambda: "data_Tmin.csv")
    def tmin_download():
        df = data_Tmin.reset_index()
        with io.StringIO() as buf:
            df.to_csv(buf, index=False)
            yield buf.getvalue().encode()

# ----- EJECUCIÓN DE LA APLICACIÓN -----
app = App(app_ui, server)