import flet as ft
import flet_map as fm
import requests
from caching import *
import flet_geolocator as gl

class Torremap:
    def __init__(self, app=None):
        self.app = app
        self.geo = gl.Geolocator(
            on_position_change=self.on_position_change,
            on_error=self.on_error
        )

        self.app.page.overlay.append(self.geo)

        self.build_map()

    def on_position_change(self, e=None):
        if e.data:
            lat = e.data['latitude']
            lon = e.data['longitude']
            print('GeoLocation: ', lat, lon)

            user_marker = fm.Marker(
                coordinates=fm.MapLatitudeLongitude(lat, lon),
                content=ft.Icon(name=ft.Icons.MY_LOCATION, color=ft.Colors.BLUE, size=36)
                )

            self.marker_layer.markers.append(user_marker)



    def on_error(self, e=None):
        self.app.page.open(ft.Banner(content=ft.Text('Error'), actions=[]))

    def locate_me(self):
        if self.geo not in self.app.page.overlay:
            self.app.page.overlay.append(self.geo)
            self.app.page.update()
        self.geo.get_current_position()


    def search_places(self):
        self.timeouted = False

        cached = get_cached_places()
        if cached:
            return cached

        try:
            overpass_url = "http://overpass-api.de/api/interpreter"
            query = """
            [out:json];
            (
              node["amenity"="pharmacy"](41.1347,1.3929,41.1563,1.4177);
              node["shop"="supermarket"](41.1347,1.3929,41.1563,1.4177);
            );
            out;
            """
            resp = requests.get(overpass_url, params={'data': query}, timeout=5)
            places = []
            if resp.ok:
                for el in resp.json()["elements"]:
                    tags = el.get("tags", {})
                    if tags.get("amenity") == "pharmacy":
                        kind = "pharmacy"
                        icon = ft.Icons.LOCAL_PHARMACY
                        color = ft.Colors.GREEN
                        name = tags.get("name", "Pharmacy")
                    elif tags.get("shop") == "supermarket":
                        kind = "supermarket"
                        icon = ft.Icons.SHOPPING_CART
                        color = ft.Colors.RED
                        name = tags.get("name", "Supermarket")
                    else:
                        continue

                    address = tags.get("addr:full") or f"{tags.get('addr:street','')} {tags.get('addr:housenumber','')}".strip()
                    tooltip = name
                    if address:
                        tooltip += "\n" + address
                    places.append({
                        "lat": el["lat"],
                        "lon": el["lon"],
                        "tooltip": tooltip,
                        "icon": icon,
                        "color": color,
                        "kind": kind,
                    })
                if places:
                    save_cached_places(places)
            return places
        except requests.exceptions.ConnectionError:
            return cached

        except requests.exceptions.ReadTimeout:
            self.timeouted = True

        except:
            self.timeouted = True

    def build_map(self):
        places = self.search_places()
        markers = []
        if places:
            markers = [
                fm.Marker(
                    coordinates=fm.MapLatitudeLongitude(place["lat"], place["lon"]),
                    content=ft.Container(
                        ft.Icon(name=place["icon"], color=place["color"], size=32),
                        tooltip=place["tooltip"],
                    ),
                ) for place in places
            ]
        self.marker_layer = fm.MarkerLayer(markers=markers)
        self.class_map = fm.Map(
            layers=[
                fm.TileLayer(
                    url_template="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",
                    subdomains=["a", "b", "c", "d"],
                    on_image_error=lambda e: print("TileLayer Error"),
                ),
                self.marker_layer,
            ],
            initial_center=fm.MapLatitudeLongitude(41.145, 1.405),
            initial_zoom=14,
            max_zoom=20,
            expand=True
        )




