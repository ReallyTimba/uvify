import flet as ft

class LoadingScreen:
    def __init__(self, app):
        self.app = app
        self.loading_page = ft.Container(
            content=ft.Column(
                [
                    ft.Text('Loading...'),
                    ft.ProgressRing()
                ],
                alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            visible=False,
            expand=True,
            alignment=ft.alignment.center
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