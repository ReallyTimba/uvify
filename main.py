import flet as ft
import requests
import sqlite3
import json
import datetime

from db_manager import Database
Database.initialize()

import calc
import skin_selector as ss
from ui import UIBuilder

from config import API





class UVifyApp:
    def __init__(self, page):

        self.page = page
        self.page.title = 'UVify'  # window title
        self.page.theme_mode = 'dark'  # it let us change the app theme
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER  # sets vertical alignment of all the elements in the center of the window
        self.page.window.width = 540
        self.page.window.height = 960
        self.page.bgcolor = None  # ft.Colors.GREEN_200 -> good one
        self.page.adaptive = True


        self.ui = UIBuilder(self)

        self.load_data()


    def get_weather(self, e=None):
        if len(self.ui.user_data.value) < 2:
            self.ui.uv_data.value = ''
            self.page.update()
            return

        else:
            self.ui.uv_data.value = ''


            self.page.update()

         # OpenWeather API key
        URL_CURRENT = f'http://api.weatherapi.com/v1/current.json?key={API}&q={self.ui.user_data.value}&aqi=yes'
        URL_FORECAST = f'http://api.weatherapi.com/v1/forecast.json?key={API}&days=3&q={self.ui.user_data.value}'
        URL_SEARCH = ''

        res_cur = requests.get(URL_CURRENT).json() # gets all the city info
        res_fore = requests.get(URL_FORECAST).json()


        #res_search = requests.get(URL_SEARCH).json()



        print(res_cur)
        print(res_fore)
        print(res_cur['current']['cloud'])


        with open('requests/weather.json', 'w') as file:
            json.dump(res_fore, file, indent=4)


        with open('requests/days3.json', 'w') as file:
            json.dump(res_fore, file, indent=4)

        # UVI


        uv = res_cur['current']['uv']
        # uv = calc.get_real_uv(res_cur['current']['cloud'], res_cur['current']['uv'])
        self.ui.uv_data.value = 'UV Index: ' + str(uv)

        self.ui.uv_progress.visible = True
        self.ui.uv_progress.value = float(uv / 13)



        self.ui.uv_spf.value = 'SPF ' + str(calc.get_spf(uv, ss.MED[ss.get_skin()]))

        self.ui.act_temp.value = str(res_cur['current']['temp_c']) + " °C"
        self.ui.weather_descr.value = res_cur['current']['condition']['text']
        self.ui.weather_icon.visible = True
        self.ui.weather_icon.src = "https:" + res_cur['current']['condition']['icon']

        # UVI forecasts
        uv_forecasts1 = {}
        uv_forecasts2 = {}
        uv_forecasts3 = {}

        for h in range(0, 24):
            uv_forecasts1[h] = res_fore['forecast']['forecastday'][0]['hour'][h]['uv']

        for h in range(0, 24):
            uv_forecasts2[h] = res_fore['forecast']['forecastday'][1]['hour'][h]['uv']

        for h in range(0, 24):
            uv_forecasts3[h] = res_fore['forecast']['forecastday'][2]['hour'][h]['uv']


        # Adding to the ExpansionPanel


        # Day 1
        self.ui.uv_fore.controls[0].content.title.controls.append(ft.Text(res_fore['forecast']['forecastday'][0]['date'][5:10].replace('-', '/'), size=25))

        year = res_fore['forecast']['forecastday'][0]['date'][:4]
        month = res_fore['forecast']['forecastday'][0]['date'][5:7]
        day = y = res_fore['forecast']['forecastday'][0]['date'][8:]
        print(year, month, day)
        date_converter = datetime.date(int(year), int(month), int(day))

        week = date_converter.isoweekday()
        print(week)

        if week == datetime.date.today().isoweekday():
            self.ui.uv_fore.controls[0].header.title.value = 'Today'



        for k, v in uv_forecasts1.items():






            fore_icon = res_fore['forecast']['forecastday'][0]['hour'][k]['condition']['icon']

            self.ui.uv_fore.controls[0].content.subtitle.controls.append(ft.Column([ft.Text(res_fore['forecast']['forecastday'][0]['hour'][k]['time'][11:], size=20, text_align=ft.alignment.center), ft.Image(src=str("https:" + fore_icon), width=100)], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER))






        self.page.update()






        print(uv_forecasts1)
        print(uv_forecasts2)
        print(uv_forecasts3)

        # General



        # Wind

        self.ui.wind_vel.value = str(res_cur['current']['wind_kph']) + " km/h"

        # AQI

        aqi_units = " μg/m3"

        self.ui.aqi_co.value = "CO: " + str(res_cur['current']['air_quality']['co']) + aqi_units
        self.ui.aqi_no2.value = "NO2: " + str(res_cur['current']['air_quality']['no2']) + aqi_units
        self.ui.aqi_so2.value = "SO2: " + str(res_cur['current']['air_quality']['so2']) + aqi_units


        # SUN

        sunrise24 = datetime.datetime.strptime(res_fore['forecast']['forecastday'][0]['astro']['sunrise'], "%I:%M %p").strftime("%H:%M") # 24-hour format time
        sunset24 = datetime.datetime.strptime(res_fore['forecast']['forecastday'][0]['astro']['sunset'], "%I:%M %p").strftime("%H:%M") # 24-hour format time

        self.ui.sunrise.value = "Sunrise time: " + sunrise24
        self.ui.sunset.value = "Sunset time: " + sunset24



        # DB UPDATE


        db = sqlite3.connect('data.db1')
        cur = db.cursor()

        cur.execute("UPDATE logged SET city_set = ? where user_logged = 1",
                    (res_cur['location']['name'],))
        # cur.execute("INSERT INTO logged (user_logged, city_set) VALUES (?, ?)", (1, res_cur['location']['name']))

        city_name = res_cur['location']['name']
        self.ui.user_city.content.value = city_name

        db.commit()
        db.close()



        self.page.update()


    def set_city(self, e=None):
        # SETS A CITY TO GET THE WEATHER INFO

        self.page.clean()
        self.get_weather(e) # gettings weather info

        self.page.update()
        self.page.navigation_bar.destinations[1].disabled = False # enabling the weather tab
        self.page.add(self.ui.weather_page)

        self.page.navigation_bar.destinations[0].visible = False # hiding the track tab (because the city is already set)
        self.page.navigation_bar.selected_index = 0 # because of the hidden "Track" tab, selected_index = 0 opens the weather info page

        self.page.update()



    def change_theme(self, e):
        self.page.theme_mode = 'light' if self.page.theme_mode == 'dark' else 'dark'
        self.ui.theme_button.icon = ft.Icons.LIGHT_MODE if self.page.theme_mode == 'light' else ft.Icons.DARK_MODE
        self.page.update()

    def navigate(self, e):
        i = self.page.navigation_bar.selected_index
        self.page.clean()

        if self.page.navigation_bar.destinations[0].label == 'Track' and self.page.navigation_bar.destinations[0].visible is True:

            if i == 0:
                self.page.add(self.ui.welcome_page)
            elif i == 1:
                self.page.add(self.ui.weather_page)
            elif i == 2:
                self.page.add(self.ui.settings_page)

        else:
            if i == 0:
                self.page.add(self.ui.weather_page)
            elif i == 1:
                self.page.add(self.ui.settings_page)


        self.page.update()


    def get_context(self, e):

        self.ui.welcome_page.controls[1].controls[0].content = self.ui.user_data
        self.ui.welcome_page.controls[1].controls[1].content = self.ui.set_button

        self.page.update()


    def reset_city(self, e=None):
        self.page.clean()
        self.page.navigation_bar.destinations[0].visible = True
        self.page.navigation_bar.destinations[1].disabled = True
        self.page.navigation_bar.selected_index = 0



        self.page.add(
            self.ui.welcome_updated_col
        )

        self.page.update()


    def load_data(self):
        city_value = Database.get_city()
        if city_value:
            self.ui.user_data.value = city_value
            self.get_weather()
            self.page.navigation_bar.destinations[1].disabled = False
            self.page.navigation_bar.destinations[0].visible = False
            self.page.navigation_bar.selected_index = 0
            self.page.add(self.ui.weather_page)
        else:
            self.page.add(self.ui.welcome_page)



def main(page: ft.Page):
    UVifyApp(page)


if __name__ == "__main__":
    ft.app(target=main) # run app
