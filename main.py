import flet as ft
import requests
import sqlite3
import os



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
    uv_data = ft.Text('')
    act_temp = ft.Text('')
    weather_icon = ft.Image(src="https://cdn.weatherapi.com/weather/64x64/night/113.png", width=50, height=50, visible=False)
    uv_progress = ft.ProgressBar(width=400, visible=False)
    weather_descr = ft.Text('')
    weather_symbol = ft.IconButton(ft.Icons.SUNNY, visible=False, on_click=lambda e: get_context(e))





    # EVENTS


    def get_weather(e=None):

        # Data base user reg

        db = sqlite3.connect('data.db1')  # -> opens the connection with the db

        cur = db.cursor()  # -> sets a cursor to move inside the db
        cur.execute("""CREATE TABLE IF NOT EXISTS logged (
                            id INTEGER PRIMARY KEY,
                            user_logged INTEGER,
                            city_set TEXT
                        )""")
        cur.execute(f"INSERT INTO logged VALUES(NULL, 1, NULL)")

        db.commit()
        db.close()  # -> To close the connection with the db


        if len(user_data.value) < 2:
            uv_data.value = ''
            page.update()
            return

        else:
            uv_data.value = ''

            # entering the db



            # request


            page.update()

        API = '48bb86d3877b44dc9ad193043250606' # OpenWeather API key
        URL = f'http://api.weatherapi.com/v1/current.json?key={API}&q={user_data.value}'
        res = requests.get(URL).json() # gets all the city info
        print(res)
        uv = res['current']['uv']
        act_temp.value = str(res['current']['temp_c']) + " °C"
        weather_descr.value = res['current']['condition']['text']

        uv_data.value = 'UV Index: ' + str(uv)

        weather_icon.visible = True
        weather_icon.src = "https:" + res['current']['condition']['icon']


        uv_progress.visible = True
        uv_progress.value = float(uv / 13)


        weather_symbol.visible = True

        db = sqlite3.connect('data.db1')
        cur = db.cursor()

        cur.execute("DELETE FROM logged")  # очистка старых записей
        cur.execute("INSERT INTO logged (user_logged, city_set) VALUES (?, ?)", (1, user_data.value))

        db.commit()
        db.close()

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



    def get_city():
        db = sqlite3.connect('data.db1')  # -> opens the connection with the db
        cur = db.cursor()  # -> sets a cursor to move inside the db

        cur.execute("SELECT city_set FROM logged WHERE user_logged = 1")
        city = cur.fetchone()[0]

        return city if city is not None else "Moscow"





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
    city_text = ft.Container(ft.Text("Your city: "), padding=ft.padding.only(left=8))
    city = ft.TextButton(content=ft.Text(str(get_city()), color=ft.Colors.BLUE), style=ft.ButtonStyle(overlay_color=ft.Colors.TRANSPARENT), on_click=None)


    title_row_weather = ft.Row(
        [
        ft.Column([city_text, city], alignment=ft.MainAxisAlignment.START),
        ft.Row([theme_button, ft.Text('Weather App')],
               alignment=ft.MainAxisAlignment.CENTER
               )
    ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )


    main_col = ft.Column( # ALL THE WEATHER INFO IS HERE
        [
                        ft.Row([weather_icon, weather_descr], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([act_temp], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                        ft.Row([uv_data], alignment=ft.MainAxisAlignment.CENTER),
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

    # Logged or not check

    if os.path.exists('data.db1'):
        db = sqlite3.connect('data.db1')  # -> opens the connection with the db
        cur = db.cursor()  # -> sets a cursor to move inside the db

        cur.execute("SELECT city_set FROM logged WHERE user_logged = 1")
        city = cur.fetchone()[0]

        cur.execute("""CREATE TABLE IF NOT EXISTS logged (
            id INTEGER PRIMARY KEY,
            user_logged INTEGER,
            city_set TEXT
        )""")

        if city:
            user_data.value = city
            get_weather()


        db.commit()
        db.close()


        page.navigation_bar.destinations[1].disabled = False # enabling the weather tab
        page.navigation_bar.destinations[0].visible = False # hiding the track tab (because the city is already set)
        page.navigation_bar.selected_index = 0 # because of the hidden "Track" tab, selected_index = 0 opens the weather info page
        page.add(weather_page)


    else:

        page.add(
            welcome_page
        )





ft.app(target=main) # run app

#ft.app(target=main, view=ft.AppView.WEB_BROWSER) # -> to run the app in the browser