import datetime
import random
import sqlite3
import threading
import time

import flet as ft
import requests
from db_manager import Database

Database.initialize()

import calc
from ui_dropdowns import SkinSelector, MED
from ui_builder import UIBuilder, lang
from ui_uv_progress import SemicircleProgress
from ui_screens import LoadingScreen, NoConnectionScreen
from ui_banners import ErrorBanner, AdviceBanner
from advices import ADVICES, SKIN_DESCRS
from config import API
from translations import translate_city, t, run_async
import caching




class UVifyApp:
    def __init__(self, page):

        self.page = page
        self.page.title = 'UVify'  # window title
        self.page.theme_mode = 'dark'  # it let us change the app theme
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER  # sets vertical alignment of all the elements in the center of the window
        # self.page.window.width = 1080
        # self.page.window.height = 1920

        self.page.adaptive = True

        self.page.fonts = {
            'Inter': 'fonts/Inter.ttf'
        }


        self.page.bgcolor = '#2a0845' # original





        self.page.theme = ft.Theme(font_family='Inter')
        # self.page.padding = ft.padding.only(left=20, right=20, top=20, bottom=20)
        self.page.padding = 0
        self.page.spacing = 0

        self.page.adaptive = True


        self.page.foreground_decoration = ft.BoxDecoration(
            image=ft.DecorationImage(
                src="icons/wallpaper.png",
                fit=ft.BoxFit.COVER,
                opacity=0.15,
                filter_quality=ft.FilterQuality.LOW
            ),

        )



        db = sqlite3.connect(Database.DB_FILE)  # -> opens the connection with the db
        cur = db.cursor()  # -> sets a cursor to move inside the db

        cur.execute("SELECT units FROM logged WHERE user_logged = 1")
        measure = cur.fetchone()[0]

        self.measure = measure

        db.commit()
        db.close()



        # Builds main UI elements
        self.ui = UIBuilder(self)

        # Builds the UV index progress
        self.sc_progress = SemicircleProgress()

        # Builds the loading screen
        self.loading_screen = LoadingScreen(self)

        # Builds the no connection screen
        self.noconnection = NoConnectionScreen(self, self.ui.retry_button)

        # Builds the banners
        self.error_banner = ErrorBanner(self, self.ui)
        self.advice_banner = AdviceBanner(self, self.ui)



        # Loads the DB data
        self.load_data()


    def get_weather(self, trigger_snack=False, return_settings_page=False):


        if len(self.ui.user_data.value) < 2:

            try:
                self.advice_banner.close_banner()
            except ValueError:
                pass
            self.error_banner.set_city_name(self.ui.user_data.value)
            self.error_banner.trigger_banner()

            return


        # self.loading_screen.show_loading()



        self.weather_data = ''
        def load():


            lang_additions = '&lang=en'
            city = self.ui.user_data.value


            if lang == 'es':

                try:

                    city = run_async(translate_city(self.ui.user_data.value)).text
                    lang_additions = '&lang=es'

                except (requests.exceptions.ConnectionError, sqlite3.OperationalError):
                    self.noconnection.show_screen()



            # OpenWeather API key
            # URL_CURRENT = f'http://api.weatherapi.com/v1/current.json?key={API}&q={self.ui.user_data.value}&aqi=yes&lang=es'

            # URL_CURRENT = f'http://api.weatherapi.com/v1/current.json?key={API}&q={city}&aqi=yes' + lang_additions
            URL = f'http://api.weatherapi.com/v1/forecast.json?key={API}&days=3&q={city}&aqi=yes' + lang_additions


            # self.res_cur = requests.get(URL_CURRENT).json() # gets all the city info
            try:
                self.weather_data = requests.get(URL).json()
            except:
                self.noconnection.show_screen()

            # caching.save_json('assets/requests/res_fore.json', self.weather_data)
            self.__process_weather_data(self.weather_data, trigger_snack=trigger_snack, return_settings_page=return_settings_page)



        threading.Thread(target=load).start()

    def __process_weather_data(self, data, trigger_snack, return_settings_page):

        try:
            # UVI
            ss = SkinSelector()


            raw_uv = data['current']['uv']
            self.clouds = data['current']['cloud']
            uv = raw_uv
            h = int(data['location']['localtime'][11:13])

            uv_a1 = calc.uv_ahead(h, 1)
            uv_a2 = calc.uv_ahead(h, 2)

            try:
                uv2 = data['forecast']['forecastday'][uv_a1[0]]['hour'][uv_a1[1]]['uv']
                uv3 = data['forecast']['forecastday'][uv_a2[0]]['hour'][uv_a2[1]]['uv']
            except IndexError:
                return





            spf = 'SPF ' if lang == 'en' else 'FPS '

            self.ui.uv_spf.value = spf + str(calc.get_spf(uv, MED[ss.get_skin()]))

            self.ui.uv_level.value = t('high_uv', lang) if uv >= 6 else t('moderate_uv', lang) if uv >= 3 else t('low_uv', lang)
            # self.ui.uv_level.color = self.ui.progress_colors[0.666] if uv >= 6 else self.ui.progress_colors[0.333] if uv >= 3 else self.ui.progress_colors[0]

            v_d = calc.get_vitamin_d(uv, MED[ss.get_skin()])
            if v_d != 'no_d':
                self.ui.vitamin_d.content.controls[1].controls[1].value = str(v_d) + ' min'
            else:
                self.ui.vitamin_d.content.controls[1].controls[1].value = t('no_vitamin_d', lang)
                self.ui.vitamin_d.content.controls[1].controls[1].size = 14

            # converts the uv in to a progress semicircle value

            self.sc_progress.set_index(uv)

            # sets the UV level text color as the last semicircle progress color

            self.ui.uv_level.color = self.sc_progress.color



            self.ui.main_col.controls[1].content.controls[1].content.controls[0] = ft.Container(self.sc_progress.progress_bar, padding=ft.Padding(left=35))
            # self.ui.main_col.controls[1].content.controls[2].controls.append(ft.Row([ft.Container(ft.Icon(name=ft.Icons.WARNING, size=30, color='#ea0000'), padding=ft.padding.only(right=25, bottom=10, left=10))], alignment=ft.MainAxisAlignment.END))
            if uv >= 7:
                self.ui.main_col.controls[1].content.controls[1].content.controls[1] = ft.Container(ft.Icon(icon=ft.Icons.WARNING, size=30, color='#ea0000'), padding=ft.Padding(top=65))
            else:
                self.ui.main_col.controls[1].content.controls[1].content.controls[1] = ft.Container()


            burn_minutes = calc.get_burn([uv, uv2, uv3], MED[ss.get_skin()])


            burn_hours = burn_minutes // 60
            rest_burn_minutes = burn_minutes % 60

            if burn_minutes:
                if burn_hours and rest_burn_minutes:
                    self.ui.burn_time.value = f'{burn_hours} h {rest_burn_minutes} min'
                elif burn_hours and not rest_burn_minutes:
                    self.ui.burn_time.value = f'{burn_hours} h'
                elif rest_burn_minutes and not burn_hours:
                    self.ui.burn_time.value = f'{rest_burn_minutes} min'
            else:
                self.ui.burn_time.value = '∞ min'

            # if burn_hours != 0 and burn_minutes != 0 and rest_burn_minutes != 0:
            #     self.ui.burn_time.value = f'{burn_hours} h {rest_burn_minutes} min'
            # elif rest_burn_minutes == 0 and burn_minutes != 0:
            #     self.ui.burn_time.value = f'{burn_hours} h'
            # elif burn_hours == 0 and burn_minutes != 0:
            #     self.ui.burn_time.value = f'{rest_burn_minutes} min'
            # else:
            #     self.ui.burn_time.value = '∞ min'

            #self.ui.burn_time.value = f'{burn_hours} h {rest_burn_minutes} min' if rest_burn_minutes != 0 and burn_minutes != 0 else f'{burn_hours} h' if burn_minutes != 0 else '∞ min'

            # GENERAL

            degrees = " °C" if self.measure == 'metric' else " °F"
            degrees_format = 'c' if self.measure == 'metric' else 'f'

            self.ui.act_temp.value = str(data['current'][f'temp_{degrees_format}']) + degrees
            self.ui.weather_descr.value = data['current']['condition']['text']
            self.ui.weather_icon.visible = True
            self.ui.weather_icon.src = "https:" + data['current']['condition']['icon']

            self.ui.localtime.value = data['location']['localtime'][11:]

            self.is_day = data['current']['is_day']


            # UVI FORECASTS

            # Cleaning previous info

            for panel in self.ui.uv_fore.controls:
                panel.content.content.title.controls.clear()
                panel.content.content.subtitle.controls.clear()

            # Adding to the ExpansionPanel

            for i in range(3):

                # Date adding on the title widget

                self.ui.uv_fore.controls[i].expanded = False
                date = f"{data['forecast']['forecastday'][i]['date'][8:]}/{data['forecast']['forecastday'][i]['date'][5:7]}"
                self.ui.uv_fore.controls[i].content.content.title.controls.append(
                    ft.Text(date, size=20, weight=ft.FontWeight.W_600))

                # Adding the header for the ExpansionPanel

                year = data['forecast']['forecastday'][i]['date'][:4]
                month = data['forecast']['forecastday'][i]['date'][5:7]
                day = y = data['forecast']['forecastday'][i]['date'][8:]
                date_converter = datetime.date(int(year), int(month), int(day))

                week = date_converter.isoweekday()

                # Checking if the first forecast day is today

                if week == datetime.date.today().isoweekday():
                    self.ui.uv_fore.controls[i].header.content.title.value = t('today', lang)

                else:
                    self.ui.uv_fore.controls[i].header.content.title.value = t(date_converter.strftime("%A").lower(), lang)



                self.ui.uv_fore.controls[i].content.content.subtitle.controls.append(

                    ft.Column(
                        [
                            ft.Text(t('time', lang), size=20, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500,
                                    text_align=ft.TextAlign.CENTER),
                            ft.Image(src="icons/vitamind_icon.png", color=ft.Colors.TRANSPARENT, width=80),
                            ft.Container(ft.Text('UV', size=20, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500,
                                                 text_align=ft.TextAlign.CENTER), border_radius=15, padding=ft.Padding(top=3, bottom=3, left=12, right=12), margin=ft.Margin(bottom=20)
                                         ),

                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    )
                )

                # Entering the information of the UV forecast on the page
                for h_index in range(24):

                    fore_uv = data['forecast']['forecastday'][i]['hour'][h_index]['uv']
                    fore_time = data['forecast']['forecastday'][i]['hour'][h_index]['time'][11:]
                    uv_color = self.ui.uv_colors[6] if fore_uv >= 6 else self.ui.uv_colors[3] if fore_uv >= 3 else \
                        self.ui.uv_colors[0]


                    fore_icon = data['forecast']['forecastday'][i]['hour'][h_index]['condition']['icon']


                    self.ui.uv_fore.controls[i].content.content.subtitle.controls.append(ft.Column([
                        ft.Text(fore_time, size=20, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500,
                                text_align=ft.TextAlign.CENTER),
                        ft.Image(src=str("https:" + fore_icon), width=80),
                        ft.Container(ft.Text(
                            str(fore_uv), size=20, color=uv_color, weight=ft.FontWeight.W_500,
                            text_align=ft.TextAlign.CENTER), bgcolor=ft.Colors.WHITE, border_radius=15, padding=ft.Padding(top=3, bottom=3, left=12, right=12), margin=ft.Margin(bottom=20)),
                        # ft.Text(
                        # str(calc.get_vitamin_d(data['forecast']['forecastday'][i]['hour'][h_index]['uv'], ss.MED[ss.get_skin()])), size=20,
                        # text_align=ft.TextAlign.CENTER),

                    ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                    )

            # General

            # Wind

            velocity = ' km/h' if self.measure == 'metric' else ' mph'
            velocity_format = 'kph' if self.measure == 'metric' else 'mph'

            other_units = f'{round(data['current']['wind_kph'] / 3.6, 1)} m/s' if self.measure == 'metric' else f'{round(data['current']['wind_mph'] * 1.4667, 2)} ft/s'

            self.ui.wind_vel.value = str(data['current'][f'wind_{velocity_format}']) + velocity + f'\n({other_units})'

            # AQI

            # aqi_units = " μg/m3"


            co = float(data['current']['air_quality']['co']) / 3000
            no2 = float(data['current']['air_quality']['no2']) / 100
            so2 = float(data['current']['air_quality']['so2']) / 35

            # Arithmetical mean of the three air data values
            a_mean = (co + no2 + so2) / 3


            self.ui.air_estimated.value = t('aqi_critical', lang) if a_mean >= 0.666 else t('aqi_moderate', lang) if a_mean >= 0.333 else t('aqi_good', lang)
            self.ui.air_estimated.color = self.ui.progress_colors[0.666] if a_mean >= 0.666 else self.ui.progress_colors[0.333] if a_mean >= 0.333 else \
                self.ui.progress_colors[0]

            co_color = self.ui.progress_colors[0.666] if co >= 0.666 else self.ui.progress_colors[0.333] if co >= 0.333 else \
                self.ui.progress_colors[0]
            no2_color = self.ui.progress_colors[0.666] if no2 >= 0.666 else self.ui.progress_colors[
                0.333] if no2 >= 0.333 else self.ui.progress_colors[0]
            so2_color = self.ui.progress_colors[0.666] if so2 >= 0.666 else self.ui.progress_colors[
                0.333] if so2 >= 0.333 else self.ui.progress_colors[0]


            self.ui.progress_co.color = co_color
            self.ui.progress_no2.color = no2_color
            self.ui.progress_so2.color = so2_color

            self.ui.progress_co.value = co
            self.ui.progress_no2.value = no2
            self.ui.progress_so2.value = so2

            self.ui.co_level.value = self.ui.progress_levels[co_color]
            self.ui.no2_level.value = self.ui.progress_levels[no2_color]
            self.ui.so2_level.value = self.ui.progress_levels[so2_color]

            # SUN

            sunrise24 = datetime.datetime.strptime(data['forecast']['forecastday'][0]['astro']['sunrise'],
                                                   "%I:%M %p").strftime("%H:%M")  # 24-hour format time
            sunset24 = datetime.datetime.strptime(data['forecast']['forecastday'][0]['astro']['sunset'],
                                                  "%I:%M %p").strftime("%H:%M")  # 24-hour format time

            self.ui.sunrise_time.value = sunrise24
            self.ui.sunset_time.value = sunset24



            # DB UPDATE

            db = sqlite3.connect('data.db1')
            cur = db.cursor()

            city_name = data['location']['name']
            country_name = data['location']['country']

            cur.execute("UPDATE logged SET city_set = ?, country_set = ? where user_logged = 1",
                        (city_name, country_name,))

            self.ui.user_city.content.value = f"{city_name}, {country_name}"

            if lang == 'es':
                try:

                    self.ui.user_city.content.value = run_async(translate_city(f"{city_name}, {country_name}", src='en', dest='es')).text
                    self.ui.user_data.value = run_async(translate_city(city_name, src='en', dest='es')).text
                except (requests.exceptions.ConnectionError, sqlite3.OperationalError):
                    self.noconnection.show_screen()

            db.commit()
            db.close()

            self.page.clean()
            self.page.navigation_bar.visible = True
            if return_settings_page:
                self.page.add(self.ui.settings_page)


            else:
                self.page.add(self.ui.weather_page)
                self.loading_screen.hide_loading()
                self.page.navigation_bar.selected_index = 0


            if trigger_snack:
                skin_description = ft.SnackBar(content=ft.Text(SKIN_DESCRS[lang][ss.get_skin()], color=ft.Colors.WHITE), bgcolor='#f27121')
                self.page.show_dialog(skin_description)


        except KeyError:
            self.page.clean()
            self.reset_city()
            self.error_banner.set_city_name(self.ui.user_data.value)
            self.error_banner.trigger_banner()

        except requests.exceptions.ConnectionError:
            self.get_weather()


        self.page.update()

        # ADVICES

        self.set_advice(data)

    def set_city(self, e=None, settings=False):
        # SETS A CITY TO GET THE WEATHER INFO

        self.get_weather(return_settings_page=settings) # gettings weather info

        self.page.update()
        self.page.navigation_bar.destinations[1].disabled = False # enabling the weather tab


        self.page.navigation_bar.destinations[0].visible = False # hiding the track tab (because the city is already set)
        self.page.navigation_bar.selected_index = 0 # because of the hidden "Track" tab, selected_index = 0 opens the weather info page

        # self.page.add(self.ui.weather_page)
        # self.page.update()


    def set_advice(self, weather_data=None):

        if Database.user_advices() == 1 and self.ui.switches.controls[0].controls[1].value is True:

            cathegory = random.choices([0, 1], weights=[0.6, 0.4])[0]

            if self.page.navigation_bar.selected_index == 0 and not self.page.navigation_bar.destinations[0].visible and self.is_day == 1:

                if cathegory == 0 and self.clouds < 80 and weather_data['current']['uv'] > 4:
                    if float(weather_data['current'][f'temp_c']) > 24:

                        self.advice_banner.advice_text.value = random.choice(ADVICES[lang]['statistic_advices']['high_temp'])
                        self.advice_banner.trigger_banner()

                    elif 17 < float(weather_data['current'][f'temp_c']) <= 24:

                        self.advice_banner.advice_text.value = random.choice(ADVICES[lang]['statistic_advices']['moderate_temp'])
                        self.advice_banner.trigger_banner()

                    elif float(weather_data['current'][f'temp_c']) <= 17:

                        self.advice_banner.advice_text.value = random.choice(ADVICES[lang]['statistic_advices']['low_temp'])
                        self.advice_banner.trigger_banner()

                elif cathegory == 1:

                    subcathegory = random.choice(['clouds', 'remind', 'special'])

                    self.advice_banner.advice_text.value = random.choice(ADVICES[lang]['reminders'][subcathegory])
                    self.advice_banner.trigger_banner()



    # def change_theme(self, e):
    #     self.page.theme_mode = 'light' if self.page.theme_mode == 'dark' else 'dark'
    #     self.ui.theme_button.icon = ft.Icons.LIGHT_MODE if self.page.theme_mode == 'light' else ft.Icons.DARK_MODE
    #
    #     self.ui.air_info.bgcolor = ft.Colors.WHITE if self.page.theme_mode == 'dark' else ft.Colors.BLACK
    #     self.ui.air_info.content.controls[0].controls[0].color = ft.Colors.WHITE if self.page.theme_mode == 'light' else ft.Colors.BLACK
    #     for el in self.ui.air_info.content.controls[1].controls:
    #         el.color = ft.Colors.WHITE if self.page.theme_mode == 'light' else ft.Colors.BLACK
    #         print(el)
    #
    #     self.page.update()


    def change_system(self, e):
        time.sleep(0.25)
        self.measure = 'imperial' if self.measure != 'imperial' else 'metric'

        db = sqlite3.connect(Database.DB_FILE)
        cur = db.cursor()

        cur.execute("UPDATE logged SET units = ? where user_logged = 1",
                    (self.measure,))
        # cur.execute("INSERT INTO logged (user_logged, city_set) VALUES (?, ?)", (1, res_cur['location']['name']))


        db.commit()
        db.close()

        self.ui.switches.controls[2].controls[0].value = f'{t('units', lang)}: {t(f'{self.measure}_units', lang)}'

        if self.weather_data:
            self.__process_weather_data(self.weather_data, False, False)
        else:
            self.get_weather()

    def toggle_advices(self, e=None, banner_hide=False):

        self.advices_enabled = 0 if Database.user_advices() == 1 else 1


        db = sqlite3.connect(Database.DB_FILE)
        cur = db.cursor()

        if banner_hide:
            cur.execute("UPDATE logged SET advices = ? where user_logged = 1",
                        (0,))

        else:
            cur.execute("UPDATE logged SET advices = ? where user_logged = 1",
                        (self.advices_enabled,))


        db.commit()
        db.close()




    def navigate(self, e):
        i = self.page.navigation_bar.selected_index
        self.page.clean()


        if self.page.navigation_bar.destinations[0].label == t('track_nav', lang) and self.page.navigation_bar.destinations[0].visible is True:

            if i == 0:
                if self.ui.user_data:
                    self.page.add(self.ui.welcome_updated)
                else:
                    self.page.add(self.ui.welcome_page)
                try:
                    self.advice_banner.close_banner()
                except ValueError:
                    pass
            elif i == 1:
                self.page.add(self.ui.weather_page)
                self.set_advice(self.weather_data)
            elif i == 2:
                self.page.add(self.ui.settings_page)
                try:
                    self.advice_banner.close_banner()
                except ValueError:
                    pass

        else:
            if i == 0:
                self.page.add(self.ui.weather_page)
                if self.weather_data:
                    self.set_advice(self.weather_data)

            elif i == 1:
                self.page.add(self.ui.settings_page)
                try:
                    self.advice_banner.close_banner()
                except ValueError:
                    pass


        self.page.update()


    def get_started(self, e):

        self.ui.welcome_page.content.controls[3].controls[0] = self.ui.user_data
        self.ui.welcome_page.content.controls[3].controls[2] = self.ui.set_button
        self.ui.welcome_page.content.controls[3].controls[1].content.visible = True

        self.page.update()


    def reset_city(self, e=None):
        self.page.clean()
        self.page.navigation_bar.destinations[0].visible = True
        self.page.navigation_bar.destinations[1].disabled = True
        self.page.navigation_bar.selected_index = 0


        self.page.add(
            self.ui.welcome_updated
        )

        self.page.update()


    def load_data(self):

        city_value = Database.get_city()
        self.ui.switches.controls[2].controls[0].value = f'{t('units', lang)}: {t(f'{self.measure}_units', lang)}'
        displayed_name = city_value


        try:

            displayed_name = run_async(translate_city(city_value, src='en', dest='es')).text if lang == 'es' else city_value
        except Exception as e:
            print(e)
            self.noconnection.show_screen()

        if city_value:
            self.ui.user_data.value = displayed_name
            self.page.navigation_bar.destinations[1].disabled = False
            self.page.navigation_bar.destinations[0].visible = False
            self.page.navigation_bar.selected_index = 0
            # self.page.add(self.ui.weather_page)
            self.get_weather()
        else:
            self.page.add(self.ui.welcome_page)






def main(page: ft.Page):
    UVifyApp(page)


if __name__ == "__main__":
    ft.run(main, assets_dir="assets") # run app
