import flet as ft
from translations import t
from ui_builder import lang


class ErrorBanner:
    def __init__(self, app, ui):

        self.app = app
        self.ui = ui

        self.city_name = '_'

        self.banner = ft.Banner(
            bgcolor=ft.Colors.AMBER_100,
            leading=ft.Icon(icon=ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
            content=ft.Text(
                '',
                color=ft.Colors.BLACK
            ),
            actions=[
                ft.TextButton(
                    content=t('understood', lang), style=ft.ButtonStyle(color=ft.Colors.BLUE),
                    on_click=self.close_banner
                )
            ],
            force_actions_below=True,

        )



    def set_city_name(self, value):
        self.city_name = value if value != '' else None

        self.banner.content.value = t('city_not_found', lang, city_name=self.city_name)


    def trigger_banner(self):

        self.app.page.show_dialog(self.banner)



    def close_banner(self):
        self.app.page.pop_dialog(self.banner)
        self.ui.user_data.value = ''
        self.app.page.update()




class AdviceBanner:
    def __init__(self, app, ui):
        self.app = app
        self.ui = ui

        self.city_name = '_'

        self.advice_text = ft.Text('', size=16, no_wrap=False, expand=True)

        self.banner = ft.Container(
            bgcolor='#f27121',
            padding=ft.Padding(top=20, bottom=10),
            margin=ft.Margin(top=40, left=20, right=20),

            content=ft.Container(ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(icon=ft.Icons.TIPS_AND_UPDATES, color=self.ui.icon_color),
                            self.advice_text
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Container(ft.TextButton(content=t('hide_advices', lang,), style=ft.ButtonStyle(color=ft.Colors.WHITE, text_style=ft.TextStyle(size=16)),
                                               on_click=self.hide_banner), alignment=ft.Alignment.CENTER_RIGHT),


                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
                margin=ft.Margin(left=25, right=25)
            ),
            alignment=ft.Alignment.CENTER,
            border_radius=15,

        )



    def trigger_banner(self):
        # self.app.page.open(self.banner)
        self.app.page.insert(0, self.banner)




    def close_banner(self):
        self.app.page.remove(self.banner, ValueError)



    def hide_banner(self, e=None):
        try:
            self.app.page.remove(self.banner)
        except ValueError:
            pass

        self.app.toggle_advices(e, banner_hide=True)
        self.ui.switches.controls[0].controls[1].value = False

        self.app.page.update()

