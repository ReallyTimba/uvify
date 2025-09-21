import flet as ft
import sqlite3
from db_manager import Database
from translations import t


SKIN_TONES = [
    {'name': 'pale', 'color': '#FFDFC4'},
    {'name': 'fair', 'color': '#F0D5BE'},
    {'name': 'medium', 'color': '#E1B899'},
    {'name': 'olive', 'color': '#BD8B5A'},
    {'name': 'brown', 'color': '#8D5524'},
    {'name': 'dark_brown', 'color': '#5A3A1A'},
]



# MED in J/m2
MED = {
    'pale': 200,
    'fair': 250,
    'medium': 300,
    'olive': 450,
    'brown': 600,
    'dark_brown': 1000
}


LANGS = {
    'en': 'English',
    'es': 'Spanish'
}

class SkinSelector:

    def __init__(self):
        from ui import lang
        self.lang = lang

        skin_translations = [
            {'name': t('pale', self.lang), 'color': '#FFDFC4'},
            {'name': t('fair', self.lang), 'color': '#F0D5BE'},
            {'name': t('medium', self.lang), 'color': '#E1B899'},
            {'name': t('olive', self.lang), 'color': '#BD8B5A'},
            {'name': t('brown', self.lang), 'color': '#8D5524'},
            {'name': t('dark_brown', self.lang), 'color': '#5A3A1A'},
        ]
        self.options = [
            ft.dropdown.Option(key=t(skin['name'], lang), leading_icon=ft.Icon(ft.Icons.CIRCLE, color=skin['color']))
            for skin in SKIN_TONES
        ]

        self.color_map = {tone['name']: tone['color'] for tone in SKIN_TONES}


        self.med = 1



    def set_skin(self, dropdown, color_map=None):

        color = ''

        selected = 'pale'

        for skin in SKIN_TONES:
            for k, v in skin.items():
                if dropdown.value == t(v, self.lang):

                    color = color_map.get(v)
                    selected = v

                    self.med = MED[v]

        if color:
            dropdown.leading_icon = ft.Icon(ft.Icons.CIRCLE, color=color)

        db = sqlite3.connect('data.db1')
        cur = db.cursor()

        cur.execute("UPDATE logged SET skin = ? where user_logged = 1",
                    (selected,))

        db.commit()
        db.close()


        return self.med

    def get_skin(self):
        skin_color = Database.get_skin()

        if skin_color is not None:
            return skin_color

        else:
            return 'pale'



    def on_change(self, dropdown, color_map=None):
        self.set_skin(dropdown, self.color_map)



    def dropdown(self, func):

        self.func = func

        skin_selector = ft.Dropdown(
            options=self.options,
            width=200,
            value=t(self.get_skin(), self.lang),
            leading_icon=ft.Icon(ft.Icons.CIRCLE, color=self.color_map[self.get_skin()]),
            on_change=lambda e: on_change(e, dropdown=skin_selector, color_map=self.color_map),
            border_color=ft.Colors.WHITE70,
            fill_color=ft.Colors.BLUE

        )

        def on_change(e, dropdown=None, color_map=None):
            self.set_skin(dropdown, color_map)

            self.func()


        return skin_selector


class LanguageSelector:

    def __init__(self, app):


        self.app = app
        self.options = [
            ft.dropdown.Option(key='English', leading_icon=ft.Image(src='https://flagcdn.com/w80/gb.png', width=24, height=24, border_radius=15, fit=ft.ImageFit.COVER)),
            ft.dropdown.Option(key='Spanish', leading_icon=ft.Image(src='https://flagcdn.com/w80/es.png', width=24, height=24, border_radius=15, fit=ft.ImageFit.COVER))
        ]

    def set_lang(self, dropdown):
        lang = dropdown.value

        lang_to_code = {
            'English': 'en',
            'Spanish': 'es'
        }

        if lang:

            db = sqlite3.connect('data.db1')
            cur = db.cursor()

            cur.execute("UPDATE logged SET lang = ? where user_logged = 1",
                        (lang_to_code[lang],))

            db.commit()
            db.close()


    def get_lang(self):
        language = Database.get_lang()

        if language is not None:
            return LANGS[language]

        return 'English'

    def on_change(self, e, dropdown):
        self.set_lang(dropdown=dropdown)

    def dropdown(self):

        language_selector = ft.Dropdown(
            options=self.options,
            width=200,
            #leading_icon=ft.Image(src='https://flagcdn.com/w80/gb.png', width=24, height=24, border_radius=15, fit=ft.ImageFit.COVER) if Database.get_lang() == 'en' else ft.Image(src='https://flagcdn.com/w80/es.png', width=24, height=24, border_radius=15, fit=ft.ImageFit.COVER),
            value=self.get_lang(),
            on_change=lambda e: on_change(e, dropdown=language_selector),
            border_color=ft.Colors.WHITE70,
            fill_color=ft.Colors.BLUE

        )

        def on_change(e, dropdown=None):
            from ui import lang
            self.set_lang(dropdown)

            self.app.page.open(
                    ft.AlertDialog(
                        title=ft.Text(t('change_lang', lang)),
                        content=ft.Text(t('restart_app', lang)),
                        actions=[ft.TextButton(text="Okey", on_click=lambda e: self.app.page.close(e.control.parent))],
                        bgcolor=self.app.page.bgcolor,

                    )

            )




        return language_selector
