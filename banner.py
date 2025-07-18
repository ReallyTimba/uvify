import flet as ft

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
                    text='Understood', style=ft.ButtonStyle(color=ft.Colors.BLUE),
                    on_click=self.close_banner
                )
            ],
            force_actions_below=True
        )



    def set_city_name(self, value):
        self.city_name = value if value != '' else None

        self.banner.content.value = f"No city with name '{self.city_name}' was found.\nTry to enter the full city name and the country"


    def trigger_banner(self):
        self.app.page.open(self.banner)



    def close_banner(self, e=None):
        self.app.page.close(self.banner)
        self.ui.user_data.value = ''
        self.app.page.update()





