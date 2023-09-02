from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
import json
from django.conf import settings
import os
from dashboard.models import *
from analyzeDashboard.models import *
from .forms import *


class DashboardView(View):

    def get(self, request):
        # todo Чет не могу нормально поключить файл из Медиа, пришлось пользоваться чатом
        media_path = os.path.join(settings.MEDIA_ROOT, 'map', 'regionMap.json')
        with open(media_path, encoding='utf-8') as file:
            regions_data = json.load(file)

        context = {
            'regions': regions_data,
        }

        return render(request, 'dashboard/dashboard.html', context=context)


class RegionListMeasurementView(View):
    def get(self, request, **kwargs):
        media_path = os.path.join(settings.MEDIA_ROOT, 'map', 'regionMap.json')
        with open(media_path, encoding='utf-8') as file:
            regions_data = json.load(file)

        region_name = None
        for reg in regions_data:
            if reg[1]["properties"]["id"] == kwargs['region_number']:
                region_name = reg[0]
                break

        sensors = SensorReading.objects.filter(region_number=kwargs['region_number'])

        context = {
            "region_number": kwargs['region_number'],
            "region_name": region_name,
            "measurement": sensors,
        }
        return render(request, 'dashboard/measurement_list_by_region.html', context=context)


class MeasurementDetailView(View):
    def get(self, request, **kwargs):
        measurement = SensorReading.objects.get(pk=kwargs['measurement_id'])
        return render(request, 'dashboard/measurement_detail.html', {'measurement': measurement})


class SensorDetailView(View):
    def get(self, request, **kwargs):
        sensor = Sensor.objects.get(pk=kwargs['sensor_id'])
        return render(request, 'dashboard/sensor_detail.html', {'sensor': sensor})


class BuldingsListView(View):
    def get(self, request, **kwargs):
        media_path = os.path.join(settings.MEDIA_ROOT, 'map', 'regionMap.json')
        with open(media_path, encoding='utf-8') as file:
            regions_data = json.load(file)

        region_name = None
        for reg in regions_data:
            if reg[1]["properties"]["id"] == kwargs['region_number']:
                region_name = reg[0]
                break

        buildings = Building.objects.filter(id_region=kwargs['region_number'])
        context = {
            'region_number': kwargs['region_number'],
            'region_name': region_name,
            'buildings': buildings,
        }
        return render(request, 'dashboard/building_list_by_region.html', context)


import plotly.express as px
import plotly.offline as opy
from django.template.defaultfilters import date as date_filter
from collections import defaultdict
import plotly.graph_objs as go
import pandas as pd
import statsmodels.api as sm
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from django.shortcuts import render, get_object_or_404
from django.views import View
import os
import json
from django.conf import settings
from .models import Building, SensorReading
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import plotly.graph_objs as go
import plotly.offline as opy
from django.template.defaultfilters import date as date_filter
import datetime

from statsmodels.tsa.arima.model import ARIMA


class BuildingDetailView(View):
    def get(self, request, **kwargs):
        media_path = os.path.join(settings.MEDIA_ROOT, 'map', 'regionMap.json')
        with open(media_path, encoding='utf-8') as file:
            regions_data = json.load(file)

        build = Building.objects.get(pk=kwargs['building_id'])
        region_name = None
        for reg in regions_data:
            if reg[1]["properties"]["id"] == build.id_region:
                region_name = reg[0]
                break

        measurements = SensorReading.objects.filter(build=build).order_by('datetime')
        measurements_datetime = SensorReading.objects.filter(build=build).order_by('-datetime')
        last_measurement = SensorReading.objects.filter(build=build).last()

        if measurements:

            ######################################################################
            # air_temperature
            formatted_measurements_air_temperature = [
                {
                    'datetime': date_filter(sensor.datetime, 'Y-m-d H:i:s'),
                    'air_temperature': float(sensor.air_temperature),

                }
                for sensor in measurements
            ]

            df = pd.DataFrame(formatted_measurements_air_temperature)
            df['datetime'] = pd.to_datetime(df['datetime'])
            df.set_index('datetime', inplace=True)

            # Создаем модель ARIMA
            model_air_temperature = ARIMA(df['air_temperature'], order=(5, 1, 0))
            result_air_temperature = model_air_temperature.fit()

            # Прогнозируем на 3 года вперед
            forecast_periods = 3 * 365  # 3 года
            forecast_interval = 30  # Прогнозирование через каждые 10 дней
            num_forecast_dates = forecast_periods // forecast_interval  # Вычисляем количество дат прогноза

            forecast_dates = pd.date_range(start=df.index.max(), periods=num_forecast_dates,
                                           freq=f'{forecast_interval}D')  # Прогноз с пропуском 10 дней

            forecast_air_temperature = result_air_temperature.forecast(steps=forecast_periods)

            max_air_temperature = build.max_air_temperature
            min_air_temperature = build.min_air_temperature

            for forecast_temp in forecast_air_temperature:
                if (forecast_temp > max_air_temperature) or (forecast_temp < min_air_temperature):
                    build.status = 'yellow'
                    build.save()
                    break

            # Создаем график
            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['air_temperature'],
                    mode='lines+markers',
                    name='Температура воздуха'
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=forecast_dates,
                    y=forecast_air_temperature,
                    mode='lines',
                    name='Прогноз по температуре воздуха'
                )
            )

            y_min = min(df['air_temperature'])
            y_max = max(df['air_temperature'])
            y_range = max(abs(y_min), abs(y_max))
            y_axis_range = [-y_range, y_range]

            fig.update_layout(
                title='Температура строения',
                xaxis_title='Дата и время',
                yaxis_title='Температура',
                yaxis=dict(zeroline=True, range=y_axis_range),
                legend=dict(yanchor="top", y=-0.2, xanchor="left", x=0.4),
                height=500  # Задайте высоту графика по вашему усмотрению
            )

            # Получаем HTML код для графика
            graph_div_air_temperature = opy.plot(fig, auto_open=False, output_type="div")

            ######################################################################
            # surface_soil_temperature
            formatted_measurements_surface_soil_temperature = [
                {
                    'datetime': date_filter(sensor.datetime, 'Y-m-d H:i:s'),
                    'surface_soil_temperature': float(sensor.surface_soil_temperature),
                    'soil_temperature_10m': float(sensor.soil_temperature_10m),
                    'soil_temperature_5m': float(sensor.soil_temperature_5m)
                }
                for sensor in measurements
            ]

            df = pd.DataFrame(formatted_measurements_surface_soil_temperature)
            df['datetime'] = pd.to_datetime(df['datetime'])
            df.set_index('datetime', inplace=True)

            # Создаем модель ARIMA
            model_surface_soil_temperature = ARIMA(df['surface_soil_temperature'], order=(5, 1, 0))
            result_surface_soil_temperature = model_surface_soil_temperature.fit()

            model_soil_temperature_5m = ARIMA(df['soil_temperature_5m'], order=(5, 1, 0))
            result_soil_temperature_5m = model_soil_temperature_5m.fit()

            model_soil_temperature_10m = ARIMA(df['soil_temperature_10m'], order=(5, 1, 0))
            result_soil_temperature_10m = model_soil_temperature_10m.fit()

            # Прогнозируем на 3 года вперед
            forecast_periods = 3 * 365  # 3 года
            forecast_interval = 30  # Прогнозирование через каждые 10 дней
            num_forecast_dates = forecast_periods // forecast_interval  # Вычисляем количество дат прогноза

            forecast_dates = pd.date_range(start=df.index.max(), periods=num_forecast_dates,
                                           freq=f'{forecast_interval}D')  # Прогноз с пропуском 10 дней

            forecast_surface_soil_temperature = result_surface_soil_temperature.forecast(steps=forecast_periods)
            forecast_soil_temperature_5m = result_soil_temperature_5m.forecast(steps=forecast_periods)
            forecast_soil_temperature_10m = result_soil_temperature_10m.forecast(steps=forecast_periods)

            max_surface_soil_temperature = build.max_surface_soil_temperature
            min_surface_soil_temperature = build.min_surface_soil_temperature

            max_soil_temperature_5m = build.max_soil_temperature_5m
            min_soil_temperature_5m = build.min_soil_temperature_5m

            max_soil_temperature_10m = build.max_soil_temperature_10m
            min_soil_temperature_10m = build.min_soil_temperature_10m

            for forecast_temp in forecast_surface_soil_temperature:
                if (forecast_temp > max_surface_soil_temperature) or (forecast_temp < min_surface_soil_temperature):
                    build.status = 'yellow'
                    build.save()
                    break
            for forecast_temp in forecast_soil_temperature_5m:
                if (forecast_temp > max_soil_temperature_5m) or (forecast_temp < min_soil_temperature_5m):
                    build.status = 'yellow'
                    build.save()
                    break
            for forecast_temp in forecast_soil_temperature_10m:
                if (forecast_temp > max_soil_temperature_10m) or (forecast_temp < min_soil_temperature_10m):
                    build.status = 'yellow'
                    build.save()
                    break

            # Создаем график
            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['surface_soil_temperature'],
                    mode='lines+markers',
                    name='Температура земли на поверхности'
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['soil_temperature_5m'],
                    mode='lines+markers',
                    name='Температура земли на глубине 5м'
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['soil_temperature_10m'],
                    mode='lines+markers',
                    name='Температура земли на глубине 10м'
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=forecast_dates,
                    y=forecast_surface_soil_temperature,
                    mode='lines',
                    name='Прогноз по температуре земли на поверхности'
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=forecast_dates,
                    y=forecast_soil_temperature_5m,
                    mode='lines',
                    name='Прогноз по температуре земли на глубине 5м'
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=forecast_dates,
                    y=forecast_soil_temperature_10m,
                    mode='lines',
                    name='Прогноз по температуре земли на глубине 10м'
                )
            )

            y_min = min(df['surface_soil_temperature'])
            y_max = max(df['surface_soil_temperature'])
            y_range = max(abs(y_min), abs(y_max))
            y_axis_range = [-y_range, y_range]

            fig.update_layout(
                title='Температура строения',
                xaxis_title='Дата и время',
                yaxis_title='Температура',
                yaxis=dict(zeroline=True, range=y_axis_range),
                legend = dict(yanchor="top", y=-0.2, xanchor="left", x=0.4),
                height = 500  # Задайте высоту графика по вашему усмотрению
            )

            # Получаем HTML код для графика
            graph_div_surface_soil_temperature = opy.plot(fig, auto_open=False, output_type="div")


        else:
            graph_div_air_temperature = None
            graph_div_surface_soil_temperature = None

        context = {
            'building': build,
            'region_name': region_name,
            'measurements': measurements_datetime,
            'last_measurement': last_measurement,
            'graph_div_air_temperature': graph_div_air_temperature,
            'graph_div_surface_soil_temperature': graph_div_surface_soil_temperature,
        }
        return render(request, 'dashboard/building_detail.html', context)


# class BuildingDetailView(View):
#     def get(self, request, **kwargs):
#         media_path = os.path.join(settings.MEDIA_ROOT, 'map', 'regionMap.json')
#         with open(media_path, encoding='utf-8') as file:
#             regions_data = json.load(file)
#
#         building = Building.objects.get(id=kwargs['building_id'])
#         region_name = None
#         for reg in regions_data:
#             if reg[1]["properties"]["id"] == building.id_region:
#                 region_name = reg[0]
#                 break
#
#         build = Building.objects.get(pk=kwargs['building_id'])
#         measurements = SensorReading.objects.filter(build=build).order_by('-timestamp')
#         last_measurement = SensorReading.objects.filter(build=build).last()
#
#         if measurements:
#             formatted_measurements = []
#             for sensor in measurements:
#                 formatted_measurement = {
#                     'timestamp': date_filter(sensor.timestamp, 'Y-m-d H:i:s'),
#                     'surface_temperature': sensor.surface_temperature
#                 }
#                 formatted_measurement[
#                     'explanation'] = f"Температура: {sensor.surface_temperature}°C, Время: {formatted_measurement['timestamp']}"
#                 formatted_measurements.append(formatted_measurement)
#
#                 # Extract timestamps, soil temperatures, and explanations for Plotly traces
#                 timestamps = [measurement['timestamp'] for measurement in formatted_measurements]
#                 surface_temperature = [measurement['surface_temperature'] for measurement in formatted_measurements]
#                 explanations = [measurement['explanation'] for measurement in formatted_measurements]
#
#                 # Получаем данные с частотой дней
#                 df = pd.DataFrame(list(measurements.values('timestamp', 'surface_temperature')))
#                 df['timestamp'] = pd.to_datetime(df['timestamp'])  # Преобразуем к стандартному формату
#
#
#                 # Create a Plotly line chart with both smooth curve and data points
#                 fig = go.Figure()
#
#                 # Add line trace for smooth curve
#                 fig.add_trace(
#                     go.Scatter(
#                         x=timestamps,
#                         y=surface_temperature,
#                         mode='lines',
#                         name='Линия трейда'
#                     )
#                 )
#
#                 # Add scatter trace for data points with tooltips
#                 fig.add_trace(
#                     go.Scatter(
#                         x=timestamps,
#                         y=surface_temperature,
#                         mode='markers',  # Use markers to indicate data points
#                         marker=dict(size=6),  # Adjust marker size
#                         name='Значения',
#                         hovertext=explanations,  # Set explanations as hovertext
#                         hoverinfo='text'  # Display hovertext on hover
#                     )
#                 )
#
#                 y_min = min(surface_temperature)
#                 y_max = max(surface_temperature)
#                 y_range = max(abs(y_min), abs(y_max))
#                 y_axis_range = [-y_range, y_range]
#
#                 fig.update_layout(
#                     title='Температура строения',
#                     xaxis_title='Дата и время',
#                     yaxis_title='Температура',
#                     yaxis=dict(zeroline=True, range=y_axis_range)
#                 )
#
#                 # Get the HTML code for the chart
#                 graph_div = opy.plot(fig, auto_open=False, output_type="div")
#
#         else:
#             # Если нет данных об измерениях, график будет пустым
#             graph_div = None
#         context = {
#             'building': building,
#             'region_name': region_name,
#             'measurements': measurements,
#             'last_measurement': last_measurement,
#             # 'average_surface_temperatures': average_surface_temperatures,
#             'graph_div': graph_div,
#         }
#         return render(request, 'dashboard/building_detail.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse


def building_edit(request, building_id):
    building = get_object_or_404(Building, pk=building_id)

    if request.method == 'POST':
        form = BuildingForm(request.POST, request.FILES, instance=building)
        if form.is_valid():
            form.save()
            return redirect(reverse('building_detail', args=[building_id]))
    else:
        form = BuildingForm(instance=building)

    return render(request, 'dashboard/building_edit.html', {'form': form, 'building': building})


class SensortView(View):
    def get(self, request, **kwargs):
        media_path = os.path.join(settings.MEDIA_ROOT, 'map', 'regionMap.json')
        with open(media_path, encoding='utf-8') as file:
            regions_data = json.load(file)

        region_name = None
        for reg in regions_data:
            if reg[1]["properties"]["id"] == kwargs['sensor_id']:
                region_name = reg[0]
                break

        sensors = Sensor.objects.filter(pk=kwargs['region_number'])

        context = {
            "region_number": kwargs['region_number'],
            "region_name": region_name,
            "sensors": sensors,
        }
        return render(request, 'dashboard/sensor_list_by_region.html', context=context)


class CriticalBuildingsView(View):
    def get(self, request):
        critical_buildings_yellow = Building.objects.filter(status='yellow')
        critical_buildings_red = Building.objects.filter(status='red')

        context = {
            'critical_buildings_yellow': critical_buildings_yellow,
            'critical_buildings_red': critical_buildings_red,  # Исправлено название переменной
        }

        return render(request, 'dashboard/critical_buildings.html', context)


from reportlab.lib.styles import ParagraphStyle
import unidecode
import matplotlib.pyplot as plt
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors as reportlab_colors
from dashboard.models import Building, SensorReading
from django.core.files.base import ContentFile
from reportlab.lib import colors


def generate_building_report(request, building_id):
    building = Building.objects.get(id=building_id)
    measurements = SensorReading.objects.filter(build=building).order_by('-timestamp')

    # Create a PDF document using ReportLab
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=0.5 * inch, rightMargin=0.5 * inch,
                            topMargin=0.5 * inch, bottomMargin=0.5 * inch)
    elements = []

    # Define colors
    dark_color = 'black'
    medium_color = '#4f4f4f'  # Dark Grey
    light_color = '#b0b0b0'  # Grey
    white_color = 'white'

    # Define styles
    styles = {
        'Title': ParagraphStyle(name='Title', fontSize=20, alignment=TA_CENTER, fontName='Helvetica-Bold',
                                textColor=dark_color),
        'Normal': ParagraphStyle(name='Normal', fontSize=12, fontName='Helvetica', textColor=dark_color),
    }

    # Add title
    title_text = f"Building Report: {unidecode.unidecode(building.name)}"
    title = Paragraph(title_text, styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.25 * inch))

    # Add building details
    building_details = f"Building Name: {building.name}<br/>" \
                       f"Status: {building.get_status_display()}<br/>" \
                       f"Telephone: {building.telephone}<br/>" \
                       f"Description: {building.description}"
    building_details = unidecode.unidecode(building_details)  # Convert Russian characters to English
    building_details_paragraph = Paragraph(building_details, styles['Normal'])
    elements.append(building_details_paragraph)
    elements.append(Spacer(1, 0.5 * inch))

    # Create data for the table
    table_data = [['Timestamp', 'Air Temperature (°C)', 'Surface Temperature (°C)', 'Soil Temperature 5m (°C)',
                   'Soil Temperature 10m']]
    for reading in measurements:
        table_data.append([
            reading.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            reading.air_temperature,
            reading.surface_soil_temperature,
            reading.soil_temperature_5m,
            reading.soil_temperature_10m,
        ])

    # Create the table
    table = Table(table_data, colWidths=[1.5 * inch] * 6)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), dark_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), white_color),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), light_color),
        ('GRID', (0, 0), (-1, -1), 1, dark_color),
    ]))
    elements.append(table)

    # Create a matplotlib line chart
    plt.figure(figsize=(6, 4))
    timestamps = [reading.timestamp for reading in measurements]
    surface_soil_temperature = [reading.surface_soil_temperature for reading in measurements]
    plt.plot(timestamps, surface_soil_temperature, marker='o', color=dark_color)
    plt.xlabel('Timestamp')
    plt.ylabel('Soil Temperature (°C)')
    plt.title('Soil Temperature Over Time')
    plt.gca().patch.set_facecolor(medium_color)  # Set plot background color
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_color(dark_color)
    plt.gca().spines['left'].set_color(dark_color)

    # Save the matplotlib plot to a BytesIO buffer
    plot_buffer = BytesIO()
    plt.savefig(plot_buffer, format='png', bbox_inches='tight', dpi=300, transparent=True)
    plt.close()

    # Create an Image object with the plot image and add it to the elements list
    img = Image(plot_buffer)
    img.drawHeight = 2.5 * inch
    img.drawWidth = 4 * inch
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph('Graph of Soil Temperature', styles['Normal']))
    elements.append(img)

    # Build the document
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    # Create a HttpResponse object with the PDF content as attachment
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="building_report_{unidecode.unidecode(building.name)}.pdf"'
    response.write(pdf)

    return response
