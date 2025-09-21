import flet as ft
from translations import t
from ui import lang


class ErrorBanner:
    def __init__(self, app, ui):

        self.app = app
        self.ui = ui

        self.city_name = '_'

        self.banner = ft.Banner(
            bgcolor=ft.Colors.AMBER_100,
            leading=ft.Icon(name=ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
            content=ft.Text(
                '',
                color=ft.Colors.BLACK
            ),
            actions=[
                ft.TextButton(
                    text=t('understood', lang), style=ft.ButtonStyle(color=ft.Colors.BLUE),
                    on_click=self.close_banner
                )
            ],
            force_actions_below=True,

        )



    def set_city_name(self, value):
        self.city_name = value if value != '' else None

        self.banner.content.value = t('city_not_found', lang, city_name=self.city_name)


    def trigger_banner(self):

        self.app.page.open(self.banner)



    def close_banner(self, e=None):
        self.app.page.close(self.banner)
        self.ui.user_data.value = ''
        self.app.page.update()




class AdviceBanner:
    def __init__(self, app, ui):
        self.app = app
        self.ui = ui

        self.city_name = '_'

        self.advice_text = ft.Text('', width=400)

        # self.banner = ft.Banner(
        #     bgcolor='#f27121',
        #     leading=ft.Icon(name=ft.Icons.TIPS_AND_UPDATES, color='#f8c4ec'),
        #     content=self.advice_text,
        #     actions=[
        #         ft.TextButton(
        #             text=t('hide_advices', lang), style=ft.ButtonStyle(color=ft.Colors.WHITE),
        #             on_click=self.hide_banner
        #         )
        #     ],
        #     force_actions_below=True,
        #
        # )
        self.banner = ft.Container(
            bgcolor='#f27121',
            padding=ft.padding.only(top=20, bottom=10),
            content=ft.Column(
                [
                    ft.Row(
                    [
                    ft.Icon(name=ft.Icons.TIPS_AND_UPDATES, color=self.ui.icon_color),
                    self.advice_text
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Container(ft.TextButton(text=t('hide_advices', lang), style=ft.ButtonStyle(color=ft.Colors.WHITE),
                on_click=self.hide_banner), alignment=ft.alignment.center_right, margin=ft.margin.only(right=20))

                ],
                alignment=ft.MainAxisAlignment.CENTER
                ),
            alignment=ft.alignment.center,
            border_radius=15
        )



    def trigger_banner(self):
        # self.app.page.open(self.banner)
        self.app.page.insert(0, self.banner)



    def close_banner(self, e=None):
        # self.app.page.close(self.banner)
        self.app.page.remove(self.banner, ValueError)



    def hide_banner(self, e=None):
        # self.app.page.close(self.banner)
        #
        # self.app.toggle_advices(e, manual=True)
        # self.ui.switches.controls[0].controls[1].value = False
        #
        # self.app.page.update()
        try:
            self.app.page.remove(self.banner)
        except ValueError:
            pass

        self.app.toggle_advices(e, manual=True)
        self.ui.switches.controls[0].controls[1].value = False

        self.app.page.update()

