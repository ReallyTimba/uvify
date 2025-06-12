import flet as ft
import requests


def main(page: ft.Page):
    page.title = 'Weather Helper' # window title
    page.theme_mode = 'dark' # lets change the app theme
    page.vertical_alignment = ft.MainAxisAlignment.CENTER # sets vertical alignment of all the elements in the center of the window
    page.window.width = 540
    page.window.height = 960


    # WIDGETS

    user_data = ft.TextField(label='Enter the city', width=400, on_submit=lambda e: get_weather(e))
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


    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        theme_button.icon = ft.Icons.LIGHT_MODE if page.theme_mode == 'light' else ft.Icons.DARK_MODE
        page.update()

    def navigate(e):
        i = page.navigation_bar.selected_index
        page.clean()

        if i == 0:
            page.add(welcome_page)
        elif i == 1:
            page.add(weather_page)
        elif i == 2:
            page.add(settings_page)


        page.update()


    def get_context(e):
        pass

    # NAVIGATION BAR

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.WB_SUNNY_OUTLINED, label="Weather",
                                        selected_icon=ft.Icons.SUNNY),
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS_OUTLINED, label="Settings",
                                        selected_icon=ft.Icons.SETTINGS_SHARP),

        ], on_change=lambda e: navigate(e)
    )



    # PAGE WIDGETS

    title_row = ft.Row([theme_button, ft.Text('Weather App')],
                       alignment=ft.MainAxisAlignment.CENTER
                       )

    main_col = ft.Column(
        [
                        ft.Row([user_data], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([weather_data, uv_icon], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([uv_progress], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([ft.ElevatedButton(text='Get', on_click=lambda e: get_weather(e))],
                               alignment=ft.MainAxisAlignment.CENTER)], # column alignment

                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True
    ) # column alignment




    # PAGES


    welcome_page = page.add(

    )

    weather_page = ft.Column([
        title_row,
        main_col
        ],
        expand=True
    )

    settings_page = ft.Row(
        [ft.Text("Settings")],
        alignment=ft.MainAxisAlignment.CENTER
    )

    page.add(
        weather_page
    )





ft.app(target=main) # run app

#ft.app(target=main, view=ft.AppView.WEB_BROWSER) # -> to run the app in the browser