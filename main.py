import time
from itertools import pairwise

import flet as ft
import requests
import sqlite3
import os
import json
import flet.canvas as cv
import math

def deploy_db():
    db = sqlite3.connect('data.db1')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS logged (
        id INTEGER PRIMARY KEY,
        user_logged INTEGER,
        city_set TEXT
    )""")
    cur.execute("SELECT * FROM logged WHERE user_logged = 1")
    if not cur.fetchone():
        cur.execute("INSERT INTO logged (user_logged, city_set) VALUES (?, ?)", (1, None))
    db.commit()
    db.close()



def main(page: ft.Page):
    deploy_db()
    page.title = 'Weatherly' # window title
    page.theme_mode = 'dark' # it let us change the app theme
    page.vertical_alignment = ft.MainAxisAlignment.CENTER # sets vertical alignment of all the elements in the center of the window
    page.window.width = 540
    page.window.height = 960
    page.bgcolor = None # ft.Colors.GREEN_200 -> good one



    # WIDGETS

    user_data = ft.TextField(label='Search your city', width=400, on_submit=lambda e: get_weather(e))
    theme_button = ft.IconButton(ft.Icons.DARK_MODE, on_click=lambda e: change_theme(e))


    # UVI

    uv_data = ft.Text('')
    uv_progress = ft.ProgressBar(width=400, visible=False)

    # General

    weather_descr = ft.Text('')
    weather_icon = ft.Image(src="https://cdn.weatherapi.com/weather/64x64/night/113.png", width=50, height=50,
                            visible=False)
    act_temp = ft.Text('')


    # Wind

    wind_vel = ft.Text('')

    # AQI
    black = ft.Colors.BLACK


    aqi_co = ft.Text('', color=black)
    aqi_no2 = ft.Text('', color=black)
    aqi_so2 = ft.Text('', color=black)

    # SUN

    sunrise = ft.Text('')
    sunset = ft.Text('')
    progress = cv.Canvas()
    progress.shapes.clear()
    progress.shapes.append(cv.Arc(width=100, height=50, start_angle=math.pi, sweep_angle=math.pi, paint=ft.Paint(ft.Colors.BLUE, stroke_width=10)))



    # Buttons

    set_button = ft.Row([ft.ElevatedButton(text='Set', on_click=lambda e: set_city(e))], alignment=ft.MainAxisAlignment.CENTER)





    # EVENTS


    def get_weather(e=None):

        # Data base user reg

        db = sqlite3.connect('data.db1')  # -> opens the connection with the db

        cur = db.cursor()  # -> sets a cursor to move inside the db

        cur.execute(f"INSERT INTO logged VALUES(NULL, 1, NULL)")

        db.commit()
        db.close()  # -> To close the connection with the db


        if len(user_data.value) < 2:
            uv_data.value = ''
            page.update()
            return

        else:
            uv_data.value = ''


            page.update()

        API = '48bb86d3877b44dc9ad193043250606' # OpenWeather API key
        URL_CURRENT = f'http://api.weatherapi.com/v1/current.json?key={API}&q={user_data.value}&aqi=yes'
        URL_FORECAST = f'http://api.weatherapi.com/v1/forecast.json?key={API}&q={user_data.value}'
        URL_HOUR = f'http://api.weatherapi.com/v1/future.json?key={API}&hour=20&q={user_data.value}'
        URL_SEARCH = f''

        res_cur = requests.get(URL_CURRENT).json() # gets all the city info
        res_fore = requests.get(URL_FORECAST).json()

        #res_search = requests.get(URL_SEARCH).json()



        print(res_cur)
        print(res_fore)


        with open('weather.json', 'w') as file:
            json.dump(res_fore, file, indent=4)

        # UVI

        uv = res_cur['current']['uv']
        uv_data.value = 'UV Index: ' + str(uv)

        uv_progress.visible = True
        uv_progress.value = float(uv / 13)

        # General

        act_temp.value = str(res_cur['current']['temp_c']) + " °C"
        weather_descr.value = res_cur['current']['condition']['text']
        weather_icon.visible = True
        weather_icon.src = "https:" + res_cur['current']['condition']['icon']

        # Wind

        wind_vel.value = str(res_cur['current']['wind_kph']) + " kph"

        # AQI

        aqi_co.value = "CO: " + str(res_cur['current']['air_quality']['co'])
        aqi_no2.value = "NO2: " + str(res_cur['current']['air_quality']['no2'])
        aqi_so2.value = "SO2: " + str(res_cur['current']['air_quality']['so2'])


        # SUN

        sunrise.value = res_fore['forecast']['forecastday'][0]['astro']['sunrise']
        sunset.value = res_fore['forecast']['forecastday'][0]['astro']['sunset']





        db = sqlite3.connect('data.db1')
        cur = db.cursor()

        cur.execute("DELETE FROM logged")  # очистка старых записей
        cur.execute("INSERT INTO logged (user_logged, city_set) VALUES (?, ?)", (1, res_cur['location']['name']))

        city_name = res_cur['location']['name']
        user_city.content.value = city_name


        db.commit()
        db.close()




        page.update()



    def set_city(e):
        # SETS A CITY TO GET THE WEATHER INFO

        page.clean()
        get_weather(e) # gettings weather info

        page.update()
        page.navigation_bar.destinations[1].disabled = False # enabling the weather tab
        page.add(weather_page)

        page.navigation_bar.destinations[0].visible = False # hiding the track tab (because the city is already set)
        page.navigation_bar.selected_index = 0 # because of the hidden "Track" tab, selected_index = 0 opens the weather info page

        page.update()


    def get_city():
        db = sqlite3.connect('data.db1')  # -> opens the connection with the db
        cur = db.cursor()  # -> sets a cursor to move inside the db

        cur.execute("SELECT city_set FROM logged WHERE user_logged = 1")
        city = cur.fetchone()[0]

        return city



        #page.update()

    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        theme_button.icon = ft.Icons.LIGHT_MODE if page.theme_mode == 'light' else ft.Icons.DARK_MODE
        page.update()

    def navigate(e):
        i = page.navigation_bar.selected_index
        page.clean()

        if page.navigation_bar.destinations[0].label == 'Track' and page.navigation_bar.destinations[0].visible is True:

            if i == 0:
                page.add(welcome_page)
            elif i == 1:
                page.add(weather_page)
            elif i == 2:
                page.add(settings_page)

        else:
            if i == 0:
                page.add(weather_page)
            elif i == 1:
                page.add(settings_page)


        page.update()


    def get_context(e):

        welcome_page.controls[1].controls[0].content = user_data
        welcome_page.controls[1].controls[1].content = set_button

        page.update()


    def reset_city(e=None):
        page.clean()
        page.navigation_bar.destinations[0].visible = True
        page.navigation_bar.destinations[1].disabled = True
        page.navigation_bar.selected_index = 0



        page.add(
            welcome_updated_col
        )

        page.update()

    def torredembarra(e):
        page.clean()

        page.add(
            weather_page
        )


    # NAVIGATION BAR

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.ADD_LOCATION_OUTLINED, label="Track",
                                        selected_icon=ft.Icons.ADD_LOCATION_SHARP),
            ft.NavigationBarDestination(icon=ft.Icons.WB_SUNNY_OUTLINED, label="Weather",
                                        selected_icon=ft.Icons.SUNNY, disabled=True), # is not able on first login
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS_OUTLINED, label="Settings",
                                        selected_icon=ft.Icons.SETTINGS_SHARP),

        ], on_change=lambda e: navigate(e)
    )



    # PAGE WIDGETS
    city_text = ft.Container(ft.Text("Your city: "), padding=ft.padding.only(left=8))
    user_city = ft.TextButton(content=ft.Text(str(get_city()), color=ft.Colors.BLUE), style=ft.ButtonStyle(overlay_color=ft.Colors.TRANSPARENT), on_click=lambda e: reset_city(e))
    page.update()

    title_row_weather = ft.Row(
        [
        ft.Column([city_text, user_city], alignment=ft.MainAxisAlignment.START),
        ft.Row([theme_button, ft.Text('Theme')],
               alignment=ft.MainAxisAlignment.CENTER
               )
    ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    wind_info = ft.Container(content=ft.Column([ft.Text('Wind Speed'), wind_vel], alignment=ft.MainAxisAlignment.CENTER), bgcolor=ft.Colors.BLUE, border_radius=10, padding=15)
    sun_info = ft.Container(content=ft.Column([ft.Text('Sun Time'), sunrise, sunset], alignment=ft.MainAxisAlignment.CENTER), bgcolor=ft.Colors.BLUE, border_radius=10, padding=30)
    air_info = ft.Container(ft.Column([ft.Text('Air Quality', color=ft.Colors.BLACK), aqi_co, aqi_no2, aqi_so2], alignment=ft.MainAxisAlignment.CENTER), bgcolor=ft.Colors.WHITE, border_radius=10, padding=30)


    main_col = ft.Column( # ALL THE WEATHER INFO IS HERE
        [
                        ft.Row([weather_icon, weather_descr], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([act_temp], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                        ft.Row([uv_data], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([uv_progress], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([wind_info], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Text(''), # change this space
                        ft.Row([air_info], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Text(''),
                        ft.Row(
                [
                    sun_info
                ],
                alignment=ft.MainAxisAlignment.CENTER),

        ], # column alignment

                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True
    ) # column alignment


    welcome_updated_col = ft.Column(
        [
                    ft.Row([user_data], alignment=ft.MainAxisAlignment.CENTER),
                    set_button

                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )

    # PAGES


    welcome_page = ft.Column( # general block
        [
            ft.Row( # Row 1 -> Header content
                [
                    ft.Text("Welcome to Weatherly!", text_align=ft.alignment.center, size=25)
                ],
                alignment=ft.MainAxisAlignment.CENTER # Row 1 -> settings
            ),
            ft.Column(
                [
                    ft.Container(content=ft.FilledButton("Start following your city", width=300, height=38, style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)), on_click=get_context), alignment=ft.alignment.center),
                    ft.Container(content=ft.TextButton("Are you from Torredembarra?", on_click=torredembarra), alignment=ft.alignment.center)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        ],
        expand=True # -> general block (Column settings)

    )

    weather_page = ft.Column([
        title_row_weather,
        main_col
        ],
        expand=True
    )

    settings_page = ft.Column(
        [
            ft.Row([ft.Text("Settings")], alignment=ft.MainAxisAlignment.CENTER)

        ],
        alignment=ft.MainAxisAlignment.START
    )

    # Logged or not check

    city_value = get_city()
    if city_value:
        user_data.value = city_value
        get_weather()
        page.navigation_bar.destinations[1].disabled = False
        page.navigation_bar.destinations[0].visible = False
        page.navigation_bar.selected_index = 0
        page.add(weather_page)
    else:
        page.add(welcome_page)



if __name__ == "__main__":
    ft.app(target=main) # run app

#ft.app(target=main, view=ft.AppView.WEB_BROWSER) # -> to run the app in the browser