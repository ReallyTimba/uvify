import flet as ft
import requests
import sqlite3

from dateutil.utils import within_delta


def main(page: ft.Page):
    page.title = 'Weatherly' # window title
    page.theme_mode = 'dark' # it let us change the app theme
    page.vertical_alignment = ft.MainAxisAlignment.CENTER # sets vertical alignment of all the elements in the center of the window
    page.window.width = 540
    page.window.height = 960
    page.bgcolor = None # ft.Colors.GREEN_200 -> good one


    # WIDGETS

    user_data = ft.TextField(label='Search your city', width=400, on_submit=lambda e: get_weather(e))
    theme_button = ft.IconButton(ft.Icons.DARK_MODE, on_click=lambda e: change_theme(e))
    weather_data = ft.Text('')
    uv_icon = ft.Image(src="images/uv_low.webp", width=50, height=50, visible=False)
    uv_progress = ft.ProgressBar(width=400, visible=False)

    weather_symbol = ft.IconButton(ft.Icons.SUNNY, visible=False, on_click=lambda e: get_context(e))





    # EVENTS


    def get_weather(e):
        if len(user_data.value) < 2:
            weather_data.value = ''
            page.update()
            return

        else:
            weather_data.value = ''
            uv_icon.src = ft.Image(src="images/uv_low.webp", width=50, height=50)
            page.update()

        API = '48bb86d3877b44dc9ad193043250606' # OpenWeather API key
        URL = f'http://api.weatherapi.com/v1/current.json?key={API}&q={user_data.value}'
        res = requests.get(URL).json() # gets all the city info
        print(res)
        temp = res['current']['uv']
        weather_data.value = 'UV Index: ' + str(temp)

        uv_icon.visible = True
        uv_icon.src = "images/uv_low.webp" if temp < 5 else "images/uv_high.png"

        uv_progress.visible = True
        uv_progress.value = float(temp / 13)


        weather_symbol.visible = True

        print(res)
        page.update()


    def set_city(e):
        # SETS A CITY TO GET THE WEATHER INFO

        page.clean()
        get_weather(e) # gettings weather info

        page.navigation_bar.destinations[1].disabled = False # enabling the weather tab
        page.add(weather_page)

        page.navigation_bar.destinations[0].visible = False # hiding the track tab (because the city is already set)
        page.navigation_bar.selected_index = 0 # because of the hidden "Track" tab, selected_index = 0 opens the weather info page

        page.update()


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
        welcome_page.controls[1].controls[1].content = ft.ElevatedButton(text='Set', on_click=lambda e: set_city(e))

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

    title_row_weather = ft.Row([theme_button, ft.Text('Weather App')],
                       alignment=ft.MainAxisAlignment.CENTER
                       )

    main_col = ft.Column(
        [

                        ft.Row([weather_data, uv_icon], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([uv_progress], alignment=ft.MainAxisAlignment.CENTER),

        ], # column alignment

                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True
    ) # column alignment


    welcome_updated_col = ft.Column(
                [

                    ft.Row([user_data], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([ft.ElevatedButton(text='Set', on_click=lambda e: get_weather(e))], alignment=ft.MainAxisAlignment.CENTER)
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

    page.add(
        welcome_page
    )





ft.app(target=main) # run app

#ft.app(target=main, view=ft.AppView.WEB_BROWSER) # -> to run the app in the browser