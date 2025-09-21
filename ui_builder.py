from math import pi
from db_manager import Database
import flet as ft
from ui_dropdowns import SkinSelector, LanguageSelector
from ui_torremap import Torremap
from translations import t, translate_city
from asyncio import run

APP_VERSION = "1.3.0"
lang = Database.get_lang()


class UIBuilder:
    def __init__(self, app):
        self.app = app

        from ui_screens import NoConnectionScreen
        self.retry_button = ft.IconButton(ft.Icons.REFRESH, icon_size=35, on_click=lambda e: self.app.get_weather())
        self.noconnection = NoConnectionScreen(self.app, self.retry_button)

        self._build_widgets()
        self._build_pages()
        self._setup_navigation()



    def _build_widgets(self):

        # self.widget_color = ft.LinearGradient(
        # begin=ft.alignment.top_left,
        # end=ft.alignment.bottom_right,
        # colors=["#8e2de2", "#f27121"],
        # )

        self.widget_color = ft.LinearGradient(
        begin=ft.alignment.top_left,
        end=ft.alignment.bottom_right,
        colors=["#6f1a86", "#f27121"],
        )

        # self.bg_color = ft.LinearGradient(
        #     begin=ft.alignment.top_left,
        #     end=ft.alignment.bottom_right,
        #     colors=["#543056", "#c65449"],
        #     stops=[0, 1]
        #
        # )

        # self.widget_color = ft.LinearGradient(
        #     begin=ft.alignment.top_left,
        #     end=ft.alignment.bottom_right,
        #     colors=["#1a4f0e", "#f27121"]
        # )

        self.icon_color = '#f8c4ec'


        self.user_data = ft.TextField(label=t('search_city', lang), width=400, color=ft.Colors.BLUE, border_color=ft.Colors.WHITE, label_style=ft.TextStyle(color=ft.Colors.WHITE))
        self.eg = ft.Text(t('search_example', lang), color=ft.Colors.GREY_200, size=13, text_align=ft.alignment.center, visible=False)




        # UVI


        self.uv_spf = ft.Text('', size=15)
        self.uv_descr = ft.Text(t('uv', lang), size=20, weight=ft.FontWeight.W_700)
        self.uv_level = ft.Text('', size=20, weight=ft.FontWeight.W_700)
        self.vitamin_d = ft.Container(
            ft.Row(
                [
                    ft.Image(src='assets/icons/d1.png', width=50, height=50),
                    ft.Column(
                        [
                            ft.Text(t('vitamin_d', lang), size=16),
                            ft.Text('', size=20, weight=ft.FontWeight.W_600)
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.START
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,

        ),

            alignment=ft.alignment.center, gradient=self.widget_color, border_radius=15, expand=True,
            padding=ft.padding.only(top=36, bottom=36, left=-30)
        )


        self.burn_time = ft.Text('', size=20, weight=ft.FontWeight.W_600)
        self.burntime_widget = ft.Container(
            ft.Row(
                [
                    ft.Image(src='assets/icons/burn.png', width=50, height=50),
                    ft.Column(
                        [
                            ft.Text(t('time_till_burn', lang), width=150, text_align=ft.TextAlign.START, size=16),
                            self.burn_time
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.START
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            border_radius=15, expand=True, gradient=self.widget_color, padding=ft.padding.only(top=25, bottom=25)
        )



        # General

        self.weather_descr = ft.Text('', size=16, text_align=ft.alignment.top_left)
        self.weather_icon = ft.Image(src="", width=55,
                                visible=False, fit=ft.ImageFit.FIT_WIDTH)
        self.act_temp = ft.Text('', size=20, weight=ft.FontWeight.W_700)

        self.general_data = ft.Container(
                    ft.Row(
                        [
                        self.weather_icon,
                        ft.Column(
                            [
                            self.act_temp,
                            ft.Container(self.weather_descr, padding=ft.padding.only(top=-10))
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.START,

                        )
                    ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    gradient=self.widget_color,
                    border_radius=15,
                    expand=True,
                    alignment=ft.alignment.center,
                    # padding=ft.padding.only(top=35, bottom=30, left=-13)
                    padding=ft.padding.only(top=18, bottom=18, left=-25)
                )

        self.localtime = ft.Text('', size=20, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.CENTER)

        self.time_widget = ft.Container(
                    ft.Column(
                        [
                            ft.Text(t('current_time', lang), size=16, text_align=ft.TextAlign.CENTER),
                            ft.Container(self.localtime, padding=ft.padding.only(top=-8))
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                gradient=self.widget_color,

                border_radius=15,
                alignment=ft.alignment.center,
                # padding=ft.padding.only(top=33, bottom=29),
                    padding=ft.padding.only(top=20, bottom=20),
                width=150
                )

        self.water_temp = ft.Text('', size=22, weight=ft.FontWeight.BOLD)

        # Wind

        self.wind_vel = ft.Text('', size=20, weight=ft.FontWeight.BOLD)

        # AQI


        self.progress_colors = {
            0: ft.Colors.GREEN,
            0.333: ft.Colors.YELLOW,
            0.666: ft.Colors.RED
        }
        self.progress_levels = {
            ft.Colors.GREEN: t('air_good', lang),
            ft.Colors.YELLOW: t('air_moderate', lang),
            ft.Colors.RED: t('air_critical', lang)
        }

        self.progress_co = ft.ProgressBar(value=0, width=90, height=35, rotate=-pi/2)
        self.progress_no2 = ft.ProgressBar(value=0, width=90, height=35, rotate=-pi/2)
        self.progress_so2 = ft.ProgressBar(value=0, width=90, height=35, rotate=-pi/2)

        self.co_level = ft.Text('', size=14)
        self.no2_level = ft.Text('', size=14)
        self.so2_level = ft.Text('', size=14)

        self.air_progress = ft.Container(
            ft.Row(
                [
                    ft.Column([ft.Container(ft.Text('CO', size=19, weight=ft.FontWeight.W_500), padding=ft.padding.only(bottom=25)), self.progress_co, ft.Container(self.co_level, padding=ft.padding.only(top=30))],
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Column([ft.Container(ft.Text('NO2', size=19, weight=ft.FontWeight.W_500), padding=ft.padding.only(bottom=25)), self.progress_no2, ft.Container(self.no2_level, padding=ft.padding.only(top=30))],
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Column([ft.Container(ft.Text('SO2', size=19, weight=ft.FontWeight.W_500), padding=ft.padding.only(bottom=25)), self.progress_so2, ft.Container(self.so2_level, padding=ft.padding.only(top=30))],
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.START,



            ),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.TRANSPARENT, border_radius=15,
            padding=ft.padding.only(top=20, bottom=0), expand=True,
            margin=ft.margin.only(left=35, right=35)

        )

        # SUN

        self.sunrise = ft.Text(t('sunrise', lang), size=15)
        self.sunset = ft.Text(t('sunset', lang), size=15)

        self.sunrise_time = ft.Text('', size=15)
        self.sunset_time = ft.Text('', size=15)

        # Buttons

        self.set_button = ft.Container(content=ft.ElevatedButton(text=t('set_button', lang), on_click=lambda e: self.app.set_city(e)),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=20)
                            )

        city_from_db = Database.get_city()
        displayed_city = city_from_db
        try:
            displayed_city = run(translate_city(city_from_db, src='en', dest='es')).text if lang == 'es' else city_from_db
        except:
            self.noconnection.show_screen()


        self.city_text = ft.Container(ft.Text(t('your_city', lang), size=16), padding=ft.padding.only(left=8))
        self.user_city = ft.TextButton(content=ft.Text(str(displayed_city), color='#f27121', size=16),
                                  style=ft.ButtonStyle(overlay_color=ft.Colors.TRANSPARENT),
                                  on_click=lambda e: self.app.reset_city(e))

        self.wind_info = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(name=ft.Icons.AIR, size=35, color=ft.Colors.WHITE),
                            ft.Text(t('wind', lang), size=16)
                        ], alignment=ft.MainAxisAlignment.CENTER),
                    self.wind_vel
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            gradient=self.widget_color, border_radius=15,
            padding=ft.padding.only(top=40, bottom=40), expand=True)

        # self.wind_info = ft.Container(
        #     ft.Row(
        #         [
        #             ft.Container(ft.Icon(name=ft.Icons.AIR, size=35, color=ft.Colors.WHITE), padding=ft.padding.only(bottom=70)),
        #             ft.Column(
        #                 [
        #                     ft.Text(t('wind', lang), size=16),
        #                     self.wind_vel
        #                 ],
        #                 alignment=ft.MainAxisAlignment.START
        #             )
        #         ],
        #         alignment=ft.MainAxisAlignment.CENTER
        #     ),
        #
        #     gradient=self.widget_color, border_radius=15,
        #     padding=ft.padding.only(top=40, bottom=40), expand=True
        # )

        # self.sun_info = ft.Container(ft.Column([ft.Row([ft.Icon(name=ft.Icons.WB_TWIGHLIGHT, size=35, color=ft.Colors.YELLOW_800), ft.Text(t('sun', lang), size=14, weight=ft.FontWeight.W_600, opacity=0.8)], alignment=ft.MainAxisAlignment.CENTER), ft.Row([self.sunrise, self.sunrise_time], alignment=ft.MainAxisAlignment.CENTER), ft.Row([self.sunset, self.sunset_time], alignment=ft.MainAxisAlignment.CENTER)], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), gradient=self.widget_color, border_radius=15, padding=ft.padding.only(top=25, bottom=25), expand=True)
        self.sun_info = ft.Container(
        ft.Column(
            [
                ft.Row(
            [
                ft.Icon(name=ft.Icons.WB_TWIGHLIGHT, size=35, color='#f9d623'),
                ft.Text(t('sun', lang), size=16)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
                ft.Row(
                    [
                       ft.Column([self.sunrise, self.sunset]),
                       ft.Column([self.sunrise_time, self.sunset_time])
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
                ],
                                               alignment=ft.MainAxisAlignment.CENTER,
                                               horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                     gradient=self.widget_color, border_radius=15,
                                     padding=ft.padding.only(top=43, bottom=43), expand=True)
        self.air_info = ft.Container(ft.Column([ft.Row([ft.Container(ft.Text(t('aqi', lang), size=25, weight=ft.FontWeight.W_600)), ft.Icon(name=ft.Icons.GRAIN, size=35, color=self.icon_color)], alignment=ft.MainAxisAlignment.CENTER), ft.Row([self.air_progress], alignment=ft.MainAxisAlignment.CENTER, expand=True)],
                                          alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), gradient=self.widget_color,
                                border_radius=15, padding=30, expand=True)

        self.water_info = ft.Container(
            ft.Column([ft.Row([ft.Icon(name=ft.Icons.WATER_DROP, size=30, color='#00bfff'), ft.Text(t('water', lang), size=16)], alignment=ft.MainAxisAlignment.CENTER), ft.Row([self.water_temp], alignment=ft.MainAxisAlignment.CENTER, expand=True)],
                                          alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            gradient=self.widget_color, border_radius=15, width=400, padding=ft.padding.only(top=34, bottom=34), expand=True, visible=False
        )

        self.uv_colors = {
            0: ft.Colors.GREEN,
            3: ft.Colors.YELLOW_ACCENT_700,
            6: ft.Colors.RED
        }

        self.uv_fore = ft.ExpansionPanelList(
            expand_icon_color=ft.Colors.WHITE,
            divider_color=ft.Colors.WHITE,
            on_change=None,
            expand=True,
            expanded_header_padding=0,
            controls=[
                ft.ExpansionPanel(

                    expanded=False,
                    header=ft.Container(ft.ListTile(title=ft.Text('Monday', size=16)), gradient=self.widget_color),
                    expand=True,

                    content=ft.Container(ft.ListTile(

                        title=ft.Row([], alignment=ft.MainAxisAlignment.CENTER),
                        subtitle=ft.Row([], scroll=ft.ScrollMode.ADAPTIVE, height=250, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START),


                    ),
                        gradient=self.widget_color,



                ),
                    bgcolor='#f27121',




            ),
            ft.ExpansionPanel(

                expanded=False,
                header=ft.Container(ft.ListTile(title=ft.Text('Tuesday', size=16)), gradient=self.widget_color),
                expand=True,

                content=ft.Container(ft.ListTile(
                    title=ft.Row([], alignment=ft.MainAxisAlignment.CENTER),
                    subtitle=ft.Row([], scroll=ft.ScrollMode.ADAPTIVE, height=250, alignment=ft.MainAxisAlignment.START,
                                    vertical_alignment=ft.CrossAxisAlignment.START),

                ),
                    gradient=self.widget_color,

                ),
                bgcolor='#f27121'
            ),
            ft.ExpansionPanel(

                expanded=False,
                header=ft.Container(ft.ListTile(title=ft.Text('Wednesday', size=16)), gradient=self.widget_color),
                expand=True,

                content=ft.Container(ft.ListTile(
                    title=ft.Row([], alignment=ft.MainAxisAlignment.CENTER),
                    subtitle=ft.Row([], scroll=ft.ScrollMode.ADAPTIVE, height=250, alignment=ft.MainAxisAlignment.START,
                                    vertical_alignment=ft.CrossAxisAlignment.START),

                ),
                    gradient=self.widget_color,


                ),
                bgcolor='#f27121'
            )


                    ]
        )

        # TORREDEMBARRA MAP


        tmap = Torremap()


        self.map_button = ft.Container(
            content=ft.TextButton(content=ft.Text(t('open_map', lang), size=18, text_align=ft.TextAlign.CENTER, opacity=0.8, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500), on_click=self.app.open_map),

            alignment=ft.alignment.center,

        )

        self.return_button = ft.Container(
            content=ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_size=40, icon_color='#f27121',
                                  on_click=lambda e: self.app.return_to_main(e)),
            bgcolor=ft.Colors.WHITE,

            border_radius=15,
            alignment=ft.alignment.center_left,
            width=55
        )


        self.map_access = ft.Container(
            # ft.Column(
            # [
            #     ft.IconButton(icon=ft.Icons.MAP, style=ft.ButtonStyle(color=self.icon_color, icon_size=32), on_click=lambda e: self.app.open_map(e)),
            #     self.map_button
            # ],
            ft.Row([
               # ft.IconButton(icon=ft.Icons.SEARCH, icon_size=30, icon_color=ft.Colors.WHITE),
                ft.Icon(ft.Icons.SEARCH, size=30, color=ft.Colors.WHITE),
                self.map_button
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
            ),

            alignment=ft.alignment.center, #gradient=self.widget_color,
            border_radius=15, padding=ft.padding.only(top=20, bottom=20), expand=True,
            bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.PURPLE),

        )

        self.torremap = ft.Column(
            [
                ft.Container(None, expand=True),

                self.return_button,

            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )




        self.title_row_weather = ft.Row(
            [
                ft.Column([self.city_text, self.user_city], alignment=ft.MainAxisAlignment.START),
                # ft.Row([self.theme_button, ft.Text('Theme')],
                #        alignment=ft.MainAxisAlignment.CENTER
                #        )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN

        )


        # Mesure System Switcher

        state = True if Database.get_units() == 'metric' else False



        advices_enabled = bool(Database.user_advices())

        self.switches = ft.Column([
        # Advices
        ft.Row(
            [
                ft.Text(t('advices', lang), size=14, color=ft.Colors.WHITE),
                ft.CupertinoSwitch(
                    value=advices_enabled,
                    active_color=ft.Colors.BLUE,
                    on_change=lambda e: self.app.toggle_advices(e)
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            width=250
        ),

        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        # Units
        ft.Row(
            [
                ft.Text('', size=16, color=ft.Colors.WHITE),
                ft.CupertinoSwitch(
                    value=state,
                    inactive_track_color=ft.Colors.RED,
                    active_color=ft.Colors.BLUE,
                    on_change=lambda e: self.app.change_system(e)
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            width=250
        ),
    ])



        self.main_col = ft.Column(  # ALL THE WEATHER INFO IS HERE
            [
        ft.Row([self.time_widget, self.general_data], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(ft.Column([ft.Container(ft.Row([self.uv_descr, self.uv_level], alignment=ft.MainAxisAlignment.CENTER), padding=ft.padding.only(bottom=15)), ft.Container(ft.Stack([ft.Container(), ft.Icon()])), ft.Row([self.uv_spf], alignment=ft.MainAxisAlignment.CENTER)], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.alignment.center, border_radius=15, padding=ft.padding.only(top=20, bottom=20), gradient=self.widget_color),
        ft.Row([self.vitamin_d, self.burntime_widget], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([self.map_access], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(self.uv_fore, border_radius=15, alignment=ft.alignment.center, bgcolor=ft.Colors.TRANSPARENT),
        ft.Row([self.water_info], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([self.wind_info, self.sun_info], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([self.air_info], alignment=ft.MainAxisAlignment.CENTER),


            ],  # column alignment

            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True
        )  # column alignment





    def _build_pages(self):

        self.welcome_page = ft.Container(
            expand=True,
            content=ft.Column(
                [
                    ft.Container(ft.Text(
                        t('welcome', lang),
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER
                    ),
                        padding=ft.padding.only(top=30)
                    ),
                    ft.Container(
                        content=ft.Icon(
                            name=ft.Icons.SUNNY,
                            color='#f27121',
                            size=160

                        ),
                        padding=ft.padding.only(top=30, bottom=20),
                        alignment=ft.alignment.center
                    ),

                    ft.Divider(height=150, color=ft.Colors.TRANSPARENT),

                    ft.Column(
                        [
                            ft.ElevatedButton(
                            content=ft.Row([ft.Icon(ft.Icons.LANGUAGE), ft.Text(t('start_following', lang), text_align=ft.TextAlign.CENTER)], alignment=ft.MainAxisAlignment.CENTER),
                            width=290,
                            height=48,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=15),

                                color=ft.Colors.WHITE,
                                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_600),
                            ),
                            on_click=self.app.get_started
                        ),
                        ft.Container(content=self.eg, alignment=ft.alignment.center),

                        ft.TextButton(
                            t('from_torre', lang),
                            on_click=lambda e: self.app.torredembarra(e),
                            style=ft.ButtonStyle(
                                color=ft.Colors.WHITE,
                                overlay_color=ft.Colors.TRANSPARENT,
                                padding=ft.padding.symmetric(vertical=5)
                            )
                        )

                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        self.welcome_updated = ft.Column(
            [
                ft.Row([self.user_data], alignment=ft.MainAxisAlignment.CENTER),
                self.set_button,

            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )


        self.weather_page = ft.Stack(
            [


            # ft.Image(
            # src="assets/icons/wallpaper1.jpg",
            # fit=ft.ImageFit.COVER,
            # opacity=0.15,
            # filter_quality=ft.FilterQuality.HIGH,
            # expand=True
            # ),

        ft.Container(
            ft.Column([
                ft.Container(self.title_row_weather, padding=ft.padding.only(bottom=25, top=20)),
                self.main_col
            ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                expand=True,
                scroll=ft.ScrollMode.AUTO
            ), padding=20,

        )
        ],
            expand=True,
            fit=ft.StackFit.EXPAND,


        )

        ss = SkinSelector()
        ls = LanguageSelector(self.app)


        self.settings_page = ft.Container(
            content=ft.Column(
                [
                    ft.Text(t('settings', lang), size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.WHITE),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                    ft.Container(
                        content=ft.Column([
                            ft.Text(t('language', lang), size=16, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                            ls.dropdown()
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=10,
                        width=300,
                        alignment=ft.alignment.center
                    ),

                    ft.Container(
                        content=ft.Column([
                            ft.Text(t('skin', lang), size=16, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                            ss.dropdown(lambda: self.app.get_weather(trigger_snack=True, return_settings_page=True))
                        ],
                        alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=10,
                        width=300
                    ),

                    ft.Divider(height=20, color=ft.Colors.WHITE),

                    ft.Container(
                        content=self.switches,
                        padding=10,
                        width=300
                    ),

                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Text(f'version: {APP_VERSION}', size=12, color=ft.Colors.WHITE60),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
            ),
            margin=20,
            border_radius=20,
            padding=20,
            gradient=self.widget_color,

        )

    def _setup_navigation(self):

        self.app.page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.ADD_LOCATION_OUTLINED, label=t('track_nav', lang),
                                            selected_icon=ft.Icons.ADD_LOCATION_SHARP),
                ft.NavigationBarDestination(icon=ft.Icons.WB_SUNNY_OUTLINED, label=t('weather_nav', lang),
                                            selected_icon=ft.Icons.SUNNY, disabled=True),  # is not able on first login
                ft.NavigationBarDestination(icon=ft.Icons.SETTINGS_OUTLINED, label=t('settings', lang),
                                            selected_icon=ft.Icons.SETTINGS_SHARP),

            ], on_change=lambda e: self.app.navigate(e), bgcolor=self.app.page.bgcolor
        )