from db_manager import Database
import flet as ft
import skin_selector as ss

class UIBuilder:
    def __init__(self, app):
        self.app = app

        self._build_widgets()
        self._build_pages()
        self._setup_navigation()



    def _build_widgets(self):

        self.user_data = ft.TextField(label='Search your city', width=400, on_submit=lambda e: self.app.get_weather(e))
        self.theme_button = ft.IconButton(ft.Icons.DARK_MODE, on_click=lambda e: self.app.change_theme(e))

        # UVI

        self.uv_data = ft.Text('')
        self.uv_progress = ft.ProgressBar(width=400, visible=False)
        self.uv_spf = ft.Text('')

        # General

        self.weather_descr = ft.Text('')
        self.weather_icon = ft.Image(src="", width=50, height=50,
                                visible=False)
        self.act_temp = ft.Text('')

        # Wind

        self.wind_vel = ft.Text('')

        # AQI
        black = ft.Colors.BLACK

        self.aqi_co = ft.Text('', color=black)
        self.aqi_no2 = ft.Text('', color=black)
        self.aqi_so2 = ft.Text('', color=black)

        # SUN

        self.sunrise = ft.Text('')
        self.sunset = ft.Text('')

        # Buttons

        self.set_button = ft.Row([ft.ElevatedButton(text='Set', on_click=lambda e: self.app.set_city(e))],
                            alignment=ft.MainAxisAlignment.CENTER)

        self.city_text = ft.Container(ft.Text("Your city: "), padding=ft.padding.only(left=8))
        self.user_city = ft.TextButton(content=ft.Text(str(Database.get_city()), color=ft.Colors.BLUE),
                                  style=ft.ButtonStyle(overlay_color=ft.Colors.TRANSPARENT),
                                  on_click=lambda e: self.app.reset_city(e))

        self.wind_info = ft.Container(
            content=ft.Column([ft.Text('Wind Speed'), self.wind_vel], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLUE, border_radius=10, padding=ft.padding.symmetric(horizontal=100, vertical=30))

        self.sun_info = ft.Container(
            content=ft.Column([ft.Text('Sun Time'), self.sunrise, self.sunset], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLUE, border_radius=10, padding=30)

        self.air_info = ft.Container(ft.Column([ft.Text('Air Quality', color=ft.Colors.BLACK), self.aqi_co, self.aqi_no2, self.aqi_so2],
                                          alignment=ft.MainAxisAlignment.CENTER), bgcolor=ft.Colors.WHITE,
                                border_radius=10, padding=30)


        self.uv_fore = ft.ExpansionPanelList(
            expand_icon_color=ft.Colors.WHITE,
            elevation=8,
            divider_color=ft.Colors.WHITE,
            on_change=None,
            width=500,

            controls=[
                ft.ExpansionPanel(
                    bgcolor=ft.Colors.BLUE,
                    expanded=False,
                    header=ft.ListTile(title=ft.Text('Monday')),
                    expand=True,

                    content=ft.ListTile(
                        title=ft.Row([], alignment=ft.MainAxisAlignment.CENTER),
                        subtitle=ft.Row([], scroll=ft.ScrollMode.ADAPTIVE, width=250, height=150, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START),
                        bgcolor=ft.Colors.BLUE,


                    )
            ),

            ]
        )





        self.title_row_weather = ft.Row(
            [
                ft.Column([self.city_text, self.user_city], alignment=ft.MainAxisAlignment.START),
                ft.Row([self.theme_button, ft.Text('Theme')],
                       alignment=ft.MainAxisAlignment.CENTER
                       )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )



        self.main_col = ft.Column(  # ALL THE WEATHER INFO IS HERE
            [
                ft.Row([self.weather_icon, self.weather_descr], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.act_temp], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                ft.Row([self.uv_data, self.uv_spf], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(self.uv_fore, alignment=ft.alignment.center),
                ft.Row([self.uv_progress], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.wind_info], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text(''),  # change this space
                ft.Row([self.air_info], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text(''),
                ft.Row(
                    [
                        self.sun_info
                    ],
                    alignment=ft.MainAxisAlignment.CENTER),

            ],  # column alignment

            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )  # column alignment



    def _build_pages(self):

        self.welcome_page = ft.Column(  # general block
            [
                ft.Row(  # Row 1 -> Header content
                    [
                        ft.Text("Welcome to UVify!", text_align=ft.alignment.center, size=25)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER  # Row 1 -> settings
                ),
                ft.Column(
                    [
                        ft.Container(content=ft.FilledButton("Start following your city", width=300, height=38,
                                                             style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
                                                             on_click=self.app.get_context), alignment=ft.alignment.center),
                        ft.Container(content=ft.TextButton("Are you from Torredembarra?", on_click=None),
                                     alignment=ft.alignment.center)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True
                )
            ],
            expand=True  # -> general block (Column settings)

        )

        self.welcome_updated_col = ft.Column(
            [
                ft.Row([self.user_data], alignment=ft.MainAxisAlignment.CENTER),
                self.set_button

            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )


        self.weather_page = ft.Column([
            self.title_row_weather,
            self.main_col
        ],
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE
        )

        self.settings_page = ft.Column(
            [
                ft.Row([ft.Text("Settings")], alignment=ft.MainAxisAlignment.CENTER),
                ft.Column(
                    [
                        ft.Text('Your skin color'),
                        ss.dropdown(self.app.get_weather)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )



    def _setup_navigation(self):

        self.app.page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.ADD_LOCATION_OUTLINED, label="Track",
                                            selected_icon=ft.Icons.ADD_LOCATION_SHARP),
                ft.NavigationBarDestination(icon=ft.Icons.WB_SUNNY_OUTLINED, label="Weather",
                                            selected_icon=ft.Icons.SUNNY, disabled=True),  # is not able on first login
                ft.NavigationBarDestination(icon=ft.Icons.SETTINGS_OUTLINED, label="Settings",
                                            selected_icon=ft.Icons.SETTINGS_SHARP),

            ], on_change=lambda e: self.app.navigate(e)
        )