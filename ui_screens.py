import flet as ft
from ui_builder import lang
from translations import t

class LoadingScreen:
    def __init__(self, app):
        self.app = app
        self.loading_page = ft.Container(
            content=ft.Column(
                [
                    ft.Text(t('loading', lang)),
                    ft.ProgressRing(color='#f8c4ec')
                ],
                alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            visible=False,
            expand=True,
            alignment=ft.Alignment.CENTER
        )


    def show_loading(self):

        self.app.page.clean()
        self.app.page.add(self.loading_page)
        self.loading_page.visible = True
        self.app.page.navigation_bar.visible = False
        self.app.page.update()


    def hide_loading(self):
        self.loading_page.visible = False
        self.app.page.navigation_bar.visible = True
        self.app.page.update()


class NoConnectionScreen:
    def __init__(self, app, button):
        self.app = app
        self.button = button

        self.noconnection_screen = ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text('No Internet Connection'),
                            self.button
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )

    def show_screen(self):
        self.app.page.clean()
        self.app.page.add(
            self.noconnection_screen
        )
