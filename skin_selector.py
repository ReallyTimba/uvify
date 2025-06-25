import flet as ft
import sqlite3



SKIN_TONES = [
    {'name': 'Pale', 'color': '#FFDFC4'},
    {'name': 'Fair', 'color': '#F0D5BE'},
    {'name': 'Medium', 'color': '#E1B899'},
    {'name': 'Olive', 'color': '#BD8B5A'},
    {'name': 'Brown', 'color': '#8D5524'},
    {'name': 'Dark brown', 'color': '#5A3A1A'},
]

MED = {
    'Pale': 20,
    'Fair': 25,
    'Medium': 33,
    'Olive': 43,
    'Brown': 60,
    'Dark brown': 80
}


options = [
    ft.dropdown.Option(key=skin['name'], leading_icon=ft.Icon(ft.Icons.CIRCLE, color=skin['color']))
    for skin in SKIN_TONES
]

color_map = {tone['name']: tone['color'] for tone in SKIN_TONES}

med = 1

def set_skin(e=None, dropdown=None, page=None, color_map=None):
    page = e.page
    _color = color_map.get(dropdown.value)

    global med
    med = MED[dropdown.value]



    if _color:
        dropdown.leading_icon = ft.Icon(ft.Icons.CIRCLE, color=_color)

    db = sqlite3.connect('data.db1')
    cur = db.cursor()

    cur.execute("UPDATE logged SET skin = ? where user_logged = 1",
                (dropdown.value,))


    db.commit()
    db.close()


    page.update()

    print(med)
    return med

def get_skin():
    db = sqlite3.connect('data.db1')  # -> opens the connection with the db
    cur = db.cursor()  # -> sets a cursor to move inside the db

    cur.execute("SELECT skin FROM logged WHERE user_logged = 1")
    skin_color = cur.fetchone()[0]

    if skin_color is not None:
        return skin_color

    else:
        return 'Pale'

dd = ft.Dropdown(
    options=options,
    width=200,
    value=get_skin(),
    leading_icon=ft.Icon(ft.Icons.CIRCLE, color=color_map[get_skin()]),
    on_change=lambda e: set_skin(e, dropdown=dd, color_map=color_map),

)
